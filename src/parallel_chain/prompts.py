"""
Prompts for the Parallel Chain Pattern.

The summary and sentiment prompts come from the Sequential Chain package;
only the keywords prompt is new.
"""

from langchain_core.prompts import ChatPromptTemplate


def create_keywords_prompt() -> ChatPromptTemplate:
    """Create a prompt that extracts the main keywords of a text."""
    system = (
        "system",
        "Extract up to 5 keywords from the following text. "
        "Return only the keywords, separated by commas.",
    )
    user = ("user", "{text}")
    return ChatPromptTemplate.from_messages([system, user])
