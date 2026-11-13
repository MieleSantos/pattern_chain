"""
Prompt and fixed message for the Fallback and Retry Patterns.
"""

from langchain_core.prompts import ChatPromptTemplate

# Last resort: sent when every model failed. It is fixed text, so it cannot fail.
SAFE_MESSAGE = (
    "Estamos com instabilidade no atendimento automático. Sua mensagem foi "
    "registrada e uma pessoa da equipe vai responder em breve."
)


def create_support_prompt() -> ChatPromptTemplate:
    """Short support answer; the pattern is in the chain, not in the prompt."""
    system = (
        "system",
        "You are the support assistant of Nuvem. Answer in Portuguese, in one "
        "short paragraph.",
    )
    return ChatPromptTemplate.from_messages([system, ("user", "{question}")])
