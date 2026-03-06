from __future__ import annotations

from typing import Optional, Tuple

import pandas as pd


class DatasetAgent:
    """Detects id, code, and optional correct columns in a bug-dataset DataFrame."""

    def detect_columns(self, df: pd.DataFrame) -> Tuple[str, str, Optional[str]]:
        cols = {c.lower(): c for c in df.columns}

        id_col = next((cols[c] for c in cols if "id" in c), df.columns[0])
        code_col = next((cols[c] for c in cols if "code" in c), None)
        correct_col = next((cols[c] for c in cols if "correct" in c), None)

        if code_col is None:
            raise ValueError("No code column found in CSV")

        return id_col, code_col, correct_col