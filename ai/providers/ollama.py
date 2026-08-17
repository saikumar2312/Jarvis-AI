"""
Ollama AI provider.
"""

from ollama import chat

from ai.providers.base import AIProvider


class OllamaProvider(AIProvider):

    def __init__(self, model: str = "qwen3:4b"):
        self.model = model

    def ask(self, prompt: str) -> str:

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]