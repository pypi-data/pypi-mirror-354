from dataclasses import dataclass
from typing import Optional

@dataclass
class LLMConfig:
    """Holds configuration for the LLM provider."""
    provider: str                  # "openai", "openrouter", or "ollama"
    api_key: str                   # API key or token
    base_url: Optional[str] = None # e.g. custom OpenRouter or Ollama URL
    model: str = "gpt-4o-mini"
