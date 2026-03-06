# MCP + Agentic Bug Hunter System

This repository contains two integrated components:

1.  **MCP Server (Python)**
2.  **Agentic Bug Hunter (LLM-based code bug detection system)**

Together they form an **AI-assisted bug detection pipeline** where the
Agentic system analyzes code and optionally retrieves contextual
knowledge from the MCP server using vector search.

------------------------------------------------------------------------

# System Overview

Pipeline flow:

CSV → Dataset Agent → LLM Bug Detection → MCP Retrieval → Explanation
Agent → bug_report.csv

The **Agentic Bug Hunter** performs bug detection using LLM reasoning,
while the **MCP Server** provides additional knowledge via vector
similarity search.

------------------------------------------------------------------------

# Repository Structure

    MCP_infineon/
    │
    ├── agentic_bug_hunter/
    │   ├── api.py
    │   ├── main.py
    │   ├── config.py
    │   ├── requirements.txt
    │   │
    │   ├── frontend/
    │   │   ├── index.html
    │   │   ├── styles.css
    │   │   └── app.js
    │   │
    │   ├── agents/
    │   │   ├── dataset_agent.py
    │   │   ├── llm_bug_agent.py
    │   │   ├── retrieval_agent.py
    │   │   └── explanation_agent.py
    │   │
    │   ├── llm/
    │   │   └── client.py
    │   │
    │   └── utils/
    │       └── csv_writer.py
    │
    └── server/
        ├── mcp_server.py
        ├── client_test.py
        ├── requirements.txt
        ├── pyproject.toml
        │
        ├── src/
        │   └── infineon_mcp_server/
        │       ├── app.py
        │       └── tools/
        │           ├── math_tools.py
        │           ├── fs_tools.py
        │           └── retrieval_tools.py
        │
        ├── embedding_model/
        └── storage/

------------------------------------------------------------------------

# 1. MCP Server

The MCP server is built using **FastMCP** and exposes several tools
through **Server-Sent Events (SSE)**.

## Available MCP Tools

### Math Tools

-   add(a, b) → returns sum
-   multiply(a, b) → returns product
-   sine(a) → returns sine of angle in degrees

### File System Tool

-   list_files_and_folders() → returns files and folders in working
    directory

### Retrieval Tool

-   search_documents(query) → performs vector similarity search using
    LlamaIndex

Example response:

    [
      {
        "text": "retrieved document content",
        "score": 0.91
      }
    ]

------------------------------------------------------------------------

## Running the MCP Server

Navigate to:

    server/

Create environment:

    python -m venv .venv

Install dependencies:

    .\.venv\Scripts\python.exe -m pip install --upgrade pip
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    .\.venv\Scripts\python.exe -m pip install -e .

Run server:

    python mcp_server.py

Server runs at:

    http://localhost:8003

Test server:

    python client_test.py

------------------------------------------------------------------------

# 2. Agentic Bug Hunter

Agentic Bug Hunter is an **LLM-powered bug detection system** that
analyzes code stored in CSV files.

The system:

1.  Reads code samples from CSV
2.  Detects buggy lines using an LLM
3.  Optionally retrieves supporting context from the MCP server
4.  Generates explanations
5.  Produces `bug_report.csv`

------------------------------------------------------------------------

## Output Format

The generated CSV contains:

    id
    bug_line
    explanation

------------------------------------------------------------------------

# Running the Web Interface

Navigate to:

    agentic_bug_hunter/

Install dependencies:

    pip install -r requirements.txt

Start API server:

    python api.py

Open browser:

    http://localhost:5000

------------------------------------------------------------------------

# Running Desktop Version

    python main.py

A file picker will appear allowing you to select a CSV file.

The output `bug_report.csv` will be generated in the same folder.

------------------------------------------------------------------------

# Environment Variables

Create `.env` file in the `agentic_bug_hunter` directory.

Example:

    OPENROUTER_API_KEY=YOUR_OPENROUTER_KEY
    OPENROUTER_MODEL=nvidia/nemotron-3-nano-30b-a3b:free

    MCP_URL=http://localhost:8003

------------------------------------------------------------------------

# CSV Input Format

The input CSV should include:

-   column containing **code**
-   optional **id** column
-   optional **correct** column

Example:

    id,code,correct
    1,print("Hello",print("Hello")

------------------------------------------------------------------------

# MCP Retrieval Integration

The Agentic system queries the MCP server using:

    POST {MCP_URL}/tool/search_documents

Example:

    POST http://localhost:8003/tool/search_documents

Request body:

    {
      "query": "<code snippet>"
    }

If MCP is unavailable, the system continues using only LLM reasoning.

------------------------------------------------------------------------

# How Both Systems Work Together

    Agentic Bug Hunter
            |
            | HTTP API call
            |
            v
        MCP Server
            |
            v
    Vector Search (LlamaIndex)
            |
            v
    Context returned to LLM

Final pipeline:

    CSV → LLM Bug Detection → MCP Retrieval → Explanation → bug_report.csv

------------------------------------------------------------------------

# Notes

-   `embedding_model/` contains the local embedding model used for
    vector search.
-   `storage/` contains the persisted LlamaIndex index.
-   These directories are typically excluded from Git commits due to
    size.

------------------------------------------------------------------------

# Recommended Python Version

Python **3.10+**
