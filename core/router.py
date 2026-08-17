"""
Routes user commands to the appropriate module.
"""

from ai.manager import AIManager


class Router:

    def __init__(self):
        self.ai = AIManager()

    def route(self, command: str):

        command = command.strip()

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

        return self.ai.ask(command)