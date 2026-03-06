from __future__ import annotations

from typing import List

import requests

from config import MCP_URL


class RetrievalAgent:
    """Retrieves relevant document snippets from MCP search_documents for a code query."""

    def retrieve(self, query: str) -> List[str]:
        try:
            response = requests.post(
                f"{MCP_URL}/tool/search_documents",
                json={"query": query},
                timeout=30,
            )
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return [item.get("text", "") for item in data if isinstance(item, dict)]
                return []
        except requests.exceptions.RequestException as exc:
            print("⚠️ MCP retrieval failed:", exc)
        except (ValueError, TypeError) as exc:
            print("⚠️ MCP response invalid:", exc)

        return []