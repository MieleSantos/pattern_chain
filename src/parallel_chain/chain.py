"""
Chain configuration for the Parallel Chain Pattern.

Flow: translate (one step) -> summary, sentiment and keywords at the same
time. The three analyses only need the translated text, so none of them
waits for the others.
"""

from operator import itemgetter

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from parallel_chain.prompts import create_keywords_prompt
from sequential_chain.prompts import (
    create_sentiment_prompt,
    create_summary_prompt,
    create_translation_prompt,
)


def create_analyses(llm: BaseChatModel) -> RunnableParallel:
    """Three independent analyses that receive the same {"text": ...} input."""
    parser = StrOutputParser()
    return RunnableParallel(
        summary=create_summary_prompt() | llm | parser,
        sentiment=create_sentiment_prompt() | llm | parser,
        keywords=create_keywords_prompt() | llm | parser,
    )


def create_parallel_analysis_chain(llm: BaseChatModel | None = None):
    """
    Translate the text, then run the three analyses in parallel.

    Output: the input dict plus "translated" and "analysis", where
    "analysis" is {"summary": ..., "sentiment": ..., "keywords": ...}.
    """
    if llm is None:
        llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")

    parser = StrOutputParser()
    translate = (
        {"target_language": itemgetter("language"), "text": itemgetter("text")}
        | create_translation_prompt()
        | llm
        | parser
    )

    return (
        RunnablePassthrough.assign(translated=translate)
        | RunnablePassthrough.assign(
            analysis={"text": itemgetter("translated")} | create_analyses(llm)
        )
    )
