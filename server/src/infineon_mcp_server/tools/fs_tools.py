from __future__ import annotations

import os

from fastmcp import FastMCP


def register_fs_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    def list_files_and_folders() -> list[str]:
        return os.listdir(".")

