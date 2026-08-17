"""
Routes user commands to the appropriate module.
"""

from ai.manager import AIManager
from tools.registry import ToolRegistry
from tools.intent import IntentManager
from tools.ai_intent import AIIntentDetector


class Router:

    def __init__(self):
        self.ai = AIManager()
        self.tools = ToolRegistry()
        self.intent = IntentManager()
        self.ai_intent = AIIntentDetector()

    def route(self, command: str):

        command = command.strip()

        if not command:
            return ""

        # -------------------------
        # Basic commands
        # -------------------------

        if command.lower() == "hello":
            return "Hello Sai! 👋"

        if command.lower() in ["exit", "quit"]:
            return "Goodbye!"

        if command.lower() == "help":
            return (
                "Commands:\n"
                "- hello\n"
                "- remember <something>\n"
                "- what do you remember?\n"
                "- open <application>\n"
                "- exit\n"
                "- Anything else will be sent to AI."
            )

        # -------------------------
        # Rule-based intent
        # -------------------------

        detected = self.intent.detect(command)
        intent = detected["intent"]

        # -------------------------
        # Memory
        # -------------------------

        if intent == "remember":
            return self.tools.execute(
                "remember",
                content=detected["content"],
            )

        # -------------------------
        # Recall memories
        # -------------------------

        if intent == "recall_memories":

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
        # Open application
        # -------------------------

        if intent == "open_application":
            return self.tools.execute(
                "open_application",
                application=detected["application"],
            )

        # -------------------------
        # AI-assisted fallback
        # -------------------------

        if intent == "unknown":

            ai_detected = self.ai_intent.detect(command)
            ai_intent = ai_detected["intent"]

            if ai_intent == "remember":
                return self.tools.execute(
                    "remember",
                    content=ai_detected["content"],
                )

            if ai_intent == "recall_memories":

                memories = self.tools.execute(
                    "recall_memories"
                )

                if not memories:
                    return "I don't have any memories yet."

                lines = ["Here is what I remember:"]

                for _, content, _ in memories:
                    lines.append(f"- {content}")

                return "\n".join(lines)

            if ai_intent == "open_application":
                return self.tools.execute(
                    "open_application",
                    application=ai_detected["application"],
                )

            # If the AI classifier also doesn't detect a tool,
            # treat the request as normal conversation.
            return self.ai.ask(command)

        # -------------------------
        # Normal AI conversation
        # -------------------------

        return self.ai.ask(detected["message"])