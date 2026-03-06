from __future__ import annotations

import os
from pathlib import Path

from fastmcp import FastMCP
from llama_index.core import Settings, StorageContext, load_index_from_storage
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from .tools.fs_tools import register_fs_tools
from .tools.math_tools import register_math_tools
from .tools.retrieval_tools import register_retrieval_tools


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EMBEDDING_MODEL_DIR = PROJECT_ROOT / "embedding_model"
DEFAULT_STORAGE_DIR = PROJECT_ROOT / "storage"


def _resolve_dir(path_like: str | os.PathLike[str] | None, *, default: Path) -> Path:
    if path_like is None or str(path_like).strip() == "":
        return default
    p = Path(path_like)
    if not p.is_absolute():
        p = (PROJECT_ROOT / p).resolve()
    return p


def build_retriever(
    *,
    embedding_model_dir: str | os.PathLike[str] | None = None,
    storage_dir: str | os.PathLike[str] | None = None,
    similarity_top_k: int = 20,
) -> VectorIndexRetriever:
    model_dir = _resolve_dir(embedding_model_dir, default=DEFAULT_EMBEDDING_MODEL_DIR)
    storage_path = _resolve_dir(storage_dir, default=DEFAULT_STORAGE_DIR)

    embed_model = HuggingFaceEmbedding(model_name=str(model_dir))
    Settings.embed_model = embed_model

    storage_context = StorageContext.from_defaults(persist_dir=str(storage_path))
    index = load_index_from_storage(storage_context=storage_context)
    return VectorIndexRetriever(index=index, similarity_top_k=similarity_top_k)


def create_mcp(*, name: str = "ABH_Server", port: int = 8003) -> FastMCP:
    retriever = build_retriever()
    mcp = FastMCP(name, port=port)

    register_math_tools(mcp)
    register_fs_tools(mcp)
    register_retrieval_tools(mcp, retriever=retriever)

    return mcp


def run(*, transport: str = "sse", port: int = 8003) -> None:
    mcp = create_mcp(port=port)
    mcp.run(transport=transport)

