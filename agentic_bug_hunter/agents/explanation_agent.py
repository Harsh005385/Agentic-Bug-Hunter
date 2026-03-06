from __future__ import annotations

from typing import List, Sequence


class ExplanationAgent:
    """Combines LLM explanation with optional retrieved context into a final explanation string."""

    def generate(self, explanation: str, context: Sequence[str]) -> str:
        if context and len(context) > 0:
            return f"{explanation}\n\nKnowledge Context:\n{context[0]}"
        return explanation