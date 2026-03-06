from __future__ import annotations

from pathlib import Path
from typing import Union

import pandas as pd


def write_csv(rows: list[dict], path: Union[str, Path]) -> None:
    """Write a list of dicts to a CSV file. Raises on empty rows or write failure."""
    if not rows:
        raise ValueError("Cannot write CSV: rows is empty")
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)