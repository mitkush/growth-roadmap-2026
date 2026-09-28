# Multi-stage build: install dependencies with uv in a builder image, copy only the result.
FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0
WORKDIR /app
# 1. Dependencies first (cached until pyproject.toml or uv.lock change).
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev
# 2. Then the application code.
COPY . .
RUN uv sync --locked --no-dev --no-editable

FROM python:3.13-slim
RUN useradd --create-home app
WORKDIR /app
COPY --from=builder --chown=app:app /app /app
ENV PATH="/app/.venv/bin:$PATH"
USER app
EXPOSE 8000
# Apply migrations, then start the server (like `bin/rails db:migrate && bin/rails server`).
CMD ["sh", "-c", "alembic upgrade head && uvicorn kb_api.main:app --host 0.0.0.0 --port 8000"]
