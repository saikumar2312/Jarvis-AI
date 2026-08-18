"""
Registry of tools available to Jarvis.
"""

from tools.manager import ToolManager


class ToolRegistry:

    def __init__(self):
        self.tools = ToolManager()

    def list_tools(self) -> list[str]:
        """Return the names of available tools."""

        return [
            "open_application",
            "remember",
            "recall_memories",
            "list_documents",
            "create_folder",
            "create_text_file",
            "search_documents",
            "read_text_file",
        ]

    def execute(self, tool_name: str, **kwargs):
        """Execute a registered tool."""

        # -------------------------
        # Desktop
        # -------------------------

        if tool_name == "open_application":
            return self.tools.open_application(
                kwargs["application"]
            )

        # -------------------------
        # Memory
        # -------------------------

        if tool_name == "remember":
            return self.tools.remember(
                kwargs["content"]
            )

        if tool_name == "recall_memories":
            return self.tools.recall_memories()

        # -------------------------
        # Files
        # -------------------------

        if tool_name == "list_documents":
            return self.tools.list_documents()

        if tool_name == "create_folder":
            return self.tools.create_folder(
                kwargs["name"]
            )

        if tool_name == "create_text_file":
            return self.tools.create_text_file(
                kwargs["name"]
            )

        if tool_name == "search_documents":
            return self.tools.search_documents(
                kwargs["query"]
            )

        if tool_name == "read_text_file":
            return self.tools.read_text_file(
                kwargs["name"]
            )

        raise ValueError(
            f"Unknown tool: {tool_name}"
        )