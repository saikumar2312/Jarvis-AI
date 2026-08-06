"""
Routes commands to the appropriate module.
"""

from ai.providers.ollama import OllamaProvider


class Router:

    def __init__(self):
        self.ai = OllamaProvider()

    def route(self, command: str):

        command = command.strip()

        # Built-in commands
        if command.lower() == "hello":
            return "Hello Sai! 👋"

        if command.lower() == "help":
            return (
                "Commands:\n"
                "- hello\n"
                "- help\n"
                "- exit\n"
                "- Anything else will be sent to AI."
            )

        # Everything else goes to AI
        return self.ai.ask(command)