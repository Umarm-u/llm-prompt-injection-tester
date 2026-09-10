"""OpenAI provider."""

import os

from openai import OpenAI

from .base import BaseProvider, LLMResponse


class OpenAIProvider(BaseProvider):
    name = "openai"

    def __init__(self, model: str = "gpt-4o-mini", api_key: str | None = None):
        self.model = model
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def complete(self, system_prompt: str, user_prompt: str, **kwargs) -> LLMResponse:
        resp = self.client.chat.completions.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", 1024),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return LLMResponse(
            text=resp.choices[0].message.content or "",
            model=self.model,
            provider=self.name,
            raw=resp.model_dump(),
        )
