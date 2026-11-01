"""
Prompts for the Few-Shot Prompting Pattern.

The examples are inserted as real conversation turns (user -> assistant),
so the model sees the style instead of reading a description of it.
"""

from langchain_core.example_selectors import BaseExampleSelector
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

SYSTEM = (
    "You are the support team of Nuvem, a SaaS company. "
    "Reply to the customer in Portuguese following exactly the tone, "
    "length and structure of the previous answers."
)

# How each example becomes messages
EXAMPLE_PROMPT = ChatPromptTemplate.from_messages(
    [("human", "{message}"), ("ai", "{reply}")]
)


def _wrap(few_shot: FewShotChatMessagePromptTemplate) -> ChatPromptTemplate:
    """System instructions, then the examples, then the real message."""
    return ChatPromptTemplate.from_messages(
        [("system", SYSTEM), few_shot, ("human", "{message}")]
    )


def create_fixed_few_shot_prompt(examples: list[dict[str, str]]) -> ChatPromptTemplate:
    """Always send the same examples."""
    few_shot = FewShotChatMessagePromptTemplate(
        examples=examples,
        example_prompt=EXAMPLE_PROMPT,
    )
    return _wrap(few_shot)


def create_dynamic_few_shot_prompt(selector: BaseExampleSelector) -> ChatPromptTemplate:
    """Pick the examples most similar to the incoming message."""
    few_shot = FewShotChatMessagePromptTemplate(
        example_selector=selector,
        example_prompt=EXAMPLE_PROMPT,
        input_variables=["message"],
    )
    return _wrap(few_shot)
