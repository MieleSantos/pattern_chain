"""
Chain-of-Thought: make the model reason before it answers.

The reasoning is a field of the structured output (Part 3), so the code can
log it for auditing and show only the answer to the customer.
"""

from pathlib import Path

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from cot_reflection.prompts import create_cot_prompt, create_direct_prompt
from cot_reflection.schemas import ReasonedAnswer
from rag.indexing import DATA_DIR, load_documents


def default_llm() -> BaseChatModel:
    return init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")


def load_policy(data_dir: Path = DATA_DIR) -> str:
    """
    The whole knowledge base as one text.

    It is small enough to fit in the prompt. With a large base, use the
    retriever of the RAG Pattern (Part 7) to get only the relevant chunks.
    """
    return "\n\n".join(doc.page_content for doc in load_documents(data_dir))


def create_direct_chain(llm: BaseChatModel | None = None):
    """Baseline without reasoning: {question, context} -> str."""
    return create_direct_prompt() | (llm or default_llm()) | StrOutputParser()


def create_cot_chain(llm: BaseChatModel | None = None):
    """Chain-of-Thought: {question, context} -> ReasonedAnswer."""
    llm = llm or default_llm()
    return create_cot_prompt() | llm.with_structured_output(ReasonedAnswer)
