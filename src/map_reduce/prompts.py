"""
Prompts for the Map-Reduce Pattern.

map:      a batch of tickets -> one note per ticket
collapse: many notes -> a shorter text, when they do not fit in one prompt
reduce:   notes + counts -> the final report
"""

from langchain_core.prompts import ChatPromptTemplate


def create_map_prompt() -> ChatPromptTemplate:
    """Map step: runs once per batch and only sees that batch."""
    system = (
        "system",
        "You are a support analyst. Write one note for each ticket below. "
        "Use only what is written in the ticket.",
    )
    return ChatPromptTemplate.from_messages([system, ("user", "{text}")])


def create_collapse_prompt() -> ChatPromptTemplate:
    """Intermediate step: shrink a group of notes without losing tickets."""
    system = (
        "system",
        "Condense the ticket notes below, in Portuguese. Group tickets with the "
        "same problem in one line and keep every ticket number. Keep the "
        "tickets marked as blocked. Do not add information.",
    )
    return ChatPromptTemplate.from_messages([system, ("user", "{text}")])


def create_reduce_prompt() -> ChatPromptTemplate:
    """Reduce step: write the report from the notes of all batches."""
    system = (
        "system",
        "You write the weekly support report of Nuvem, in Portuguese, for the "
        "support manager. Use only the notes and the totals below.\n"
        "The totals were counted by the system: copy them, do not recount.\n"
        "Sections: 1) Totals by category. 2) Recurring problems, with the "
        "ticket numbers. 3) Blocked customers that need attention now.",
    )
    user = ("user", "Totals:\n{totals}\n\nNotes:\n{notes}")
    return ChatPromptTemplate.from_messages([system, user])
