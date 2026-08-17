"""
Natural-language intent detection for Jarvis.
"""

from difflib import SequenceMatcher


class IntentManager:

    def _similar(self, text: str, target: str, threshold: float = 0.75) -> bool:
        """Check whether two pieces of text are reasonably similar."""
        return SequenceMatcher(
            None,
            text.lower(),
            target.lower(),
        ).ratio() >= threshold

    def detect(self, command: str) -> dict:
        """
        Detect the user's intended action.
        """

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

        if any(
            phrase in text
            for phrase in [
                "what do you remember",
                "what are my memories",
                "show my memories",
                "list my memories",
            ]
        ):
            return {
                "intent": "recall_memories",
            }

        # -------------------------
        # Direct application commands
        # -------------------------

        for phrase in ["open ", "launch ", "start "]:

            if text.startswith(phrase):

                application = original[len(phrase):].strip()

                return {
                    "intent": "open_application",
                    "application": application,
                }

        # -------------------------
        # Natural language
        # -------------------------

        if (
            "open" in text
            and "notes" in text
        ):
            return {
                "intent": "open_application",
                "application": "Notes",
            }

        if (
            "open" in text
            and (
                "music" in text
                or "apple music" in text
            )
        ):
            return {
                "intent": "open_application",
                "application": "Apple Music",
            }

        if "open" in text and "calculator" in text:
            return {
                "intent": "open_application",
                "application": "Calculator",
            }

        # -------------------------
        # Handle common typos
        # -------------------------

        words = text.split()

        for word in words:

            if self._similar(word, "oprn"):
                if "notes" in words:
                    return {
                        "intent": "open_application",
                        "application": "Notes",
                    }

        # -------------------------
        # Chat
        # -------------------------

        return {
            "intent": "chat",
            "message": original,
        }