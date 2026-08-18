"""
Controlled file management tools for Jarvis.

Jarvis is restricted to the user's Documents folder for
file-management operations.
"""

from pathlib import Path
import subprocess


class FileManager:

    IGNORED_DIRECTORIES = {
        ".git",
        ".venv",
        "__pycache__",
        "node_modules",
        "build",
        "dist",
        ".dart_tool",
        ".idea",
        ".vscode",
        "Pods",
        "DerivedData",
    }

    def __init__(self):
        self.home = Path.home()
        self.documents = self.home / "Documents"
        self.desktop = self.home / "Desktop"
        self.downloads = self.home / "Downloads"

    # -------------------------
    # Safety
    # -------------------------

    def _safe_document_path(self, name: str) -> Path | None:
        """Return a path safely inside Documents."""

        name = name.strip()

        if not name:
            return None

        candidate = (self.documents / name).resolve()

        try:
            candidate.relative_to(self.documents.resolve())
        except ValueError:
            return None

        return candidate

    # -------------------------
    # Ignored directories
    # -------------------------

    def _should_ignore(self, path: Path) -> bool:
        """Check whether a path belongs to an ignored directory."""

        try:
            relative_parts = path.relative_to(
                self.documents
            ).parts
        except ValueError:
            return True

        for part in relative_parts:

            if part in self.IGNORED_DIRECTORIES:
                return True

            if part.startswith("."):
                return True

        return False

    # -------------------------
    # Search words
    # -------------------------

    def _search_matches(self, query: str) -> list[tuple[int, Path]]:
        """
        Find matching files/folders and return them with
        a simple relevance score.
        """

        query = query.strip().lower()

        words = [
            word.strip(".,!?-_")
            for word in query.split()
            if word.strip(".,!?-_")
        ]

        if not words:
            return []

        matches = []

        try:

            for item in self.documents.rglob("*"):

                if self._should_ignore(item):
                    continue

                item_name = item.name.lower()

                normalized_name = (
                    item_name
                    .replace("-", " ")
                    .replace("_", " ")
                    .replace(".", " ")
                )

                matched_words = sum(
                    1
                    for word in words
                    if word in normalized_name
                )

                if matched_words > 0:

                    # Give a small bonus when the entire query
                    # appears in the normalized filename.
                    score = matched_words

                    normalized_query = " ".join(words)

                    if normalized_query in normalized_name:
                        score += 2

                    matches.append(
                        (
                            score,
                            item,
                        )
                    )

        except OSError:
            return []

        matches.sort(
            key=lambda result: (
                -result[0],
                str(result[1]).lower(),
            )
        )

        return matches

    # -------------------------
    # Find best file
    # -------------------------

    def _find_best_file(self, query: str) -> Path | None:
        """
        Find the best matching file for a natural-language
        filename query.
        """

        matches = self._search_matches(query)

        for score, item in matches:

            if item.is_file():
                return item

        return None

    # -------------------------
    # List Documents
    # -------------------------

    def list_documents(self) -> str:
        """List files and folders directly inside Documents."""

        if not self.documents.exists():
            return "Your Documents folder could not be found."

        items = sorted(
            self.documents.iterdir(),
            key=lambda item: (
                not item.is_dir(),
                item.name.lower(),
            ),
        )

        if not items:
            return "Your Documents folder is empty."

        lines = ["Your Documents contains:"]

        for item in items:

            prefix = (
                "[Folder]"
                if item.is_dir()
                else "[File]"
            )

            lines.append(
                f"- {prefix} {item.name}"
            )

        return "\n".join(lines)

    # -------------------------
    # Create Folder
    # -------------------------

    def create_folder(self, name: str) -> str:
        """Create a folder inside Documents."""

        name = name.strip()

        if not name:
            return "Please specify a folder name."

        if "/" in name or "\\" in name:
            return "Folder names cannot contain path separators."

        folder = self._safe_document_path(name)

        if folder is None:
            return "That folder name is not allowed."

        if folder.exists():
            return f"The folder '{name}' already exists."

        try:

            folder.mkdir()

            return (
                f"Created folder '{name}' in Documents."
            )

        except OSError as error:

            return (
                f"I couldn't create the folder: {error}"
            )

    # -------------------------
    # Create Text File
    # -------------------------

    def create_text_file(self, name: str) -> str:
        """Create an empty text file inside Documents."""

        name = name.strip()

        if not name:
            return "Please specify a file name."

        if "/" in name or "\\" in name:
            return (
                "File names cannot contain path separators."
            )

        if not name.endswith(".txt"):
            name += ".txt"

        file_path = self._safe_document_path(name)

        if file_path is None:
            return "That file name is not allowed."

        if file_path.exists():
            return (
                f"The file '{name}' already exists."
            )

        try:

            file_path.touch()

            return (
                f"Created '{name}' in Documents."
            )

        except OSError as error:

            return (
                f"I couldn't create the file: {error}"
            )

    # -------------------------
    # Search Documents
    # -------------------------

    def search_documents(self, query: str) -> str:
        """
        Search for files and folders inside Documents.
        """

        query = query.strip()

        if not query:
            return (
                "Please specify what you want me "
                "to search for."
            )

        if not self.documents.exists():
            return (
                "Your Documents folder could not be found."
            )

        matches = self._search_matches(query)

        if not matches:
            return (
                f"I couldn't find anything matching "
                f"'{query}'."
            )

        lines = [
            f"Search results for '{query}':"
        ]

        for score, item in matches:

            relative = item.relative_to(
                self.documents
            )

            prefix = (
                "[Folder]"
                if item.is_dir()
                else "[File]"
            )

            lines.append(
                f"- {prefix} {relative}"
            )

        return "\n".join(lines)

    # -------------------------
    # Open File
    # -------------------------

    def open_file(self, name: str) -> str:
        """
        Open a file from Documents.

        First tries an exact filename.

        If the exact filename doesn't exist, it searches
        Documents for the best matching file.
        """

        name = name.strip()

        if not name:
            return "Please specify a file name."

        # --------------------------------
        # Try exact path first
        # --------------------------------

        file_path = self._safe_document_path(name)

        if file_path is None:
            return "That file path is not allowed."

        if file_path.exists():

            if file_path.is_dir():
                return (
                    f"'{name}' is a folder, not a file."
                )

            try:

                subprocess.Popen(
                    ["open", str(file_path)]
                )

                return f"Opened '{file_path.name}'."

            except OSError as error:

                return (
                    f"I couldn't open "
                    f"'{file_path.name}': {error}"
                )

        # --------------------------------
        # Exact path not found.
        # Search intelligently.
        # --------------------------------

        matched_file = self._find_best_file(name)

        if matched_file is None:

            return (
                f"I couldn't find '{name}' "
                "in Documents."
            )

        # --------------------------------
        # Open best match
        # --------------------------------

        try:

            subprocess.Popen(
                ["open", str(matched_file)]
            )

            return (
                f"Opened '{matched_file.name}'."
            )

        except OSError as error:

            return (
                f"I couldn't open "
                f"'{matched_file.name}': {error}"
            )

    # -------------------------
    # Read Text File
    # -------------------------

    def read_text_file(
        self,
        name: str,
        max_characters: int = 12000,
    ) -> str:
        """
        Read a supported text file inside Documents.
        """

        name = name.strip()

        if not name:
            return "Please specify a file name."

        file_path = self._safe_document_path(name)

        if file_path is None:
            return "That file path is not allowed."

        # --------------------------------
        # Exact file not found.
        # Try intelligent search.
        # --------------------------------

        if not file_path.exists():

            matched_file = self._find_best_file(name)

            if matched_file is None:
                return (
                    f"I couldn't find '{name}' "
                    "in Documents."
                )

            file_path = matched_file

        # --------------------------------
        # Validate file
        # --------------------------------

        if not file_path.is_file():
            return (
                f"'{file_path.name}' is not a file."
            )

        supported_extensions = {
            ".txt",
            ".md",
            ".py",
            ".json",
            ".csv",
            ".log",
        }

        if file_path.suffix.lower() not in supported_extensions:

            return (
                "I can currently read text files such as "
                ".txt, .md, .py, .json, .csv, and .log. "
                f"'{file_path.name}' is not a supported "
                "text file."
            )

        # --------------------------------
        # Read
        # --------------------------------

        try:

            content = file_path.read_text(
                encoding="utf-8"
            )

        except UnicodeDecodeError:

            return (
                f"I couldn't read "
                f"'{file_path.name}' as UTF-8 text."
            )

        except OSError as error:

            return (
                f"I couldn't read "
                f"'{file_path.name}': {error}"
            )

        if not content:
            return (
                f"'{file_path.name}' is empty."
            )

        if len(content) > max_characters:

            content = (
                content[:max_characters]
                + "\n\n[File truncated]"
            )

        return (
            f"Contents of '{file_path.name}':\n\n"
            f"{content}"
        )