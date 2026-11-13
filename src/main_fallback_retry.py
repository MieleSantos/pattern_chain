"""
Main entry point for the Fallback and Retry Patterns example.

The failures are simulated: each scenario makes the models fail a fixed
number of times before they work, and prints who answered.
"""

from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model

from fallback_retry import TransientError, create_resilient_chain, failing

QUESTION = "Fui cobrado duas vezes. O que eu faço?"
ALWAYS = 99

# (description, failures of the primary model, failures of the fallback model)
SCENARIOS = [
    ("Tudo funcionando", 0, 0),
    ("Principal falha 2 vezes e volta", 2, 0),
    ("Principal fora do ar", ALWAYS, 0),
    ("Os dois fora do ar", ALWAYS, ALWAYS),
]


def main():
    primary = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai", max_retries=0)
    fallback = init_chat_model(model="gemini-2.5-flash-lite", model_provider="google_genai", max_retries=0)

    for description, primary_failures, fallback_failures in SCENARIOS:
        log: list[str] = []
        chain = create_resilient_chain(
            primary=failing(primary, primary_failures, "principal", log),
            fallback=failing(fallback, fallback_failures, "reserva", log),
            attempts=3,
            retry_on=(TransientError,),  # only the simulated transient error is retried
            wait=False,                  # no backoff, so the example runs fast
        )
        answer = chain.invoke({"question": QUESTION})

        print(f"=== {description}")
        print("Chamadas:", ", ".join(log))
        print(answer, end="\n\n")


if __name__ == "__main__":
    main()
