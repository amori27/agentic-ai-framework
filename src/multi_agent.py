"""Multi-Agent Orchestration Module.

This module provides utilities for coordinating multiple
agents to work together on complex tasks. Supports parallel
execution via asyncio.
"""

import asyncio
from typing import Any
from .agent import Agent


class AgentTeam:
    """Coordinates multiple agents to solve complex tasks."""

    def __init__(self, agents: list[Agent], orchestrator: Agent | None = None):
        self.agents = {agent.name: agent for agent in agents}
        self.orchestrator = orchestrator
        self.team_history: list[dict[str, Any]] = []

    def get_agent(self, name: str) -> Agent | None:
        return self.agents.get(name)

    def delegate_task(self, task: str, agent_name: str) -> str:
        agent = self.get_agent(agent_name)
        if agent:
            result = agent.run(task)
            self.team_history.append({
                "task": task,
                "agent": agent_name,
                "result": result,
            })
            return result
        return f"Agent '{agent_name}' not found"

    async def delegate_task_async(self, task: str, agent_name: str) -> str:
        agent = self.get_agent(agent_name)
        if agent:
            result = await agent.run_async(task)
            self.team_history.append({
                "task": task,
                "agent": agent_name,
                "result": result,
            })
            return result
        return f"Agent '{agent_name}' not found"

    def solve(self, problem: str) -> dict[str, Any]:
        if self.orchestrator:
            plan = self.orchestrator.think(problem)
            self.team_history.append({
                "task": "Planning",
                "agent": self.orchestrator.name,
                "result": plan,
            })

        task_results = {}
        for name, agent in self.agents.items():
            task_results[name] = agent.run(f"Work on: {problem}")

        return {
            "problem": problem,
            "task_results": task_results,
            "team_history": self.team_history,
        }

    async def solve_async(self, problem: str) -> dict[str, Any]:
        if self.orchestrator:
            plan = await self.orchestrator.think_async(problem)
            self.team_history.append({
                "task": "Planning",
                "agent": self.orchestrator.name,
                "result": plan,
            })

        async def _run_agent(name: str, agent: Agent) -> tuple[str, str]:
            return name, await agent.run_async(f"Work on: {problem}")

        results = await asyncio.gather(
            *[_run_agent(n, a) for n, a in self.agents.items()]
        )
        task_results = dict(results)

        return {
            "problem": problem,
            "task_results": task_results,
            "team_history": self.team_history,
        }

    def parallel_execute(self, tasks: list[str]) -> dict[str, str]:
        agent_list = list(self.agents.values())
        results = {}
        for i, task in enumerate(tasks):
            agent = agent_list[i % len(agent_list)]
            results[task] = agent.run(task)
        return results

    async def parallel_execute_async(self, tasks: list[str]) -> dict[str, str]:
        agent_list = list(self.agents.values())

        async def _run(task: str, agent: Agent) -> tuple[str, str]:
            return task, await agent.run_async(task)

        results = await asyncio.gather(
            *[_run(t, agent_list[i % len(agent_list)]) for i, t in enumerate(tasks)]
        )
        return dict(results)

    def get_team_summary(self) -> dict[str, Any]:
        return {
            "total_agents": len(self.agents),
            "agent_names": list(self.agents.keys()),
            "orchestrator": self.orchestrator.name if self.orchestrator else None,
            "total_tasks": len(self.team_history),
        }


class HierarchicalTeam(AgentTeam):
    """Hierarchical team with manager and workers."""

    def __init__(self, manager: Agent, workers: list[Agent]):
        super().__init__(workers, orchestrator=manager)

    def solve(self, problem: str) -> dict[str, Any]:
        plan = self.orchestrator.think(problem) if self.orchestrator else problem
        subtasks = plan.split(",") if "," in plan else [plan]

        results = {}
        for i, subtask in enumerate(subtasks):
            worker = list(self.agents.values())[i % len(self.agents)]
            results[worker.name] = worker.run(subtask.strip())

        return {"problem": problem, "plan": plan, "subtask_results": results}

    async def solve_async(self, problem: str) -> dict[str, Any]:
        plan = (
            await self.orchestrator.think_async(problem)
            if self.orchestrator
            else problem
        )
        subtasks = plan.split(",") if "," in plan else [plan]
        worker_list = list(self.agents.values())

        async def _run(subtask: str, worker: Agent) -> tuple[str, str]:
            return worker.name, await worker.run_async(subtask.strip())

        results = await asyncio.gather(
            *[_run(st, worker_list[i % len(worker_list)]) for i, st in enumerate(subtasks)]
        )

        return {"problem": problem, "plan": plan, "subtask_results": dict(results)}
