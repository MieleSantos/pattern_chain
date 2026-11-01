"""RAG (Retrieval-Augmented Generation) Pattern package."""

from rag.indexing import DATA_DIR, load_documents, split_documents, create_retriever
from rag.prompts import NOT_FOUND, create_rag_prompt
from rag.chain import source_label, format_docs, create_rag_chain

__all__ = [
    "DATA_DIR",
    "load_documents",
    "split_documents",
    "create_retriever",
    "NOT_FOUND",
    "create_rag_prompt",
    "source_label",
    "format_docs",
    "create_rag_chain",
]
