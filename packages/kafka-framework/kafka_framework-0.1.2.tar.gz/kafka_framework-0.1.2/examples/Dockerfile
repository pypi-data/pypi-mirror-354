FROM python:3.10-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
# Copy only the example app and its pyproject.toml
COPY . /app

# Install dependencies (including kafka-framework from PyPI or Git)
RUN uv sync

# Set working dir and run
# CMD ["ls"]
# CMD ["python", "app.py"]
# CMD ["uv", "run", "app.py"]