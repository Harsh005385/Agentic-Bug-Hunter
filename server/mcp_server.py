from __future__ import annotations

import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    root = Path(__file__).resolve().parent
    src = root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))


if __name__ == "__main__":
    _ensure_src_on_path()
    from infineon_mcp_server.app import run

    run(transport="sse", port=8003)