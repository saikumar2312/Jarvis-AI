"""
AI-assisted intent detection for Jarvis.

The AI is only used to classify requests.
It does not execute commands.
"""

from ai.manager import AIManager


class AIIntentDetector:

    def __init__(self):
        self.ai = AIManager()

    def detect(self, command: str) -> dict:
        prompt = f"""
You are the intent classifier for Jarvis.

Available tools:

1. open_application
   Use this when the user wants to open or launch a Mac application.

2. remember
   Use this when the user wants Jarvis to remember information.

3. recall_memories
   Use this when the user asks what Jarvis remembers.

4. chat
   Use this for normal questions and conversation.

User request:
{command}

Return ONLY one line in this exact format:

intent|value

Examples:

open_application|Notes
open_application|Safari
remember|My favorite language is Python
recall_memories|
chat|

Do not explain your answer.
Do not use markdown.
"""

        response = self.ai.ask(prompt).strip()

        if "|" not in response:
            return {
                "intent": "chat",
                "message": command,
            }

        intent, value = response.split("|", 1)

        intent = intent.strip()
        value = value.strip()

        allowed = {
            "open_application",
            "remember",
            "recall_memories",
            "chat",
        }

        if intent not in allowed:
            return {
                "intent": "chat",
                "message": command,
            }

        if intent == "open_application":
            return {
                "intent": intent,
                "application": value,
            }

        if intent == "remember":
            return {
                "intent": intent,
                "content": value,
            }

        if intent == "recall_memories":
            return {
                "intent": intent,
            }

        return {
            "intent": "chat",
            "message": command,
        }
        