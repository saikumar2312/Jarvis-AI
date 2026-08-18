"""
AI-assisted intent detection for Jarvis.

The AI only decides what the user wants.
It never executes tools directly.
"""

from ai.manager import AIManager


class AIIntentDetector:

    def __init__(self):
        self.ai = AIManager()

    def detect(self, command: str) -> dict:

        prompt = f"""
You are Jarvis's intent classifier.

Your job is ONLY to classify the user's request.

Available intents:

1. open_application
Open a macOS application.

Examples:
Open Notes
Launch Safari
Start Calculator

2. open_file
Open a specific file or document from the user's Documents folder.

Examples:
Open my internship report
Open my presentation
Launch my project file
Open Social-Internship-Report.key

IMPORTANT:
If the user says "open", "launch", or "start" and is referring
to a document, report, presentation, file, or something that
sounds like a personal file, ALWAYS use open_file.

3. remember
Save information to Jarvis memory.

Examples:
Remember that I like Python
Keep in mind that I am building Jarvis

4. recall_memories
Tell the user what Jarvis remembers.

Examples:
What do you remember?
What have you remembered about me?

5. list_documents
Show the contents of the Documents folder.

Examples:
Show me my Documents
What is inside my Documents folder?
List my files

6. create_folder
Create a folder inside Documents.

7. create_text_file
Create a text file inside Documents.

8. search_documents
SEARCH for a file when the user explicitly asks to find,
search, locate, or look for something.

Examples:
Find my internship report
Search for my Python files
Locate my project

IMPORTANT:
"Find" or "search" means search_documents.
"Open" means open_file when referring to a file.

9. read_text_file
Read the contents of a supported text file.

Examples:
Read notes.txt
Read my text file

10. chat
Normal questions and conversation.

User request:
{command}

Return ONLY:

intent|value

Examples:

Open Notes
→ open_application|Notes

Open my internship report
→ open_file|internship report

Open my presentation
→ open_file|presentation

Open Social-Internship-Report.key
→ open_file|Social-Internship-Report.key

Find my internship report
→ search_documents|internship report

Search for my Python files
→ search_documents|Python

Read notes.txt
→ read_text_file|notes.txt

Remember that I prefer Python
→ remember|I prefer Python

What do you remember?
→ recall_memories|

Show my Documents
→ list_documents|

What is machine learning?
→ chat|

Rules:

- Return exactly one intent.
- Return exactly one line.
- Do not explain.
- Do not use markdown.
- Do not return shell commands.
- Do not return absolute paths.
- "open" + application → open_application.
- "open" + file/document/report/presentation/project → open_file.
- "find", "search", "locate", or "look for" → search_documents.
- For open_file, return the user's description of the file.
- For search_documents, return the search terms.
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
            "open_file",
            "remember",
            "recall_memories",
            "list_documents",
            "create_folder",
            "create_text_file",
            "search_documents",
            "read_text_file",
            "chat",
        }

        if intent not in allowed:
            return {
                "intent": "chat",
                "message": command,
            }

        if intent == "open_application":
            return {
                "intent": "open_application",
                "application": value,
            }

        if intent == "open_file":
            return {
                "intent": "open_file",
                "name": value,
            }

        if intent == "remember":
            return {
                "intent": "remember",
                "content": value,
            }

        if intent == "recall_memories":
            return {
                "intent": "recall_memories",
            }

        if intent == "list_documents":
            return {
                "intent": "list_documents",
            }

        if intent == "create_folder":
            return {
                "intent": "create_folder",
                "name": value,
            }

        if intent == "create_text_file":
            return {
                "intent": "create_text_file",
                "name": value,
            }

        if intent == "search_documents":
            return {
                "intent": "search_documents",
                "query": value,
            }

        if intent == "read_text_file":
            return {
                "intent": "read_text_file",
                "name": value,
            }

        return {
            "intent": "chat",
            "message": command,
        }