You are a senior staff engineer and technical mentor. Build a high-quality, practical learning roadmap as a set of Markdown files in this repository, then commit them and open a pull request.

## About me
- Software engineer with 3+ years of professional Ruby on Rails experience (production apps, APIs, background jobs, testing).
- I have worked as an LLM trainer on earlier projects, so I already understand LLM behaviour and prompting. Do NOT teach prompt-engineering basics.
- Python: beginner. Start Python from fundamentals, but move fast and relate concepts to Ruby wherever possible.
- I work full-time, so plan for about 8-10 hours per week (about 1-1.5 hours on weekdays and 3-4 hours at weekends).

## The goal (already approved by my manager)
Title: "Strengthen Core Engineering Skills in Ruby on Rails and Build Hands-on Python & AI Skills"
Timeline: 28 Sep 2026 to 15 Dec 2026
Success criteria: a deeper Rails/Ruby foundation applied to real work; 1-2 open-source or internal tool contributions; Python proficiency; at least one real AI tool published on GitHub; 1-2 blog posts or write-ups; weekly tracked progress.

## The 8 steps (a starting point: research and refine the topics)
| # | Step | Weight | Due |
|---|------|--------|-----|
| 1 | Advanced Ruby: concurrency (Fibers, Ractors, threads and the GVL), YJIT, GC tuning, memory/CPU profiling on a real app | 10% | 4 Oct |
| 2 | Rails at scale: PostgreSQL deep dive (EXPLAIN ANALYZE, locking, partitioning), multi-DB and sharding, Rails 8 Solid Queue/Cache/Cable, Kamal deployment | 10% | 11 Oct |
| 3 | Architecture and system design: modular monolith (Packwerk), domain-driven boundaries, event-driven patterns, API design, observability (OpenTelemetry) | 10% | 18 Oct |
| 4 | Open-source contribution: Ruby gem or Rails, or publish my own gem, internal dev tool or learning content | 10% | 25 Oct |
| 5 | Python fundamentals: syntax, data structures, OOP, idioms, type hints, venv/pip, pytest, 5 practice problems, port a small Ruby utility to Python | 15% | 8 Nov |
| 6 | Applied Python: requests and pandas basics, then a REST API with FastAPI, Pydantic v2 and async SQLAlchemy 2.0, Docker, tests and CI | 15% | 22 Nov |
| 7 | Agentic AI engineering: tool use/function calling, MCP servers, multi-step agents, RAG with pgvector, LLM evals | 15% | 29 Nov |
| 8 | Build an AI tool MVP (e.g. an MCP server for Rails codebases or an AI PR-review agent) with evals, published on GitHub | 15% | 15 Dec |

### Research and refine these steps first
The topics listed in each step were drafted quickly and may be incomplete, contain extras, or be slightly off. Before writing the roadmap, research each step thoroughly and decide what a 3+ year Rails engineer (or, for Python, a beginner) actually needs in late 2026:
- **Add** important topics that are missing.
- **Remove or de-prioritise** topics that are outdated, too niche, low-value, or unrealistic for the time available.
- **Re-scope** a step if it is too heavy or too light for its duration and weight.
- Keep the overall shape (Rails depth, then contribution, then Python, then AI, with the AI tool as the capstone) and the final end date of 15 Dec 2026. Step titles, weights and due dates may be adjusted only if there is a strong reason.

Record every change in a `CHANGES.md` file: for each step, list what was added, removed or re-scoped and why, and give the final step title (short enough to paste into my company's goal tracker) with its weight and due date. The weights must still add up to 100%.

## What to create
```
README.md                      # overview, calendar, weekly rhythm, progress tracker
CHANGES.md                     # what was added/removed/re-scoped per step, and why
steps/01-advanced-ruby.md
steps/02-rails-at-scale.md
steps/03-architecture-system-design.md
steps/04-open-source-contribution.md
steps/05-python-fundamentals.md
steps/06-applied-python.md
steps/07-agentic-ai-engineering.md
steps/08-ai-tool-mvp.md
templates/weekly-update.md     # short Friday update I can paste to my manager
templates/blog-post-outline.md
```

### README.md must include
- A one-paragraph summary of the goal and how the steps build on each other: Rails depth, then contribution, then Python, then AI, with the AI tool as the capstone.
- A week-by-week calendar from 28 Sep to 15 Dec 2026, mapping each week to a step (steps 5, 6 and 8 span about 2 weeks).
- A recommended weekly rhythm (what to do on weekdays and at weekends).
- A progress-tracker table with a checkbox, weight, due date and "proof of completion" link column for each step.
- Where to naturally produce the 1-2 blog posts or write-ups (for example after Step 2 or 3 and after Step 8).

### Every steps/*.md file must follow this exact structure
1. **Objective**: what I will be able to do by the end, written for a 3+ year engineer (not a beginner, except for the Python fundamentals in Step 5).
2. **Why it matters**: real-world and career relevance.
3. **Day-by-day plan**: each day with its topic, concrete tasks and an estimated number of hours, fitting the weekly hour budget. For 2-week steps, plan both weeks.
4. **Topic checklist**: each subtopic as a checkbox, with the depth expected (for example "can explain X and demonstrate it in code").
5. **Hands-on lab**: a concrete exercise, ideally applied to a real or sample Rails app (or Python project for steps 5-8), with clear acceptance criteria.
6. **Deliverable / proof of completion**: exactly what to show my manager to mark the step done (a PR link, repo, benchmark numbers, write-up, and so on).
7. **Curated resources**: at most 5-8 high-signal resources (official docs, well-known books with specific chapters, notable conference talks, or repos). Only include resources you are confident exist. Prefer official documentation. Mark anything uncertain with "(verify)". No link farms.
8. **Self-check questions**: 8-10 probing questions that test real understanding, not trivia.
9. **Common pitfalls**: mistakes experienced engineers still make with this topic.
10. **Stretch goals**: optional work for when I finish early.

### Step-specific requirements
- **Step 1-3**: advanced depth, with benchmarks and measurable before/after results where possible (for example query time or memory). Use current stable Ruby 3.x and Rails 8.x features. Avoid material that is outdated in 2026.
- **Step 4**: a practical playbook: how to find suitable issues (labels, triaging, reading contribution guides), a shortlist of 5-8 well-known active Ruby gems or projects that are good to contribute to and why, how to write a PR that gets merged, and a fallback plan (my own gem or internal tool) if no PR is merged in time. This step must stand on its own, with no dependency on interview preparation.
- **Step 5**: a Ruby-to-Python "translation table" of concepts (blocks vs lambdas/comprehensions, modules vs packages, Bundler vs uv/pip, RSpec vs pytest, and so on). Use modern tooling (uv, ruff, type hints). The 5 practice problems should be specified.
- **Step 6**: one coherent project built up across 2 weeks (not disconnected tutorials), with a suggested repository structure, and CI with GitHub Actions.
- **Step 7**: focus on engineering: tool calling, building an MCP server, agent loops, retrieval quality, and eval design (datasets, metrics, regression checks). Include cost, latency and safety considerations. No prompt-engineering basics.
- **Step 8**: propose 3 concrete project options that solve real developer or team problems (at least one relevant to Rails teams). For each option give the problem, target users, architecture (a Mermaid diagram), tech stack, eval plan, and milestone plan across about 2 weeks. Recommend one, and include a README template for the final public repository.

## Quality bar
- Be specific and actionable. Every task should be something I can start immediately, with no vague "learn about X".
- Keep each step file focused (roughly 150-300 lines). Use tables and checklists for scannability.
- Be accurate. Do not invent gem names, APIs, book titles or URLs.
- Write in clear, simple English.

When finished, commit to a new branch named `roadmap/initial`, push it, and open a pull request with a short summary of what was created.
