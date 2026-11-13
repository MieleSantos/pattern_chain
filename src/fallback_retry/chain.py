"""
Fallback and Retry: keep the chain answering when a model call fails.

Three layers, from the inside out:

    retry     try the same model again (transient errors: rate limit, timeout)
    fallback  switch to another model when the retries are over
    safe      a fixed message when every model failed

with_retry and with_fallbacks exist on every Runnable, so the same layers
work for a model, a chain or a single step.
"""

from langchain.chat_models import init_chat_model
from langchain_core.exceptions import OutputParserException
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableLambda
from pydantic import ValidationError

from fallback_retry.prompts import SAFE_MESSAGE, create_support_prompt
from structured_output import create_structured_chain

ExceptionTypes = tuple[type[BaseException], ...]


def with_layers(
    primary: Runnable,
    fallback: Runnable,
    attempts: int = 3,
    retry_on: ExceptionTypes = (Exception,),
    wait: bool = True,
) -> Runnable:
    """
    primary with retries, then fallback with retries.

    retry_on should list only transient errors of your provider (rate limit,
    timeout, server error). The default retries everything, including errors
    that will never succeed, such as an invalid API key.

    wait=True sleeps between attempts with exponential backoff and jitter.
    """

    def retrying(model: Runnable) -> Runnable:
        return model.with_retry(
            stop_after_attempt=attempts,
            retry_if_exception_type=retry_on,
            wait_exponential_jitter=wait,
        )

    return retrying(primary).with_fallbacks([retrying(fallback)])


def create_resilient_chain(
    primary: BaseChatModel | None = None,
    fallback: BaseChatModel | None = None,
    attempts: int = 3,
    retry_on: ExceptionTypes = (Exception,),
    wait: bool = True,
    safe_message: str = SAFE_MESSAGE,
) -> Runnable:
    """
    {question} -> str, always. The answer comes from the primary model, from
    the fallback model or, when both fail, from safe_message.
    """
    if primary is None:
        # max_retries=0: the retries are done here, not hidden inside the client
        primary = init_chat_model(
            model="gemini-2.5-flash", model_provider="google_genai", max_retries=0, timeout=20
        )
    if fallback is None:
        fallback = init_chat_model(
            model="gemini-2.5-flash-lite", model_provider="google_genai", max_retries=0, timeout=20
        )

    model = with_layers(primary, fallback, attempts=attempts, retry_on=retry_on, wait=wait)
    chain = create_support_prompt() | model | StrOutputParser()
    return chain.with_fallbacks([RunnableLambda(lambda _: safe_message)])


def create_validated_ticket_chain(llm: BaseChatModel | None = None, attempts: int = 2) -> Runnable:
    """
    Structured output (Part 3) that asks again when the output is invalid.

    An answer that breaks the schema is also a failure: the call worked, but
    the result cannot be used. Only validation and parsing errors are
    retried here.
    """
    return create_structured_chain(llm).with_retry(
        stop_after_attempt=attempts,
        retry_if_exception_type=(ValidationError, OutputParserException),
        wait_exponential_jitter=False,
    )
