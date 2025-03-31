# Use the official uv image (choose version as needed)
FROM ghcr.io/astral-sh/uv:python3.13-alpine

# Set working directory to match uv workspace structure
WORKDIR /workspace

# Copy root workspace files
COPY pyproject.toml ./

# Copy the backend project
COPY backend backend

# Move into backend workspace project
WORKDIR /workspace/backend

# Install backend dependencies (project in workspace context)
RUN uv pip install --system -e .

# Expose app port (FastAPI default)
EXPOSE 8000

# Default command for production (can be overridden in docker-compose)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]