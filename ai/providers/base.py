"""
Base interface for AI providers.
"""

from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def ask(self, prompt: str) -> str:
        """Send a prompt to the AI provider and return its response."""
        raise NotImplementedError