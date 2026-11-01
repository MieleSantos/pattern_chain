"""
Retrieval + generation step of the RAG Pattern.

Flow: question -> retriever (top k chunks) -> prompt with context -> answer.
"""

from operator import itemgetter

from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from rag.indexing import create_retriever
from rag.prompts import create_rag_prompt


def source_label(doc: Document) -> str:
    """Readable reference for a chunk, e.g. 'cobranca.md > Cobrança em duplicidade'."""
    section = doc.metadata.get("section") or doc.metadata.get("title", "")
    return f"{doc.metadata['source']} > {section}"


def format_docs(docs: list[Document]) -> str:
    """Join the chunks with their source, so the model can cite them."""
    return "\n\n---\n\n".join(f"[{source_label(d)}]\n{d.page_content}" for d in docs)


def create_rag_chain(
    llm: BaseChatModel | None = None,
    retriever: BaseRetriever | None = None,
):
    """
    Output: the input dict plus "docs" (retrieved chunks), "answer" (str)
    and "sources" (labels of the retrieved chunks, not necessarily all used).
    """
    if llm is None:
        llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai")
    if retriever is None:
        retriever = create_retriever()

    to_prompt_input = RunnableLambda(
        lambda x: {"question": x["question"], "context": format_docs(x["docs"])}
    )
    generate = to_prompt_input | create_rag_prompt() | llm | StrOutputParser()

    return (
        RunnablePassthrough.assign(docs=itemgetter("question") | retriever)
        | RunnablePassthrough.assign(
            answer=generate,
            sources=lambda x: list(dict.fromkeys(source_label(d) for d in x["docs"])),
        )
    )
