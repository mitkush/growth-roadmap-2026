Please revise this PR (branch `roadmap/initial`). Keep the current plan, steps, weights, dates and repository structure, but turn the roadmap from a task plan into a **self-contained learning course** that I can follow day by day without searching elsewhere to understand what things mean.

## The problem with the current version
The step files are good *plans* but they are hard to *follow*. They are dense lists of tasks full of terms that are never explained. For example, in Step 7 I am told to "run a manual tool-calling loop", "return all tool_result blocks in one user message", "add an HNSW index with vector_cosine_ops", "compute recall@5 and MRR", "use reciprocal rank fusion" and "calibrate an LLM judge", but nothing explains **what** these things are, **why** they exist, or **how** they work. I have never built agents, MCP servers, RAG or evals, so I cannot act on these tasks. The same problem exists in Steps 5-6 (I am a Python beginner) and, to a lesser degree, in Steps 1-3.

## About me (for pitch and tone)
- 3+ years of Ruby on Rails. I understand web apps, ActiveRecord, background jobs and testing well.
- I worked as an LLM trainer, so I know what LLMs are and how prompting works, but I have **no hands-on experience** building AI applications (APIs, tools, agents, MCP, embeddings, RAG, evals).
- Python: beginner.
- Explain new ideas by relating them to Rails/Ruby concepts I already know whenever possible.

## What to add: learning content ("lessons")
For each step, create a folder of short lessons that teach the concepts the day-by-day plan needs:

```
steps/07-agentic-ai-engineering.md          # keep: the plan (updated with links to lessons)
lessons/07-agentic-ai/
  00-start-here.md                         # mental model of the whole step + glossary
  01-how-an-llm-api-call-works.md
  02-tool-calling.md
  ...
```

Every day in the day-by-day plan must start with **"Read first:"** links to the lesson(s) it needs, so the flow each day is: read the lesson (20-40 min), then do the tasks.

### Every lesson must follow this structure
1. **In one sentence**: what this is, in plain English.
2. **Why it exists**: the problem it solves. What goes wrong without it.
3. **Rails analogy**: "This is like ... in Rails" (and where the analogy breaks).
4. **How it works**: a step-by-step explanation, with a Mermaid diagram (sequence or flow) where it helps. Explain each moving part.
5. **Minimal working example**: a small, complete, runnable code example (with the exact command to run it and the expected output), built up in small steps with comments explaining each part. Not pseudo-code.
6. **Key terms**: each new term defined in 1-2 lines.
7. **Common mistakes**: what beginners get wrong and how to notice it.
8. **Check your understanding**: 3-5 questions, with answers in a collapsible `<details>` block.
9. **Go deeper (optional)**: 1-3 high-quality resources.

Target length: about 150-300 lines per lesson. Explain as a patient senior engineer would to a smart colleague who is new to the area. Use simple, clear English. No jargon without a definition the first time it appears.

### Scope and depth per step
- **Steps 7-8 (AI): highest priority and most depth.** I am new to all of this, so start from the ground up:
  - `00-start-here.md`: the big picture. How an AI application is built (app → LLM API → tools → data), where agents, MCP, RAG and evals fit, and a diagram of the whole `kb-api` system at the end of the week. Include a full glossary (token, context window, system prompt, stop reason, tool use, agent, MCP host/client/server, embedding, vector, cosine similarity, chunking, vector index, HNSW, full-text search, hybrid search, RRF, recall@k, MRR, golden dataset, LLM-as-judge, prompt caching, prompt injection, and any other term used in the step).
  - Lessons covering at least: how an LLM API call works (messages, roles, tokens, `usage`, `stop_reason`, cost); tool calling from first principles; building an agent loop (and workflow vs agent); MCP concepts and building a server; embeddings and vector search explained intuitively; chunking; pgvector and indexes; full-text vs vector vs hybrid search; what RAG is end to end; evals from zero (why, golden datasets, metrics with worked numeric examples of recall@k and MRR, LLM-as-judge and calibration, evals in CI); cost and latency (with a worked cost calculation); security and prompt injection.
  - For Step 8, add lessons for any concept the chosen option needs (for example Rails introspection with `bin/rails runner`, building a project that others can install, packaging and releasing, writing an eval report). Explain the 3 project options in plain language: what each tool does for a user, with an example conversation or screenshot-style walkthrough, so I can choose with confidence.
  - Use the current Claude models (check https://platform.claude.com/docs/en/about-claude/models/overview; for example, the current Opus model ID is `claude-opus-5-5`). Fix any outdated or incorrect model IDs in the plan.
- **Steps 5-6 (Python): high depth.** Teach Python concepts properly for a beginner, always comparing with Ruby. For Step 6, explain FastAPI, Pydantic, SQLAlchemy 2.0 (async), Alembic, dependency injection, Docker and GitHub Actions in terms of their Rails equivalents, and show how the pieces of `kb-api` connect (with a diagram).
- **Steps 1-3 (Rails depth): medium depth.** I know Rails, but explain the advanced concepts I am asked to use (GVL, Fibers and the fiber scheduler, Ractors, YJIT, GC and heap slots, Vernier profiles and how to read a flame graph, EXPLAIN ANALYZE output line by line, lock types, partitioning, Solid Queue internals, Kamal architecture, Packwerk, outbox pattern, OpenTelemetry concepts). Include real example output (for example an annotated EXPLAIN ANALYZE plan) and explain how to read it.
- **Step 4: light.** Add a lesson on the open-source contribution workflow (forking, running a gem's test suite locally, writing a good PR description, handling review).

### Also update
- **Each step file**: add a short "What you will learn this step" paragraph in plain English at the top, and "Read first:" lesson links in each day's row. Where a task uses a term, make sure a lesson explains it.
- **README.md**: add a "How to use this roadmap" section (read the step overview → each day read the lesson, then do the tasks → Sunday self-check) and a link to a top-level `GLOSSARY.md` that combines all glossary terms with links to the lesson that explains each one.
- Where a lab needs starter code or setup (for example the `shop-lab` seed data, the `kb-api` skeleton), provide exact setup commands and starter files or snippets so I never get stuck at "set up X".

## Quality bar
- Accuracy over volume. Code examples must be correct and runnable with the stated versions. Do not invent APIs, gem names, library functions or URLs; mark anything uncertain with "(verify)".
- Every concept used in a task is explained somewhere in the lessons. After finishing, go through each step's day-by-day plan and check that no term is left unexplained.
- Keep the existing plans, weights and dates unless a change is clearly needed; record any change in `CHANGES.md`.

## How to work (to keep this focused)
Do this in two phases and commit after each:
1. **Phase 1:** Steps 7 and 8 (lessons, plan links, glossary, model ID fix). Commit and push.
2. **Phase 2:** Steps 5-6, then Steps 1-4, then README and `GLOSSARY.md`. Commit and push.

Push to the same branch so this PR updates, and add a comment to the PR summarising what was added.
