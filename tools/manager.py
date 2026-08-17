"""
Central manager for Jarvis tools.
"""

from automation.desktop import DesktopManager
from memory.memory_manager import MemoryManager


class ToolManager:

    def __init__(self):
        self.desktop = DesktopManager()
        self.memory = MemoryManager()

    def open_application(self, application: str) -> str:
        """Open a macOS application."""
        return self.desktop.open_application(application)

    def remember(self, content: str) -> str:
        """Store a memory."""
        return self.memory.remember(content)

    def recall_memories(self) -> list[tuple]:
        """Return stored memories."""
        return self.memory.recall_all()