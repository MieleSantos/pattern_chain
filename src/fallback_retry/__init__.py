"""Fallback and Retry Patterns package."""

from fallback_retry.prompts import SAFE_MESSAGE, create_support_prompt
from fallback_retry.chain import (
    with_layers,
    create_resilient_chain,
    create_validated_ticket_chain,
)
from fallback_retry.simulate import TransientError, failing

__all__ = [
    "SAFE_MESSAGE",
    "create_support_prompt",
    "with_layers",
    "create_resilient_chain",
    "create_validated_ticket_chain",
    "TransientError",
    "failing",
]
