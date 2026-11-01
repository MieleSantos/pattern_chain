"""
Output schemas for the Structured Output Pattern.

Each field's description is sent to the model as part of the schema,
so it works as an instruction for that field.
"""

from typing import Literal

from pydantic import BaseModel, Field


class TicketAnalysis(BaseModel):
    """Triage of a customer support message."""

    category: Literal["billing", "technical", "cancellation", "question"] = Field(
        description="Main subject of the message"
    )
    priority: Literal["low", "medium", "high"] = Field(
        description="high when the customer is blocked or losing money"
    )
    summary: str = Field(
        description="One-sentence summary of the request, in Portuguese",
        max_length=200,
    )
    products: list[str] = Field(
        default_factory=list,
        description="Products or features mentioned in the message",
    )
    needs_human: bool = Field(
        description="True when the request cannot be solved by an automatic answer"
    )
