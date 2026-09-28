# CHANGES: how the original 8 steps were refined

<!-- nav:top -->
[Course home](README.md) · [Glossary](GLOSSARY.md)
<!-- nav:end -->

This file records what changed from the first draft of the goal and why. The overall shape is unchanged: **Rails depth, then contribution, then Python, then AI, with the AI tool as the capstone**. The end date is still **15 Dec 2026**.

## Summary

| # | Final step title (paste into the goal tracker) | Weight | Due | What changed |
|---|---|---|---|---|
| 1 | Advanced Ruby: Concurrency, YJIT & Profiling | 10% | Sun 4 Oct 2026 | Re-scoped: Ractors reduced; Puma tuning, Vernier and jemalloc added |
| 2 | Rails at Scale: PostgreSQL, Solid Queue & Kamal | 10% | Sun 11 Oct 2026 | Re-scoped: sharding moved to stretch; safe migrations, indexing and N+1 control added |
| 3 | Rails Architecture: Modular Monolith & Observability | 10% | Sun 18 Oct 2026 | Added ADRs, outbox pattern, Rails 8.1 structured events; microservice extraction removed |
| 4 | Open-Source Contribution to the Ruby Ecosystem | 10% | Sun 25 Oct 2026 | Added issue scouting in weeks 1-3 and a clear fallback; "learning content" moved to blog posts |
| 5 | Python Fundamentals for Rubyists | 15% | Sun 8 Nov 2026 | Added uv, ruff and type checking; 5 practice problems specified |
| 6 | Applied Python: FastAPI Service with Tests & CI | 15% | Sun 22 Nov 2026 | Re-scoped: one project across 2 weeks; `httpx` added; pandas cut to one session |
| 7 | Agentic AI Engineering: Tools, MCP, RAG & Evals | 15% | Sun 29 Nov 2026 | Re-scoped for 1 week: RAG narrowed, evals and cost/safety made central |
| 8 | AI Tool MVP with Evals, Published on GitHub | 15% | Tue 15 Dec 2026 | 3 options given with one recommended; the eval suite is required |

**Weights:** 10 + 10 + 10 + 10 + 15 + 15 + 15 + 15 = **100%**. No weights or due dates were changed.

> **Note on weights (considered, not changed):** Step 7 is worth 15% but has only 1 week, while Step 8 has about 2 weeks. Moving 5% from Step 7 to Step 8 would match effort to weight better. I did **not** make this change because your manager has already approved the weights, and the imbalance is small. Instead, Step 7 is tightly scoped, and Step 6 prepares the database (Postgres with pgvector) so that Step 7 starts quickly.

---

## Step 1: Advanced Ruby

**Final title:** Advanced Ruby: Concurrency, YJIT & Profiling (10%, due 4 Oct)

| Change | Item | Why |
|---|---|---|
| Added | **Puma threads/workers tuning** and DB connection pool sizing | This is where the GVL affects a Rails app in practice. Rails 7.2+ sets 3 Puma threads by default, and most real latency wins come from this tuning. |
| Added | **Vernier** profiler (with the Firefox Profiler UI) | Vernier is the modern sampling profiler for Ruby 3.2.1+. It shows GVL waits and GC pauses on one timeline, which stackprof does not. |
| Added | **jemalloc / `MALLOC_ARENA_MAX`** | Memory growth in Puma and Sidekiq/Solid Queue processes is often caused by malloc fragmentation, not a Ruby leak. This is a common, measurable fix. |
| Added | **Load testing method** (`oha` or `wrk`, warm-up, p50/p95/p99) | "Before/after" numbers are useless without a repeatable benchmark method. |
| Added | Fiber scheduler with the `async` gem | This is the practical form of Fibers today (for example, concurrent HTTP calls). Raw `Fiber.new` alone has little real-world value. |
| Re-scoped | **Ractors**: from a main topic to a "can explain + one small demo" topic | Ractors are still experimental. Most gems, including Rails, are not Ractor-safe. It is worth understanding but not worth a full day. |
| Re-scoped | **GC tuning**: focus on `GC.stat`, heap slot env vars and the `autotuner` gem | Manual GC tuning without data is guesswork. The `autotuner` gem gives data-driven suggestions from a real app. |
| Removed | Hand-written C extensions and deep MRI internals | Low value for the time available. |
| Stretch | ZJIT (the new experimental JIT in Ruby 4.0) and modular GC | Too new to rely on in production. Good for curiosity. |

**Version note:** The plan targets **Ruby 3.4** (current stable 3.x) and notes where **Ruby 4.0** (released December 2025) changes things. Use whatever your work app runs.

## Step 2: Rails at scale

**Final title:** Rails at Scale: PostgreSQL, Solid Queue & Kamal (10%, due 11 Oct)

| Change | Item | Why |
|---|---|---|
| Added | **Index design** (composite, partial, covering `INCLUDE`, GIN) and `pg_stat_statements` | EXPLAIN ANALYZE is only useful when you know which queries to look at and how to fix them. |
| Added | **Safe, zero-downtime migrations** (`lock_timeout`, `CREATE INDEX CONCURRENTLY`, `strong_migrations`) | This is the most common real production incident linked to locking. It fits the locking topic directly. |
| Added | **N+1 control** (`strict_loading`, `includes` vs `preload` vs `eager_load`) and `load_async` | These are high-value, daily Rails performance skills. |
| Added | **Connection pooling / PgBouncer** caveats | Multi-DB and Solid Queue both increase connection count. This is a real scaling limit. |
| Added | Mission Control – Jobs dashboard for Solid Queue | You need visibility into queues, not just a working job runner. |
| Re-scoped | **Sharding**: moved to stretch goals | Horizontal sharding is rare below very large scale. Multi-DB with read replicas is the common need. |
| Re-scoped | **Partitioning**: one focused lab task (range partitioning of an events table) | This is useful for large append-only tables but does not need more than a few hours. |
| Re-scoped | **Kamal**: one deployment of the sample app to a cheap VPS (or local VM), not a full production setup | One real deploy teaches the model (kamal-proxy, accessories, secrets). Full production hardening is out of scope. |
| Re-scoped | **Solid Cache / Solid Cable**: understand the design and config; Solid Queue gets the hands-on depth | Solid Queue affects most apps (background jobs). Cache and Cable are simpler to adopt. |

## Step 3: Architecture and system design

**Final title:** Rails Architecture: Modular Monolith & Observability (10%, due 18 Oct)

| Change | Item | Why |
|---|---|---|
| Added | **Architecture Decision Records (ADRs)** and a one-page design doc | Senior engineers are judged on how clearly they communicate design. This is also good proof of completion. |
| Added | **Transactional outbox** and idempotent consumers | "Event-driven" in a Rails monolith usually fails at the edges (lost or duplicated events). The outbox pattern fixes this. |
| Added | **Rails 8.1 structured event reporting** (`Rails.event`) | This is new in Rails 8.1 and links events and observability directly. |
| Added | API design details: cursor pagination, idempotency keys, RFC 9457 problem details, Rails `rate_limit` | These are practical API topics, not abstract theory. |
| Added | Correlating logs and traces (trace IDs in structured logs) | Traces without log correlation are hard to use during incidents. |
| Re-scoped | **Packwerk**: used on one or two packs of the sample app, plus a clear view of its trade-offs | Packwerk is useful, but full modularisation of a large app is a multi-month effort. The skill is identifying boundaries. |
| Re-scoped | DDD: strategic design only (bounded contexts, context map, public APIs of a pack) | Tactical DDD patterns rarely fit Active Record apps well. |
| Removed | Extracting microservices | Out of scope for a modular-monolith step and not realistic in one week. |
| Removed | Event sourcing as a main topic (moved to stretch with Rails Event Store) | Powerful but niche. The outbox pattern gives most of the value. |

## Step 4: Open-source contribution

**Final title:** Open-Source Contribution to the Ruby Ecosystem (10%, due 25 Oct)

| Change | Item | Why |
|---|---|---|
| Added | **Issue scouting during weeks 1-3** (20-30 minutes each Sunday) | Finding a good issue is the slowest part. Starting early makes a PR in week 4 realistic. |
| Added | A shortlist of 8 projects, two of which (Solid Queue, Kamal) you will have used in Step 2 | Contributing to a tool you just studied is much faster. |
| Added | **A clear "done" definition:** PR opened and reviewed by 25 Oct; merge tracked until 15 Dec | Merge timing depends on maintainers, which you cannot control. |
| Added | A fallback: publish your own small gem or internal tool built from Step 1-2 work | This keeps the step within your control. |
| Removed | "Learning content" as a contribution type | It overlaps with the blog-post goal. Blog posts are tracked separately in the README. |

## Step 5: Python fundamentals

**Final title:** Python Fundamentals for Rubyists (15%, due 8 Nov)

| Change | Item | Why |
|---|---|---|
| Added | **uv** (instead of plain venv/pip) as the main tool; venv/pip explained for context | uv is now the standard fast tool for Python versions, venvs, dependencies and lockfiles. It is close to Bundler + rbenv. |
| Added | **ruff** (lint + format) and a type checker (**mypy**) | These are the modern equivalents of RuboCop and Sorbet/Steep. |
| Added | Generators, context managers, decorators, `dataclasses`, `Protocol`, `match` | These idioms are where Ruby developers most often write "Ruby in Python syntax". |
| Added | A Ruby-to-Python translation table | This speeds up learning by linking new concepts to what you already know. |
| Specified | The 5 practice problems (each linked to a Ruby-developer skill) | The draft only said "5 practice problems". |
| Specified | The Ruby utility to port (your own, or a `Gemfile.lock` analyser) | This makes the port a concrete task. |
| Re-scoped | asyncio basics moved to Step 6 | Async only makes sense with a real I/O workload (FastAPI and async SQLAlchemy). |

## Step 6: Applied Python

**Final title:** Applied Python: FastAPI Service with Tests & CI (15%, due 22 Nov)

| Change | Item | Why |
|---|---|---|
| Re-scoped | **One coherent project** (`kb-api`, an engineering knowledge-base API) built across 2 weeks | The draft read like separate tutorials. One project is closer to real work and is reused in Step 7. |
| Added | **`httpx`** (with a short `requests` intro) | `httpx` supports sync and async and is the standard client for testing FastAPI apps. |
| Added | Alembic migrations, `pydantic-settings`, FastAPI dependency injection and lifespan | Needed for a production-shaped service; the equivalents of Rails migrations and credentials. |
| Added | Postgres in Docker uses the **pgvector image** from day 1 | Step 7 can then add embeddings without new infrastructure. |
| Re-scoped | **pandas**: one session (a small ingest/report script), not a full topic | pandas is useful for evals and data work, but it is not the goal of this step. |
| Added | GitHub Actions CI with a Postgres service container, ruff, mypy and pytest | This was listed in the draft; it is now specified. |

## Step 7: Agentic AI engineering

**Final title:** Agentic AI Engineering: Tools, MCP, RAG & Evals (15%, due 29 Nov)

| Change | Item | Why |
|---|---|---|
| Re-scoped | **Built on the Step 6 project**: add tools, an MCP server and retrieval to `kb-api` | There is only 1 week. Reusing the project avoids setup time. |
| Added | **Cost and latency engineering**: token accounting, prompt caching, model tiering, Batch API for eval runs | Real AI features fail on cost and latency as often as on quality. |
| Added | **Safety**: prompt injection through retrieved documents and tool output, least-privilege tools, confirmation for write actions | Agents with tools have a real attack surface. |
| Added | Hybrid search (Postgres full-text + vector with reciprocal rank fusion) | Pure vector search often misses exact identifiers such as class names and error codes, which are common in engineering documents. |
| Re-scoped | **RAG**: retrieval quality and measurement, not framework tours | Retrieval quality (recall@k) matters more than which framework you use. |
| Re-scoped | **Evals** are the centre of the step: golden dataset, metrics, LLM-as-judge calibration, CI regression gate | Evals are what separate an AI demo from an AI tool, and they are required in Step 8. |
| Removed | Agent frameworks (LangChain, LlamaIndex and so on) as a topic | These hide the loop you need to understand. You can adopt one later if it helps. |
| Removed | Prompt-engineering basics | You already know them. |
| Removed | Fine-tuning | Not needed for these tools and not realistic in the time available. |

## Step 8: AI tool MVP

**Final title:** AI Tool MVP with Evals, Published on GitHub (15%, due 15 Dec)

| Change | Item | Why |
|---|---|---|
| Added | **3 concrete options** with architecture, eval plan and milestones; **Option A (Rails codebase MCP server) recommended** | It directly reuses Steps 1-3 and Step 7, it is useful to Rails teams, and deterministic ground truth makes its evals credible. |
| Added | Evals in CI and a public eval report are **required** for "done" | This matches the success criteria and makes the project credible. |
| Added | A README template for the public repository | Good packaging increases the chance of real users. |
| Added | Blog post #2 is written from the project (14-15 Dec) | This gives the second write-up a natural topic. |
| Re-scoped | Timeline: 30 Nov - 15 Dec (2 weeks + 2 days), with a feature freeze on 11 Dec | This leaves time to polish, publish and write. |

---

## Revision 2: from task plan to self-contained course

The roadmap was revised so that every task can be followed without searching elsewhere. Each step now has a folder of **lessons** in [`lessons/`](lessons/), and every day in each plan starts with **"Read first:"** links to the lessons it needs. The overall plan, weights and due dates are unchanged. The changes below were needed to make the plan accurate and achievable.

### Phase 1: Steps 7 and 8

| Change | Item | Why |
|---|---|---|
| Added | 15 lessons in `lessons/07-agentic-ai/` (API calls, tool calling, agent loop, MCP, embeddings, chunking, pgvector, hybrid search, RAG, evals, LLM-as-judge, cost and latency, security) with a full glossary | You are new to building AI applications; every term the plan uses is now explained with a runnable example. |
| Added | 8 lessons in `lessons/08-ai-tool-mvp/` (the three options in plain language, Rails introspection, static mode, building the server, A/B evals, packaging, eval report, GitHub bots for Options B/C) | Step 8 needs concepts that Step 7 does not cover (introspection, packaging, releasing, reporting). |
| Fixed | Model IDs: `claude-opus-5` → **`claude-opus-5-5`** as the default model; `claude-sonnet-5` and `claude-haiku-4-5` kept for comparison and judging | Use the current Opus model. The lessons also explain its API behaviour: thinking is always on, `temperature` and forced `tool_choice` are rejected, and responses must be passed back unchanged in tool loops. |
| Fixed | MCP Python SDK: `FastMCP` → **`MCPServer`** (`from mcp.server import MCPServer`), `ToolError` for model-visible errors | The current SDK is v2 (2.2 at the time of writing); v1 code (`mcp.server.fastmcp`) fails with an import error. |
| Changed | Embeddings: `sentence-transformers` → **`fastembed`** with `BAAI/bge-small-en-v1.5` (384 dimensions) | `fastembed` runs on CPU without PyTorch (a much smaller install); same free, local approach. |
| Re-scoped | Step 7: daily reading time (~30 min) is now inside the 10 hours; end-to-end tasks 20 → **15**; judge calibration 15 → **10-15** labels; `claude-haiku-4-5` comparison made optional; the **CI regression gate moved to Step 8** (Thu 10 Dec) | Reading the lessons takes time out of a 1-week step. Step 8 already builds CI evals, so the gate fits naturally there. |
| Changed | Step 8 Option A tools: `table_schema` folded into `describe_model`; tools are `describe_model`, `find_routes`, `model_graph`, `search_code` | Fewer, non-overlapping tools are easier for the model to choose between (Step 7 lesson 02). |
| Added | Step 8 day-by-day plan links each day to its lesson; the RAG workflow and the agent are both compared in the Step 7 report | Required by the revision; comparing workflow and agent is the practical point of Step 7 lesson 03. |

**How the lesson code was checked:** all Python examples were run with the current library versions (anthropic 1.8, mcp 2.2, SQLAlchemy 2.1, pgvector 0.5). SQL was run on PostgreSQL 16 with pgvector, and Ruby on Ruby 3.3 with Rails 8.1. The one exception is live Claude API calls: no API key was available, so those examples were run against a local stand-in for the API that checks the request format. Their sample outputs are labelled "example output". All Mermaid diagrams were rendered to check their syntax.

### Phase 2: Steps 1-6, README and glossary

| Change | Item | Why |
|---|---|---|
| Added | 12 lessons in `lessons/05-python-fundamentals/` (tooling, values and truthiness, collections, functions and closures, modules, pytest, errors and files, classes and dataclasses, iterators and generators, type hints, decorators and context managers, pattern matching and enums) | Python is new to you; each lesson puts the Ruby you know next to the Python equivalent and spends its time on the differences that cause bugs. Outputs come from real runs on Python 3.13. |
| Added | 12 lessons in `lessons/06-applied-python/` (HTTP clients, asyncio, pandas, FastAPI, Pydantic and settings, async SQLAlchemy, Alembic, dependency injection, full-text search and cursor pagination, testing FastAPI, Docker, GitHub Actions) | Every tool Step 6 uses is taught through its Rails equivalent, with runnable examples. |
| Added | **`starters/kb-api/`**: a working FastAPI skeleton (Document CRUD with cursor pagination, API-key auth, settings, one Alembic migration, 7 passing tests at 93% coverage, Dockerfile, `compose.yaml`, CI workflow) | Lets Step 6 start from correct, tested foundations and spend the time on the harder parts (ingestion, search, tests). |
| Re-scoped | Step 6 day tasks now build **on the starter** (Tue: copy it; Wed-Fri: add `Source`, its migration and router; Mon 16 Nov: understand and break the test setup; Thu 19 Nov: build the Docker image) instead of scaffolding from scratch | Scaffolding was a day and a half of setup with many ways to go wrong; the time moves to understanding and to the features. Weights and dates unchanged. |
| Fixed | Secrets use Pydantic **`SecretStr`** (`api_key`, `github_token`) | During testing a real `GITHUB_TOKEN` from the environment was printed in a plain `repr()` of the settings; `SecretStr` masks it. |
| Fixed | SQLAlchemy models use a **naming convention** for constraints; Alembic uses the async template; coverage uses `concurrency = ["greenlet", "thread"]` | Without the naming convention, Alembic could not drop unnamed foreign keys on downgrade; without the coverage setting, lines after `await` were reported as not covered. |
| Added | 6 lessons in `lessons/01-advanced-ruby/` (GVL and thread safety, Fibers and Ractors, Puma sizing and benchmarking, YJIT, GC and memory, profiling with Vernier/stackprof/memory_profiler/benchmark-ips) | Explains the runtime concepts the plan used without explanation, with measured results (for example: 16 Puma threads made the I/O-bound endpoint 5× faster and did nothing for the CPU-bound one). |
| Added | **`starters/shop-lab/`**: models, fast SQL seeds (20k customers and products, 200k orders, 600k line items, 2M events), three deliberately slow endpoints (N+1, CPU-heavy report, slow upstream I/O), a slow upstream server, a load generator, and a production-like **`benchmark`** environment | Step 1 Monday was "build the app and seed it"; the kit makes that 15 minutes, and gives every learner the same measurable problems. The `benchmark` environment exists because inheriting from `production` failed locally (it needs the Solid Cache/Queue/Cable databases and SSL). |
| Changed | Step 1 YJIT task uses `YJIT=0` (read by the kit's `benchmark.rb`) instead of `RUBY_YJIT_ENABLE=1` to switch YJIT off | Rails turns YJIT on after boot when `config.yjit` is true, whatever the environment variable says; the lesson explains how to confirm the state. |
| Added | 6 lessons in `lessons/02-rails-at-scale/` (pg_stat_statements and EXPLAIN ANALYZE read line by line, indexes and N+1, locks and safe migrations, partitioning and replicas, Solid Queue internals, Kamal architecture) | All plans and outputs are real: a composite index took one query from 22.2 ms to 0.21 ms; a queued `ALTER TABLE` made a plain `SELECT` wait 4.1 s; killing a Solid Queue worker mid-job produced a `ProcessExitError` failed execution. |
| Clarified | Step 2 partitioning result: pruning made a one-month count 2.8× faster than a full scan, but a plain index on `occurred_at` was faster still | Partitioning's value is data lifecycle (dropping months, smaller indexes), not single-query speed; the lesson and lab now say so honestly. |
| Added | 5 lessons in `lessons/03-architecture/` (bounded contexts and Packwerk, events and the outbox, API design, OpenTelemetry, ADRs) | Each example was run: Packwerk dependency and privacy violations, `Rails.event` output, an outbox with an idempotent consumer, an idempotent `POST` safe under concurrent requests, and one trace from HTTP into a job. |
| Fixed | Step 3: OpenTelemetry configured in an initializer, with Active Job `propagation_style: :child` | OTel's `use_all` fails after boot; and the Active Job instrumentation's default (`:link`) puts jobs in a separate trace, which contradicted the lab's "one trace" criterion. |
| Found | Outbox consumer inside the publisher's transaction needs `transaction(requires_new: true)` | Without a savepoint, a duplicate delivery aborted the whole publisher transaction (`PG::InFailedSqlTransaction`). The lesson shows the bug and the fix. |
| Added | Short `lessons/04-open-source/` (glossary + one workflow lesson) with a worked example of running Solid Queue's own test suite | Step 4 is mostly practice; the one lesson covers fork setup, test suites, PR descriptions and review. The example records real setup errors (missing MySQL/Postgres client libraries) and 5 environment-related failures on an unmodified clone, to teach "record the baseline before changing code". |
| Added | "What you will learn this step" paragraph and **"Read first:"** links on every day of Steps 1-6 (and the Step 4 scouting Sundays) | Required by the revision; each day now names the lesson to read before the tasks. |
| Added | README **"How to use this roadmap"** section, a lessons/starters table, and **[GLOSSARY.md](GLOSSARY.md)** (every term from the per-step glossaries, A to Z, linked to its lesson; regenerate with `python3 scripts/build_glossary.py`) | Makes the repository usable as a self-contained course. |
| Clarified | Terms used only in stretch goals (UUIDv7, Rails Event Store) are explained where they appear | No term in the plans is left unexplained. |

**How Phase 2 was checked:** Ruby/Rails examples ran on Ruby 3.3.6, Rails 8.1.4, PostgreSQL 16 (with the full `shop-lab` seed), Solid Queue 1.7.0, strong_migrations 2.8.0, Packwerk 3.3.1 with packwerk-extensions 0.4.0, Kamal 2.12.0 (`kamal init` and the Rails 8.1 templates were read; no server deploy was possible, so the Kamal lesson has no deploy output) and the OpenTelemetry Ruby SDK 1.13. Python examples ran on Python 3.13 with the versions pinned in `starters/kb-api/uv.lock`; the kb-api tests pass (7 tests, 93% coverage). Docker was not available, so the `kb-api` Dockerfile was not built (Step 6 Thu 19 Nov says so). YJIT was not compiled into the test machine's Ruby, so the YJIT lesson's numbers are labelled illustrative. All 67 Mermaid diagrams were rendered, and all relative links were checked.

### Verification pass

Every lesson example was re-run, and the course was checked again against primary sources: the Claude docs, Ruby's NEWS files, the documentation sources of GitHub, uv and Rails, gem READMEs and package registries. Fixed:

| Change | Item | Why |
|---|---|---|
| Fixed | Step 6: the full-text `search_vector` column is now **declared in the `Document` model** (`Computed(...)` plus a GIN `Index`) and its migration is autogenerated, instead of written by hand | Lesson 09's query used `Document.search_vector`, which did not exist in the model. Worse, after a hand-written migration, `alembic check` and the next autogenerate proposed **dropping** the column. Tested: with the model declaration, autogenerate drafts the column correctly and `alembic check` reports no changes. Lesson 09 now shows the tested SQLAlchemy query. |
| Fixed | Step 2: Mission Control – Jobs on the API-only `shop-lab` needs **`propshaft`** | Without an asset pipeline the app failed to boot (`undefined method 'assets'`). Tested: with Propshaft, `/jobs` returns 401 without credentials and 200 with them, and retrying a failed job works. Lesson 05 now has the exact steps. |
| Fixed | Step 1 profiling: `naive` and `plucked` gave different `top_skus` order for tied SKUs, so "same results" was false on a fresh seed | Both now break ties the same way (`[-count, sku]`). The kit's `ReportsController` was changed to match. Real numbers re-measured: about **8×** faster and 75% fewer allocations (it said 12×). The lesson also now includes the missing comparison script and says where to save each file. |
| Fixed | Step 7: token size (about 2.5 characters or half a word on current Claude models, not 4 characters or ¾ of a word); context window (1M on Opus 5.5 and Sonnet 5, 200k on Haiku 4.5); cache-read prices for Sonnet 5 ($0.20) and Haiku 4.5 ($0.10); 1-hour cache writes (2×); 512-token cache minimum on Opus 5.5 | Checked against the models overview, pricing and "What's new in Claude Opus 5.5" pages. |
| Added | Step 7: Claude Haiku 4.5 may be retired from 15 Oct 2026, before Step 7; the lessons now say to check the deprecations page and skip the optional comparison if it is gone | Its retirement date is "not sooner than October 15, 2026". |
| Added | Step 7: sampling parameters are rejected by the API and not accepted by the Python SDK (`TypeError`); editing the system prompt or tools mid-conversation can make thinking blocks fail (400) | From the Opus 5.5 migration guide. |
| Fixed | Broken or moved links: Ruby's YJIT docs (`doc/jit/yjit.md`), Puma's default branch (`main`), five GitHub Actions docs pages that moved | Checked against the repositories and the GitHub Docs source; the new paths were confirmed. |
| Resolved | "(verify)" marks that could be checked: Ruby 4.0 Ractor API (`Ractor#value`, `Ractor::Port`) and ZJIT flags (`--zjit`), `--yjit-mem-size` default (128 MiB), the `gvltools` API, the `rails-mcp-server` gem, Rails 8.1 release notes, pgvector-python's `hybrid_search` example, Anthropic's "Writing effective tools for AI agents" | Confirmed from Ruby's NEWS files and docs, RubyGems, the Rails guides source and the web. The remaining "(verify)" marks are things that change over time (for example book chapters and the OWASP list version). |
| Fixed | Removed the claim that "`bundle exec packwerk` was not found with Bundler 4" | Re-tested on a fresh app with Bundler 4.0.9: it works. The `bin/packwerk` binstub is kept because Packwerk's own messages use it. |
| Changed | kb-api Dockerfile uses `ghcr.io/astral-sh/uv:0.12` (was 0.8); workflows use `actions/checkout@v7` and `astral-sh/setup-uv@v7` | These match the versions current at the time of writing. The image tags and action tags were confirmed to exist, and the Dockerfile's `uv sync` steps were run against the lockfile. |
| Fixed | Small code issues in lesson snippets: a missing `import os`, and unused imports that would fail the course's own ruff checks | Found by linting every complete Python block. |
| Clarified | Step 1: `ruby -retc` replaced by a plain `require "etc"`; Ractor performance claim softened; README states that the daily hours include lesson reading | Easier to follow, and no claim the course could not verify. |

**What was re-run:** a fresh `shop-lab` built from the kit README (full seed; all three endpoints; the load test, which gave 30.4 req/s against the 29.4 in the kit's README); the Step 1 scripts; the kb-api starter's full CI sequence on a clean copy (ruff, mypy, Alembic, 7 tests, 93% coverage); every Step 5 and 6 lesson example, with output compared to the lesson text; Alembic autogenerate, upgrade and downgrade; and every Python block in Steps 7-8, linted against the anthropic 1.8 and mcp 2.2 SDKs (every SDK attribute the lessons use exists).

### Routing check

Checked every link and reference in the course:
- All 889 relative links and heading anchors resolve (the checker skipped code blocks; the two hits inside inline code are not rendered as links).
- Every numbered link label matches its target lesson.
- Every link to another step's lesson says which step it is.
- Every "Read first" hint names a section, part or quoted heading that exists.
- Every lesson is listed on its start page and linked from its step plan on the days the start page names.
- The README links every step, lesson folder, starter, the glossary and the templates, and each start page links back to its step plan.
- Each glossary term's linked lesson explains it.

Fixed:
- The Step 8 start page's list of reused lessons now says "Step 7 lesson …". Inside Step 8, a bare "lesson 02" means Step 8's own lesson.
- The Step 8 plan's first day now links lesson 07 for Options B and C.
- Step 2's `pluck` note now points to Step 1 lesson 06 with the re-measured numbers.
- "Interpreter", "PyPI" and the `help wanted` label are now explained in the lessons their glossary entries link to.

<!-- nav:bottom -->

---

[← Course home](README.md)
<!-- nav:end -->

### Navigation on every page

| Change | Item | Why |
|---|---|---|
| Added | A navigation bar at the top and bottom of every step plan, lesson, start page, starter README, template, `CHANGES.md` and `GLOSSARY.md`. Lessons show course home › step plan › step lessons at the top, and previous/next lesson at the bottom (the last lesson links back to the step plan). Start pages link to the previous and next step's lessons. Step plans link to the previous and next step. The README has a "Jump to" line. | So you can follow the course page to page without going back to the README. |
| Added | `scripts/build_nav.py` generates the bars between `<!-- nav:top -->` / `<!-- nav:bottom -->` markers; re-running it only replaces those regions (tested: only additions, and a second run changes nothing). `scripts/build_glossary.py` runs it after rebuilding the glossary. | Keeps the links correct if lessons are added or renamed. |
| Clarified | Weekly update template: "copy everything between the two horizontal lines" | The tips (and now the navigation links) are also below the first line. |

<!-- nav:bottom -->

---

[← Course home](README.md)
<!-- nav:end -->
