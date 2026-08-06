"""
Ollama Provider
Handles communication with the local Ollama server.
"""

from ollama import chat


class OllamaProvider:
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