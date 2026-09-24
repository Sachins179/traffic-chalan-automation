"""
Groq client wrapper.

Provides a single shared Groq client for all LLM modules.
"""
from groq import Groq

from src.utils.config_loader import config
from src.utils.logger import get_logger

log = get_logger("llm.client")

_client: Groq | None = None


def get_client() -> Groq | None:
    """
    Return a singleton Groq client.

    Returns None if the API key is missing.
    """
    global _client
    if _client is not None:
        return _client

    api_key = config.env.get("GROQ_API_KEY", "")
    if not api_key:
        log.error("GROQ_API_KEY is missing. LLM features will be disabled.")
        return None

    _client = Groq(api_key=api_key)
    log.info("Groq client initialized (model=%s)", config.env["GROQ_VISION_MODEL"])
    return _client