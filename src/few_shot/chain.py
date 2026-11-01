"""
Chain configuration for the Few-Shot Prompting Pattern.
"""

from langchain.chat_models import init_chat_model
from langchain_core.embeddings import Embeddings
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import InMemoryVectorStore

from few_shot.examples import EXAMPLES
from few_shot.prompts import create_dynamic_few_shot_prompt, create_fixed_few_shot_prompt


def _default_llm() -> BaseChatModel:
    return init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")


def create_fixed_few_shot_chain(
    llm: BaseChatModel | None = None,
    examples: list[dict[str, str]] = EXAMPLES,
):
    """Few-shot chain that always sends every example."""
    llm = llm or _default_llm()
    return create_fixed_few_shot_prompt(examples) | llm | StrOutputParser()


def create_semantic_selector(
    embeddings: Embeddings | None = None,
    examples: list[dict[str, str]] = EXAMPLES,
    k: int = 2,
) -> SemanticSimilarityExampleSelector:
    """
    Select the k examples whose message is closest to the new message.

    Only the "message" field is embedded (input_keys), so the replies do
    not influence which examples are picked.
    """
    if embeddings is None:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

    return SemanticSimilarityExampleSelector.from_examples(
        examples,
        embeddings,
        InMemoryVectorStore,
        k=k,
        input_keys=["message"],
    )


def create_dynamic_few_shot_chain(
    llm: BaseChatModel | None = None,
    embeddings: Embeddings | None = None,
    k: int = 2,
):
    """Few-shot chain that sends only the k most similar examples."""
    llm = llm or _default_llm()
    selector = create_semantic_selector(embeddings=embeddings, k=k)
    return create_dynamic_few_shot_prompt(selector) | llm | StrOutputParser()
