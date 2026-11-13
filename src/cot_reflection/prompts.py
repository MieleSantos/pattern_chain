"""
Prompts for the Chain-of-Thought and Reflection Patterns.

All of them receive the documentation in {context}. The reasoning and the
critique formats come from the schemas, so the prompts only explain the task.
"""

from langchain_core.prompts import ChatPromptTemplate

GROUNDING = (
    "Use ONLY the documentation below. Do not assume rules that are not written in it.\n\n"
    "Documentation:\n{context}"
)


def create_direct_prompt() -> ChatPromptTemplate:
    """Baseline: answer right away, with no reasoning step."""
    system = (
        "system",
        "You are the support assistant of Nuvem. Answer in Portuguese, in one "
        "short paragraph. " + GROUNDING,
    )
    return ChatPromptTemplate.from_messages([system, ("user", "{question}")])


def create_cot_prompt() -> ChatPromptTemplate:
    """Chain-of-Thought: reason through the rules before answering."""
    system = (
        "system",
        "You are the support assistant of Nuvem. Before answering, reason step by step:\n"
        "1. List the facts the customer gave (dates, plan, payment method).\n"
        "2. Quote each rule of the documentation that applies to those facts.\n"
        "3. Apply the rules to the facts, one at a time.\n"
        "Only then write the final answer, covering every part of the question.\n\n"
        + GROUNDING,
    )
    return ChatPromptTemplate.from_messages([system, ("user", "{question}")])


def create_critique_prompt() -> ChatPromptTemplate:
    """Reflection, step 1: review a draft against the documentation."""
    system = (
        "system",
        "You are a strict reviewer of customer support answers. Check the draft "
        "answer against the documentation and the customer question:\n"
        "- Does every claim agree with the documentation?\n"
        "- Is every claim actually written in the documentation?\n"
        "- Was every part of the question answered?\n"
        "Report only real problems. Do not ask for changes of style or tone.\n\n"
        "Documentation:\n{context}",
    )
    user = ("user", "Customer question:\n{question}\n\nDraft answer:\n{answer}")
    return ChatPromptTemplate.from_messages([system, user])


def create_revise_prompt() -> ChatPromptTemplate:
    """Reflection, step 2: rewrite the draft fixing the reported problems."""
    system = (
        "system",
        "You are the support assistant of Nuvem. A reviewer found problems in "
        "your draft answer. Reason step by step about each problem and write a "
        "new answer that fixes all of them and keeps what was already right.\n\n"
        + GROUNDING,
    )
    user = (
        "user",
        "Customer question:\n{question}\n\nDraft answer:\n{answer}\n\n"
        "Problems found by the reviewer:\n{issues}",
    )
    return ChatPromptTemplate.from_messages([system, user])
