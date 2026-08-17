"""
Controlled file management tools for Jarvis.
"""

from pathlib import Path


class FileManager:

    def __init__(self):
        self.home = Path.home()
        self.documents = self.home / "Documents"
        self.desktop = self.home / "Desktop"
        self.downloads = self.home / "Downloads"

    def list_documents(self) -> str:
        """List files and folders in Documents."""

        if not self.documents.exists():
            return "Your Documents folder could not be found."

        items = sorted(
            self.documents.iterdir(),
            key=lambda item: (not item.is_dir(), item.name.lower()),
        )

        if not items:
            return "Your Documents folder is empty."

        lines = ["Your Documents contains:"]

        for item in items:
            prefix = "[Folder]" if item.is_dir() else "[File]"
            lines.append(f"- {prefix} {item.name}")

        return "\n".join(lines)

    def create_folder(self, name: str) -> str:
        """Create a folder inside Documents."""

        name = name.strip()

        if not name:
            return "Please specify a folder name."

        if "/" in name or "\\" in name:
            return "Folder names cannot contain path separators."

        folder = self.documents / name

        if folder.exists():
            return f"The folder '{name}' already exists."

        try:
            folder.mkdir()
            return f"Created folder '{name}' in Documents."

        except OSError as error:
            return f"I couldn't create the folder: {error}"

    def create_text_file(self, name: str) -> str:
        """Create an empty text file inside Documents."""

        name = name.strip()

        if not name:
            return "Please specify a file name."

        if "/" in name or "\\" in name:
            return "File names cannot contain path separators."

        if not name.endswith(".txt"):
            name += ".txt"

        file_path = self.documents / name

        if file_path.exists():
            return f"The file '{name}' already exists."

        try:
            file_path.touch()
            return f"Created '{name}' in Documents."

        except OSError as error:
            return f"I couldn't create the file: {error}"