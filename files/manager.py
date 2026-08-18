"""
Controlled file management tools for Jarvis.

Jarvis is restricted to the user's Documents folder for
file-management operations.
"""

from pathlib import Path


class FileManager:

    # Directories that should never be searched.
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
        """
        Return a path inside Documents.

        Prevents paths such as:
        ../../some-file
        /Users/...
        """

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
    # Check ignored directory
    # -------------------------

    def _should_ignore(self, path: Path) -> bool:
        """
        Determine whether a path belongs to a directory
        that should be ignored during searches.
        """

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
    # List Documents
    # -------------------------

    def list_documents(self) -> str:
        """List files and folders in Documents."""

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
            prefix = "[Folder]" if item.is_dir() else "[File]"
            lines.append(f"- {prefix} {item.name}")

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
            return f"Created folder '{name}' in Documents."

        except OSError as error:
            return f"I couldn't create the folder: {error}"

    # -------------------------
    # Create Text File
    # -------------------------

    def create_text_file(self, name: str) -> str:
        """Create an empty text file inside Documents."""

        name = name.strip()

        if not name:
            return "Please specify a file name."

        if "/" in name or "\\" in name:
            return "File names cannot contain path separators."

        if not name.endswith(".txt"):
            name += ".txt"

        file_path = self._safe_document_path(name)

        if file_path is None:
            return "That file name is not allowed."

        if file_path.exists():
            return f"The file '{name}' already exists."

        try:
            file_path.touch()
            return f"Created '{name}' in Documents."

        except OSError as error:
            return f"I couldn't create the file: {error}"

    # -------------------------
    # Search Documents
    # -------------------------

    def search_documents(self, query: str) -> str:
        """
        Search for files and folders inside Documents.

        Searches individual words so that:

            internship report

        can find:

            Social-Internship-Report.key

        Generated/dependency directories such as node_modules
        and .venv are ignored.
        """

        query = query.strip().lower()

        if not query:
            return "Please specify what you want me to search for."

        if not self.documents.exists():
            return "Your Documents folder could not be found."

        # Break query into useful search words.
        words = [
            word.strip(".,!?-_")
            for word in query.split()
            if word.strip(".,!?-_")
        ]

        if not words:
            return "Please specify what you want me to search for."

        matches = []

        try:
            for item in self.documents.rglob("*"):

                # Ignore generated/dependency/hidden directories.
                if self._should_ignore(item):
                    continue

                item_name = item.name.lower()

                # Normalize common filename separators.
                normalized_name = (
                    item_name
                    .replace("-", " ")
                    .replace("_", " ")
                    .replace(".", " ")
                )

                # Count matching search words.
                matched_words = sum(
                    1
                    for word in words
                    if word in normalized_name
                )

                if matched_words > 0:
                    matches.append(
                        (
                            matched_words,
                            item,
                        )
                    )

        except OSError as error:
            return f"I couldn't search Documents: {error}"

        if not matches:
            return f"I couldn't find anything matching '{query}'."

        # Best matches first.
        matches.sort(
            key=lambda result: (
                -result[0],
                str(result[1]).lower(),
            )
        )

        lines = [
            f"Search results for '{query}':"
        ]

        for matched_words, item in matches:

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
    # Read Text File
    # -------------------------

    def read_text_file(
        self,
        name: str,
        max_characters: int = 12000,
    ) -> str:
        """
        Read a text file inside Documents.

        Reading is intentionally limited to text files.
        """

        name = name.strip()

        if not name:
            return "Please specify a file name."

        file_path = self._safe_document_path(name)

        if file_path is None:
            return "That file path is not allowed."

        if not file_path.exists():
            return f"I couldn't find '{name}' in Documents."

        if not file_path.is_file():
            return f"'{name}' is not a file."

        if file_path.suffix.lower() not in {
            ".txt",
            ".md",
            ".py",
            ".json",
            ".csv",
            ".log",
        }:
            return (
                "I can currently read text files such as "
                ".txt, .md, .py, .json, .csv, and .log. "
                f"'{name}' is not a supported text file."
            )

        try:
            content = file_path.read_text(
                encoding="utf-8"
            )

        except UnicodeDecodeError:
            return (
                f"I couldn't read '{name}' as UTF-8 text."
            )

        except OSError as error:
            return f"I couldn't read '{name}': {error}"

        if not content:
            return f"'{name}' is empty."

        if len(content) > max_characters:
            content = (
                content[:max_characters]
                + "\n\n[File truncated]"
            )

        return (
            f"Contents of '{name}':\n\n"
            f"{content}"
        )