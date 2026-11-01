"""
Main entry point for the RAG (Retrieval-Augmented Generation) Pattern example.
"""

from dotenv import load_dotenv

load_dotenv()

from rag import create_rag_chain

QUESTIONS = [
    "Fui cobrado duas vezes. Em quanto tempo recebo o estorno?",
    "Paguei o boleto e a conta continua bloqueada, o que eu faço?",
    "Meu webhook foi desativado, como reativo?",
    "Vocês têm aplicativo para Android?",  # not in the documentation
]


def main():
    # Indexing happens here, once; every question reuses the same index
    chain = create_rag_chain()

    for question in QUESTIONS:
        result = chain.invoke({"question": question})
        print(f"=== {question}")
        print(result["answer"])
        print("Trechos recuperados:", ", ".join(result["sources"]), end="\n\n")


if __name__ == "__main__":
    main()
