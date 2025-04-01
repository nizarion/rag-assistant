# RAG Assistant

A robust RAG-based virtual assistant powered by FastAPI, Azure OpenAI, and Qdrant, designed for efficient document processing and intelligent responses.

## Overview

RAG Assistant combines modern technologies to provide an intelligent document processing and question-answering system. It leverages Retrieval-Augmented Generation (RAG) to deliver accurate, context-aware responses based on your documents.

## Key Features

- Real-time document processing and indexing
- Intelligent question answering using RAG
- Scalable vector storage with Qdrant
- Modern web interface using Chainlit
- RESTful API powered by FastAPI

## Architecture

- **Backend**: FastAPI service handling core logic
- **Frontend**: Chainlit-based interactive UI
- **Vector Store**: Qdrant for efficient embedding storage
- **LLM Integration**: Azure OpenAI for text generation

## Development Tools

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

## Local Development

### Prerequisites

- Python 3.10+
- Docker and Docker Compose
- Azure OpenAI API access

### Environment Setup

Create a `.env` file in the project root:

```env
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
```

### Installation

```bash
uv pip install --dependency-group=dev -e .
```

## Services

Services are available at:
- Backend API: http://localhost:8000 (API docs at /docs)
- Frontend UI: http://localhost:8001
- Qdrant Dashboard: http://localhost:6333

## Running the Application

```bash
docker compose up -d     # Start all services
```

## Contributing

We welcome contributions! Please ensure your code:
- Passes all checks (`uv run poe all`)
- Includes appropriate tests
- Follows our code style guidelines

## License

MIT License - See LICENSE file for details

## Support

For issues and feature requests, please use the GitHub issue tracker.