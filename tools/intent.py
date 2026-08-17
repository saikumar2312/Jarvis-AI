"""
Natural-language intent detection for Jarvis.
"""

import re
from difflib import SequenceMatcher


class IntentManager:

    OPEN_WORDS = [
        "open",
        "launch",
        "start",
    ]

    def _similar(self, text: str, target: str, threshold: float = 0.75) -> bool:
        return SequenceMatcher(
            None,
            text.lower(),
            target.lower(),
        ).ratio() >= threshold

    def _extract_application(self, command: str) -> str | None:
        """
        Try to extract an application name from a natural-language request.
        """

        text = command.strip()

        # Common sentence patterns.
        patterns = [
            r"(?:can you|could you|please|would you)?\s*"
            r"(?:open|launch|start)\s+(?:my\s+)?(.+?)(?:\s+for me)?[?.!]*$",

            r"(?:i want to|i need to|i'd like to)\s+"
            r"(?:open|launch|start)\s+(?:my\s+)?(.+?)[?.!]*$",

            r"(?:open|launch|start)\s+(?:the\s+)?"
            r"(?:app|application)?\s*(.+?)[?.!]*$",
        ]

        for pattern in patterns:

            match = re.match(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:
                application = match.group(1).strip()

                # Remove common trailing words.
                application = re.sub(
                    r"\s+(app|application)$",
                    "",
                    application,
                    flags=re.IGNORECASE,
                )

                if application:
                    return application

        return None

    def detect(self, command: str) -> dict:

        original = command.strip()
        text = original.lower()

        # -------------------------
        # Memory
        # -------------------------

        if text.startswith("remember "):

            content = original[9:].strip()

            if content.lower().startswith("that "):
                content = content[5:].strip()

            return {
                "intent": "remember",
                "content": content,
            }

        # -------------------------
        # Recall
        # -------------------------

        recall_phrases = [
            "what do you remember",
            "what are my memories",
            "show my memories",
            "list my memories",
            "what have you remembered",
        ]

        if any(phrase in text for phrase in recall_phrases):
            return {
                "intent": "recall_memories",
            }

        # -------------------------
        # Application opening
        # -------------------------

        application = self._extract_application(original)

        if application:

            # Handle common typo: "oprn"
            if "oprn" in application.lower():
                application = application.lower().replace(
                    "oprn",
                    "open",
                )

            return {
                "intent": "open_application",
                "application": application,
            }

        # -------------------------
        # Chat
        # -------------------------

        return {
            "intent": "chat",
            "message": original,
        }