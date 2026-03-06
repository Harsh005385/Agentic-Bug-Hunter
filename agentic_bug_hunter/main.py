from __future__ import annotations

from pathlib import Path
from tkinter import Tk, filedialog
from typing import List, Optional

import pandas as pd

from agents.dataset_agent import DatasetAgent
from agents.explanation_agent import ExplanationAgent
from agents.llm_bug_agent import LLMBugAgent
from agents.retrieval_agent import RetrievalAgent
from utils.csv_writer import write_csv


dataset_agent = DatasetAgent()
bug_agent = LLMBugAgent()
retriever = RetrievalAgent()
explainer = ExplanationAgent()


def select_file() -> str:
    """Open a file picker dialog and return the selected CSV path, or an empty string if cancelled."""
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])


def run(input_path: Optional[str] = None) -> None:
    """
    Run the bug detection pipeline on a CSV file.

    If `input_path` is not provided, a file dialog is shown.
    """
    if not input_path:
        input_path = select_file()

    if not input_path:
        print("No file selected")
        return

    csv_path = Path(input_path)
    if not csv_path.exists():
        print(f"Input file does not exist: {csv_path}")
        return

    print("📂 Selected:", csv_path)

    try:
        df = pd.read_csv(csv_path)
    except Exception as exc:  # pragma: no cover - defensive
        print(f"Failed to read CSV '{csv_path}': {exc}")
        return

    try:
        id_col, code_col, correct_col = dataset_agent.detect_columns(df)
    except ValueError as exc:
        print(f"Dataset error: {exc}")
        return

    results: List[dict] = []

    for _, row in df.iterrows():
        code = str(row[code_col])
        correct = str(row[correct_col]) if correct_col else ""

        bug_line, explanation = bug_agent.detect(code, correct)
        context = retriever.retrieve(code)
        final_explanation = explainer.generate(explanation, context)

        results.append(
            {
                "id": row[id_col],
                "bug_line": bug_line,
                "explanation": final_explanation,
            }
        )

    output_path = csv_path.parent / "bug_report.csv"
    write_csv(results, output_path)

    print("✅ Report saved to:", output_path)


if __name__ == "__main__":
    run()