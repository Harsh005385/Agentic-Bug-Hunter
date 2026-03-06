# Frontend Implementation Prompt — AGENTIC_BUG_HUNTER

Use this prompt to implement or extend the frontend for the AGENTIC_BUG_HUNTER project. The frontend must live inside the project and integrate with all existing folders and subfolders.

**Run the UI:** `pip install -r requirements.txt` then `python api.py`; open **http://localhost:5000** in a browser.

---

## Objective

Create a **frontend** (user interface) that:

1. Lives in a dedicated folder inside `AGENTIC_BUG_HUNTER` (e.g. `frontend/`).
2. **Connects** to the existing backend logic in:
   - `agents/` (DatasetAgent, LLMBugAgent, RetrievalAgent, ExplanationAgent)
   - `llm/` (OpenRouter client in `client.py`)
   - `utils/` (e.g. `csv_writer.py`)
   - `config.py` (env-based configuration)
3. Provides a **web UI** so users can:
   - Upload or select a CSV file (with columns: id, code, optional correct).
   - Trigger the bug-detection pipeline (LLM + optional MCP retrieval).
   - See progress and results (id, bug_line, explanation).
   - Download the generated `bug_report.csv`.

---

## Backend Context (Do Not Duplicate Logic)

- **Entry point:** `main.py` runs the pipeline: read CSV → detect columns → for each row run `bug_agent.detect`, `retriever.retrieve`, `explainer.generate` → write results via `write_csv`.
- **Agents:** `agents/dataset_agent.py`, `agents/llm_bug_agent.py`, `agents/retrieval_agent.py`, `agents/explanation_agent.py`.
- **LLM:** `llm/client.py` — `call_llm(prompt)` calling OpenRouter; config in `config.py` (API key, model, MCP_URL).
- **Output:** `utils/csv_writer.write_csv(rows, path)` writes the report CSV.

The frontend must **call** this logic (e.g. via a small **backend API** in the same repo that imports these modules), not reimplement it.

---

## Integration Requirements

1. **Single project root:** All code stays under `AGENTIC_BUG_HUNTER`. No separate repo for frontend.
2. **Backend API:** Add a thin HTTP API (e.g. Flask or FastAPI) in the project root that:
   - Imports from `agents`, `llm`, `utils`, `config`.
   - Exposes at least:
     - **POST** endpoint: accept CSV file upload (or path), run the same pipeline as `main.run()`, return JSON results and/or a link to download `bug_report.csv`.
     - Optional: **GET** health/config status (e.g. API key set, MCP URL).
3. **Frontend folder:** Create `frontend/` (or `frontend/public/`) containing:
   - **HTML:** One or more pages; at minimum: file upload, “Run” button, area for results (table or list), “Download report” button.
   - **CSS:** Styling for the UI (can be one file or inline).
   - **JavaScript:** Call the backend API (upload CSV, poll or wait for response, render results, trigger download).
4. **CORS:** If the API runs on a different port than the static frontend, enable CORS on the backend so the browser can call it.
5. **Consistency:** Reuse the same column semantics (id, code, correct) and the same output shape: `id`, `bug_line`, `explanation`.

---

## UI Design Guidelines

- **Clear flow:** Upload CSV → Start analysis → Show progress (e.g. “Processing row X of Y” or spinner) → Show results table (id, bug line, explanation) → Offer “Download bug_report.csv”.
- **Error handling:** Display backend errors (e.g. missing code column, API key not set, LLM/MCP failure) in the UI.
- **Accessibility:** Use semantic HTML and labels where applicable.
- **Responsive:** Layout should work on desktop and optionally on smaller screens.

---

## Folder Structure to Achieve

```
AGENTIC_BUG_HUNTER/
├── agents/           # existing
├── llm/              # existing
├── utils/            # existing
├── data/             # existing
├── config.py         # existing
├── main.py           # existing (CLI/desktop entry)
├── api.py            # NEW: backend API (Flask/FastAPI) that imports agents, llm, utils, config
├── frontend/         # NEW: frontend folder
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── requirements.txt  # add flask (or fastapi + uvicorn) if needed
└── FRONTEND_IMPLEMENTATION_PROMPT.md  # this file
```

The frontend is **connected** to the rest of the project by:

- `api.py` importing and calling `agents.*`, `llm.client`, `utils.csv_writer`, `config`.
- The browser loading `frontend/index.html` and `app.js`, which send requests to the backend API.

---

## Summary Checklist

- [ ] Create `frontend/` folder with `index.html`, `styles.css`, `app.js`.
- [ ] Add `api.py` (or equivalent) that uses `agents`, `llm`, `utils`, `config` and exposes POST (run pipeline) and optionally GET (health).
- [ ] UI: upload CSV, run, show results, download report.
- [ ] CORS enabled if frontend and API are on different origins.
- [ ] Update `requirements.txt` with API framework and run instructions (e.g. `python api.py` then open `frontend/index.html` or serve it via same app).

Use this prompt to implement the frontend so it **seamlessly integrates** with the existing AGENTIC_BUG_HUNTER structure and does not duplicate pipeline logic.
