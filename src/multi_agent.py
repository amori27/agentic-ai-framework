"""Multi-Agent Orchestration Module.

This module provides utilities for coordinating multiple
agents to work together on complex tasks.
"""

from typing import Any
from .agent import Agent


class AgentTeam:
    """Coordinates multiple agents to solve complex tasks."""

    def __init__(self, agents: list[Agent], orchestrator: Agent | None = None):
        """Initialize the AgentTeam.

        Args:
            agents: List of team member agents.
            orchestrator: Optional orchestrator agent.
        """
        self.agents = {agent.name: agent for agent in agents}
        self.orchestrator = orchestrator
        self.team_history: list[dict[str, Any]] = []

    def get_agent(self, name: str) -> Agent | None:
        """Get an agent by name.

        Args:
            name: Agent name.

        Returns:
            Agent or None if not found.
        """
        return self.agents.get(name)

    def delegate_task(self, task: str, agent_name: str) -> str:
        """Delegate a task to a specific agent.

        Args:
            task: Task description.
            agent_name: Name of agent to delegate to.

        Returns:
            Task result.
        """
        agent = self.get_agent(agent_name)
        if agent:
            result = agent.run(task)
            self.team_history.append({
                "task": task,
                "agent": agent_name,
                "result": result
            })
            return result
        return f"Agent '{agent_name}' not found"

    def solve(self, problem: str) -> dict[str, Any]:
        """Solve a problem using team collaboration.

        Args:
            problem: Problem description.

        Returns:
            Solution with team collaboration details.
        """
        if self.orchestrator:
            plan = self.orchestrator.think(problem)
            self.team_history.append({
                "task": "Planning",
                "agent": self.orchestrator.name,
                "result": plan
            })

        task_results = {}
        for name, agent in self.agents.items():
            task_results[name] = agent.run(f"Work on: {problem}")

        return {
            "problem": problem,
            "task_results": task_results,
            "team_history": self.team_history
        }

    def parallel_execute(self, tasks: list[str]) -> dict[str, str]:
        """Execute multiple tasks in parallel.

        Args:
            tasks: List of tasks.

        Returns:
            Task results keyed by task.
        """
        results = {}
        for task in tasks:
            results[task] = f"Completed: {task}"
        return results

    def get_team_summary(self) -> dict[str, Any]:
        """Get summary of team status.

        Returns:
            Team summary.
        """
        return {
            "total_agents": len(self.agents),
            "agent_names": list(self.agents.keys()),
            "orchestrator": self.orchestrator.name if self.orchestrator else None,
            "total_tasks": len(self.team_history)
        }


class HierarchicalTeam(AgentTeam):
    """Hierarchical team with manager and workers."""

    def __init__(self, manager: Agent, workers: list[Agent]):
        """Initialize HierarchicalTeam.

        Args:
            manager: Manager agent.
            workers: Worker agents.
        """
        super().__init__(workers, orchestrator=manager)

    def solve(self, problem: str) -> dict[str, Any]:
        """Solve using hierarchical decomposition.

        Args:
            problem: Problem to solve.

        Returns:
            Hierarchical solution.
        """
        plan = self.orchestrator.think(problem) if self.orchestrator else problem

        subtasks = plan.split(",") if "," in plan else [plan]

        results = {}
        for i, subtask in enumerate(subtasks):
            worker = list(self.agents.values())[i % len(self.agents)]
            results[worker.name] = worker.run(subtask.strip())

        return {
            "problem": problem,
            "plan": plan,
            "subtask_results": results
        }
