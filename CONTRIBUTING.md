# Contributing to agentic-ai-framework

We love contributions! Here's how you can help.

## Getting Started

1. Fork the repository.
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/agentic-ai-framework.git
   ```
3. Create a feature branch:
   ```bash
   git checkout -b feature/my-feature
   ```

## Development Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Code Standards

- Follow PEP 8 style guidelines.
- Type hints are required for all function signatures.
- Run Ruff before committing:
  ```bash
  pip install ruff
  ruff check .
  ```

## Testing

```bash
pip install pytest
pytest tests/
```

## Pull Request Process

1. Update `CHANGELOG.md` with your changes.
2. Ensure all tests pass.
3. Open a PR against the `main` branch.
4. A maintainer will review your PR.

## Reporting Issues

Use the [issue templates](.github/ISSUE_TEMPLATE/) to report bugs or request features.
