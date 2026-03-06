"""
Backend API for AGENTIC_BUG_HUNTER. Exposes the pipeline to the frontend.
Uses: agents, llm.client, utils.csv_writer, config.
"""
from __future__ import annotations

import io
import tempfile
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from agents.dataset_agent import DatasetAgent
from agents.explanation_agent import ExplanationAgent
from agents.llm_bug_agent import LLMBugAgent
from agents.retrieval_agent import RetrievalAgent

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

dataset_agent = DatasetAgent()
bug_agent = LLMBugAgent()
retriever = RetrievalAgent()
explainer = ExplanationAgent()


def run_pipeline(csv_path: Path) -> list[dict]:
    """Run bug detection pipeline on a CSV file; return list of result dicts."""
    df = pd.read_csv(csv_path)
    id_col, code_col, correct_col = dataset_agent.detect_columns(df)
    results: list[dict] = []
    for _, row in df.iterrows():
        code = str(row[code_col])
        correct = str(row[correct_col]) if correct_col else ""
        bug_line, explanation = bug_agent.detect(code, correct)
        context = retriever.retrieve(code)
        final_explanation = explainer.generate(explanation, context)
        results.append({
            "id": row[id_col],
            "bug_line": int(bug_line),
            "explanation": final_explanation,
        })
    return results


@app.route("/")
def index():
    """Serve the frontend."""
    return send_file(Path(__file__).parent / "frontend" / "index.html")


@app.route("/api/health", methods=["GET"])
def health():
    """Health/status check."""
    from config import OPENROUTER_API_KEY, MCP_URL
    return jsonify({
        "status": "ok",
        "api_key_set": bool(OPENROUTER_API_KEY),
        "mcp_url": MCP_URL,
    })


@app.route("/api/run", methods=["POST"])
def run():
    """Accept CSV file, run pipeline, return JSON results and optionally CSV bytes."""
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    if not file.filename.lower().endswith(".csv"):
        return jsonify({"error": "File must be a CSV"}), 400

    try:
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as tmp:
            tmp.write(file.read())
            tmp_path = Path(tmp.name)
        try:
            results = run_pipeline(tmp_path)
        finally:
            tmp_path.unlink(missing_ok=True)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Pipeline failed: {e}"}), 500

    return jsonify({"results": results, "count": len(results)})


@app.route("/api/download", methods=["POST"])
def download():
    """Accept JSON body with results array; return CSV file."""
    data = request.get_json()
    if not data or "results" not in data:
        return jsonify({"error": "Missing 'results' in body"}), 400
    results = data["results"]
    if not results:
        return jsonify({"error": "Results cannot be empty"}), 400

    buf = io.BytesIO()
    pd.DataFrame(results).to_csv(buf, index=False)
    buf.seek(0)
    return send_file(
        buf,
        mimetype="text/csv",
        as_attachment=True,
        download_name="bug_report.csv",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
