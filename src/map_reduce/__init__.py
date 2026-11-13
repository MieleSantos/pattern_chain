"""Map-Reduce Pattern package."""

from map_reduce.schemas import Category, TicketNote, BatchNotes
from map_reduce.prompts import create_map_prompt, create_collapse_prompt, create_reduce_prompt
from map_reduce.chain import (
    TICKETS_FILE,
    load_tickets,
    group_texts,
    format_note,
    count_categories,
    summarize_tickets,
)

__all__ = [
    "Category",
    "TicketNote",
    "BatchNotes",
    "create_map_prompt",
    "create_collapse_prompt",
    "create_reduce_prompt",
    "TICKETS_FILE",
    "load_tickets",
    "group_texts",
    "format_note",
    "count_categories",
    "summarize_tickets",
]
