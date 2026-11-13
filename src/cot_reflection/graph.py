"""
Reflection: a draft is reviewed and rewritten until it is approved.

    draft -> review -> (approved or limit reached) -> END
                 \\-> revise -> review -> ...

The loop is a LangGraph conditional edge. max_revisions bounds it, so the
graph always ends, even when the reviewer never approves.
"""

from typing import TypedDict

from langchain_core.language_models import BaseChatModel
from langgraph.graph import END, START, StateGraph

from cot_reflection.chain import create_cot_chain, default_llm, load_policy
from cot_reflection.prompts import create_critique_prompt, create_revise_prompt
from cot_reflection.schemas import Critique, ReasonedAnswer


class ReflectionState(TypedDict, total=False):
    question: str
    reasoning: str
    answer: str
    critique: Critique
    revisions: int


def create_reflection_graph(
    llm: BaseChatModel | None = None,
    critic_llm: BaseChatModel | None = None,
    context: str | None = None,
    max_revisions: int = 2,
):
    """
    Input: {"question": ...}. Output: the state, with the final "answer",
    the last "critique" and how many "revisions" were made.

    When the output has critique.approved == False, the limit was reached
    with problems still open: send the case to a person instead of the customer.

    critic_llm lets the reviewer be a different model from the writer.
    """
    llm = llm or default_llm()
    critic_llm = critic_llm or llm
    if context is None:
        context = load_policy()

    draft_chain = create_cot_chain(llm)
    critique_chain = create_critique_prompt() | critic_llm.with_structured_output(Critique)
    revise_chain = create_revise_prompt() | llm.with_structured_output(ReasonedAnswer)

    def draft(state: ReflectionState) -> dict:
        result = draft_chain.invoke({"question": state["question"], "context": context})
        return {"reasoning": result.reasoning, "answer": result.answer, "revisions": 0}

    def review(state: ReflectionState) -> dict:
        critique = critique_chain.invoke(
            {"question": state["question"], "answer": state["answer"], "context": context}
        )
        # The verdict comes from the list, not from the model's own flag
        critique.approved = not critique.issues
        return {"critique": critique}

    def revise(state: ReflectionState) -> dict:
        result = revise_chain.invoke(
            {
                "question": state["question"],
                "answer": state["answer"],
                "issues": "\n".join(f"- {issue}" for issue in state["critique"].issues),
                "context": context,
            }
        )
        return {
            "reasoning": result.reasoning,
            "answer": result.answer,
            "revisions": state["revisions"] + 1,
        }

    def after_review(state: ReflectionState) -> str:
        if state["critique"].approved or state["revisions"] >= max_revisions:
            return END
        return "revise"

    graph = StateGraph(ReflectionState)
    graph.add_node("draft", draft)
    graph.add_node("review", review)
    graph.add_node("revise", revise)
    graph.add_edge(START, "draft")
    graph.add_edge("draft", "review")
    graph.add_conditional_edges("review", after_review, ["revise", END])
    graph.add_edge("revise", "review")
    return graph.compile()
