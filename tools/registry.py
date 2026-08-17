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
        ]

    def execute(self, tool_name: str, **kwargs):
        """Execute a registered tool."""

        if tool_name == "open_application":
            return self.tools.open_application(
                kwargs["application"]
            )

        if tool_name == "remember":
            return self.tools.remember(
                kwargs["content"]
            )

        if tool_name == "recall_memories":
            return self.tools.recall_memories()

        raise ValueError(f"Unknown tool: {tool_name}")