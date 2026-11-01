"""
Indexing step of the RAG Pattern: load -> split -> embed -> store.

This runs once (or whenever the documents change), not on every question.
"""

from pathlib import Path

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore, VectorStoreRetriever
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "nuvem"


def load_documents(data_dir: Path = DATA_DIR) -> list[Document]:
    """Read every markdown file and keep its file name as the source."""
    return [
        Document(page_content=path.read_text(encoding="utf-8"), metadata={"source": path.name})
        for path in sorted(data_dir.glob("*.md"))
    ]


def split_documents(
    documents: list[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 100,
) -> list[Document]:
    """
    Split by markdown headers first, so each chunk is one topic, then by
    size, so no chunk is too long. Header names go into the metadata.
    """
    by_header = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "title"), ("##", "section")],
        strip_headers=False,
    )
    by_size = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    chunks: list[Document] = []
    for doc in documents:
        sections = by_header.split_text(doc.page_content)
        for section in sections:
            section.metadata["source"] = doc.metadata["source"]
        chunks.extend(by_size.split_documents(sections))
    return chunks


def create_retriever(
    embeddings: Embeddings | None = None,
    k: int = 3,
    data_dir: Path = DATA_DIR,
) -> VectorStoreRetriever:
    """Index the documents in memory and return a retriever for the top k chunks."""
    if embeddings is None:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

    chunks = split_documents(load_documents(data_dir))
    vectorstore = InMemoryVectorStore.from_documents(chunks, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": k})
