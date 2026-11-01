"""
Prompts for the Structured Output Pattern.

The prompt explains the task; the output format comes from the schema,
so there is no need to describe the JSON here.
"""

from langchain_core.prompts import ChatPromptTemplate


def create_ticket_prompt() -> ChatPromptTemplate:
    """Create a prompt that triages a customer support message."""
    system = (
        "system",
        "You are a support analyst. Classify the customer message "
        "and extract the requested information.",
    )
    user = ("user", "{message}")
    return ChatPromptTemplate.from_messages([system, user])
