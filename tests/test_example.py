"""Tests for agentic-ai-framework."""

import asyncio
import pytest
from src.agent import Agent, ReasoningAgent, create_react_agent
from src.agent import Tool as AgentTool
from src.tool import Tool, ToolRegistry, get_default_tools, get_async_default_tools
from src.multi_agent import AgentTeam, HierarchicalTeam


def test_imports():
    assert Agent is not None
    assert Tool is not None


def test_agent_creation():
    agent = Agent(name="TestBot", role="tester")
    assert agent.name == "TestBot"
    assert agent.role == "tester"
    assert len(agent.tools) == 0


def test_agent_run():
    agent = Agent(name="TestBot", role="tester")
    result = agent.run("hello")
    assert result is not None
    assert "[TestBot]" in result


def test_use_tool_sync():
    def echo(text: str) -> str:
        return f"echo: {text}"

    tool = AgentTool(name="echo", description="Echo tool", function=echo)
    agent = Agent(name="Bot", role="helper", tools=[tool])
    result = agent.use_tool("echo", text="hello")
    assert result == "echo: hello"


def test_use_tool_not_found():
    agent = Agent(name="Bot", role="helper")
    result = agent.use_tool("nonexistent")
    assert "not found" in result


def test_tool_registry():
    registry = ToolRegistry()
    tool = Tool(name="test", description="test", function=lambda: "ok")
    registry.register(tool)
    assert "test" in registry.list_tools()
    assert registry.get("test") is tool
    assert registry.unregister("test") is True
    assert registry.get("test") is None


def test_get_default_tools():
    tools = get_default_tools()
    assert len(tools) == 3
    names = [t.name for t in tools]
    assert "web_search" in names
    assert "calculator" in names
    assert "file_reader" in names


def test_async_default_tools():
    tools = get_async_default_tools()
    assert len(tools) == 3


def test_agent_history():
    agent = Agent(name="Bot", role="helper")
    agent.run("task1")
    agent.run("task2")
    assert len(agent.history) == 4
    agent.clear_history()
    assert len(agent.history) == 0


def test_agent_team():
    a1 = Agent(name="A1", role="worker1")
    a2 = Agent(name="A2", role="worker2")
    team = AgentTeam(agents=[a1, a2])
    result = team.solve("test problem")
    assert "A1" in result["task_results"]
    assert "A2" in result["task_results"]


def test_hierarchical_team():
    manager = Agent(name="Manager", role="manager")
    worker1 = Agent(name="W1", role="worker")
    worker2 = Agent(name="W2", role="worker")
    team = HierarchicalTeam(manager=manager, workers=[worker1, worker2])
    result = team.solve("build something")
    assert "subtask_results" in result


# Async tests


@pytest.mark.asyncio
async def test_use_tool_async():
    async def async_echo(text: str) -> str:
        return f"async echo: {text}"

    tool = AgentTool(name="async_echo", description="Async echo", function=async_echo)
    agent = Agent(name="Bot", role="helper", tools=[tool])
    result = await agent.use_tool_async("async_echo", text="hello")
    assert result == "async echo: hello"


@pytest.mark.asyncio
async def test_use_tool_async_with_sync_tool():
    def sync_echo(text: str) -> str:
        return f"sync: {text}"

    tool = AgentTool(name="sync_echo", description="Sync echo", function=sync_echo)
    agent = Agent(name="Bot", role="helper", tools=[tool])
    result = await agent.use_tool_async("sync_echo", text="world")
    assert result == "sync: world"


@pytest.mark.asyncio
async def test_use_tools_parallel():
    call_count = 0

    async def slow_tool(query: str) -> str:
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.01)
        return f"result-{query}"

    tool = AgentTool(name="slow", description="slow", function=slow_tool)
    agent = Agent(name="Bot", role="helper", tools=[tool])

    calls = [("slow", {"query": "a"}), ("slow", {"query": "b"}), ("slow", {"query": "c"})]
    results = await agent.use_tools_parallel_async(calls)
    assert len(results) == 3
    assert call_count == 3


@pytest.mark.asyncio
async def test_agent_run_async():
    agent = Agent(name="Bot", role="helper")
    result = await agent.run_async("hello async")
    assert "[Bot]" in result
    assert len(agent.history) == 2


@pytest.mark.asyncio
async def test_agent_team_parallel():
    a1 = Agent(name="A1", role="w1")
    a2 = Agent(name="A2", role="w2")
    team = AgentTeam(agents=[a1, a2])
    result = await team.solve_async("async problem")
    assert "A1" in result["task_results"]
    assert "A2" in result["task_results"]


@pytest.mark.asyncio
async def test_parallel_execute_async():
    a1 = Agent(name="A1", role="w1")
    a2 = Agent(name="A2", role="w2")
    team = AgentTeam(agents=[a1, a2])
    tasks = ["task1", "task2"]
    results = await team.parallel_execute_async(tasks)
    assert len(results) == 2


@pytest.mark.asyncio
async def test_hierarchical_team_async():
    manager = Agent(name="Mgr", role="manager")
    w1 = Agent(name="W1", role="worker")
    team = HierarchicalTeam(manager=manager, workers=[w1])
    result = await team.solve_async("build async")
    assert "subtask_results" in result
