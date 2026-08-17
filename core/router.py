"""
Routes user commands to the appropriate module.
"""

from ai.manager import AIManager
from tools.registry import ToolRegistry


class Router:

    def __init__(self):
        self.ai = AIManager()
        self.tools = ToolRegistry()

    def route(self, command: str):

        command = command.strip()

        if not command:
            return ""

        lower_command = command.lower().strip()

        # -------------------------
        # Basic commands
        # -------------------------

        if lower_command == "hello":
            return "Hello Sai! 👋"

        if lower_command == "help":
            return (
                "Commands:\n"
                "- hello\n"
                "- help\n"
                "- remember <something>\n"
                "- what do you remember?\n"
                "- open <application>\n"
                "- exit\n"
                "- Anything else will be sent to AI."
            )

        # -------------------------
        # Memory
        # -------------------------

        if lower_command.startswith("remember "):

            content = command[len("remember "):].strip()

            if content.lower().startswith("that "):
                content = content[5:].strip()

            return self.tools.execute(
                "remember",
                content=content,
            )

        recall_commands = {
            "what do you remember",
            "what do you remember?",
            "show my memories",
            "show my memories?",
            "list my memories",
            "list my memories?",
            "what are my memories",
            "what are my memories?",
        }

        if lower_command in recall_commands:

            memories = self.tools.execute(
                "recall_memories"
            )

            if not memories:
                return "I don't have any memories yet."

            lines = ["Here is what I remember:"]

            for _, content, _ in memories:
                lines.append(f"- {content}")

            return "\n".join(lines)

        # -------------------------
        # Desktop
        # -------------------------

        if lower_command.startswith("open "):

            application = command[5:].strip()

            if not application:
                return "Please tell me which application to open."

            return self.tools.execute(
                "open_application",
                application=application,
            )

        # -------------------------
        # AI
        # -------------------------

        return self.ai.ask(command)