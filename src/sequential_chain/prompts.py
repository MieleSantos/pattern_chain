"""
Sequential Chain Pattern Implementation.

This module provides sequential chain examples where the output of one step
becomes the input for the next step.
"""

from langchain_core.prompts import ChatPromptTemplate


def create_translation_prompt() -> ChatPromptTemplate:
    """Create a prompt for translating text to a specific language."""
    system = ("system", "Translate the following text to {target_language}")
    user = ("user", "{text}")
    return ChatPromptTemplate.from_messages([system, user])


def create_summary_prompt() -> ChatPromptTemplate:
    """Create a prompt for summarizing text."""
    system = ("system", "Provide a concise summary of the following text")
    user = ("user", "{text}")
    return ChatPromptTemplate.from_messages([system, user])


def create_sentiment_prompt() -> ChatPromptTemplate:
    """Create a prompt for analyzing sentiment."""
    system = ("system", "Analyze the sentiment of the following text and provide a brief explanation")
    user = ("user", "{text}")
    return ChatPromptTemplate.from_messages([system, user])
