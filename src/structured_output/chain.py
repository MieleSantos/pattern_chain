"""
Chain configuration for the Structured Output Pattern.
"""

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from structured_output.prompts import create_ticket_prompt
from structured_output.schemas import TicketAnalysis


def create_structured_chain(
    llm: BaseChatModel | None = None,
    include_raw: bool = False,
):
    """
    Create a chain that returns a validated TicketAnalysis instead of text.

    There is no output parser: with_structured_output already returns the
    Pydantic object. With include_raw=True the chain returns a dict with
    "raw", "parsed" and "parsing_error" instead of raising on bad output.
    """
    if llm is None:
        llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")

    structured_llm = llm.with_structured_output(TicketAnalysis, include_raw=include_raw)
    return create_ticket_prompt() | structured_llm
