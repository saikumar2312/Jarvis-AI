"""
Central manager for Jarvis tools.
"""

from automation.desktop import DesktopManager
from memory.memory_manager import MemoryManager
from files.manager import FileManager


class ToolManager:

    def __init__(self):
        self.desktop = DesktopManager()
        self.memory = MemoryManager()
        self.files = FileManager()

    # -------------------------
    # Desktop
    # -------------------------

    def open_application(self, application: str) -> str:
        return self.desktop.open_application(application)

    # -------------------------
    # Memory
    # -------------------------

    def remember(self, content: str) -> str:
        return self.memory.remember(content)

    def recall_memories(self) -> list[tuple]:
        return self.memory.recall_all()

    # -------------------------
    # Files
    # -------------------------

    def list_documents(self) -> str:
        return self.files.list_documents()

    def create_folder(self, name: str) -> str:
        return self.files.create_folder(name)

    def create_text_file(self, name: str) -> str:
        return self.files.create_text_file(name)

    def search_documents(self, query: str) -> str:
        return self.files.search_documents(query)

    def read_text_file(self, name: str) -> str:
        return self.files.read_text_file(name)