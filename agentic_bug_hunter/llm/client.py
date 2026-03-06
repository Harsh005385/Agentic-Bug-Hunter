from __future__ import annotations

import time
from typing import Any

import requests

from config import MODEL_NAME, OPENROUTER_API_KEY

API_URL = "https://openrouter.ai/api/v1/chat/completions"


def call_llm(prompt: str, retries: int = 3, timeout: int = 60) -> str:
    """
    Call OpenRouter chat API; return assistant content or a fallback string on failure.
    """
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not set in environment variables")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload: dict[str, Any] = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert C/C++/Python code reviewer. Return structured output.",
            },
            {"role": "user", "content": prompt},
        ],
    }

    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=timeout)

            if response.status_code == 200:
                body = response.json()
                try:
                    return body["choices"][0]["message"]["content"]
                except (KeyError, IndexError, TypeError):
                    print("⚠️ Unexpected API response shape:", body)
                    break

            print(f"⚠️ API error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as exc:
            print(f"⚠️ Request failed (attempt {attempt + 1}/{retries}): {exc}")

        time.sleep(2)

    return "Bug Line: 1\nExplanation: Unable to analyze due to API error."