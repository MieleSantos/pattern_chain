"""
Prompts for the Router Chain Pattern.

Each route has its own specialized prompt. All of them receive the same
variables ({message} and {summary}), so any route can handle any ticket.
"""

from langchain_core.prompts import ChatPromptTemplate


def _response_prompt(instructions: str) -> ChatPromptTemplate:
    """Build a response prompt that shares the same input variables."""
    system = (
        "system",
        instructions + " Answer in Portuguese, in at most 4 sentences. "
        "Ticket summary: {summary}",
    )
    user = ("user", "{message}")
    return ChatPromptTemplate.from_messages([system, user])


def create_billing_prompt() -> ChatPromptTemplate:
    """Route for invoices, charges and refunds."""
    return _response_prompt(
        "You are a billing specialist. Explain the charge, the refund "
        "process and the expected deadline."
    )


def create_technical_prompt() -> ChatPromptTemplate:
    """Route for bugs, errors and integrations."""
    return _response_prompt(
        "You are a technical support engineer. Give clear troubleshooting "
        "steps and ask for the information needed to investigate."
    )


def create_cancellation_prompt() -> ChatPromptTemplate:
    """Route for customers who want to cancel."""
    return _response_prompt(
        "You are a retention specialist. Acknowledge the request, explain how "
        "to cancel and offer one relevant alternative without pressure."
    )


def create_question_prompt() -> ChatPromptTemplate:
    """Default route for general questions."""
    return _response_prompt(
        "You are a friendly support agent. Answer the question directly."
    )
