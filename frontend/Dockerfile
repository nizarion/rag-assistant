# Use official uv image
FROM ghcr.io/astral-sh/uv:python3.13-bookworm

# Set working directory
WORKDIR /workspace

# Copy root workspace files
COPY pyproject.toml ./

# Copy the frontend project
COPY frontend frontend/

# Move into frontend workspace project
WORKDIR /workspace/frontend


# Install frontend dependencies in workspace context
RUN uv pip install --system -e .

# Expose Chainlit port
EXPOSE 8001

# Run Chainlit server
CMD ["uv", "run", "chainlit", "run", "app.py", "--port", "8001", "--host", "0.0.0.0"]
