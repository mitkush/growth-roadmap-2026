# kb-api starter (Step 6)

A small, working starting point for the Step 6 project: a FastAPI service with async SQLAlchemy 2.x, Alembic migrations, API-key auth, cursor pagination, tests against a real Postgres, Docker and GitHub Actions. It implements **one resource** (`documents`) end to end. You build the rest (sources, GitHub ingestion, full-text search) during Step 6, following [the Step 6 plan](../../steps/06-applied-python.md) and [its lessons](../../lessons/06-applied-python/00-start-here.md).

Tested with Python 3.13, uv 0.8, FastAPI 0.141, SQLAlchemy 2.1, Alembic 1.20 and PostgreSQL 16 with pgvector (the compose file uses the Postgres 17 image). The Docker image build itself was not run while preparing the starter (Docker was not available), so treat the first `docker compose up --build` as part of your Thursday task.

## Set up (about 10 minutes)

```bash
# 1. Copy the starter into a new repository
cp -r starters/kb-api ~/code/kb-api && cd ~/code/kb-api
git init   # .github/workflows/ci.yml is already in the right place for GitHub Actions

# 2. Start Postgres (with pgvector, and a kb_test database for the tests)
docker compose up -d db

# 3. Install dependencies and create your .env
uv sync
cp .env.example .env

# 4. Create the tables
uv run alembic upgrade head

# 5. Run the tests, then the server
uv run pytest --cov
uv run fastapi dev src/kb_api/main.py      # http://127.0.0.1:8000/docs
```

Try it:

```bash
curl -s -X POST localhost:8000/documents \
  -H 'X-API-Key: dev-key' -H 'content-type: application/json' \
  -d '{"title": "Kamal", "path": "docs/kamal.md", "body": "Deploy with kamal deploy."}'
curl -s 'localhost:8000/documents?limit=10'
```

## What is where

| File | Rails equivalent | What it does |
|---|---|---|
| `src/kb_api/main.py` | `config/application.rb` + `routes.rb` | Creates the app, mounts routers, `/healthz`, shutdown hook |
| `src/kb_api/config.py` | credentials + `ENV` | Settings from environment variables / `.env` (pydantic-settings) |
| `src/kb_api/db.py` | `database.yml` + connection pool | Async engine and one session per request |
| `src/kb_api/models.py` | `app/models/document.rb` | SQLAlchemy model (the table) |
| `src/kb_api/schemas.py` | strong params + serializers | Pydantic models for input and output |
| `src/kb_api/api/documents.py` | `DocumentsController` | The routes: list (cursor), show, create, update, destroy |
| `src/kb_api/api/deps.py` | `before_action`s | Session and API-key dependencies |
| `migrations/` | `db/migrate/` | Alembic migrations (async template) |
| `tests/conftest.py` | `rails_helper.rb` | Test DB, rolled-back transaction per test, HTTP client |
| `compose.yaml`, `Dockerfile` | Kamal / Docker setup | Local Postgres; production image |
| `.github/workflows/ci.yml` | CI config | ruff, mypy, migrations, pytest with coverage, Docker build |

## Everyday commands

| Task | Command |
|---|---|
| Run the server with reload | `uv run fastapi dev src/kb_api/main.py` |
| New migration after changing models | `uv run alembic revision --autogenerate -m "add sources"` then **read it**, then `uv run alembic upgrade head` |
| Roll back one migration | `uv run alembic downgrade -1` |
| Tests (one file / one test) | `uv run pytest tests/test_documents.py::test_cursor_pagination` |
| Lint, format, types | `uv run ruff check . && uv run ruff format . && uv run mypy src` |
| Everything in Docker | `docker compose up --build` |
