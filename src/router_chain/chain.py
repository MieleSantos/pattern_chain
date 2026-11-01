"""
Chain configuration for the Router Chain Pattern.

Flow: classify the message (Structured Output) -> pick a route -> answer.
"""

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    Runnable,
    RunnableBranch,
    RunnableLambda,
    RunnablePassthrough,
)

from router_chain.prompts import (
    create_billing_prompt,
    create_cancellation_prompt,
    create_question_prompt,
    create_technical_prompt,
)
from structured_output import create_structured_chain

ESCALATION_MESSAGE = (
    "Sua solicitação foi encaminhada para um atendente, que vai falar "
    "com você em breve."
)


def _to_prompt_input(state: dict) -> dict:
    """Map the router state to the variables every route prompt expects."""
    return {"message": state["message"], "summary": state["ticket"].summary}


def create_routes(llm: BaseChatModel) -> dict[str, Runnable]:
    """One specialized chain per ticket category."""
    parser = StrOutputParser()
    prompts = {
        "billing": create_billing_prompt(),
        "technical": create_technical_prompt(),
        "cancellation": create_cancellation_prompt(),
        "question": create_question_prompt(),
    }
    return {
        category: RunnableLambda(_to_prompt_input) | prompt | llm | parser
        for category, prompt in prompts.items()
    }


def create_router_chain(
    llm: BaseChatModel | None = None,
    classifier_llm: BaseChatModel | None = None,
):
    """
    Router using a plain Python function (recommended).

    The function returns the chain that should run. LangChain invokes the
    returned chain with the same input. Output: the input dict plus
    "ticket" (TicketAnalysis) and "answer" (str).
    """
    if llm is None:
        llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")

    classify = create_structured_chain(llm=classifier_llm or llm)
    routes = create_routes(llm)
    escalate = RunnableLambda(lambda state: ESCALATION_MESSAGE)

    def route(state: dict) -> Runnable:
        ticket = state["ticket"]
        if ticket.priority == "high" and ticket.needs_human:
            return escalate
        return routes.get(ticket.category, routes["question"])

    return (
        RunnablePassthrough.assign(ticket=classify)
        | RunnablePassthrough.assign(answer=RunnableLambda(route))
    )


def create_branch_router_chain(
    llm: BaseChatModel | None = None,
    classifier_llm: BaseChatModel | None = None,
):
    """Same router written with RunnableBranch, for comparison."""
    if llm is None:
        llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")

    classify = create_structured_chain(llm=classifier_llm or llm)
    routes = create_routes(llm)

    branch = RunnableBranch(
        (
            lambda s: s["ticket"].priority == "high" and s["ticket"].needs_human,
            RunnableLambda(lambda s: ESCALATION_MESSAGE),
        ),
        (lambda s: s["ticket"].category == "billing", routes["billing"]),
        (lambda s: s["ticket"].category == "technical", routes["technical"]),
        (lambda s: s["ticket"].category == "cancellation", routes["cancellation"]),
        routes["question"],  # default branch
    )

    return (
        RunnablePassthrough.assign(ticket=classify)
        | RunnablePassthrough.assign(answer=branch)
    )
