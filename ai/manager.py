"""
AI Manager.

Provides a single interface between Jarvis and AI providers.
"""

from ai.providers.ollama import OllamaProvider


class AIManager:

    def __init__(self):
        self.provider = OllamaProvider()

    def ask(self, prompt: str) -> str:
        """Send a prompt to the configured AI provider."""
        return self.provider.ask(prompt)