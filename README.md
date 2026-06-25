# Agentic AI Framework
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


Multi-agent system framework for building autonomous AI agents that can collaborate, delegate tasks, and execute complex workflows with tool use and memory.

## Description

A comprehensive framework for building agentic AI systems with multi-agent orchestration, task decomposition, tool use, and persistent memory. Supports various agent architectures including react, plan-execute, and hierarchical agents.

## Skills & Technologies

- Python 3.9+
- LangChain
- OpenAI API
- Tool Use & Function Calling
- Multi-Agent Orchestration
- Task Decomposition
- Memory Management
- Autonomous Workflows

## Installation

```bash
git clone https://github.com/amori27/agentic-ai-framework.git
cd agentic-ai-framework
pip install -r requirements.txt
```

## Usage

### Create an Agent

```python
from src.agent import Agent
from src.tool import Tool

agent = Agent(name="ResearchAgent", role="researcher")
agent.add_tool(search_tool)
result = agent.run("Research the latest AI trends")
```

### Multi-Agent Collaboration

```python
from src.multi_agent import AgentTeam

team = AgentTeam(agents=[researcher, coder, reviewer])
output = team.solve("Build a web scraper")
```

## Project Structure

```
agentic-ai-framework/
├── src/
│   ├── agent.py          # Base agent class
│   ├── tool.py            # Tool definition
│   ├── multi_agent.py     # Multi-agent orchestration
│   ├── memory.py          # Memory management
│   └── executor.py        # Task executor
├── requirements.txt
└── README.md
```

## References

- [LangChain Documentation](https://docs.langchain.com/)
- [AutoGPT Architecture](https://github.com/Significant-Gravitas/AutoGPT)
- [Agent Design Patterns](https://arxiv.org/abs/2308.03688)

## License

MIT License
