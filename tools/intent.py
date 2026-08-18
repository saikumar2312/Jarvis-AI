"""
Rule-based intent detection for Jarvis.

This handles obvious commands quickly.

If a request is unclear, it returns "unknown" so that
AIIntentDetector can handle it.
"""

import re


class IntentManager:

    def __init__(self):
        pass

    def detect(self, command: str) -> dict:

        original = command.strip()
        text = original.lower().strip()

        if not text:
            return {
                "intent": "unknown",
                "message": original,
            }

        # --------------------------------
        # Recall memories
        # --------------------------------

        recall_patterns = [
            r"what do you remember",
            r"what have you remembered",
            r"show me what you remember",
            r"what memories do you have",
            r"tell me what you remember",
        ]

        for pattern in recall_patterns:
            if re.search(pattern, text):
                return {
                    "intent": "recall_memories"
                }

        # --------------------------------
        # Remember
        # --------------------------------

        remember_patterns = [
            r"^remember that (.+)$",
            r"^remember (.+)$",
            r"^please remember that (.+)$",
            r"^please remember (.+)$",
            r"^keep in mind that (.+)$",
            r"^don't forget that (.+)$",
            r"^dont forget that (.+)$",
        ]

        for pattern in remember_patterns:

            match = re.search(
                pattern,
                text,
            )

            if match:
                content = match.group(1).strip()

                return {
                    "intent": "remember",
                    "content": content,
                }

        # --------------------------------
        # Open application
        # --------------------------------

        application_match = re.match(
            r"^(?:open|launch|start)\s+(?:the\s+)?(.+)$",
            text,
        )

        if application_match:

            target = application_match.group(1).strip()

            # Words that strongly suggest this is a file,
            # document, report, folder, etc. rather than
            # an application.
            file_indicators = [
                "file",
                "document",
                "report",
                "folder",
                ".txt",
                ".pdf",
                ".doc",
                ".docx",
                ".key",
                ".ppt",
                ".pptx",
                ".xlsx",
                ".csv",
                ".json",
                ".md",
                ".py",
            ]

            looks_like_file = any(
                indicator in target
                for indicator in file_indicators
            )

            if looks_like_file:

                return {
                    "intent": "unknown",
                    "message": original,
                }

            # Otherwise let the existing desktop
            # application tool handle it.

            return {
                "intent": "open_application",
                "application": target,
            }

        # --------------------------------
        # List Documents
        # --------------------------------

        document_list_patterns = [
            r"show me .*documents",
            r"show .*documents",
            r"list .*documents",
            r"what is inside .*documents",
            r"what's inside .*documents",
            r"what are in .*documents",
            r"show my documents",
        ]

        for pattern in document_list_patterns:

            if re.search(pattern, text):

                return {
                    "intent": "list_documents"
                }

        # --------------------------------
        # Search documents
        # --------------------------------

        search_match = re.match(
            r"^(?:find|search for|search)\s+(.+)$",
            text,
        )

        if search_match:

            query = search_match.group(1).strip()

            return {
                "intent": "unknown",
                "message": original,
            }

        # --------------------------------
        # Create folder
        # --------------------------------

        folder_match = re.match(
            r"^(?:create|make)\s+(?:a\s+)?folder\s+(?:called|named)?\s*(.+)$",
            text,
        )

        if folder_match:

            name = folder_match.group(1).strip()

            return {
                "intent": "create_folder",
                "name": name,
            }

        # --------------------------------
        # Create text file
        # --------------------------------

        file_match = re.match(
            r"^(?:create|make)\s+(?:a\s+)?(?:text\s+)?file\s+(?:called|named)?\s*(.+)$",
            text,
        )

        if file_match:

            name = file_match.group(1).strip()

            return {
                "intent": "create_text_file",
                "name": name,
            }

        # --------------------------------
        # Unknown
        # --------------------------------

        return {
            "intent": "unknown",
            "message": original,
        }