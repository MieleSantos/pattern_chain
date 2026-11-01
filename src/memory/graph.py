"""
Memory and conversation history with LangGraph persistence.

The conversation lives in the graph state ("messages"). A checkpointer
saves the state after every run, keyed by thread_id, so the next call
with the same thread_id continues the conversation. This is the
approach recommended by LangChain 1.x (RunnableWithMessageHistory is
deprecated).
"""

from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, trim_messages
from langchain_core.output_parsers import StrOutputParser
from langchain_core.retrievers import BaseRetriever
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph

from memory.prompts import (
    create_chat_prompt,
    create_condense_prompt,
    create_conversational_rag_prompt,
)
from rag import create_retriever, format_docs


def _default_llm() -> BaseChatModel:
    return init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")


def trim_history(messages: list[BaseMessage], max_messages: int = 10) -> list[BaseMessage]:
    """
    Keep only the last max_messages messages sent to the model.

    token_counter=len counts messages instead of tokens, and
    start_on="human" avoids a history that starts with a lone AI answer.
    The saved state is not changed, only what goes into the prompt.
    """
    return trim_messages(
        messages,
        max_tokens=max_messages,
        token_counter=len,
        strategy="last",
        start_on="human",
    )


def _split(messages: list[BaseMessage]) -> tuple[list[BaseMessage], str]:
    """Previous turns and the text of the newest question."""
    return messages[:-1], messages[-1].content


# --- Plain chat with memory -------------------------------------------------


def create_chat_graph(llm: BaseChatModel | None = None, max_messages: int = 10, checkpointer=None):
    """Chat that remembers each conversation (thread_id)."""
    llm = llm or _default_llm()
    chain = create_chat_prompt() | llm | StrOutputParser()

    def respond(state: MessagesState) -> dict:
        history, question = _split(state["messages"])
        answer = chain.invoke({"history": trim_history(history, max_messages), "question": question})
        return {"messages": [AIMessage(answer)]}  # appended to the state, not replaced

    graph = StateGraph(MessagesState)
    graph.add_node("respond", respond)
    graph.add_edge(START, "respond")
    graph.add_edge("respond", END)
    return graph.compile(checkpointer=checkpointer or InMemorySaver())


# --- Conversational RAG -------------------------------------------------------


class ConversationalRAGState(MessagesState):
    """Messages plus what each turn produced, for logging and debugging."""

    standalone_question: str
    docs: list[Document]


def create_conversational_rag_graph(
    llm: BaseChatModel | None = None,
    retriever: BaseRetriever | None = None,
    max_messages: int = 10,
    checkpointer=None,
):
    """
    RAG (Part 7) that understands follow-up questions.

    condense: rewrite the newest question as a standalone question
              (skipped on the first turn)
    retrieve: search the documentation with the rewritten question
    answer:   answer with documentation + conversation
    """
    llm = llm or _default_llm()
    if retriever is None:
        retriever = create_retriever()
    parser = StrOutputParser()
    condense_chain = create_condense_prompt() | llm | parser
    answer_chain = create_conversational_rag_prompt() | llm | parser

    def condense(state: ConversationalRAGState) -> dict:
        history, question = _split(state["messages"])
        if not history:
            return {"standalone_question": question}
        rewritten = condense_chain.invoke(
            {"history": trim_history(history, max_messages), "question": question}
        )
        return {"standalone_question": rewritten}

    def retrieve(state: ConversationalRAGState) -> dict:
        return {"docs": retriever.invoke(state["standalone_question"])}

    def answer(state: ConversationalRAGState) -> dict:
        history, question = _split(state["messages"])
        text = answer_chain.invoke(
            {
                "history": trim_history(history, max_messages),
                "question": question,
                "context": format_docs(state["docs"]),
            }
        )
        return {"messages": [AIMessage(text)]}

    graph = StateGraph(ConversationalRAGState)
    graph.add_node("condense", condense)
    graph.add_node("retrieve", retrieve)
    graph.add_node("answer", answer)
    graph.add_edge(START, "condense")
    graph.add_edge("condense", "retrieve")
    graph.add_edge("retrieve", "answer")
    graph.add_edge("answer", END)
    return graph.compile(checkpointer=checkpointer or InMemorySaver())
