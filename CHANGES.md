# CHANGES: how the original 8 steps were refined

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
