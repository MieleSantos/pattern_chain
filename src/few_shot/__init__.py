"""Few-Shot Prompting Pattern package."""

from few_shot.examples import EXAMPLES
from few_shot.prompts import (
    EXAMPLE_PROMPT,
    create_fixed_few_shot_prompt,
    create_dynamic_few_shot_prompt,
)
from few_shot.chain import (
    create_fixed_few_shot_chain,
    create_semantic_selector,
    create_dynamic_few_shot_chain,
)

__all__ = [
    "EXAMPLES",
    "EXAMPLE_PROMPT",
    "create_fixed_few_shot_prompt",
    "create_dynamic_few_shot_prompt",
    "create_fixed_few_shot_chain",
    "create_semantic_selector",
    "create_dynamic_few_shot_chain",
]
