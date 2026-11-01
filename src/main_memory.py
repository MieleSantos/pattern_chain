"""
Main entry point for the Memory and conversation history Pattern example.
"""

from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import HumanMessage

from memory import create_conversational_rag_graph

CONVERSATION = [
    "Fui cobrado duas vezes no mesmo mês. Em quanto tempo recebo o estorno?",
    "E se eu tiver pago com Pix?",          # only makes sense with the history
    "Qual foi mesmo o prazo que você falou?",
]


def ask(graph, thread_id: str, question: str):
    # Send only the new message: the checkpointer brings back the rest
    state = graph.invoke(
        {"messages": [HumanMessage(question)]},
        config={"configurable": {"thread_id": thread_id}},
    )
    print(f"=== [{thread_id}] {question}")
    print(f"(pergunta reescrita: {state['standalone_question']})")
    print(state["messages"][-1].content, end="\n\n")


def main():
    graph = create_conversational_rag_graph()

    for question in CONVERSATION:
        ask(graph, "cliente-1", question)

    # A different thread has no history: the follow-up is ambiguous here
    ask(graph, "cliente-2", "E se eu tiver pago com Pix?")


if __name__ == "__main__":
    main()
