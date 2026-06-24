"""Agent Module.

This module provides the base Agent class with tool use,
reasoning, and action capabilities.
"""

from typing import Any, Callable
from dataclasses import dataclass


@dataclass
class Tool:
    """Represents a tool that an agent can use."""
    name: str
    description: str
    function: Callable[..., str]


class Agent:
    """Base agent class with reasoning and tool use."""

    def __init__(
        self,
        name: str,
        role: str,
        tools: list[Tool] | None = None,
        memory_enabled: bool = True
    ):
        """Initialize the Agent.

        Args:
            name: Agent name.
            role: Agent role/description.
            tools: List of tools available to agent.
            memory_enabled: Whether to enable memory.
        """
        self.name = name
        self.role = role
        self.tools = tools or []
        self.memory_enabled = memory_enabled
        self.history: list[dict[str, str]] = []

    def add_tool(self, tool: Tool) -> None:
        """Add a tool to the agent.

        Args:
            tool: Tool to add.
        """
        self.tools.append(tool)

    def think(self, prompt: str) -> str:
        """Process a prompt and generate a response.

        Args:
            prompt: Input prompt.

        Returns:
            Generated response.
        """
        system_prompt = f"You are {self.name}, a {self.role}."

        if self.tools:
            system_prompt += f"\n\nYou have access to these tools: "
            for tool in self.tools:
                system_prompt += f"\n- {tool.name}: {tool.description}"

        return f"[{self.name}] Processed: {prompt}"

    def act(self, action: str) -> str:
        """Execute an action.

        Args:
            action: Action description.

        Returns:
            Action result.
        """
        return f"[{self.name}] Action result: {action}"

    def use_tool(self, tool_name: str, **kwargs: Any) -> str:
        """Use a specific tool.

        Args:
            tool_name: Name of the tool to use.
            **kwargs: Arguments for the tool.

        Returns:
            Tool execution result.
        """
        for tool in self.tools:
            if tool.name == tool_name:
                return tool.function(**kwargs)

        return f"Tool '{tool_name}' not found"

    def run(self, task: str) -> str:
        """Run a task through think-act-observe loop.

        Args:
            task: Task description.

        Returns:
            Task result.
        """
        thought = self.think(task)

        self.history.append({
            "task": task,
            "thought": thought,
            "action": None,
            "observation": None
        })

        action_result = self.act(task)

        self.history.append({
            "task": task,
            "thought": thought,
            "action": action_result,
            "observation": "Task completed"
        })

        return action_result

    def get_history(self) -> list[dict[str, str]]:
        """Get agent's execution history.

        Returns:
            List of history entries.
        """
        return self.history

    def clear_history(self) -> None:
        """Clear agent's history."""
        self.history.clear()


class ReasoningAgent(Agent):
    """Agent with chain-of-thought reasoning capabilities."""

    def __init__(self, name: str, role: str, tools: list[Tool] | None = None):
        """Initialize the ReasoningAgent.

        Args:
            name: Agent name.
            role: Agent role.
            tools: Available tools.
        """
        super().__init__(name, role, tools)

    def think(self, prompt: str) -> str:
        """Generate reasoning steps.

        Args:
            prompt: Input prompt.

        Returns:
            Reasoning chain.
        """
        return f"[{self.name}] Reasoning about: {prompt}"


def create_react_agent(
    name: str,
    role: str,
    tools: list[Tool]
) -> Agent:
    """Create a ReAct-style agent.

    Args:
        name: Agent name.
        role: Agent role.
        tools: Available tools.

    Returns:
        Configured ReAct agent.
    """
    agent = Agent(name=name, role=role, tools=tools)

    return agent
