# AGENTIC_BUG_HUNTER

Upload a CSV of code samples, run an **LLM-based bug detector**, optionally enrich with **MCP document retrieval**, and generate a `bug_report.csv` containing:

- `id`
- `bug_line`
- `explanation`

This repo includes both:

- **Web UI** (Flask API + static frontend)
- **Local Tkinter runner** (file-picker based)

---

## Project structure

```
agentic_bug_hunter/
├── api.py                    # Web API + serves frontend/
├── main.py                   # Tkinter file-picker runner (no browser)
├── config.py                 # Loads .env and exposes OPENROUTER + MCP config
├── requirements.txt
├── frontend/                 # Web UI (HTML/CSS/JS)
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── agents/                   # Pipeline building blocks
│   ├── dataset_agent.py      # Detects id/code/correct columns
│   ├── llm_bug_agent.py      # Prompts LLM + parses "Bug Line" and "Explanation"
│   ├── retrieval_agent.py    # Calls MCP /tool/search_documents
│   └── explanation_agent.py  # Merges explanation + retrieved context
├── llm/
│   └── client.py             # OpenRouter Chat Completions client (retries)
├── utils/
│   └── csv_writer.py         # Writes report CSV
└── data/                     # Sample CSV inputs
```

---

## Requirements

- Python 3.10+ recommended
- OpenRouter API key (for LLM calls)
- (Optional) MCP server running (for retrieval context)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment setup (`.env`)

Create a `.env` file in the project root (same folder as `config.py`).

**Do not commit** `.env` (this project ignores it in `.gitignore`).

Example:

```env
OPENROUTER_API_KEY=YOUR_OPENROUTER_KEY
OPENROUTER_MODEL=nvidia/nemotron-3-nano-30b-a3b:free

# Optional: set if your MCP server runs elsewhere
MCP_URL=http://localhost:8003
```

---

## Running the Web UI (recommended)

Start the API server:

```bash
python api.py
```

Open the UI:

- `http://localhost:5000`

### Web API endpoints

- `GET /api/health`  
  Returns status plus whether `OPENROUTER_API_KEY` is set.
- `POST /api/run`  
  Upload a CSV as multipart form-data field `file`. Returns JSON results.
- `POST /api/download`  
  Post JSON `{ "results": [...] }` to download `bug_report.csv`.

---

## Running the Tkinter version (desktop file picker)

```bash
python main.py
```

Select your input CSV in the file dialog. Output `bug_report.csv` will be saved in the **same folder** as the selected CSV.

---

## Input CSV format

Your CSV should contain:

- A column with `code` in its name (required), e.g. `code`, `buggy_code`
- A column with `id` in its name (optional; defaults to the first column)
- A column with `correct` in its name (optional), e.g. `correct_code`

---

## How MCP retrieval fits in

`agents/retrieval_agent.py` calls:

```
POST {MCP_URL}/tool/search_documents
Body: { "query": "<code>" }
```

If the MCP server is not reachable, retrieval returns an empty list and the pipeline continues (you still get an LLM explanation).

### Note about your `server/` folder

You mentioned you have a separate folder at:

`D:\Hackathon\Infineon\MCP_infineon\server`

That is expected to host the **MCP server + model**. Make sure it is running and that `MCP_URL` points to it (default `http://localhost:8003`).

---

## Troubleshooting

- **“OPENROUTER_API_KEY not set”**
  - Ensure `.env` exists and contains `OPENROUTER_API_KEY=...`, or set it in your shell environment.
- **MCP retrieval warnings**
  - If you don’t need retrieval, ignore them.
  - Otherwise ensure the MCP server is running and `MCP_URL` is correct.
- **CSV column error**
  - Ensure your CSV has a column with `code` in its header name.

