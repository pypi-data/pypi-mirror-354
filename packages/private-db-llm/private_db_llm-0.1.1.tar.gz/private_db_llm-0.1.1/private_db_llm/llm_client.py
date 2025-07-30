from abc import ABC, abstractmethod
from .config import LLMConfig
from .exceptions import LLMResponseError

# OpenAI implementation
from openai import OpenAI

# HTTP client for others
import httpx

class LLMClient(ABC):
    """Interface for any LLM provider."""
    def __init__(self, config: LLMConfig):
        self.config = config

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Returns the raw SQL string from the LLM."""
        pass

class OpenAIClient(LLMClient):
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        # instantiate the new client
        self.client = OpenAI(api_key=config.api_key)

    def generate(self, prompt: str) -> str:
        try:
            resp = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": "You are an expert SQL generator."},
                    {"role": "user",   "content": prompt},
                ],
                temperature=0,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            raise LLMResponseError(f"OpenAI v1 client error: {e}")


class OpenRouterClient(LLMClient):
    def generate(self, prompt: str) -> str:
        if not self.config.base_url:
            raise LLMResponseError("OpenRouter base_url not configured.")
        headers = {"Authorization": f"Bearer {self.config.api_key}"}
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": "You are an expert SQL generator."},
                {"role": "user", "content": prompt},
            ],
        }
        r = httpx.post(f"{self.config.base_url}/v1/chat/completions",
                       json=payload, headers=headers, timeout=30.0)
        r.raise_for_status()
        data = r.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise LLMResponseError(f"OpenRouter response invalid: {e}")

class OllamaClient(LLMClient):
    def generate(self, prompt: str) -> str:
        if not self.config.base_url:
            raise LLMResponseError("Ollama base_url not configured.")
        payload = {"model": self.config.model, "prompt": prompt}
        r = httpx.post(f"{self.config.base_url}/generate",
                       json=payload, timeout=30.0)
        r.raise_for_status()
        data = r.json()
        try:
            return data.get("results", [{}])[0].get("text", "").strip()
        except Exception as e:
            raise LLMResponseError(f"Ollama response invalid: {e}")
