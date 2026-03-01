"""
Prompt Template Pattern Implementation.

This module provides reusable prompt templates following the Prompt Template Pattern.
"""

from langchain_core.prompts import ChatPromptTemplate


def create_qa_prompt() -> ChatPromptTemplate:
    """Create a basic QA prompt template with style and question variables."""
    system = ("system", "you are an assistant that answers questions in a {style} style")
    user = ("user", "{question}")
    return ChatPromptTemplate.from_messages([system, user])


def create_formatter_prompt() -> ChatPromptTemplate:
    """Create a prompt for formatting output."""
    system = ("system", "Format the following content as {format_type}")
    user = ("user", "{content}")
    return ChatPromptTemplate.from_messages([system, user])
