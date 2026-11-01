"""
Prompt for the RAG Pattern.

The retrieved chunks go into {context}. The instructions keep the model
inside that context and make it admit when the answer is not there.
"""

from langchain_core.prompts import ChatPromptTemplate

NOT_FOUND = "Não encontrei essa informação na documentação."


def create_rag_prompt() -> ChatPromptTemplate:
    """Answer only from the retrieved documentation and cite the sources."""
    system = (
        "system",
        "You are the support assistant of Nuvem. Answer in Portuguese using ONLY "
        "the documentation below. If the answer is not in the documentation, "
        f'reply exactly: "{NOT_FOUND}" '
        "At the end, list the sources you used in the format [file > section].\n\n"
        "Documentation:\n{context}",
    )
    user = ("user", "{question}")
    return ChatPromptTemplate.from_messages([system, user])
