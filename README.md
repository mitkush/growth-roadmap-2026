# Growth Roadmap 2026: Rails Depth, Python and AI Engineering

**Goal:** Strengthen Core Engineering Skills in Ruby on Rails and Build Hands-on Python & AI Skills
**Timeline:** Mon 28 Sep 2026 to Tue 15 Dec 2026 (11 weeks + 2 days)
**Time budget:** 8-10 hours per week (1-1.5 h on weekdays, 3-4 h at the weekend)

## Summary

This roadmap turns 3+ years of Rails experience into senior-level depth, then uses that base to learn Python and AI engineering quickly. **Steps 1-3** go deep on Ruby runtime performance, PostgreSQL and Rails 8 infrastructure, and architecture. Each step produces measured before/after results on one sample Rails app (`shop-lab`) or your real work app. **Step 4** turns that knowledge into a public open-source contribution. **Steps 5-6** build Python skills fast by mapping each concept to Ruby, ending in one production-shaped FastAPI service (`kb-api`) with tests and CI. **Step 7** adds tool calling, an MCP server, retrieval and evals on top of that service. **Step 8** is the capstone: a real AI tool for developers, published on GitHub with an eval suite. Each step reuses what the previous one built, so no week starts from zero.

See [CHANGES.md](CHANGES.md) for how the original draft was refined.

## Steps

| # | Step | Weight | Due | Plan |
|---|---|---|---|---|
| 1 | Advanced Ruby: Concurrency, YJIT & Profiling | 10% | Sun 4 Oct | [steps/01-advanced-ruby.md](steps/01-advanced-ruby.md) |
| 2 | Rails at Scale: PostgreSQL, Solid Queue & Kamal | 10% | Sun 11 Oct | [steps/02-rails-at-scale.md](steps/02-rails-at-scale.md) |
| 3 | Rails Architecture: Modular Monolith & Observability | 10% | Sun 18 Oct | [steps/03-architecture-system-design.md](steps/03-architecture-system-design.md) |
| 4 | Open-Source Contribution to the Ruby Ecosystem | 10% | Sun 25 Oct | [steps/04-open-source-contribution.md](steps/04-open-source-contribution.md) |
| 5 | Python Fundamentals for Rubyists | 15% | Sun 8 Nov | [steps/05-python-fundamentals.md](steps/05-python-fundamentals.md) |
| 6 | Applied Python: FastAPI Service with Tests & CI | 15% | Sun 22 Nov | [steps/06-applied-python.md](steps/06-applied-python.md) |
| 7 | Agentic AI Engineering: Tools, MCP, RAG & Evals | 15% | Sun 29 Nov | [steps/07-agentic-ai-engineering.md](steps/07-agentic-ai-engineering.md) |
| 8 | AI Tool MVP with Evals, Published on GitHub | 15% | Tue 15 Dec | [steps/08-ai-tool-mvp.md](steps/08-ai-tool-mvp.md) |

## Week-by-week calendar

Weeks run Monday to Sunday. The due date of each step is the Sunday that ends its last week.

| Week | Dates | Step | Focus | Side threads |
|---|---|---|---|---|
| W1 | 28 Sep - 4 Oct | **1** | GVL, threads, Fibers, Puma tuning, YJIT, GC, profiling | Sun: 20 min OSS issue scouting |
| W2 | 5 - 11 Oct | **2** | EXPLAIN ANALYZE, indexing, locking, safe migrations, multi-DB, Solid Queue, Kamal | Sun: 20 min OSS issue scouting |
| W3 | 12 - 18 Oct | **3** | Packwerk, boundaries, events + outbox, API design, OpenTelemetry, ADRs | Sun: pick OSS issue shortlist; outline **Blog post #1** |
| W4 | 19 - 25 Oct | **4** | Open-source PR (or fallback gem/tool) | Publish **Blog post #1** while waiting for review |
| W5 | 26 Oct - 1 Nov | **5** (week 1) | Python syntax, data structures, functions, OOP, uv/ruff/pytest | Respond to OSS review comments |
| W6 | 2 - 8 Nov | **5** (week 2) | Idioms, typing, generators, 5 practice problems, Ruby port | Respond to OSS review comments |
| W7 | 9 - 15 Nov | **6** (week 1) | `kb-api`: FastAPI, Pydantic v2, async SQLAlchemy 2.0, Alembic | |
| W8 | 16 - 22 Nov | **6** (week 2) | `kb-api`: tests, Docker, GitHub Actions CI, pandas report | |
| W9 | 23 - 29 Nov | **7** | Tool calling, agent loop, MCP server, pgvector RAG, evals | Choose Step 8 option (Sun) |
| W10 | 30 Nov - 6 Dec | **8** (week 1) | MVP core + eval harness | |
| W11 | 7 - 13 Dec | **8** (week 2) | Evals in CI, polish, docs; feature freeze Fri 11 Dec | |
| Final | Mon 14 - Tue 15 Dec | **8** (launch) | Publish v0.1.0, **Blog post #2**, final report to manager | |

## Weekly rhythm

| Day | Time | What to do |
|---|---|---|
| Mon | 1-1.5 h | **Read + plan.** Read the week's main resource. Write 3 bullet goals for the week in your log. |
| Tue | 1-1.5 h | **Build.** Small, focused coding tasks from the day-by-day plan. |
| Wed | 1-1.5 h | **Build.** Continue. Commit every session, even if unfinished. |
| Thu | 1-1.5 h | **Build + measure.** Run benchmarks or tests; record numbers in the step's results file. |
| Fri | 1-1.5 h | **Consolidate.** 15 min: send the [weekly update](templates/weekly-update.md). The rest: finish the day's task. |
| Sat | 2-2.5 h | **Deep work.** The hands-on lab: the longest, hardest task of the week. |
| Sun | 1-1.5 h | **Close out.** Self-check questions, write notes, prepare the proof of completion, 20 min of OSS scouting (W1-W3). |

Rules that keep the plan on track:

- **Protect the Saturday block.** Weekday sessions are for small steps; the lab needs a longer block.
- **Measure first, change second.** In Steps 1-3, never change code before you have a baseline number.
- **If you fall behind,** cut stretch goals first, then the lowest-priority checklist items (marked "Nice to have"). Never cut the lab or the deliverable.
- **Keep a learning log** (`log.md` in your practice repo): date, time spent, what you did, one thing you learned. It makes Friday updates take 5 minutes.

## Practice repositories

You will create these outside this roadmap repository:

| Repo | Used in | Purpose |
|---|---|---|
| `shop-lab` (Rails 8, PostgreSQL) | Steps 1-3 | A sample shop with seeded data for benchmarks. Use your work app instead if allowed (on a staging copy). |
| `python-katas` | Step 5 | Practice problems and the Ruby port. |
| `kb-api` (FastAPI) | Steps 6-7 | An engineering knowledge-base API that later gets tools, MCP and retrieval. |
| Step 8 project | Step 8 | The public AI tool (for example `rails-lens-mcp`). |

## Progress tracker

Tick the box and add a link when the proof of completion is ready.

| Done | # | Step | Weight | Due | Proof of completion |
|---|---|---|---|---|---|
| [ ] | 1 | Advanced Ruby: Concurrency, YJIT & Profiling | 10% | 4 Oct | _link to `shop-lab` perf report + PR_ |
| [ ] | 2 | Rails at Scale: PostgreSQL, Solid Queue & Kamal | 10% | 11 Oct | _link to query-tuning report + deployed URL_ |
| [ ] | 3 | Rails Architecture: Modular Monolith & Observability | 10% | 18 Oct | _link to ADRs + trace screenshot + Packwerk PR_ |
| [ ] | 4 | Open-Source Contribution to the Ruby Ecosystem | 10% | 25 Oct | _link to upstream PR (or published gem)_ |
| [ ] | 5 | Python Fundamentals for Rubyists | 15% | 8 Nov | _link to `python-katas` repo with green CI_ |
| [ ] | 6 | Applied Python: FastAPI Service with Tests & CI | 15% | 22 Nov | _link to `kb-api` repo + CI run_ |
| [ ] | 7 | Agentic AI Engineering: Tools, MCP, RAG & Evals | 15% | 29 Nov | _link to `kb-api` AI branch + eval report_ |
| [ ] | 8 | AI Tool MVP with Evals, Published on GitHub | 15% | 15 Dec | _link to public repo + v0.1.0 release_ |

**Completed weight:** 0% / 100%

### Success criteria tracker

| Done | Criterion | Planned in | Proof |
|---|---|---|---|
| [ ] | Deeper Rails/Ruby foundation applied to real work | Steps 1-3 (apply at least one finding to the work app) | _link_ |
| [ ] | 1-2 open-source or internal tool contributions | Step 4 (+ Step 8 counts as a second public tool) | _link_ |
| [ ] | Python proficiency | Steps 5-6 | _link_ |
| [ ] | At least one real AI tool published on GitHub | Step 8 | _link_ |
| [ ] | Blog post #1 | Outline W3, publish W4 | _link_ |
| [ ] | Blog post #2 | 14-15 Dec | _link_ |
| [ ] | Weekly tracked progress | Every Friday, [template](templates/weekly-update.md) | _link to log_ |

## Blog posts and write-ups

Use [templates/blog-post-outline.md](templates/blog-post-outline.md) for both.

| Post | When | Suggested topic | Why this timing |
|---|---|---|---|
| **#1** | Outline Sun 18 Oct, publish by Sun 25 Oct | *"Measuring before tuning: what YJIT, Puma threads and one missing index did to a Rails 8 app"*, built from the numbers you recorded in Steps 1-2 | The data already exists. Step 4 has natural waiting time while maintainers review your PR. |
| **#2** | Mon 14 - Tue 15 Dec | *"Building an MCP server for Rails codebases, and how I evaluated it"* (or the option you choose in Step 8) | The capstone is finished, and the eval results make a strong, honest story. |

Optional short write-up: a short internal note on the Step 3 ADRs, if your team has a tech-blog or wiki.

## Templates

- [templates/weekly-update.md](templates/weekly-update.md): 5-minute Friday update for your manager.
- [templates/blog-post-outline.md](templates/blog-post-outline.md): structure for both blog posts.
