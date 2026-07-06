# Agentic AI Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-red.svg)](https://github.com/astral-sh/ruff)
[![CI](https://github.com/amori27/agentic-ai-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/amori27/agentic-ai-framework/actions/workflows/ci.yml)

A lightweight Python framework for building autonomous AI agents with tool use, planning, and multi-agent coordination. Designed for clarity and easy extension — no vendor lock-in, no heavy dependencies.

---

## Features

- **`Agent`** — base class with role-based prompting, tool use, and conversation memory.
- **`Tool` + `ToolRegistry`** — register any Python callable as a typed tool the agent can invoke.
- **`AgentTeam`** — coordinate multiple agents, with an optional orchestrator that delegates tasks.
- **Pluggable LLM backend** — drop in any function that takes a prompt and returns a string.
- **Stateless design** — no global state, easy to test, easy to embed in a FastAPI service.

---

## Quick Start

```bash
pip install -r requirements.txt
```

```python
from src.agent import Agent
from src.tool import Tool

# 1. Define a tool the agent can use
def get_weather(city: str) -> str:
    return f"It's 22°C and sunny in {city}."

weather_tool = Tool(
    name="get_weather",
    description="Returns the current weather for a city.",
    function=get_weather,
)

# 2. Create an agent
agent = Agent(
    name="Researcher",
    role="helpful research assistant with access to weather data",
    tools=[weather_tool],
)

# 3. Run it
print(agent.run("What's the weather like in Tokyo?"))
```

---

## Multi-Agent Teams

```python
from src.agent import Agent
from src.multi_agent import AgentTeam
from src.tool import Tool

def search(query: str) -> str:
    return f"Results for '{query}': ..."

def summarize(text: str) -> str:
    return f"Summary: {text[:80]}..."

researcher = Agent("Researcher", "web researcher",
                   tools=[Tool("search", "Search the web", search)])
writer = Agent("Writer", "technical writer",
               tools=[Tool("summarize", "Summarize text", summarize)])

team = AgentTeam(agents=[researcher, writer], orchestrator=researcher)

# Delegate to a specific agent
result = team.delegate_task(
    "Find the latest on retrieval-augmented generation and summarize it",
    agent_name="Researcher",
)
print(result)
```

---

## Project Structure

```
agentic-ai-framework/
├── src/
│   ├── agent.py          # Base Agent class
│   ├── tool.py           # Tool definition + registry
│   └── multi_agent.py    # AgentTeam coordinator
├── tests/
│   └── test_example.py   # Placeholder tests
├── docs/
│   └── index.md          # Documentation index
├── .github/
│   ├── workflows/
│   │   └── ci.yml        # GitHub Actions CI
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
├── .env.example
├── CONTRIBUTING.md
├── CHANGELOG.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── requirements.txt
├── LICENSE               # MIT
└── README.md
```

---

## Extending

- **Custom LLM backend** — pass any `Callable[[str], str]` as the agent's `think()` implementation.
- **Custom tools** — wrap any Python function (including async) with `Tool(...)`.
- **Persistent memory** — subclass `Agent` and override `history` storage (e.g. Redis, SQLite).

---

## License

MIT — see [LICENSE](LICENSE).
