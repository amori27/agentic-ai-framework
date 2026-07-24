"""Agent Module.

This module provides the base Agent class with tool use,
reasoning, and action capabilities. Supports both synchronous
and asynchronous tool execution.
"""

import asyncio
import inspect
from typing import Any, Awaitable, Callable, Union
from dataclasses import dataclass


SyncCallable = Callable[..., str]
AsyncCallable = Callable[..., Awaitable[str]]
ToolFunction = Union[SyncCallable, AsyncCallable]


@dataclass
class Tool:
    """Represents a tool that an agent can use."""
    name: str
    description: str
    function: ToolFunction


def _is_coroutine(func: ToolFunction) -> bool:
    return inspect.iscoroutinefunction(func)


class Agent:
    """Base agent class with reasoning and tool use."""

    def __init__(
        self,
        name: str,
        role: str,
        tools: list[Tool] | None = None,
        memory_enabled: bool = True,
    ):
        self.name = name
        self.role = role
        self.tools = tools or []
        self.memory_enabled = memory_enabled
        self.history: list[dict[str, str]] = []

    def add_tool(self, tool: Tool) -> None:
        self.tools.append(tool)

    def think(self, prompt: str) -> str:
        system_prompt = f"You are {self.name}, a {self.role}."
        if self.tools:
            system_prompt += "\n\nYou have access to these tools: "
            for tool in self.tools:
                system_prompt += f"\n- {tool.name}: {tool.description}"
        return f"[{self.name}] Processed: {prompt}"

    async def think_async(self, prompt: str) -> str:
        return self.think(prompt)

    def act(self, action: str) -> str:
        return f"[{self.name}] Action result: {action}"

    async def act_async(self, action: str) -> str:
        return self.act(action)

    def use_tool(self, tool_name: str, **kwargs: Any) -> str:
        for tool in self.tools:
            if tool.name == tool_name:
                result = tool.function(**kwargs)
                if _is_coroutine(tool.function):
                    raise RuntimeError(
                        f"Tool '{tool_name}' is async. Use 'await use_tool_async()' instead."
                    )
                return result
        return f"Tool '{tool_name}' not found"

    async def use_tool_async(self, tool_name: str, **kwargs: Any) -> str:
        for tool in self.tools:
            if tool.name == tool_name:
                if _is_coroutine(tool.function):
                    return await tool.function(**kwargs)
                return tool.function(**kwargs)
        return f"Tool '{tool_name}' not found"

    async def use_tools_parallel_async(
        self, calls: list[tuple[str, dict[str, Any]]]
    ) -> list[str]:
        tasks = [self.use_tool_async(name, **kw) for name, kw in calls]
        return list(await asyncio.gather(*tasks))

    def run(self, task: str) -> str:
        thought = self.think(task)
        self.history.append({
            "task": task,
            "thought": thought,
            "action": None,
            "observation": None,
        })
        action_result = self.act(task)
        self.history.append({
            "task": task,
            "thought": thought,
            "action": action_result,
            "observation": "Task completed",
        })
        return action_result

    async def run_async(self, task: str) -> str:
        thought = await self.think_async(task)
        self.history.append({
            "task": task,
            "thought": thought,
            "action": None,
            "observation": None,
        })
        action_result = await self.act_async(task)
        self.history.append({
            "task": task,
            "thought": thought,
            "action": action_result,
            "observation": "Task completed",
        })
        return action_result

    def get_history(self) -> list[dict[str, str]]:
        return self.history

    def clear_history(self) -> None:
        self.history.clear()


class ReasoningAgent(Agent):
    """Agent with chain-of-thought reasoning capabilities."""

    def __init__(self, name: str, role: str, tools: list[Tool] | None = None):
        super().__init__(name, role, tools)

    def think(self, prompt: str) -> str:
        return f"[{self.name}] Reasoning about: {prompt}"


def create_react_agent(
    name: str,
    role: str,
    tools: list[Tool],
) -> Agent:
    return Agent(name=name, role=role, tools=tools)
