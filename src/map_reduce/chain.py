"""
Map-Reduce: process a text that does not fit in one prompt.

    split -> group into batches -> map (one call per batch, in parallel)
          -> collapse (only if the notes are still too long) -> reduce

What is counting is done in code (Counter); the model only writes.
"""

import re
from collections import Counter
from pathlib import Path

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from map_reduce.prompts import create_collapse_prompt, create_map_prompt, create_reduce_prompt
from map_reduce.schemas import BatchNotes, TicketNote

TICKETS_FILE = Path(__file__).resolve().parents[2] / "data" / "tickets" / "semana.md"


def load_tickets(path: Path = TICKETS_FILE) -> list[str]:
    """One text per ticket: the file is split where a "## " header starts."""
    text = path.read_text(encoding="utf-8")
    sections = re.split(r"(?m)^(?=## )", text)
    return [section.strip() for section in sections[1:]]  # [0] is the file title


def group_texts(texts: list[str], max_chars: int) -> list[str]:
    """
    Pack whole texts into batches of up to max_chars characters.

    A text is never cut in the middle. A single text longer than max_chars
    becomes a batch by itself.
    """
    batches: list[str] = []
    current: list[str] = []
    size = 0
    for text in texts:
        if current and size + len(text) > max_chars:
            batches.append("\n\n".join(current))
            current, size = [], 0
        current.append(text)
        size += len(text)
    if current:
        batches.append("\n\n".join(current))
    return batches


def format_note(note: TicketNote) -> str:
    flag = " [BLOQUEADO]" if note.blocked else ""
    return f"- Ticket {note.ticket} ({note.category}){flag}: {note.problem}"


def count_categories(notes: list[TicketNote]) -> dict[str, int]:
    """Totals by category, most frequent first."""
    return dict(Counter(note.category for note in notes).most_common())


def summarize_tickets(
    tickets: list[str],
    llm: BaseChatModel | None = None,
    max_chars: int = 1500,
    max_concurrency: int = 4,
) -> dict:
    """
    Output: "report" (str), "notes" (one TicketNote per ticket), "totals"
    (category -> count), "map_calls" and "collapse_rounds".

    max_chars bounds every prompt input: the size of a map batch and the
    size of the notes sent to the reduce step.
    """
    if llm is None:
        llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")
    config = {"max_concurrency": max_concurrency}

    # Map: every batch is independent, so they run at the same time
    batches = group_texts(tickets, max_chars)
    map_chain = create_map_prompt() | llm.with_structured_output(BatchNotes)
    results = map_chain.batch([{"text": batch} for batch in batches], config=config)
    notes = [note for result in results for note in result.notes]

    # Collapse: shrink the notes until they fit in one prompt
    collapse_chain = create_collapse_prompt() | llm | StrOutputParser()
    parts = [format_note(note) for note in notes]
    rounds = 0
    while sum(len(part) for part in parts) > max_chars:
        groups = group_texts(parts, max_chars)
        if len(groups) == len(parts):  # nothing left to group: stop instead of looping
            break
        parts = collapse_chain.batch([{"text": group} for group in groups], config=config)
        rounds += 1

    # Reduce: the totals come from code, the text from the model
    totals = count_categories(notes)
    reduce_chain = create_reduce_prompt() | llm | StrOutputParser()
    report = reduce_chain.invoke(
        {
            "totals": "\n".join(f"- {category}: {count}" for category, count in totals.items()),
            "notes": "\n".join(parts),
        }
    )

    return {
        "report": report,
        "notes": notes,
        "totals": totals,
        "map_calls": len(batches),
        "collapse_rounds": rounds,
    }
