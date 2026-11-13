"""
Output schemas for the Chain-of-Thought and Reflection Patterns.

Field order matters: the model fills the fields in the order they appear,
so the reasoning comes before the answer and the issues before the verdict.
"""

from pydantic import BaseModel, Field


class ReasonedAnswer(BaseModel):
    """An answer preceded by the reasoning that led to it."""

    reasoning: str = Field(
        description=(
            "Step-by-step reasoning in Portuguese: the facts given by the customer, "
            "the rules of the documentation that apply to them, and what follows"
        )
    )
    answer: str = Field(
        description="Final answer to the customer, in Portuguese, without the reasoning"
    )


class Critique(BaseModel):
    """Review of a draft answer against the documentation."""

    issues: list[str] = Field(
        default_factory=list,
        description=(
            "One item per problem, in Portuguese: a claim that contradicts the "
            "documentation, a claim that is not in it, or a part of the question "
            "left unanswered. Empty when there are no problems"
        ),
    )
    approved: bool = Field(description="True only when the list of issues is empty")
