# RAG Assistant

A RAG-based virtual assistant using FastAPI, Azure OpenAI, and Qdrant.

## Development Tools

This project uses several development tools to maintain code quality:

### Ruff (Code Formatting and Linting)
Ruff is an extremely fast Python linter and formatter written in Rust.

- Format code: `uv run poe fmt`
- Lint code: `uv run poe lint`
- CI check formatting: `uv run poe ci-fmt`
- CI check linting: `uv run poe ci-lint`

Use Ruff when you want to:
- Automatically format Python code
- Find and fix common Python issues
- Ensure consistent code style

### BasedPyright (Type Checking)
BasedPyright is a fast type checker for Python.

- Run type checking: `uv run poe check`

Use BasedPyright when you want to:
- Verify type annotations
- Catch type-related errors before runtime
- Improve code reliability

### Pytest (Testing)
Pytest is a feature-rich testing framework for Python.

- Run tests: `uv run poe test`

Use Pytest when you want to:
- Write and run unit tests
- Generate test coverage reports
- Ensure code reliability

### Combined Commands
- Run all checks: `uv run poe all`
  This will run formatting, linting, type checking, and tests in sequence.

## Getting Started

1. Install development dependencies:
```bash
uv pip install --dependency-group=dev -e .
```

2. Run all checks:
```bash
uv run poe all
```

## Project Structure

- `backend/` - FastAPI backend service
- `tests/` - Test files
- `.env` - Environment variables
- `docker-compose.yml` - Docker services configuration