# Step 6: Applied Python: FastAPI Service with Tests & CI

| Weight | Dates | Hours |
|---|---|---|
| 15% | Mon 9 Nov - Sun 22 Nov 2026 (2 weeks) | ~20 h |

**Stack:** Python 3.13, uv, FastAPI, Pydantic v2 + pydantic-settings, SQLAlchemy 2.0 (async, asyncpg), Alembic, httpx, pytest, Docker, GitHub Actions. PostgreSQL uses the `pgvector/pgvector` image so that Step 7 can add embeddings without new infrastructure.

## 1. Objective

By the end of these two weeks you will be able to:

- Build a production-shaped async REST API in Python with FastAPI, Pydantic v2 and async SQLAlchemy 2.0, and explain how each part maps to what you know from Rails.
- Manage schema changes with Alembic, configuration with pydantic-settings, and dependencies with FastAPI's dependency injection.
- Call external APIs efficiently with `httpx` (sync and async, bounded concurrency, timeouts, retries).
- Test the API end to end with pytest and httpx against a real Postgres, mocking only external HTTP.
- Package the service with Docker and run lint, types, migrations and tests in GitHub Actions.
- Use `requests` and `pandas` for quick scripts and reports.

## 2. Why it matters

- FastAPI + Pydantic + SQLAlchemy is the most common stack for Python services and for AI backends (Step 7-8).
- Async I/O matters for AI apps: most time is spent waiting on model APIs, databases and HTTP calls.
- Building one coherent project (not separate tutorials) shows the real problems: sessions, migrations, test isolation, CI. These are the skills your manager can see.
- The same service becomes the base for tools, an MCP server and retrieval in Step 7, so the time is reused.

## 3. Day-by-day plan

### The project: `kb-api`, an engineering knowledge-base API

`kb-api` stores engineering documents (ADRs, runbooks, READMEs, guides). It ingests Markdown files from GitHub repositories and offers CRUD and full-text search. In Step 7 you will add semantic search, tools and an MCP server on top.

**Core resources:** `Source` (a GitHub repo + path filter), `Document` (title, path, body, tags, source, content hash, updated_at).
**Endpoints:** `POST /sources`, `POST /sources/{id}/sync`, `GET /documents` (cursor pagination, filters), `GET/POST/PATCH/DELETE /documents/{id}`, `GET /search?q=` (Postgres full-text), `GET /healthz`.

### Week 1 (9 - 15 Nov): build the service

| Day | Topic | Concrete tasks | Hours |
|---|---|---|---|
| **Mon 9 Nov** | HTTP clients + asyncio | 1. Script: list Markdown files in `rails/solid_queue` using the GitHub REST API with **`requests`**. 2. Rewrite with **`httpx.Client`**, then with `httpx.AsyncClient` + `asyncio.gather` to fetch 20 file contents; compare timings. 3. Add a timeout and an `asyncio.Semaphore(5)` limit. | 1.5 |
| **Tue 10 Nov** | pandas session + scaffold | 1. Load the fetched file metadata into a pandas `DataFrame`; group by directory; write a CSV and print the top 10 largest files (`scripts/repo_report.py`). 2. `uv init --package kb-api`; `uv add "fastapi[standard]"`; hello-world route; run `uv run fastapi dev src/kb_api/main.py` and open `/docs`. | 1.5 |
| **Wed 11 Nov** | Pydantic v2 + settings | 1. Schemas: `DocumentCreate`, `DocumentUpdate` (all optional), `DocumentRead` (`model_config = ConfigDict(from_attributes=True)`). 2. Field validation (`Field(min_length=...)`, `field_validator`). 3. `Settings(BaseSettings)` reading `DATABASE_URL`, `GITHUB_TOKEN`, `API_KEY` from env/`.env`. | 1.25 |
| **Thu 12 Nov** | Async SQLAlchemy + Alembic | 1. `compose.yaml` with `pgvector/pgvector:pg17`. 2. `create_async_engine("postgresql+asyncpg://...")`, `async_sessionmaker`, models with `DeclarativeBase`, `Mapped[...]`, `mapped_column`. 3. `alembic init -t async migrations`; point it at your metadata; autogenerate and apply the first migration. | 1.25 |
| **Fri 13 Nov** | CRUD endpoints | 1. `get_session` dependency (`async with` session, one per request). 2. Routers for documents; a small repository module for queries. 3. Correct status codes (201, 204, 404, 422). 4. Send the weekly update. | 1 |
| **Sat 14 Nov** | Ingestion + search | 1. `services/github_client.py` (async httpx, token auth, bounded concurrency). 2. `POST /sources/{id}/sync` runs ingestion as a `BackgroundTasks` job: fetch Markdown, upsert by `(source_id, path)` using `content_hash` to skip unchanged files. 3. Add a generated `tsvector` column + GIN index (Alembic migration) and `GET /search?q=` with `websearch_to_tsquery` and `ts_rank`. 4. Cursor pagination on `GET /documents`. | 2.5 |
| **Sun 15 Nov** | Errors, lifespan, logging | 1. Consistent error responses (problem-details style, like Step 3). 2. `lifespan` to create/dispose the engine and the httpx client. 3. Structured JSON logs with a request ID middleware. 4. Review week 1 code with ruff and mypy. | 1 |
| | | **Week 1 total** | **10** |

### Week 2 (16 - 22 Nov): tests, packaging, CI and polish

| Day | Topic | Concrete tasks | Hours |
|---|---|---|---|
| **Mon 16 Nov** | Test setup | 1. pytest with `anyio` (or `pytest-asyncio`) for async tests. 2. `httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test")` fixture. 3. Test DB: run migrations once per session; wrap each test in a transaction that rolls back; inject with `app.dependency_overrides`. | 1.5 |
| **Tue 17 Nov** | Tests | 1. Tests for CRUD, validation errors, pagination and search ranking. 2. Mock GitHub with `respx` for ingestion tests (success, 404, rate limit 403/429, unchanged hash skipped). | 1.5 |
| **Wed 18 Nov** | Auth + coverage | 1. API-key auth as a dependency (`X-API-Key` header) on write endpoints. 2. `pytest-cov`; reach **≥ 85%** line coverage on `src/`. 3. Review the generated OpenAPI docs; add examples to schemas. | 1.25 |
| **Thu 19 Nov** | Docker | 1. Multi-stage `Dockerfile` using uv (copy `uv` binary from `ghcr.io/astral-sh/uv`, `uv sync --locked --no-dev`). 2. `compose.yaml` with app + db; run `alembic upgrade head` on start. 3. Image under ~250 MB; runs as a non-root user. | 1.25 |
| **Fri 20 Nov** | GitHub Actions CI | 1. Workflow (below): Postgres service, `astral-sh/setup-uv`, ruff, mypy, Alembic, pytest with coverage. 2. Add a Docker build job. 3. Send the weekly update. | 1 |
| **Sat 21 Nov** | Performance + polish | 1. Fix SQLAlchemy lazy-load issues (async sessions raise on lazy loads: use `selectinload`). 2. Load test `GET /search` with `oha`; record p50/p95. 3. Ingest 3 real repos (e.g. your `shop-lab` docs, `rails/solid_queue`, `basecamp/kamal`); record ingest time. 4. Write the README (setup, architecture, decisions). | 2.5 |
| **Sun 22 Nov** | Consolidate + proof | 1. Tag `v0.1.0`. 2. Self-check questions. 3. Write "Rails vs FastAPI: 10 notes" in `NOTES.md`. | 1 |
| | | **Week 2 total** | **10** |

### Suggested repository structure

```
kb-api/
├── pyproject.toml            # deps, ruff, mypy, pytest config
├── uv.lock
├── .python-version
├── Dockerfile
├── compose.yaml              # app + pgvector/pgvector:pg17
├── alembic.ini
├── migrations/               # Alembic (async template)
│   └── versions/
├── src/kb_api/
│   ├── main.py               # app factory, lifespan, routers
│   ├── config.py             # Settings (pydantic-settings)
│   ├── db.py                 # engine, async_sessionmaker, get_session
│   ├── models.py             # SQLAlchemy models
│   ├── schemas.py            # Pydantic models
│   ├── api/
│   │   ├── deps.py           # auth, session, pagination deps
│   │   ├── documents.py
│   │   ├── sources.py
│   │   ├── search.py
│   │   └── health.py
│   ├── services/
│   │   ├── github_client.py  # async httpx client
│   │   └── ingest.py
│   └── repositories/
│       └── documents.py
├── scripts/
│   └── repo_report.py        # pandas report
├── tests/
│   ├── conftest.py           # db, client, respx fixtures
│   ├── test_documents.py
│   ├── test_search.py
│   └── test_ingest.py
└── .github/workflows/ci.yml
```

### CI workflow (starting point)

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg17
        env: { POSTGRES_USER: kb, POSTGRES_PASSWORD: kb, POSTGRES_DB: kb_test }
        ports: ["5432:5432"]
        options: >-
          --health-cmd "pg_isready -U kb" --health-interval 5s
          --health-timeout 5s --health-retries 10
    env:
      DATABASE_URL: postgresql+asyncpg://kb:kb@localhost:5432/kb_test
    steps:
      - uses: actions/checkout@v5
      - uses: astral-sh/setup-uv@v6   # use the latest major version
      - run: uv sync --locked
      - run: uv run ruff check . && uv run ruff format --check .
      - run: uv run mypy src
      - run: uv run alembic upgrade head
      - run: uv run pytest --cov=kb_api --cov-fail-under=85
```

## 4. Topic checklist

**HTTP and data**
- [ ] `requests` basics: can make authenticated GET/POST calls with timeouts and handle errors.
- [ ] `httpx`: can use sync and async clients, reuse a client, set timeouts, and limit concurrency.
- [ ] asyncio: can explain the event loop, `await`, `gather`, and why a blocking call inside `async def` is harmful.
- [ ] pandas: can load records into a DataFrame, filter, `groupby`, aggregate and write CSV.

**FastAPI and Pydantic**
- [ ] Routing, path/query/body parameters, status codes and response models.
- [ ] Dependency injection (`Depends`) for sessions, auth and pagination; overriding dependencies in tests.
- [ ] Pydantic v2 models, validators, `from_attributes`, and separate create/update/read schemas.
- [ ] `lifespan` for startup/shutdown resources; `BackgroundTasks` and their limits.
- [ ] Settings with pydantic-settings; never hard-code secrets.

**Database**
- [ ] SQLAlchemy 2.0 typed models (`Mapped`, `mapped_column`), `select()` style queries, async sessions.
- [ ] Session lifecycle per request and transaction boundaries; can explain why lazy loading fails in async.
- [ ] Alembic: autogenerate, review, upgrade, downgrade; data migrations kept separate.
- [ ] Postgres full-text search with a generated `tsvector` column and GIN index.

**Quality and delivery**
- [ ] pytest async tests against a real DB with per-test rollback; `respx` for external HTTP.
- [ ] Docker multi-stage build with uv; non-root user; small image.
- [ ] GitHub Actions with a Postgres service container and required checks.
- [ ] Nice to have: structured logging with request IDs.

## 5. Hands-on lab: ship `kb-api` v0.1.0

**Acceptance criteria**
- [ ] `docker compose up` starts the app and DB and applies migrations; `/docs` works.
- [ ] Syncing a real GitHub repo ingests its Markdown files; a second sync skips unchanged files (shown in logs).
- [ ] `GET /search?q=solid queue recurring` returns relevant documents ranked by `ts_rank`.
- [ ] Cursor pagination returns stable results while new documents are inserted.
- [ ] Write endpoints return 401 without a valid API key.
- [ ] CI is green: ruff, mypy (no `Any` in `src/` public functions), Alembic upgrade, pytest with **≥ 85%** coverage.
- [ ] README includes setup, architecture diagram (Mermaid), design decisions and the `GET /search` p95 under load.
- [ ] `scripts/repo_report.py` produces a CSV report with pandas.

## 6. Deliverable / proof of completion

1. **Link to the `kb-api` repo** at tag `v0.1.0` with a green CI run.
2. **README** with architecture diagram and load-test numbers.
3. **`NOTES.md`**: "Rails vs FastAPI: 10 notes" (for example: `ActiveRecord` vs SQLAlchemy sessions, migrations, DI vs `before_action`).

## 7. Curated resources

1. **FastAPI docs**: Tutorial - User Guide, "Dependencies", "Bigger Applications", "Testing", "Lifespan Events": https://fastapi.tiangolo.com/
2. **Pydantic v2 docs** (models, validators, settings): https://docs.pydantic.dev/latest/
3. **SQLAlchemy 2.0**: "ORM Quick Start", "Unified Tutorial" and "Asynchronous I/O (asyncio)": https://docs.sqlalchemy.org/en/20/
4. **Alembic tutorial** (and the async template): https://alembic.sqlalchemy.org/en/latest/tutorial.html
5. **HTTPX docs** (async client, timeouts, transports for testing): https://www.python-httpx.org/
6. **uv: Using uv in Docker**: https://docs.astral.sh/uv/guides/integration/docker/ and **uv in GitHub Actions**: https://docs.astral.sh/uv/guides/integration/github/
7. **pandas: 10 minutes to pandas**: https://pandas.pydata.org/docs/user_guide/10min.html
8. **Harry Percival & Bob Gregory, *Architecture Patterns with Python*** (O'Reilly, 2020): ch. 1-2 (domain model, repository pattern). Free online at https://www.cosmicpython.com

## 8. Self-check questions

1. What happens to your API's throughput if one endpoint calls a synchronous library (like `requests`) inside `async def`? How do you fix it?
2. How is a FastAPI dependency like a Rails `before_action`, and how is it different?
3. Why do you need separate Pydantic schemas for create, update and read? What goes wrong with one shared model?
4. Where does a SQLAlchemy session start and end in your app, and what would happen if two requests shared one?
5. Why does lazy loading raise an error with async SQLAlchemy, and how do `selectinload` and `joinedload` differ?
6. How do your tests stay isolated from each other while still using a real Postgres?
7. Why is `BackgroundTasks` not a replacement for a real job queue? What would you use in production?
8. Alembic autogenerate produced a migration. What do you check before applying it?
9. How does your ingestion avoid hitting GitHub's rate limit, and what happens when it does?
10. What is in your Docker image that does not need to be there?

## 9. Common pitfalls

- **Blocking the event loop** with sync I/O or CPU-heavy work inside `async def`.
- **Creating a new `httpx.AsyncClient` per request** instead of reusing one (connection pooling lost).
- **Trusting Alembic autogenerate blindly** (it misses some changes, such as renames, and some constraint changes).
- **Using SQLite in tests** when production is Postgres; full-text search and types behave differently.
- **Mocking the database** instead of testing against it; mock only external HTTP.
- **Mixing Pydantic v1 examples** from old blog posts with v2 (`orm_mode` → `from_attributes`, `.dict()` → `.model_dump()`).
- **Forgetting timeouts** on outbound HTTP calls.

## 10. Stretch goals

- Replace `BackgroundTasks` with a real job queue (e.g. `arq` or Celery, verify current maintenance) and compare with Solid Queue.
- Add OpenTelemetry instrumentation for FastAPI and SQLAlchemy and send traces to the same `otel-lgtm` stack as Step 3.
- Deploy `kb-api` with Kamal (it deploys any Docker image, not only Rails apps).
- Add ETag/`If-None-Match` support to `GET /documents/{id}`.
