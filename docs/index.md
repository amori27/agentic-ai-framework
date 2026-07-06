# Agentic AI Framework Documentation

Welcome to the documentation for **agentic-ai-framework** — a lightweight Python framework for building autonomous AI agents with tool use, planning, and multi-agent coordination.

## Quick Links

- [GitHub Repository](https://github.com/amori27/agentic-ai-framework)
- [Getting Started](../README.md#quick-start)
- [Contributing](../CONTRIBUTING.md)

## Core Concepts

- **Agent** — base class with role-based prompting, tool use, and conversation memory.
- **Tool + ToolRegistry** — register any Python callable as a typed tool.
- **AgentTeam** — coordinate multiple agents with optional orchestrator.
- **Pluggable LLM backend** — drop in any function that takes a prompt and returns a string.
