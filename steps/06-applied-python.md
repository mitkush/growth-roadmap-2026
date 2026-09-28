# Step 6: Applied Python: FastAPI Service with Tests & CI

<!-- nav:top -->
[Course home](../README.md) · Step 6 of 8 · [Step 6 lessons](../lessons/06-applied-python/00-start-here.md) · [Glossary](../GLOSSARY.md)
<!-- nav:end -->

| Weight | Dates | Hours |
|---|---|---|
| 15% | Mon 9 Nov - Sun 22 Nov 2026 (2 weeks) | ~20 h |

**Stack:** Python 3.13, uv, FastAPI, Pydantic v2 + pydantic-settings, SQLAlchemy 2.x (async, asyncpg; 2.1 at the time of writing), Alembic, httpx, pytest, Docker, GitHub Actions. PostgreSQL uses the `pgvector/pgvector` image so that Step 7 can add embeddings without new infrastructure.

## What you will learn this step

You will build a real Python web service, `kb-api`, the way you would build a Rails API: routes, validation, a database with migrations, authentication, tests against real Postgres, Docker and CI. Each tool is taught through its Rails equivalent: FastAPI is your router and controllers, Pydantic your strong parameters and serializers, SQLAlchemy your Active Record, Alembic your migrations, FastAPI dependencies your `before_action`s. You will also learn `asyncio`, Python's way of doing many slow network and database calls at once, which matters for every AI step that follows. You start from a small, tested [starter](../starters/kb-api/README.md) (one resource, end to end) and extend it with sources, GitHub ingestion and full-text search. The lessons are in [`lessons/06-applied-python/`](../lessons/06-applied-python/00-start-here.md).

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

**Starting point:** copy the [kb-api starter](../starters/kb-api/README.md) (Tue 10 Nov). It already has `Document` CRUD with cursor pagination, API-key auth, settings, an Alembic migration, 7 passing tests, a Dockerfile, `compose.yaml` and a CI workflow. You add everything else below.

**Core resources:** `Source` (a GitHub repo + path filter), `Document` (title, path, body, tags, source, content hash, updated_at).
**Endpoints:** `POST /sources`, `POST /sources/{id}/sync`, `GET /documents` (cursor pagination, filters), `GET/POST/PATCH/DELETE /documents/{id}`, `GET /search?q=` (Postgres full-text), `GET /healthz`.

### Week 1 (9 - 15 Nov): build the service

| Day | Topic | Concrete tasks | Hours |
|---|---|---|---|
| **Mon 9 Nov** | HTTP clients + asyncio | **Read first:** [00 Start here](../lessons/06-applied-python/00-start-here.md), [01 HTTP clients](../lessons/06-applied-python/01-http-clients-requests-and-httpx.md), [02 asyncio basics](../lessons/06-applied-python/02-asyncio-basics.md).<br>1. Run the lesson's `fetch_readmes.py` (requests vs httpx sync vs async). 2. Write `scripts/list_docs.py`: list the Markdown files of `rails/solid_queue` with the GitHub REST API using `httpx.Client` (token from `GITHUB_TOKEN`), then fetch 20 file contents with `httpx.AsyncClient` + `asyncio.gather`; compare timings. 3. Add a timeout and an `asyncio.Semaphore(5)` limit; handle a 403/429 rate limit. | 1.5 |
| **Tue 10 Nov** | pandas + the starter | **Read first:** [03 pandas basics](../lessons/06-applied-python/03-pandas-basics.md), [04 FastAPI basics](../lessons/06-applied-python/04-fastapi-basics.md).<br>1. `scripts/repo_report.py`: load Monday's file metadata into a DataFrame; files and total KB per folder; top 10 largest; write a CSV. 2. Copy the [starter](../starters/kb-api/README.md) into a new `kb-api` repository and follow its setup (compose, `uv sync`, `alembic upgrade head`, `pytest`, `fastapi dev`). 3. Open `/docs` and call every endpoint once. | 1.5 |
| **Wed 11 Nov** | Pydantic v2 + settings | **Read first:** [05 Pydantic and settings](../lessons/06-applied-python/05-pydantic-and-settings.md).<br>1. Read the starter's `schemas.py` and `config.py`. 2. Add `SourceCreate` (`repo` like `owner/name`, validated with a `field_validator`; optional `path_prefix`) and `SourceRead`. 3. Add a `content_hash` field to `DocumentRead`. 4. Confirm secrets are `SecretStr` and `.env` is ignored by Git. | 1.25 |
| **Thu 12 Nov** | Async SQLAlchemy + Alembic | **Read first:** [06 SQLAlchemy with asyncio](../lessons/06-applied-python/06-sqlalchemy-async.md), [07 Alembic migrations](../lessons/06-applied-python/07-alembic-migrations.md).<br>1. Add the `Source` model and `Document.source_id` (plus `content_hash`) as in lesson 07. 2. `alembic revision --autogenerate`, **review** it, `upgrade head`, then test `downgrade -1` and `upgrade head`. 3. Try a query with `selectinload(Source.documents)` in a scratch script. | 1.25 |
| **Fri 13 Nov** | Sources API + dependencies | **Read first:** [08 Dependency injection](../lessons/06-applied-python/08-dependency-injection.md).<br>1. `api/sources.py` router: `POST /sources` (201, 409 on duplicate), `GET /sources`, `GET /sources/{id}` (with its documents via `selectinload`). 2. Protect writes with the existing `require_api_key` dependency. 3. Add tests for the new endpoints (copy the patterns in `tests/test_documents.py`). 4. Send the weekly update. | 1 |
| **Sat 14 Nov** | Ingestion + search | **Read first:** [09 Full-text search and cursor pagination](../lessons/06-applied-python/09-full-text-search-and-cursor-pagination.md).<br>1. `services/github_client.py` (async httpx, token auth, bounded concurrency). 2. `POST /sources/{id}/sync` runs ingestion as a `BackgroundTasks` job: fetch Markdown, upsert by `(source_id, path)` using `content_hash` to skip unchanged files. 3. Declare the generated `search_vector` column and its GIN index in the model and autogenerate the migration (lesson 07, part 5), then run `alembic check`; add `GET /search?q=` with `websearch_to_tsquery`, `ts_rank` and `ts_headline` (lesson 09). | 2.5 |
| **Sun 15 Nov** | Errors, lifespan, logging | **Read first:** [04 FastAPI basics](../lessons/06-applied-python/04-fastapi-basics.md), "The app object and routers" (lifespan), and [08 Dependency injection](../lessons/06-applied-python/08-dependency-injection.md) (review).<br>1. Consistent error responses (problem-details style, like Step 3) with an exception handler. 2. Create and close the shared `httpx.AsyncClient` in the app's `lifespan`. 3. Structured JSON logs with a request ID middleware. 4. Run ruff and mypy on the week's code. | 1 |
| | | **Week 1 total** | **10** |

### Week 2 (16 - 22 Nov): tests, packaging, CI and polish

| Day | Topic | Concrete tasks | Hours |
|---|---|---|---|
| **Mon 16 Nov** | Test setup, understood | **Read first:** [10 Testing FastAPI](../lessons/06-applied-python/10-testing-fastapi.md).<br>1. Read the starter's `tests/conftest.py` line by line with the lesson: session-scoped schema, per-test rollback with savepoints, `dependency_overrides`, `ASGITransport`. 2. Break it on purpose (remove `join_transaction_mode`) and watch data leak between tests; restore it. 3. Add `tests/test_sources.py`. | 1.5 |
| **Tue 17 Nov** | Tests | **Read first:** [10 Testing FastAPI](../lessons/06-applied-python/10-testing-fastapi.md), Part B (respx).<br>1. Tests for search ranking and pagination edge cases. 2. Mock GitHub with `respx` for ingestion tests (success, 404, rate limit 403/429, unchanged hash skipped). 3. One end-to-end test: create a source, sync with GitHub mocked, search for a word from a mocked file. | 1.5 |
| **Wed 18 Nov** | Auth, coverage, API docs | **Read first:** [08 Dependency injection](../lessons/06-applied-python/08-dependency-injection.md), "Overriding in tests" (review).<br>1. Check every write endpoint returns 401 without the key (one parametrized test). 2. `uv run pytest --cov`; reach **≥ 85%** line coverage on `src/`. 3. Review the generated OpenAPI docs; add `examples=` to schemas. | 1.25 |
| **Thu 19 Nov** | Docker | **Read first:** [11 Docker for Python services](../lessons/06-applied-python/11-docker-for-python-services.md).<br>1. `docker compose up --build`; fix anything that fails (the starter's image was not built while it was prepared). 2. Check: non-root user, no uv in the final image, image size (aim for about 250 MB or less), dependency layer cached after a code change. 3. Call `/healthz` and `/search` in the container. | 1.25 |
| **Fri 20 Nov** | GitHub Actions CI | **Read first:** [12 GitHub Actions CI](../lessons/06-applied-python/12-github-actions-ci.md).<br>1. Push to GitHub; watch the starter's workflow run (Postgres service, uv, ruff, mypy, Alembic, pytest with coverage, Docker build). 2. Make the checks required for `main`. 3. Add the CI badge to the README. 4. Send the weekly update. | 1 |
| **Sat 21 Nov** | Performance + polish | **Read first:** [06 SQLAlchemy with asyncio](../lessons/06-applied-python/06-sqlalchemy-async.md), "Why lazy loading fails in async" (review).<br>1. Fix any lazy-load errors with `selectinload`. 2. Load test `GET /search` with `oha`; record p50/p95. 3. Ingest 3 real repos (for example your `shop-lab` docs, `rails/solid_queue`, `basecamp/kamal`); record ingest time. 4. Write the README (setup, architecture, decisions). | 2.5 |
| **Sun 22 Nov** | Consolidate + proof | **Read first:** [00 Start here](../lessons/06-applied-python/00-start-here.md), the Rails-to-Python map (review, then write your own notes).<br>1. Tag `v0.1.0`. 2. Self-check questions. 3. Write "Rails vs FastAPI: 10 notes" in `NOTES.md`. | 1 |
| | | **Week 2 total** | **10** |

### Suggested repository structure

Files marked ★ are already in the [starter](../starters/kb-api/README.md); the rest you add during the two weeks.

```
kb-api/
├── pyproject.toml ★            # deps, ruff, mypy, pytest config
├── uv.lock ★
├── .python-version ★
├── Dockerfile ★
├── compose.yaml ★              # app + pgvector/pgvector:pg17
├── alembic.ini ★
├── migrations/ ★             # Alembic (async template)
│   └── versions/
├── src/kb_api/
│   ├── main.py ★               # app factory, lifespan, routers
│   ├── config.py ★             # Settings (pydantic-settings)
│   ├── db.py ★                 # engine, async_sessionmaker, get_session
│   ├── models.py ★             # SQLAlchemy models
│   ├── schemas.py ★            # Pydantic models
│   ├── api/
│   │   ├── deps.py ★           # auth, session, pagination deps
│   │   ├── documents.py ★
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
│   ├── conftest.py ★           # db, client, respx fixtures
│   ├── test_documents.py ★
│   ├── test_search.py
│   └── test_ingest.py
└── .github/workflows/ci.yml ★
```

### CI workflow

The starter already contains the workflow: [`starters/kb-api/.github/workflows/ci.yml`](../starters/kb-api/.github/workflows/ci.yml) (Postgres service container, uv, ruff, mypy, Alembic, pytest with an 85% coverage gate, and a Docker build job). [Lesson 12](../lessons/06-applied-python/12-github-actions-ci.md) explains every line.

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

1. **Lessons for this step**: [`lessons/06-applied-python/`](../lessons/06-applied-python/00-start-here.md) and the [kb-api starter](../starters/kb-api/README.md) (start here).
2. **FastAPI docs**: Tutorial - User Guide, "Dependencies", "Bigger Applications", "Testing", "Lifespan Events": https://fastapi.tiangolo.com/
3. **Pydantic v2 docs** (models, validators, settings): https://docs.pydantic.dev/latest/
4. **SQLAlchemy 2.x**: "ORM Quick Start", "Unified Tutorial" and "Asynchronous I/O (asyncio)": https://docs.sqlalchemy.org/en/20/
5. **Alembic tutorial** (and the async template): https://alembic.sqlalchemy.org/en/latest/tutorial.html
6. **HTTPX docs** (async client, timeouts, transports for testing): https://www.python-httpx.org/
7. **uv: Using uv in Docker**: https://docs.astral.sh/uv/guides/integration/docker/ and **uv in GitHub Actions**: https://docs.astral.sh/uv/guides/integration/github/
8. **pandas: 10 minutes to pandas**: https://pandas.pydata.org/docs/user_guide/10min.html
9. **Harry Percival & Bob Gregory, *Architecture Patterns with Python*** (O'Reilly, 2020): ch. 1-2 (domain model, repository pattern). Free online at https://www.cosmicpython.com

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

<!-- nav:bottom -->

---

[← Step 5: Python Fundamentals for Rubyists](05-python-fundamentals.md) · [Step 6 lessons](../lessons/06-applied-python/00-start-here.md) · [Step 7: Agentic AI Engineering: Tools, MCP, RAG & Evals →](07-agentic-ai-engineering.md)
<!-- nav:end -->
