# Architecture

## Overview

This project is a Python MCP server built with `fastmcp`.

- The server exposes MCP **tools** (functions) like `add`, `multiply`, and `search_documents`.
- The `search_documents` tool uses a LlamaIndex `VectorIndexRetriever` backed by a persisted index in `storage/`.
- Embeddings are generated with `llama_index.embeddings.huggingface.HuggingFaceEmbedding`, pointing at a local model folder (`embedding_model/`).

## Key components

- `src/infineon_mcp_server/app.py`: server composition (`create_mcp`, `run`) + retriever construction.
- `src/infineon_mcp_server/tools/*`: tool registration functions (each module registers one “tool area”).
- `embedding_model/`: local embedding model artifacts (tokenizer/config and optional ONNX files).
- `storage/`: LlamaIndex persisted index stores (docstore, vector store, etc.).

## Entry points

- `mcp_server.py`: root wrapper for running the server (kept for backwards compatibility).
- `python -m infineon_mcp_server`: module entrypoint (uses `src/infineon_mcp_server/__main__.py`).

