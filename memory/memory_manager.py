"""
Memory manager for Jarvis.
"""

from memory.database import Database


class MemoryManager:

    def __init__(self):
        self.database = Database()

    def remember(self, content: str) -> str:
        """Store a new memory."""
        content = content.strip()

        if not content:
            return "There is nothing to remember."

        self.database.add_memory(content)

        return "I'll remember that."

    def recall_all(self) -> list[tuple]:
        """Return all stored memories."""
        return self.database.get_memories()

    def close(self):
        """Close the database connection."""
        self.database.close()