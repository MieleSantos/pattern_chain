"""
Output schema of the map step of the Map-Reduce Pattern.

The category is a closed list, so the notes of different batches can be
counted together in code. Free-text themes would not match across batches.
"""

from typing import Literal

from pydantic import BaseModel, Field

Category = Literal["billing", "technical", "cancellation", "question"]


class TicketNote(BaseModel):
    """What one ticket is about."""

    ticket: str = Field(description='Ticket identifier as written in the text, e.g. "1041"')
    category: Category = Field(description="Main subject of the ticket")
    problem: str = Field(
        description="The problem or request in one short sentence, in Portuguese",
        max_length=200,
    )
    blocked: bool = Field(
        description="True when the customer cannot work or is losing money right now"
    )


class BatchNotes(BaseModel):
    """One note for each ticket of the batch, in the same order."""

    notes: list[TicketNote]
