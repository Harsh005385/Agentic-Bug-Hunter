from __future__ import annotations

from typing import Any

from fastmcp import FastMCP
from llama_index.core.retrievers import VectorIndexRetriever


def register_retrieval_tools(mcp: FastMCP, *, retriever: VectorIndexRetriever) -> None:
    @mcp.tool()
    def search_documents(query: str) -> list[dict[str, Any]]:
        nodes = retriever.retrieve(query)
        return [{"text": n.get_text(), "score": n.get_score()} for n in nodes]

