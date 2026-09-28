# Glossary

Every term defined in the course, A to Z, with the step and the lesson that explains it.
Generated from the glossary in each `lessons/*/00-start-here.md` by `python3 scripts/build_glossary.py`;
edit those files, not this one. Some terms appear twice because two steps use them in different contexts.


## A

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **A/B eval (with vs without)** | Running the same tasks with and without your tool to measure its effect. | 08 AI tool MVP | [04](lessons/08-ai-tool-mvp/04-evaluating-your-tool.md) |
| **`ActiveSupport::Notifications`** | Rails' instrumentation pub/sub (timed blocks, used by Rails internals). | 03 Architecture | [02](lessons/03-architecture/02-events-and-outbox.md) |
| **ADR** | Architecture Decision Record: a short document of one decision, its context and consequences. | 03 Architecture | [05](lessons/03-architecture/05-adrs-and-design-docs.md) |
| **Agent** | A program where the model decides the next step in a loop (call a tool, read the result, decide again) until the task is done. | 07 Agentic AI | [03](lessons/07-agentic-ai/03-agent-loop.md) |
| **Agent loop** | The `while` loop that sends messages, runs requested tools and sends results back. | 07 Agentic AI | [03](lessons/07-agentic-ai/03-agent-loop.md) |
| **Alembic / revision / autogenerate** | SQLAlchemy's migration tool / one migration / generating it by comparing models with the database. | 06 Applied Python | [07](lessons/06-applied-python/07-alembic-migrations.md) |
| **Allocation / retained object** | An object created / an object still alive after the operation. | 01 Advanced Ruby | [05](lessons/01-advanced-ruby/05-gc-and-memory.md), [06](lessons/01-advanced-ruby/06-profiling.md) |
| **API versioning / deprecation** | Changing an API without breaking existing clients / announcing and removing old behaviour. | 03 Architecture | [03](lessons/03-architecture/03-api-design.md) |
| **`*args` / `**kwargs`** | Collect extra positional / keyword arguments (Ruby's `*args` / `**opts`). | 05 Python fundamentals | [04](lessons/05-python-fundamentals/04-functions-and-closures.md) |
| **ASGI** | The interface between async Python web servers and apps (Python's async Rack). | 06 Applied Python | [04](lessons/06-applied-python/04-fastapi-basics.md) |
| **ASGITransport** | Lets `httpx` call a FastAPI app in memory, without a network server. | 06 Applied Python | [10](lessons/06-applied-python/10-testing-fastapi.md) |
| **asyncio** | Python's built-in framework for concurrent I/O in one thread, using an event loop. | 06 Applied Python | [02](lessons/06-applied-python/02-asyncio-basics.md) |
| **`asyncio.gather` / `Semaphore`** | Run coroutines concurrently / limit how many run at once. | 06 Applied Python | [02](lessons/06-applied-python/02-asyncio-basics.md) |
| **At-most-once / at-least-once** | Messages may be lost but never repeated / never lost but may be repeated. | 03 Architecture | [02](lessons/03-architecture/02-events-and-outbox.md) |
| **Attribute** | A key-value on a span (`order.id`, `http.route`). | 03 Architecture | [04](lessons/03-architecture/04-opentelemetry.md) |
| **Automatic role switching** | Rails sends GET requests to the replica and other requests to the primary. | 02 Rails at scale | [04](lessons/02-rails-at-scale/04-partitioning-and-multi-db.md) |
| **Autovacuum** | The background process that removes dead rows and refreshes statistics. | 02 Rails at scale | [01](lessons/02-rails-at-scale/01-finding-slow-queries-and-explain.md) |

## B

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **Baseline** | The result you compare against (here: the agent without your tool). | 08 AI tool MVP | [04](lessons/08-ai-tool-mvp/04-evaluating-your-tool.md) |
| **Batch API** | Send many requests to run within 24 hours at 50% of the price. Good for eval runs. | 07 Agentic AI | [13](lessons/07-agentic-ai/13-cost-and-latency.md) |
| **`bin/rails runner`** | Runs a Ruby script inside a booted Rails app, with all models loaded. | 08 AI tool MVP | [01](lessons/08-ai-tool-mvp/01-rails-introspection-with-rails-runner.md) |
| **Bounded context** | A part of the business with its own model and language (Catalog, Ordering, Billing). | 03 Architecture | [01](lessons/03-architecture/01-bounded-contexts-and-packwerk.md) |
| **Buffers (hit / read)** | 8 kB data pages found in Postgres' memory / fetched from the OS or disk. | 02 Rails at scale | [01](lessons/02-rails-at-scale/01-finding-slow-queries-and-explain.md) |
| **Bug report template** | A single-file Rails script (in `guides/bug_report_templates/`) that reproduces a bug with an in-memory database. | 04 Open source | [01](lessons/04-open-source/01-contribution-workflow.md) |

## C

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **Cache key (Git SHA)** | The commit ID used to decide whether the index is still up to date. | 08 AI tool MVP | [03](lessons/08-ai-tool-mvp/03-building-the-rails-lens-server.md) |
| **Calibration / agreement** | Checking how often the judge agrees with your own human labels. | 07 Agentic AI | [12](lessons/07-agentic-ai/12-llm-as-judge.md) |
| **Cardinality** | The number of distinct values of a label; high cardinality makes metrics expensive. | 03 Architecture | [04](lessons/03-architecture/04-opentelemetry.md) |
| **CHANGELOG** | The file listing user-visible changes per release. | 04 Open source | [01](lessons/04-open-source/01-contribution-workflow.md) |
| **Chunk / chunking** | A piece of a document (a few paragraphs), and the process of splitting documents into such pieces before embedding. | 07 Agentic AI | [07](lessons/07-agentic-ai/07-chunking.md) |
| **CI** | Continuous integration: the project's automated tests and linters that run on every PR. | 04 Open source | [01](lessons/04-open-source/01-contribution-workflow.md) |
| **CLA / DCO** | Contributor License Agreement / Developer Certificate of Origin: legal sign-offs some projects require. | 04 Open source | [01](lessons/04-open-source/01-contribution-workflow.md) |
| **Closure** | A function that remembers variables from where it was defined. | 05 Python fundamentals | [04](lessons/05-python-fundamentals/04-functions-and-closures.md) |
| **Codebase index** | The JSON snapshot of models, routes and jobs that the tools answer from. | 08 AI tool MVP | [03](lessons/08-ai-tool-mvp/03-building-the-rails-lens-server.md) |
| **CODEOWNERS** | A file mapping paths to the maintainers who review them. | 04 Open source | [01](lessons/04-open-source/01-contribution-workflow.md) |
| **Composite index** | An index on several columns; column order decides which queries it helps. | 02 Rails at scale | [02](lessons/02-rails-at-scale/02-indexes-and-n-plus-one.md) |
| **Comprehension** | `[x * 2 for x in xs if x > 0]`: Python's `map` + `select` in one expression. | 05 Python fundamentals | [03](lessons/05-python-fundamentals/03-collections-and-comprehensions.md) |
| **Concurrency controls (`limits_concurrency`)** | Limit how many jobs with the same key run at once. | 02 Rails at scale | [05](lessons/02-rails-at-scale/05-solid-queue-internals.md) |
| **concurrent-ruby** | The gem Rails already depends on, with thread-safe structures (`Concurrent::Map`, atomics, pools). | 01 Advanced Ruby | [01](lessons/01-advanced-ruby/01-gvl-threads-and-thread-safety.md) |
| **Connection pool** | Active Record's set of DB connections per process; must be ≥ threads. | 01 Advanced Ruby | [03](lessons/01-advanced-ruby/03-puma-and-benchmarking.md) |
| **Content block** | One piece of a message: `text`, `thinking`, `tool_use`, `tool_result`, and so on. A message is a list of blocks. | 07 Agentic AI | [01](lessons/07-agentic-ai/01-how-an-llm-api-call-works.md) |
| **Context manager / `with`** | An object that sets up and tears down a resource around a block. | 05 Python fundamentals | [07](lessons/05-python-fundamentals/07-errors-files-and-with.md), [11](lessons/05-python-fundamentals/11-decorators-and-context-managers.md) |
| **Context map** | A diagram of the contexts and how they depend on each other. | 03 Architecture | [01](lessons/03-architecture/01-bounded-contexts-and-packwerk.md) |
| **Context propagation** | Passing the trace id across threads, processes and services (for example into a job). | 03 Architecture | [04](lessons/03-architecture/04-opentelemetry.md) |
| **Context window** | The maximum number of tokens the model can read in one request (the whole conversation, tools and documents). | 07 Agentic AI | [01](lessons/07-agentic-ai/01-how-an-llm-api-call-works.md) |
| **`CONTRIBUTING.md`** | The project's rules for contributors (setup, style, tests, changelog). | 04 Open source | [01](lessons/04-open-source/01-contribution-workflow.md) |
| **Coroutine / `async def` / `await`** | A pausable function / how you define one / where it pauses to wait. | 06 Applied Python | [02](lessons/06-applied-python/02-asyncio-basics.md) |
| **Cosine distance** | `1 - cosine similarity`. Smaller means more similar. pgvector's `<=>` operator returns it. | 07 Agentic AI | [06](lessons/07-agentic-ai/06-embeddings-and-vector-search.md) |
| **Cosine similarity** | A measure of how closely two vectors point in the same direction: 1 = same meaning, 0 = unrelated. | 07 Agentic AI | [06](lessons/07-agentic-ai/06-embeddings-and-vector-search.md) |
| **Coverage** | The share of code lines executed by the tests. | 06 Applied Python | [10](lessons/06-applied-python/10-testing-fastapi.md) |
| **Covering index (`INCLUDE`)** | An index that also stores extra columns so a query can be answered from the index alone. | 02 Rails at scale | [02](lessons/02-rails-at-scale/02-indexes-and-n-plus-one.md) |
| **CPU-bound / I/O-bound** | Time spent computing in Ruby / time spent waiting (database, HTTP, disk). | 01 Advanced Ruby | [01](lessons/01-advanced-ruby/01-gvl-threads-and-thread-safety.md) |

## D

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **Dataclass** | `@dataclass`: generates `__init__`, `__repr__`, `__eq__` from fields (like `Struct` / `Data.define`). | 05 Python fundamentals | [08](lessons/05-python-fundamentals/08-classes-and-dataclasses.md) |
| **DataFrame** | pandas' table: rows and named columns, with fast column operations. | 06 Applied Python | [03](lessons/06-applied-python/03-pandas-basics.md) |
| **Deadlock** | Two transactions each waiting for a lock the other holds; Postgres cancels one. | 02 Rails at scale | [03](lessons/02-rails-at-scale/03-locks-and-safe-migrations.md) |
| **Decorator** | `@something` above a function: a function that wraps another function. | 05 Python fundamentals | [11](lessons/05-python-fundamentals/11-decorators-and-context-managers.md) |
| **Dependency (`Depends`)** | A function FastAPI calls before your route to provide something (session, user, settings). | 06 Applied Python | [08](lessons/06-applied-python/08-dependency-injection.md) |
| **Dependency violation** | Code in pack A uses a constant from pack B without declaring the dependency. | 03 Architecture | [01](lessons/03-architecture/01-bounded-contexts-and-packwerk.md) |
| **`dependency_overrides`** | Replacing a dependency in tests (for example, the test database session). | 06 Applied Python | [08](lessons/06-applied-python/08-dependency-injection.md), [10](lessons/06-applied-python/10-testing-fastapi.md) |
| **Design doc** | A short proposal describing a problem, options and a plan before building. | 03 Architecture | [05](lessons/03-architecture/05-adrs-and-design-docs.md) |
| **Devcontainer** | A Docker-based, ready-made development environment defined in `.devcontainer/` (used by VS Code and Codespaces). | 04 Open source | [01](lessons/04-open-source/01-contribution-workflow.md) |
| **Dimensions** | How many numbers a vector has (for example 384). Fixed by the embedding model. | 07 Agentic AI | [06](lessons/07-agentic-ai/06-embeddings-and-vector-search.md) |
| **Domain event** | A record that something happened in the business (`order.placed`). | 03 Architecture | [02](lessons/03-architecture/02-events-and-outbox.md) |
| **Dual-write problem** | Writing to the database and to another system separately, so one can succeed while the other fails. | 03 Architecture | [02](lessons/03-architecture/02-events-and-outbox.md) |
| **Dunder method** | "Double underscore" methods such as `__init__`, `__repr__`, `__eq__` that hook into language features. | 05 Python fundamentals | [08](lessons/05-python-fundamentals/08-classes-and-dataclasses.md) |

## E

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **Eager loading (code)** | Loading every class at boot (`Rails.application.eager_load!`) so lists like `ApplicationRecord.descendants` are complete. Not the same as `includes`. | 08 AI tool MVP | [01](lessons/08-ai-tool-mvp/01-rails-introspection-with-rails-runner.md) |
| **`ef_search`** | HNSW setting: how many candidates to check per query. Higher = more accurate, slower. | 07 Agentic AI | [08](lessons/07-agentic-ai/08-pgvector-and-indexes.md) |
| **Embedding** | A list of numbers (a vector) that represents the meaning of a text. Similar meanings give nearby vectors. | 07 Agentic AI | [06](lessons/07-agentic-ai/06-embeddings-and-vector-search.md) |
| **Engine / session** | The connection pool / a unit of work with its own transaction (like a request's DB connection plus identity map). | 06 Applied Python | [06](lessons/06-applied-python/06-sqlalchemy-async.md) |
| **Entry point / console script** | A command created when your package is installed (like a gem's `exe/` file). | 08 AI tool MVP | [05](lessons/08-ai-tool-mvp/05-packaging-and-releasing.md) |
| **Enum** | A fixed set of named constants (instead of Ruby symbols). | 05 Python fundamentals | [12](lessons/05-python-fundamentals/12-pattern-matching-and-enums.md) |
| **Eval** | An automated test of an AI system's quality that produces a score, not just pass/fail. | 07 Agentic AI | [11](lessons/07-agentic-ai/11-evals-from-zero.md) |
| **Eval report** | The document (`EVALS.md`) that explains how you measured and what you found, including limits. | 08 AI tool MVP | [06](lessons/08-ai-tool-mvp/06-writing-an-eval-report.md) |
| **Event loop** | The scheduler that runs coroutines and switches between them while they wait for I/O. | 06 Applied Python | [02](lessons/06-applied-python/02-asyncio-basics.md) |
| **Exception / `raise ... from`** | Error object / raising a new error while keeping the original as its cause. | 05 Python fundamentals | [07](lessons/05-python-fundamentals/07-errors-files-and-with.md) |
| **Excessive agency** | An agent that can do more (delete, send, pay) than its task needs. | 07 Agentic AI | [14](lessons/07-agentic-ai/14-security-and-prompt-injection.md) |
| **EXPLAIN / EXPLAIN ANALYZE** | Shows the plan / runs the query and shows the plan with real timings and row counts. | 02 Rails at scale | [01](lessons/02-rails-at-scale/01-finding-slow-queries-and-explain.md) |
| **Exporter / OTLP / collector** | Sends spans out / the standard protocol / a service that receives, processes and forwards telemetry. | 03 Architecture | [04](lessons/03-architecture/04-opentelemetry.md) |

## F

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **f-string** | `f"Hi {name}"`: string interpolation. | 05 Python fundamentals | [02](lessons/05-python-fundamentals/02-values-and-truthiness.md) |
| **Failing test first** | Writing a test that fails because of the bug before fixing it. | 04 Open source | [01](lessons/04-open-source/01-contribution-workflow.md) |
| **Faithfulness** | Whether every claim in an answer is supported by the retrieved sources. | 07 Agentic AI | [12](lessons/07-agentic-ai/12-llm-as-judge.md) |
| **False positive (review bot)** | A comment about a problem that is not real. The metric that decides whether people keep a bot. | 08 AI tool MVP | [07](lessons/08-ai-tool-mvp/07-github-bots-for-options-b-and-c.md) |
| **Fiber** | A lightweight, cooperatively scheduled unit of execution inside a thread. | 01 Advanced Ruby | [02](lessons/01-advanced-ruby/02-fibers-and-ractors.md) |
| **Fiber scheduler** | A hook (Ruby 3.0+) that makes blocking I/O yield to other fibers automatically; used by the `async` gem and Falcon. | 01 Advanced Ruby | [02](lessons/01-advanced-ruby/02-fibers-and-ractors.md) |
| **Flaky / environmental failure** | A test that fails for reasons unrelated to your change (timing, missing service). | 04 Open source | [01](lessons/04-open-source/01-contribution-workflow.md) |
| **Flaky test** | A test that sometimes passes and sometimes fails without code changes. | 08 AI tool MVP | [07](lessons/08-ai-tool-mvp/07-github-bots-for-options-b-and-c.md) |
| **Flame graph** | A picture of profile samples: width = time, stacking = call depth. | 01 Advanced Ruby | [06](lessons/01-advanced-ruby/06-profiling.md) |
| **Fork** | Your own copy of the upstream repository on GitHub, where you push branches. | 04 Open source | [01](lessons/04-open-source/01-contribution-workflow.md) |
| **Fragmentation / jemalloc** | Free memory scattered in unusable pieces / an alternative `malloc` that fragments less. | 01 Advanced Ruby | [05](lessons/01-advanced-ruby/05-gc-and-memory.md) |
| **Full-text search** | Postgres word search: `tsvector` (processed words of a document), `tsquery` (processed query), `ts_rank` (score). | 07 Agentic AI | [09](lessons/07-agentic-ai/09-full-text-vector-and-hybrid-search.md) |

## G

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **GC (garbage collector)** | Frees objects that are no longer referenced. | 01 Advanced Ruby | [05](lessons/01-advanced-ruby/05-gc-and-memory.md) |
| **Generator** | A function with `yield` that produces values lazily (like a Ruby `Enumerator`). | 05 Python fundamentals | [09](lessons/05-python-fundamentals/09-iterators-and-generators.md) |
| **GIN index** | An index type for values with many parts (arrays, JSONB, full-text). | 02 Rails at scale | [02](lessons/02-rails-at-scale/02-indexes-and-n-plus-one.md) |
| **`git log -S` / `git blame`** | Find commits that added or removed a string / who last changed each line and why. | 04 Open source | [01](lessons/04-open-source/01-contribution-workflow.md) |
| **GitHub Action / workflow trigger** | Automation that runs on events such as `pull_request` or `workflow_run`. | 08 AI tool MVP | [07](lessons/08-ai-tool-mvp/07-github-bots-for-options-b-and-c.md) |
| **Golden dataset** | A fixed, versioned set of test cases (inputs + expected outcomes) used for every eval run. | 07 Agentic AI | [11](lessons/07-agentic-ai/11-evals-from-zero.md) |
| **Good first issue / help wanted** | Labels maintainers use for issues suitable for new contributors. | 04 Open source | [01](lessons/04-open-source/01-contribution-workflow.md) |
| **Ground truth** | The known-correct answers you score against. | 08 AI tool MVP | [04](lessons/08-ai-tool-mvp/04-evaluating-your-tool.md) |
| **Grounding / citation** | Making the answer rely on (and point to) the retrieved sources. | 07 Agentic AI | [10](lessons/07-agentic-ai/10-rag-end-to-end.md) |
| **GVL (Global VM Lock)** | CRuby's lock that lets only one thread per process run Ruby code at a time. Released while waiting on I/O. | 01 Advanced Ruby | [01](lessons/01-advanced-ruby/01-gvl-threads-and-thread-safety.md) |

## H

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **Hallucination** | A confident answer that is not supported by the sources or by facts. | 07 Agentic AI | [10](lessons/07-agentic-ai/10-rag-end-to-end.md) |
| **Heap slot / heap page** | The fixed-size cell holding one Ruby object / a page of slots. | 01 Advanced Ruby | [05](lessons/01-advanced-ruby/05-gc-and-memory.md) |
| **Heartbeat** | A periodic "I am alive" timestamp each Solid Queue process writes. | 02 Rails at scale | [05](lessons/02-rails-at-scale/05-solid-queue-internals.md) |
| **Held-out set** | Test cases you never look at while tuning, used to report honest results. | 07 Agentic AI | [11](lessons/07-agentic-ai/11-evals-from-zero.md) |
| **HNSW** | Hierarchical Navigable Small World: the most common vector index, a layered graph of "neighbour" links. | 07 Agentic AI | [08](lessons/07-agentic-ai/08-pgvector-and-indexes.md) |
| **HTTP client** | A library for calling other services' APIs (Faraday in Ruby; `requests`, `httpx` in Python). | 06 Applied Python | [01](lessons/06-applied-python/01-http-clients-requests-and-httpx.md) |
| **Human-in-the-loop** | Asking a person to approve an action (for example a write) before the agent runs it. | 07 Agentic AI | [03](lessons/07-agentic-ai/03-agent-loop.md) |
| **Hybrid search** | Running full-text and vector search, then merging the two ranked lists. | 07 Agentic AI | [09](lessons/07-agentic-ai/09-full-text-vector-and-hybrid-search.md) |

## I

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **Idempotency key** | A client-chosen key that makes a retried `POST` return the first result instead of acting twice. | 03 Architecture | [03](lessons/03-architecture/03-api-design.md) |
| **Idempotent consumer** | A handler that produces the same result when it processes the same event twice. | 03 Architecture | [02](lessons/03-architecture/02-events-and-outbox.md) |
| **Identity vs equality** | `is` (same object) vs `==` (equal value). | 05 Python fundamentals | [02](lessons/05-python-fundamentals/02-values-and-truthiness.md) |
| **Index Scan / Index Only Scan / Bitmap Heap Scan** | Uses an index then reads rows / answers from the index alone / collects matching pages from an index, then reads them. | 02 Rails at scale | [01](lessons/02-rails-at-scale/01-finding-slow-queries-and-explain.md) |
| **Interpreter** | The program that runs Python code (`python3.13`), like `ruby`. | 05 Python fundamentals | [01](lessons/05-python-fundamentals/01-tooling-uv-ruff-mypy.md) |
| **Introspection** | A program asking a running system to describe itself (for example, asking Rails for all models and their associations). | 08 AI tool MVP | [01](lessons/08-ai-tool-mvp/01-rails-introspection-with-rails-runner.md) |
| **Iterator / iterable** | An object you can loop over / an object that produces an iterator. | 05 Python fundamentals | [09](lessons/05-python-fundamentals/09-iterators-and-generators.md) |

## J

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **JIT (just-in-time compiler)** | Compiles frequently run Ruby code to machine code while the program runs. | 01 Advanced Ruby | [04](lessons/01-advanced-ruby/04-yjit.md) |
| **JSON Schema** | A standard format for describing the shape of JSON data (types, required fields). Tool inputs are described with it. | 07 Agentic AI | [02](lessons/07-agentic-ai/02-tool-calling.md) |
| **JSON-RPC** | The simple request/response message format MCP uses underneath. | 07 Agentic AI | [04](lessons/07-agentic-ai/04-mcp-concepts.md) |

## K

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **Kamal** | A tool that deploys Docker containers to your own servers over SSH. | 02 Rails at scale | [06](lessons/02-rails-at-scale/06-kamal-architecture.md) |
| **kamal-proxy** | Kamal's HTTP proxy on each server; switches traffic to the new container after its health check passes. | 02 Rails at scale | [06](lessons/02-rails-at-scale/06-kamal-architecture.md) |
| **Keyset (cursor) pagination** | Paging by "rows after this sort key" instead of `OFFSET`. | 03 Architecture | [03](lessons/03-architecture/03-api-design.md) |
| **Keyset (cursor) pagination** | "Give me the next N rows after id X": stable and fast, unlike `OFFSET`. | 06 Applied Python | [09](lessons/06-applied-python/09-full-text-search-and-cursor-pagination.md) |

## L

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **lambda** | A one-expression anonymous function. | 05 Python fundamentals | [04](lessons/05-python-fundamentals/04-functions-and-closures.md) |
| **Latency, TTFT** | How long a response takes; *time to first token* is how long until output starts. | 07 Agentic AI | [13](lessons/07-agentic-ai/13-cost-and-latency.md) |
| **Lazy loading / `selectinload`** | Loading a relationship on first access (not allowed in async) / loading it up front in one extra query (like `preload`). | 06 Applied Python | [06](lessons/06-applied-python/06-sqlalchemy-async.md) |
| **Least privilege** | Give each tool only the access it needs (for example a read-only DB user for read tools). | 07 Agentic AI | [14](lessons/07-agentic-ai/14-security-and-prompt-injection.md) |
| **list / tuple / dict / set** | Array / frozen array / Hash / Set. | 05 Python fundamentals | [03](lessons/05-python-fundamentals/03-collections-and-comprehensions.md) |
| **Live mode / static mode** | Getting facts by booting the app (accurate, needs a working app) vs by parsing files such as `schema.rb` (always works, less complete). | 08 AI tool MVP | [01](lessons/08-ai-tool-mvp/01-rails-introspection-with-rails-runner.md), [02](lessons/08-ai-tool-mvp/02-static-mode-parsing-schema-rb.md) |
| **LLM** | Large language model: a model that reads text and predicts the text that should follow. | 07 Agentic AI | [01](lessons/07-agentic-ai/01-how-an-llm-api-call-works.md) |
| **LLM-as-judge** | Using a model with a written rubric to grade another model's answer. | 07 Agentic AI | [12](lessons/07-agentic-ai/12-llm-as-judge.md) |
| **`load_async`** | Runs a query in a background thread while your code continues. | 02 Rails at scale | [02](lessons/02-rails-at-scale/02-indexes-and-n-plus-one.md) |
| **Lock queue** | Sessions waiting for a lock, in order; a waiting `ACCESS EXCLUSIVE` blocks the reads behind it. | 02 Rails at scale | [03](lessons/02-rails-at-scale/03-locks-and-safe-migrations.md) |
| **`lock_timeout` / `statement_timeout`** | Give up waiting for a lock / give up on a statement after a time limit. | 02 Rails at scale | [03](lessons/02-rails-at-scale/03-locks-and-safe-migrations.md) |

## M

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **`Mapped` / `mapped_column`** | SQLAlchemy 2.x's typed way to declare model columns. | 06 Applied Python | [06](lessons/06-applied-python/06-sqlalchemy-async.md) |
| **`max_tokens`** | The most tokens the model may *write* in one response. If it is reached, the answer is cut off. | 07 Agentic AI | [01](lessons/07-agentic-ai/01-how-an-llm-api-call-works.md) |
| **MCP (Model Context Protocol)** | An open standard for connecting AI applications to tools and data. Write a server once; use it from any MCP-capable app. | 07 Agentic AI | [04](lessons/07-agentic-ai/04-mcp-concepts.md) |
| **MCP client** | The component inside the host that keeps a connection to one MCP server. | 07 Agentic AI | [04](lessons/07-agentic-ai/04-mcp-concepts.md) |
| **MCP host** | The AI application the user works in (Claude Code, Claude Desktop, an IDE). | 07 Agentic AI | [04](lessons/07-agentic-ai/04-mcp-concepts.md) |
| **MCP Inspector** | A browser tool for testing an MCP server by hand. | 07 Agentic AI | [05](lessons/07-agentic-ai/05-building-an-mcp-server.md) |
| **MCP server** | Your program that offers tools, resources and prompts over MCP. | 07 Agentic AI | [04](lessons/07-agentic-ai/04-mcp-concepts.md) |
| **Message / role** | One turn of the conversation, from the `user` or the `assistant`. | 07 Agentic AI | [01](lessons/07-agentic-ai/01-how-an-llm-api-call-works.md) |
| **Messages API** | Claude's HTTP endpoint (`POST /v1/messages`). You send a conversation; it returns the next assistant message. | 07 Agentic AI | [01](lessons/07-agentic-ai/01-how-an-llm-api-call-works.md) |
| **Micro-benchmark (benchmark-ips)** | Timing two small implementations against each other; `benchmark-ips` reports iterations per second with a ± margin of error. | 01 Advanced Ruby | [06](lessons/01-advanced-ruby/06-profiling.md) |
| **Minor / major GC** | Collects only young objects / collects everything (slower). | 01 Advanced Ruby | [05](lessons/01-advanced-ruby/05-gc-and-memory.md) |
| **Mission Control – Jobs** | A web dashboard for Solid Queue (inspect, retry, discard). | 02 Rails at scale | [05](lessons/02-rails-at-scale/05-solid-queue-internals.md) |
| **Model tiering** | Using a cheaper, faster model where it is good enough, and a stronger one where it is needed. | 07 Agentic AI | [13](lessons/07-agentic-ai/13-cost-and-latency.md) |
| **`model_dump` / `model_validate`** | Convert a model to a dict / build a model from data (with validation). | 06 Applied Python | [05](lessons/06-applied-python/05-pydantic-and-settings.md) |
| **Modular monolith** | One deployable app split into modules with enforced boundaries. | 03 Architecture | [01](lessons/03-architecture/01-bounded-contexts-and-packwerk.md) |
| **Module / package** | A `.py` file / a folder of modules. | 05 Python fundamentals | [05](lessons/05-python-fundamentals/05-modules-packages-and-imports.md) |
| **MRR (mean reciprocal rank)** | Average of `1 / rank of the first relevant result`. Rewards putting the right answer first. | 07 Agentic AI | [11](lessons/07-agentic-ai/11-evals-from-zero.md) |
| **MTok** | One million tokens. Prices are quoted per MTok. | 07 Agentic AI | [13](lessons/07-agentic-ai/13-cost-and-latency.md) |
| **Multi-stage Docker build** | Build in one image, copy only the result into a small final image. | 06 Applied Python | [11](lessons/06-applied-python/11-docker-for-python-services.md) |
| **Mutable / immutable** | Can be changed in place (list, dict) or not (str, tuple, int). | 05 Python fundamentals | [02](lessons/05-python-fundamentals/02-values-and-truthiness.md) |
| **Mutex** | A lock so only one thread runs a critical section at a time. | 01 Advanced Ruby | [01](lessons/01-advanced-ruby/01-gvl-threads-and-thread-safety.md) |
| **mypy** | Static type checker (like Sorbet or Steep). | 05 Python fundamentals | [10](lessons/05-python-fundamentals/10-type-hints-and-mypy.md) |

## N

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **N+1 query** | One query for a list plus one more query per item. | 02 Rails at scale | [02](lessons/02-rails-at-scale/02-indexes-and-n-plus-one.md) |
| **`__name__ == "__main__"`** | True when a file is run directly, not imported (like `if __FILE__ == $0`). | 05 Python fundamentals | [05](lessons/05-python-fundamentals/05-modules-packages-and-imports.md) |

## O

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **OpenAPI / `/docs`** | A machine-readable API description, generated automatically; `/docs` is its interactive UI. | 06 Applied Python | [04](lessons/06-applied-python/04-fastapi-basics.md) |
| **OpenTelemetry (OTel)** | The vendor-neutral standard and SDKs for traces, metrics and logs. | 03 Architecture | [04](lessons/03-architecture/04-opentelemetry.md) |
| **Optimistic locking (`lock_version`)** | Detects a concurrent update at save time instead of locking in advance. | 02 Rails at scale | [03](lessons/02-rails-at-scale/03-locks-and-safe-migrations.md) |
| **ORM** | Object-relational mapper: maps classes to tables (Active Record, SQLAlchemy). | 06 Applied Python | [06](lessons/06-applied-python/06-sqlalchemy-async.md) |
| **Overlap** | Repeating a little text between neighbouring chunks so that ideas at a boundary are not lost. | 07 Agentic AI | [07](lessons/07-agentic-ai/07-chunking.md) |

## P

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **p50 / p95** | Percentiles: half of requests are faster than p50; 95% are faster than p95. | 07 Agentic AI | [13](lessons/07-agentic-ai/13-cost-and-latency.md) |
| **p50 / p95 / p99** | Latency percentiles: 50%, 95%, 99% of requests are faster than this. | 01 Advanced Ruby | [03](lessons/01-advanced-ruby/03-puma-and-benchmarking.md) |
| **Pack (package)** | A folder with its own `package.yml`, treated by Packwerk as a module. | 03 Architecture | [01](lessons/03-architecture/01-bounded-contexts-and-packwerk.md) |
| **Package / wheel** | An installable bundle of your Python project (`.whl` file). | 08 AI tool MVP | [05](lessons/08-ai-tool-mvp/05-packaging-and-releasing.md) |
| **`package_todo.yml`** | The recorded list of existing violations, so only new ones fail CI. | 03 Architecture | [01](lessons/03-architecture/01-bounded-contexts-and-packwerk.md) |
| **Packwerk** | A static checker that reports references between packs that are not declared or not public. | 03 Architecture | [01](lessons/03-architecture/01-bounded-contexts-and-packwerk.md) |
| **Parallel tool calls** | The model asks for several tools in one response; you run them all and return all results together. | 07 Agentic AI | [02](lessons/07-agentic-ai/02-tool-calling.md) |
| **Partial index** | An index on only the rows matching a `WHERE` condition. | 02 Rails at scale | [02](lessons/02-rails-at-scale/02-indexes-and-n-plus-one.md) |
| **Partitioning / partition pruning** | Splitting one table into child tables by a key / the planner skipping partitions that cannot match. | 02 Rails at scale | [04](lessons/02-rails-at-scale/04-partitioning-and-multi-db.md) |
| **Pass rate / task success** | The share of test cases where the system did the job correctly. | 07 Agentic AI | [11](lessons/07-agentic-ai/11-evals-from-zero.md) |
| **Path allowlist** | The rule that a tool may only read files inside the app directory, and never secret files. | 08 AI tool MVP | [03](lessons/08-ai-tool-mvp/03-building-the-rails-lens-server.md) |
| **Path operation** | A FastAPI route function, such as `@router.get("/documents")`. | 06 Applied Python | [04](lessons/06-applied-python/04-fastapi-basics.md) |
| **`pathlib.Path`** | Object-oriented file paths (like Ruby's `Pathname`). | 05 Python fundamentals | [07](lessons/05-python-fundamentals/07-errors-files-and-with.md) |
| **PgBouncer (transaction mode)** | A connection pooler that hands a server connection to a client only for one transaction. | 02 Rails at scale | [02](lessons/02-rails-at-scale/02-indexes-and-n-plus-one.md) |
| **pg_stat_statements** | A Postgres extension that records calls, total and mean time for every normalised query. | 02 Rails at scale | [01](lessons/02-rails-at-scale/01-finding-slow-queries-and-explain.md) |
| **pgvector** | A Postgres extension that adds a `vector` column type, distance operators and vector indexes. | 07 Agentic AI | [08](lessons/07-agentic-ai/08-pgvector-and-indexes.md) |
| **Positional / keyword argument** | Passed by position / by name (`f(1, limit=5)`). | 05 Python fundamentals | [04](lessons/05-python-fundamentals/04-functions-and-closures.md) |
| **precision@k** | Of the top *k* results, what fraction is relevant? | 07 Agentic AI | [11](lessons/07-agentic-ai/11-evals-from-zero.md) |
| **`preload` / `eager_load` / `includes`** | Separate queries / one `JOIN` query / Rails chooses between the two. | 02 Rails at scale | [02](lessons/02-rails-at-scale/02-indexes-and-n-plus-one.md) |
| **Privacy violation** | Code outside a pack uses a constant that is not in the pack's public folder. | 03 Architecture | [01](lessons/03-architecture/01-bounded-contexts-and-packwerk.md) |
| **Prompt (MCP)** | A reusable prompt template offered by an MCP server. | 07 Agentic AI | [04](lessons/07-agentic-ai/04-mcp-concepts.md) |
| **Prompt caching** | The API stores the start of your prompt (tools, system prompt) so repeat requests read it at about 10% of the price. | 07 Agentic AI | [13](lessons/07-agentic-ai/13-cost-and-latency.md) |
| **Prompt injection** | Text in data (a document, a web page, a tool result) that tries to give the model new instructions. | 07 Agentic AI | [14](lessons/07-agentic-ai/14-security-and-prompt-injection.md) |
| **`@property`** | A method used like an attribute (like a Ruby reader method). | 05 Python fundamentals | [08](lessons/05-python-fundamentals/08-classes-and-dataclasses.md) |
| **`Protocol`** | A type describing "anything with these methods" (duck typing, checked statically). | 05 Python fundamentals | [10](lessons/05-python-fundamentals/10-type-hints-and-mypy.md) |
| **Public API (of a pack)** | The small set of classes other packs may call (`app/public/`). | 03 Architecture | [01](lessons/03-architecture/01-bounded-contexts-and-packwerk.md) |
| **Puma worker / thread** | A forked process (parallel) / a thread inside it (concurrent within the GVL). | 01 Advanced Ruby | [03](lessons/01-advanced-ruby/03-puma-and-benchmarking.md) |
| **Pydantic model** | A class that validates and converts data from type hints (`BaseModel`). | 06 Applied Python | [05](lessons/06-applied-python/05-pydantic-and-settings.md) |
| **pydantic-settings** | Reads configuration from environment variables and `.env` into a typed object. | 06 Applied Python | [05](lessons/06-applied-python/05-pydantic-and-settings.md) |
| **PyPI** | The Python package registry, like RubyGems.org. | 05 Python fundamentals | [01](lessons/05-python-fundamentals/01-tooling-uv-ruff-mypy.md) |
| **PyPI / trusted publishing** | The Python package registry (like RubyGems.org); publishing from GitHub Actions without storing a password. | 08 AI tool MVP | [05](lessons/08-ai-tool-mvp/05-packaging-and-releasing.md) |
| **`pyproject.toml` / `uv.lock`** | Project metadata and dependencies / exact resolved versions (like `Gemfile` / `Gemfile.lock`). | 05 Python fundamentals | [01](lessons/05-python-fundamentals/01-tooling-uv-ruff-mypy.md) |
| **pytest / fixture / parametrize** | Test runner / reusable setup (like `let`) / run one test with many inputs. | 05 Python fundamentals | [06](lessons/05-python-fundamentals/06-testing-with-pytest.md) |

## Q

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **Query plan** | The tree of steps (scans, joins, sorts) Postgres chooses to run a query. | 02 Rails at scale | [01](lessons/02-rails-at-scale/01-finding-slow-queries-and-explain.md) |

## R

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **Race condition** | A bug where the result depends on the timing of threads (for example lost updates). | 01 Advanced Ruby | [01](lessons/01-advanced-ruby/01-gvl-threads-and-thread-safety.md) |
| **Ractor** | An experimental actor-like unit with its own GVL, for real parallel Ruby; objects are isolated. | 01 Advanced Ruby | [02](lessons/01-advanced-ruby/02-fibers-and-ractors.md) |
| **RAG (retrieval-augmented generation)** | Search your data first, put the best pieces in the prompt, and have the model answer from them. | 07 Agentic AI | [10](lessons/07-agentic-ai/10-rag-end-to-end.md) |
| **`Rails.event`** | Rails 8.1's structured event reporter (`notify`, tags, context, subscribers). | 03 Architecture | [02](lessons/03-architecture/02-events-and-outbox.md) |
| **Rate limit** | A limit on how many requests an API accepts per time window (GitHub: `403`/`429` with headers). | 06 Applied Python | [01](lessons/06-applied-python/01-http-clients-requests-and-httpx.md) |
| **Rate limiting (`rate_limit`)** | Rejecting clients that send too many requests in a time window (HTTP 429). | 03 Architecture | [03](lessons/03-architecture/03-api-design.md) |
| **Read replica / replication lag** | A read-only copy of the database / how far behind the primary it is. | 02 Rails at scale | [04](lessons/02-rails-at-scale/04-partitioning-and-multi-db.md) |
| **Rebase** | Replaying your commits on top of the latest upstream branch. | 04 Open source | [01](lessons/04-open-source/01-contribution-workflow.md) |
| **recall@k** | Of the documents that *should* be found, what fraction appears in the top *k* results? | 07 Agentic AI | [11](lessons/07-agentic-ai/11-evals-from-zero.md) |
| **RED metrics / SLO** | Rate, Errors, Duration / a target such as "99% of requests under 300 ms". | 03 Architecture | [04](lessons/03-architecture/04-opentelemetry.md) |
| **Reflection (Active Record)** | Rails APIs that describe models, such as `reflect_on_all_associations` and `validators`. | 08 AI tool MVP | [01](lessons/08-ai-tool-mvp/01-rails-introspection-with-rails-runner.md) |
| **Regression check** | An eval in CI that fails if a score drops below a threshold. | 07 Agentic AI | [11](lessons/07-agentic-ai/11-evals-from-zero.md) |
| **Remote (`origin`, `upstream`)** | Git's names for the repositories your clone talks to: your fork and the original. | 04 Open source | [01](lessons/04-open-source/01-contribution-workflow.md) |
| **REPL** | The interactive prompt (`python` or `uv run python`), like `irb`. | 05 Python fundamentals | [01](lessons/05-python-fundamentals/01-tooling-uv-ruff-mypy.md) |
| **Reproduction (repro)** | The smallest code or test that shows the bug. | 04 Open source | [01](lessons/04-open-source/01-contribution-workflow.md) |
| **Reranking** | A second, more expensive pass that re-orders the top results for relevance. | 07 Agentic AI | [09](lessons/07-agentic-ai/09-full-text-vector-and-hybrid-search.md) |
| **Resource** | Read-only data an MCP server offers by URI (for example `kb://documents/42`). | 07 Agentic AI | [04](lessons/07-agentic-ai/04-mcp-concepts.md) |
| **respx** | A library that mocks `httpx` requests in tests (like WebMock). | 06 Applied Python | [10](lessons/06-applied-python/10-testing-fastapi.md) |
| **RFC 9457 problem details** | A standard JSON error format (`type`, `title`, `status`, `detail`, `instance`). | 03 Architecture | [03](lessons/03-architecture/03-api-design.md) |
| **Role / accessory** | A group of servers running the app with one command (web, job) / a supporting service such as Postgres. | 02 Rails at scale | [06](lessons/02-rails-at-scale/06-kamal-architecture.md) |
| **Row lock** | A lock on one row (`SELECT ... FOR UPDATE`, `UPDATE`); other writers of that row wait. | 02 Rails at scale | [03](lessons/02-rails-at-scale/03-locks-and-safe-migrations.md) |
| **RRF (reciprocal rank fusion)** | A simple way to merge ranked lists: each result scores `1 / (60 + rank)` in each list; add the scores. | 07 Agentic AI | [09](lessons/07-agentic-ai/09-full-text-vector-and-hybrid-search.md) |
| **RSS** | Resident set size: the memory a process actually uses in RAM. | 01 Advanced Ruby | [05](lessons/01-advanced-ruby/05-gc-and-memory.md) |
| **Rubric** | The written grading criteria given to a judge. | 07 Agentic AI | [12](lessons/07-agentic-ai/12-llm-as-judge.md) |
| **ruff** | Linter and formatter (RuboCop + a formatter). | 05 Python fundamentals | [01](lessons/05-python-fundamentals/01-tooling-uv-ruff-mypy.md) |

## S

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **Sampling (head / tail)** | Keeping only some traces, deciding at the start / after the trace ends. | 03 Architecture | [04](lessons/03-architecture/04-opentelemetry.md) |
| **Sampling profiler** | Records the call stack many times per second to see where time goes (Vernier, stackprof). | 01 Advanced Ruby | [06](lessons/01-advanced-ruby/06-profiling.md) |
| **Savepoint (`requires_new: true`)** | A nested transaction that can roll back without aborting the outer one. | 03 Architecture | [02](lessons/03-architecture/02-events-and-outbox.md) |
| **`self`** | The instance, passed explicitly as the first parameter of methods. | 05 Python fundamentals | [08](lessons/05-python-fundamentals/08-classes-and-dataclasses.md) |
| **Semantic / vector search** | Finding the texts whose embeddings are closest to the query's embedding. | 07 Agentic AI | [06](lessons/07-agentic-ai/06-embeddings-and-vector-search.md) |
| **Semantic versioning (SemVer)** | `MAJOR.MINOR.PATCH` version numbers that signal breaking changes. | 08 AI tool MVP | [05](lessons/08-ai-tool-mvp/05-packaging-and-releasing.md) |
| **Seq Scan** | Reads every row of a table. | 02 Rails at scale | [01](lessons/02-rails-at-scale/01-finding-slow-queries-and-explain.md) |
| **Service container (CI)** | A database container that GitHub Actions starts next to your job. | 06 Applied Python | [12](lessons/06-applied-python/12-github-actions-ci.md) |
| **Sharding** | Splitting data across several databases, each holding a subset (for example by tenant). | 02 Rails at scale | [04](lessons/02-rails-at-scale/04-partitioning-and-multi-db.md) |
| **Shareable object** | An object that may be passed between Ractors (frozen, deeply immutable, or special). | 01 Advanced Ruby | [02](lessons/01-advanced-ruby/02-fibers-and-ractors.md) |
| **`SKIP LOCKED`** | `FOR UPDATE` that skips rows already locked by others: the basis of Postgres job queues. | 02 Rails at scale | [03](lessons/02-rails-at-scale/03-locks-and-safe-migrations.md) |
| **Slicing** | `items[1:3]`, `text[::-1]`: taking parts of sequences. | 05 Python fundamentals | [03](lessons/05-python-fundamentals/03-collections-and-comprehensions.md) |
| **Solid Cache / Solid Cable** | Database-backed Rails cache store / Action Cable adapter. | 02 Rails at scale | [05](lessons/02-rails-at-scale/05-solid-queue-internals.md) |
| **Solid Queue** | Rails 8's default Active Job backend, storing jobs in database tables. | 02 Rails at scale | [05](lessons/02-rails-at-scale/05-solid-queue-internals.md) |
| **Squash** | Combining several commits into one. | 04 Open source | [01](lessons/04-open-source/01-contribution-workflow.md) |
| **`src` layout** | Keeping package code under `src/` so tests import the installed package. | 05 Python fundamentals | [05](lessons/05-python-fundamentals/05-modules-packages-and-imports.md) |
| **Stateless API** | The API remembers nothing between calls; you resend the whole conversation every time. | 07 Agentic AI | [01](lessons/07-agentic-ai/01-how-an-llm-api-call-works.md) |
| **Statistics / ANALYZE** | Postgres' sampled summary of each column's data, used to estimate row counts; `ANALYZE` refreshes it. | 02 Rails at scale | [01](lessons/02-rails-at-scale/01-finding-slow-queries-and-explain.md) |
| **Stemming** | Reducing words to a root form so "retrying" matches "retry". | 07 Agentic AI | [09](lessons/07-agentic-ai/09-full-text-vector-and-hybrid-search.md) |
| **Stop reason** | Why the model stopped: `end_turn` (finished), `tool_use` (wants a tool), `max_tokens` (cut off), `refusal` and others. | 07 Agentic AI | [01](lessons/07-agentic-ai/01-how-an-llm-api-call-works.md) |
| **Streaming** | Receiving the response piece by piece as it is generated, instead of waiting for the whole thing. | 07 Agentic AI | [13](lessons/07-agentic-ai/13-cost-and-latency.md) |
| **Strict tools** | `strict: true` on a tool: the model's input is guaranteed to match the schema. | 07 Agentic AI | [02](lessons/07-agentic-ai/02-tool-calling.md) |
| **`strict_loading`** | Active Record mode that raises instead of lazily loading an association. | 02 Rails at scale | [02](lessons/02-rails-at-scale/02-indexes-and-n-plus-one.md) |
| **`strong_migrations`** | A gem that stops unsafe migrations and shows the safe version. | 02 Rails at scale | [03](lessons/02-rails-at-scale/03-locks-and-safe-migrations.md) |
| **Structural pattern matching** | `match value: case {...}:` (like Ruby's `case ... in`). | 05 Python fundamentals | [12](lessons/05-python-fundamentals/12-pattern-matching-and-enums.md) |
| **System prompt** | Instructions that apply to the whole conversation (the `system` parameter), such as the assistant's job and rules. | 07 Agentic AI | [01](lessons/07-agentic-ai/01-how-an-llm-api-call-works.md) |

## T

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **Table lock modes** | `ACCESS SHARE` (reads) to `ACCESS EXCLUSIVE` (most `ALTER TABLE`), which conflicts with everything. | 02 Rails at scale | [03](lessons/02-rails-at-scale/03-locks-and-safe-migrations.md) |
| **Thinking / effort** | Current models reason before answering ("thinking"). The `effort` setting controls how much, and so the cost and speed. | 07 Agentic AI | [01](lessons/07-agentic-ai/01-how-an-llm-api-call-works.md) |
| **Thread::Queue** | A thread-safe queue for producer/consumer work. | 01 Advanced Ruby | [01](lessons/01-advanced-ruby/01-gvl-threads-and-thread-safety.md) |
| **Throughput / latency** | Requests per second / time per request. | 01 Advanced Ruby | [03](lessons/01-advanced-ruby/03-puma-and-benchmarking.md) |
| **Timeout** | The maximum time to wait for a response before giving up. Always set one. | 06 Applied Python | [01](lessons/06-applied-python/01-http-clients-requests-and-httpx.md) |
| **Token** | The unit models read and write: on current Claude models about half an English word (2.5 characters). Prices and limits are counted in tokens. | 07 Agentic AI | [01](lessons/07-agentic-ai/01-how-an-llm-api-call-works.md) |
| **Tool (function calling)** | A function you describe to the model (name, description, JSON Schema for inputs). The model can ask you to call it. | 07 Agentic AI | [02](lessons/07-agentic-ai/02-tool-calling.md) |
| **Tool Runner** | A helper in the Anthropic Python SDK that runs the agent loop for you. | 07 Agentic AI | [03](lessons/07-agentic-ai/03-agent-loop.md) |
| **`tool_result` block** | Your reply with the tool's output, linked by `tool_use_id`. | 07 Agentic AI | [02](lessons/07-agentic-ai/02-tool-calling.md) |
| **`tool_use` block** | The model's request to call a tool, with an `id`, the tool `name` and the `input`. | 07 Agentic AI | [02](lessons/07-agentic-ai/02-tool-calling.md) |
| **Trace** | A log of every step of an agent run (tool, input, output size, tokens, time), used for debugging. | 07 Agentic AI | [03](lessons/07-agentic-ai/03-agent-loop.md) |
| **Trace / span** | The whole journey of one request / one timed operation inside it. | 03 Architecture | [04](lessons/03-architecture/04-opentelemetry.md) |
| **Transactional outbox** | Writing the event to an `outbox_events` table in the same transaction, then publishing it later. | 03 Architecture | [02](lessons/03-architecture/02-events-and-outbox.md) |
| **Transport** | How client and server exchange messages: **stdio** (local subprocess) or **Streamable HTTP** (network). | 07 Agentic AI | [04](lessons/07-agentic-ai/04-mcp-concepts.md) |
| **Truthiness** | Whether a value counts as true in `if`. | 05 Python fundamentals | [02](lessons/05-python-fundamentals/02-values-and-truthiness.md) |
| **`tsvector` / `tsquery` / `ts_rank`** | Postgres full-text search types and ranking function. | 06 Applied Python | [09](lessons/06-applied-python/09-full-text-search-and-cursor-pagination.md) |
| **Type hint / annotation** | `def f(x: int) -> str:`, optional types checked by tools, not at runtime. | 05 Python fundamentals | [10](lessons/05-python-fundamentals/10-type-hints-and-mypy.md) |
| **`TypedDict`** | A type for dicts with known keys. | 05 Python fundamentals | [10](lessons/05-python-fundamentals/10-type-hints-and-mypy.md) |

## U

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **Upstream** | The original project repository you want to contribute to. | 04 Open source | [01](lessons/04-open-source/01-contribution-workflow.md) |
| **`usage`** | Token counts returned with every response: input, output, cache reads and cache writes. | 07 Agentic AI | [01](lessons/07-agentic-ai/01-how-an-llm-api-call-works.md) |
| **uv** | A fast tool that manages Python versions, virtual environments, dependencies and lockfiles (rbenv + Bundler in one). | 05 Python fundamentals | [01](lessons/05-python-fundamentals/01-tooling-uv-ruff-mypy.md) |
| **uvicorn** | The ASGI server that runs FastAPI (like Puma). | 06 Applied Python | [04](lessons/06-applied-python/04-fastapi-basics.md) |
| **`uvx`** | Runs a command from a Python package without installing it permanently (like `npx`). | 08 AI tool MVP | [05](lessons/08-ai-tool-mvp/05-packaging-and-releasing.md) |

## V

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **Vector** | An ordered list of numbers, for example `[0.12, -0.40, 0.88, ...]`. Embeddings are vectors with hundreds of numbers (dimensions). | 07 Agentic AI | [06](lessons/07-agentic-ai/06-embeddings-and-vector-search.md) |
| **Vector index / ANN** | An index for fast *approximate nearest neighbour* search: very fast, very slightly inexact. | 07 Agentic AI | [08](lessons/07-agentic-ai/08-pgvector-and-indexes.md) |
| **`vector_cosine_ops`** | The pgvector operator class that builds an index for cosine distance (`<=>`). | 07 Agentic AI | [08](lessons/07-agentic-ai/08-pgvector-and-indexes.md) |
| **Virtual environment (venv)** | A project-local folder (`.venv`) with its own Python and packages, like a Bundler-managed gem set per project. | 05 Python fundamentals | [01](lessons/05-python-fundamentals/01-tooling-uv-ruff-mypy.md) |

## W

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **Wall time / CPU time** | Real elapsed time (including waiting) / time on the CPU only. | 01 Advanced Ruby | [06](lessons/01-advanced-ruby/06-profiling.md) |
| **Warm-up** | Running load before measuring, so caches and JIT are ready. | 01 Advanced Ruby | [03](lessons/01-advanced-ruby/03-puma-and-benchmarking.md) |
| **Worker / dispatcher / scheduler / supervisor** | Solid Queue processes: run jobs / move due jobs to ready / enqueue recurring jobs / start and watch the others. | 02 Rails at scale | [05](lessons/02-rails-at-scale/05-solid-queue-internals.md) |
| **Workflow** | A fixed sequence of steps written in your code (for example "search, then answer"). The opposite of an agent. | 07 Agentic AI | [03](lessons/07-agentic-ai/03-agent-loop.md) |
| **Write amplification / bloat** | Every index makes writes slower / dead space left in tables and indexes after updates and deletes. | 02 Rails at scale | [02](lessons/02-rails-at-scale/02-indexes-and-n-plus-one.md) |

## Y

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **YJIT** | CRuby's production JIT (enabled by default in new Rails apps on Ruby 3.3+). | 01 Advanced Ruby | [04](lessons/01-advanced-ruby/04-yjit.md) |

## Z

| Term | Meaning | Step | Lesson |
|---|---|---|---|
| **Zero-downtime deploy** | Starting the new version and switching traffic without dropping requests. | 02 Rails at scale | [06](lessons/02-rails-at-scale/06-kamal-architecture.md) |
| **ZJIT** | A newer, experimental JIT in Ruby 4.0. | 01 Advanced Ruby | [04](lessons/01-advanced-ruby/04-yjit.md) |
