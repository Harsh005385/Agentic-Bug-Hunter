from __future__ import annotations

import re
from typing import Tuple

from llm.client import call_llm


class LLMBugAgent:
    """Uses an LLM to detect bug line and explanation from buggy (and optional correct) code."""

    def detect(self, code: str, correct_code: str = "") -> Tuple[int, str]:
        prompt = f"""
Analyze the following buggy code and identify:

1️⃣ Bug line number  
2️⃣ Short explanation  

Return in EXACT format:
Bug Line: <number>
Explanation: <text>

Buggy Code:
{code}

Correct Code:
{correct_code}
"""

        response = call_llm(prompt)

        line_match = re.search(r"Bug Line:\s*(\d+)", response)
        explanation_match = re.search(r"Explanation:\s*(.*)", response, re.DOTALL)

        bug_line = int(line_match.group(1)) if line_match else 1
        explanation = explanation_match.group(1).strip() if explanation_match else response

        return bug_line, explanation