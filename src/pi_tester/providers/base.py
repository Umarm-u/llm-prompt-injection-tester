"""Base provider interface — all LLM providers implement this."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """Standardized response across all providers."""

    text: str
    model: str
    provider: str
    raw: dict


class BaseProvider(ABC):
    """Abstract base for LLM provider implementations."""

    name: str = "base"

    @abstractmethod
    def complete(self, system_prompt: str, user_prompt: str, **kwargs) -> LLMResponse:
        """Send a prompt and get a response back."""
        raise NotImplementedError
