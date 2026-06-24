"""Tool Definition Module.

This module provides utilities for defining and managing
tools that agents can use.
"""

from typing import Any, Callable
from dataclasses import dataclass


@dataclass
class Tool:
    """Represents a callable tool."""
    name: str
    description: str
    function: Callable[..., Any]
    parameters: dict[str, Any] | None = None


class ToolRegistry:
    """Registry for managing available tools."""

    def __init__(self):
        """Initialize the ToolRegistry."""
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Register a tool.

        Args:
            tool: Tool to register.
        """
        self.tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        """Get a tool by name.

        Args:
            name: Tool name.

        Returns:
            Tool or None if not found.
        """
        return self.tools.get(name)

    def list_tools(self) -> list[str]:
        """List all registered tool names.

        Returns:
            List of tool names.
        """
        return list(self.tools.keys())

    def unregister(self, name: str) -> bool:
        """Unregister a tool.

        Args:
            name: Tool name.

        Returns:
            True if tool was removed.
        """
        if name in self.tools:
            del self.tools[name]
            return True
        return False


def create_function_tool(
    name: str,
    description: str,
    func: Callable
) -> Tool:
    """Create a tool from a function.

    Args:
        name: Tool name.
        description: Tool description.
        func: Function to wrap.

    Returns:
        Tool instance.
    """
    return Tool(
        name=name,
        description=description,
        function=func
    )


def web_search_tool(query: str) -> str:
    """Example web search tool.

    Args:
        query: Search query.

    Returns:
        Search results placeholder.
    """
    return f"Search results for '{query}': [Result 1, Result 2, Result 3]"


def calculator_tool(expression: str) -> str:
    """Example calculator tool.

    Args:
        expression: Math expression.

    Returns:
        Calculation result.
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def file_reader_tool(file_path: str) -> str:
    """Example file reader tool.

    Args:
        file_path: Path to file.

    Returns:
        File contents.
    """
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"


def get_default_tools() -> list[Tool]:
    """Get default set of tools.

    Returns:
        List of default tools.
    """
    return [
        create_function_tool(
            "web_search",
            "Search the web for information",
            web_search_tool
        ),
        create_function_tool(
            "calculator",
            "Evaluate a mathematical expression",
            calculator_tool
        ),
        create_function_tool(
            "file_reader",
            "Read contents of a file",
            file_reader_tool
        )
    ]
