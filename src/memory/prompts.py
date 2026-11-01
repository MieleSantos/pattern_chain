"""
Prompts for the Memory Pattern.

MessagesPlaceholder("history") is where the previous turns of the
conversation are inserted, between the instructions and the new question.
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from rag.prompts import NOT_FOUND


def create_chat_prompt() -> ChatPromptTemplate:
    """Plain chat with memory."""
    return ChatPromptTemplate.from_messages(
        [
            ("system", "You are the support assistant of Nuvem. Answer in Portuguese."),
            MessagesPlaceholder("history"),
            ("human", "{question}"),
        ]
    )


def create_condense_prompt() -> ChatPromptTemplate:
    """Rewrite a follow-up question so it makes sense without the conversation."""
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Given the conversation and a follow-up question, rewrite the "
                "follow-up as a standalone question in Portuguese that can be "
                "understood without the conversation. Do not answer it. "
                "Return only the rewritten question.",
            ),
            MessagesPlaceholder("history"),
            ("human", "{question}"),
        ]
    )


def create_conversational_rag_prompt() -> ChatPromptTemplate:
    """RAG answer prompt that also sees the conversation."""
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are the support assistant of Nuvem. Answer in Portuguese using ONLY "
                "the documentation below and the conversation so far. If the answer is "
                f'not in the documentation, reply exactly: "{NOT_FOUND}"\n\n'
                "Documentation:\n{context}",
            ),
            MessagesPlaceholder("history"),
            ("human", "{question}"),
        ]
    )
