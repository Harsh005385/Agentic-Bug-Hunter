# Infineon MCP Server (Python)

This folder contains a Python MCP server built with `fastmcp`, plus local embedding model artifacts (`embedding_model/`) and a persisted LlamaIndex store (`storage/`).

## What this server does

- Exposes MCP tools over **SSE** on port **8003**
  - `add(a, b) -> int`
  - `multiply(a, b) -> int`
  - `sine(a) -> float` (degrees)
  - `list_files_and_folders() -> list[str]`
  - `search_documents(query) -> list[{text, score}]` (vector similarity retrieval)

## Quickstart (Windows / PowerShell)

From `server/`:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
.\.venv\Scripts\python.exe -m pip install -e .

.\.venv\Scripts\python.exe .\mcp_server.py
```

Then in another terminal:

```powershell
.\.venv\Scripts\python.exe .\client_test.py
```

## Alternative: one-command scripts

- Start server: `.\scripts\run_server.ps1`
- Run client test: `.\scripts\run_client.ps1`

## Project structure (folder architecture)

```text
server/
  README.md
  mcp_server.py
  client_test.py
  requirements.txt
  pyproject.toml
  .gitignore
  scripts/
    run_server.ps1
    run_client.ps1
  src/
    infineon_mcp_server/
      __init__.py
      __main__.py
      app.py
      tools/
        __init__.py
        fs_tools.py
        math_tools.py
        retrieval_tools.py
  docs/
    README.md
    ARCHITECTURE.md
  tests/
    README.md
  embedding_model/
    README.md
    config.json
    modules.json
    tokenizer.json
    tokenizer_config.json
    vocab.txt
    special_tokens_map.json
    sentence_bert_config.json
    config_sentence_transformers.json
    .gitattributes
    1_Pooling/
      config.json
    onnx/
      interface.py
      check_model.py
    .cache/
      huggingface/
        .gitignore
        download/
          *.metadata
  storage/
    docstore.json
    index_store.json
    graph_store.json
    default__vector_store.json
    image__vector_store.json
```

## Important notes

- **`embedding_model/` is large**: it contains local model files (and HuggingFace cache metadata). It’s typically kept local and excluded from commits (see `.gitignore`).
- **`storage/` is runtime data**: it contains the persisted LlamaIndex index stores. If you rebuild your index, these files change.

## Entry points

- **Recommended**: run the server via `mcp_server.py` (wrapper that ensures `src/` is on `PYTHONPATH`)
- **Installed package** (after `pip install -e .`):
  - `python -m infineon_mcp_server`
  - `infineon-mcp-server` (console script)

