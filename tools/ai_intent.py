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
        """
        Ask Qwen to classify the user's request.

        The AI only returns an intent and value.
        Actual actions are handled later by ToolRegistry.
        """

        prompt = f"""
You are the intent classifier for Jarvis.

Available tools:

1. open_application
   Use this when the user wants to open or launch a Mac application.

2. remember
   Use this when the user wants Jarvis to remember information.

3. recall_memories
   Use this when the user asks what Jarvis remembers.

4. list_documents
   Use this when the user wants to see what is inside their Documents folder.

5. create_folder
   Use this when the user wants to create a new folder inside Documents.

6. create_text_file
   Use this when the user wants to create a text file inside Documents.

7. chat
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
list_documents|
create_folder|Projects
create_text_file|notes.txt
chat|

Rules:

- Do not explain your answer.
- Do not use markdown.
- Return only one intent.
- For create_folder, return only the folder name as the value.
- For create_text_file, return only the file name as the value.
- Never return shell commands.
- Never return file paths.
"""

        response = self.ai.ask(prompt).strip()

        # --------------------------------
        # Validate response format
        # --------------------------------

        if "|" not in response:
            return {
                "intent": "chat",
                "message": command,
            }

        intent, value = response.split("|", 1)

        intent = intent.strip()
        value = value.strip()

        # --------------------------------
        # Allowed intents
        # --------------------------------

        allowed = {
            "open_application",
            "remember",
            "recall_memories",
            "list_documents",
            "create_folder",
            "create_text_file",
            "chat",
        }

        if intent not in allowed:
            return {
                "intent": "chat",
                "message": command,
            }

        # --------------------------------
        # Open application
        # --------------------------------

        if intent == "open_application":

            if not value:
                return {
                    "intent": "chat",
                    "message": command,
                }

            return {
                "intent": "open_application",
                "application": value,
            }

        # --------------------------------
        # Remember
        # --------------------------------

        if intent == "remember":

            if not value:
                return {
                    "intent": "chat",
                    "message": command,
                }

            return {
                "intent": "remember",
                "content": value,
            }

        # --------------------------------
        # Recall memories
        # --------------------------------

        if intent == "recall_memories":

            return {
                "intent": "recall_memories",
            }

        # --------------------------------
        # List Documents
        # --------------------------------

        if intent == "list_documents":

            return {
                "intent": "list_documents",
            }

        # --------------------------------
        # Create folder
        # --------------------------------

        if intent == "create_folder":

            if not value:
                return {
                    "intent": "chat",
                    "message": command,
                }

            return {
                "intent": "create_folder",
                "name": value,
            }

        # --------------------------------
        # Create text file
        # --------------------------------

        if intent == "create_text_file":

            if not value:
                return {
                    "intent": "chat",
                    "message": command,
                }

            return {
                "intent": "create_text_file",
                "name": value,
            }

        # --------------------------------
        # Normal conversation
        # --------------------------------

        return {
            "intent": "chat",
            "message": command,
        }