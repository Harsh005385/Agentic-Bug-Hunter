from __future__ import annotations

import math

from fastmcp import FastMCP


def register_math_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    def add(a: int, b: int) -> int:
        return a + b

    @mcp.tool()
    def multiply(a: int, b: int) -> int:
        return a * b

    @mcp.tool()
    def sine(a: int) -> float:
        radians = math.radians(a)
        return math.sin(radians)

