"""Tool Definition Module.

This module provides utilities for defining and managing
tools that agents can use. Includes both sync and async tool examples.
"""

import asyncio
from typing import Any, Awaitable, Callable, Union
from dataclasses import dataclass


SyncCallable = Callable[..., Any]
AsyncCallable = Callable[..., Awaitable[Any]]
ToolFunction = Union[SyncCallable, AsyncCallable]


@dataclass
class Tool:
    """Represents a callable tool."""
    name: str
    description: str
    function: ToolFunction
    parameters: dict[str, Any] | None = None


class ToolRegistry:
    """Registry for managing available tools."""

    def __init__(self):
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self.tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self.tools.get(name)

    def list_tools(self) -> list[str]:
        return list(self.tools.keys())

    def unregister(self, name: str) -> bool:
        if name in self.tools:
            del self.tools[name]
            return True
        return False


def create_function_tool(
    name: str,
    description: str,
    func: ToolFunction,
) -> Tool:
    return Tool(name=name, description=description, function=func)


def web_search_tool(query: str) -> str:
    return f"Search results for '{query}': [Result 1, Result 2, Result 3]"


async def web_search_tool_async(query: str) -> str:
    await asyncio.sleep(0.1)
    return f"Search results for '{query}': [Result 1, Result 2, Result 3]"


def calculator_tool(expression: str) -> str:
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def file_reader_tool(file_path: str) -> str:
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"


async def file_reader_tool_async(file_path: str) -> str:
    try:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: open(file_path, "r").read())
    except Exception as e:
        return f"Error reading file: {e}"


def get_default_tools() -> list[Tool]:
    return [
        create_function_tool("web_search", "Search the web for information", web_search_tool),
        create_function_tool("calculator", "Evaluate a mathematical expression", calculator_tool),
        create_function_tool("file_reader", "Read contents of a file", file_reader_tool),
    ]


def get_async_default_tools() -> list[Tool]:
    return [
        create_function_tool("web_search", "Search the web for information", web_search_tool_async),
        create_function_tool("calculator", "Evaluate a mathematical expression", calculator_tool),
        create_function_tool("file_reader", "Read contents of a file", file_reader_tool_async),
    ]
