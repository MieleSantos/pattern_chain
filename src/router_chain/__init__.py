"""Router Chain Pattern package."""

from router_chain.prompts import (
    create_billing_prompt,
    create_technical_prompt,
    create_cancellation_prompt,
    create_question_prompt,
)
from router_chain.chain import (
    ESCALATION_MESSAGE,
    create_routes,
    create_router_chain,
    create_branch_router_chain,
)

__all__ = [
    "create_billing_prompt",
    "create_technical_prompt",
    "create_cancellation_prompt",
    "create_question_prompt",
    "ESCALATION_MESSAGE",
    "create_routes",
    "create_router_chain",
    "create_branch_router_chain",
]
