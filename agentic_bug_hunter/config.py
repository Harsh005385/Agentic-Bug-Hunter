import os

from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3-nano-30b-a3b:free")

MCP_URL = os.getenv("MCP_URL", "http://localhost:8003")