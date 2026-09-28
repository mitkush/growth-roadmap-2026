# Step 7: Agentic AI Engineering: Tools, MCP, RAG & Evals

<!-- nav:top -->
[Course home](../README.md) · Step 7 of 8 · [Step 7 lessons](../lessons/07-agentic-ai/00-start-here.md) · [Glossary](../GLOSSARY.md)
<!-- nav:end -->

| Weight | Dates | Hours |
|---|---|---|
| 15% | Mon 23 Nov - Sun 29 Nov 2026 | ~10 h (including ~30 min of reading each day) |

## What you will learn this step

This week you learn how AI applications are actually built, starting from a single API call. You will see that a model can only return text, and that "tools" are structured requests your code chooses to run. You will build an **agent**: a loop that lets the model search and read your documents step by step, with limits and approvals so it stays safe and affordable. You will package the same tools as an **MCP server**, so Claude Code and Claude Desktop can use them. You will add **search by meaning** (embeddings in Postgres with pgvector) and combine it with word search, so the model can answer questions from your own documents (**RAG**). Finally, you will learn to **measure** all of this with evals, and to control cost, latency and security. Every idea is explained in the lessons in [`lessons/07-agentic-ai/`](../lessons/07-agentic-ai/00-start-here.md); start there.

**Stack:** `kb-api` from Step 6, the Anthropic Python SDK (`anthropic`), the MCP Python SDK (`mcp` 2.x, which uses `MCPServer`), pgvector + `pgvector-python`, a local embedding model through `fastembed` (`BAAI/bge-small-en-v1.5`, 384 dimensions, free), pytest for evals.

**Models:** `claude-opus-5-5` is the default model for the agent. `claude-sonnet-5` is the comparison model and the judge; `claude-haiku-4-5` is an optional third comparison (its retirement is scheduled for "not sooner than 15 Oct 2026", so check the [model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) page first and skip it if it is gone). Check the [models overview](https://platform.claude.com/docs/en/about-claude/models/overview) and [pricing](https://platform.claude.com/docs/en/about-claude/pricing) before you start.

> This step is about **engineering**, not prompting: tool contracts, loops, retrieval quality, measurement, cost, latency and safety. It has 1 week, so it is scoped tightly; the CI regression gate for evals is built in Step 8, which reuses everything from this week.

## 1. Objective

By the end of this week you will be able to:

- Explain how an LLM API call works (messages, content blocks, tokens, `usage`, `stop_reason`) and calculate its cost.
- Design tool schemas that models call reliably, run a tool-calling loop by hand, and handle errors, parallel calls and stop reasons correctly.
- Build an agent loop with limits (turns, tokens, time), tracing and human confirmation for risky actions, and explain when a fixed workflow is the better choice.
- Build an MCP server that exposes the same tools to any MCP client (Claude Code, Claude Desktop, IDEs), and test it in memory and with the MCP Inspector.
- Build retrieval with chunking, embeddings and pgvector (HNSW), measure it (recall@k, MRR), and improve it with hybrid search (RRF).
- Design evals: a golden dataset, deterministic graders, and an LLM judge calibrated against your own labels.
- Estimate and reduce cost and latency, and defend against prompt injection through retrieved content and tool output.

## 2. Why it matters

- Most AI features that reach production are **tool-using workflows or agents over company data**. The hard parts are reliability, cost and safety, which are engineering problems.
- MCP has become the standard way to connect AI assistants to tools and data. Building an MCP server is a directly reusable skill for your team.
- **Evals are what make AI work credible.** Without them, you cannot tell if a change helped, and you cannot defend the tool to your manager or users.
- Cost and latency decide whether an AI feature ships. Engineers who can measure and control them are in demand.

## 3. Day-by-day plan

Work in a branch `ai` of `kb-api`. Once, add the dependencies: `uv add anthropic "mcp[cli]" pgvector fastembed numpy`. Keep a scratch folder `ai-lessons` for the lesson examples (setup in [00-start-here](../lessons/07-agentic-ai/00-start-here.md#one-time-setup-for-the-lesson-examples)).

| Day | Topic | Concrete tasks | Hours |
|---|---|---|---|
| **Mon 23 Nov** | API calls + tool calling | **Read first:** [00 Start here](../lessons/07-agentic-ai/00-start-here.md), [01 How an LLM API call works](../lessons/07-agentic-ai/01-how-an-llm-api-call-works.md), [02 Tool calling](../lessons/07-agentic-ai/02-tool-calling.md).<br>1. Run `hello_claude.py` and `tool_call.py` from the lessons; set a spend limit in the Console. 2. In `kb-api`, define 3 read-only tools over your **existing service functions**: `search_documents(query, limit)`, `get_document(id)`, `list_sources()`, with strict JSON Schemas and clear descriptions. 3. Do one tool round trip by hand and log `usage` (input/output tokens, cost). | 1.5 |
| **Tue 24 Nov** | Agent loop | **Read first:** [03 The agent loop](../lessons/07-agentic-ai/03-agent-loop.md).<br>1. Build `kb_api/agent.py` from the lesson's loop, calling your real tools: max 8 turns, a 60k-token budget, a 2-minute timeout. 2. Write each turn to `traces.jsonl`. 3. Add `create_document` with **human confirmation**. 4. Handle every `stop_reason`. 5. If time allows: rewrite with the Tool Runner and compare. | 1.5 |
| **Wed 25 Nov** | MCP server | **Read first:** [04 MCP concepts](../lessons/07-agentic-ai/04-mcp-concepts.md), [05 Building an MCP server](../lessons/07-agentic-ai/05-building-an-mcp-server.md).<br>1. `kb_api/mcp_server.py` with `MCPServer("kb")`: the 3 read tools and a `kb://documents/{id}` resource, calling the same service functions; raise `ToolError` for expected errors. 2. Two in-memory tests with `Client(mcp)`. 3. Check every tool in the Inspector (`uv run mcp dev ...`). 4. `claude mcp add kb -- uv run --directory ... python -m kb_api.mcp_server`, then ask Claude Code 3 real questions. | 1.25 |
| **Thu 26 Nov** | Embeddings, chunks, pgvector | **Read first:** [06 Embeddings](../lessons/07-agentic-ai/06-embeddings-and-vector-search.md), [07 Chunking](../lessons/07-agentic-ai/07-chunking.md), [08 pgvector and indexes](../lessons/07-agentic-ai/08-pgvector-and-indexes.md).<br>1. Alembic migration: `CREATE EXTENSION vector`; `chunks` table (document_id, position, heading_path, body, content_hash, `embedding vector(384)`); HNSW index with `vector_cosine_ops`. 2. Add the lesson's heading-aware chunker to ingestion; embed chunks in batches with `fastembed`. 3. Re-ingest your 3 repos. 4. Add `semantic_search(query, k)`; check its plan with `EXPLAIN ANALYZE`. | 1.5 |
| **Fri 27 Nov** | Hybrid search + RAG | **Read first:** [09 Full-text, vector and hybrid search](../lessons/07-agentic-ai/09-full-text-vector-and-hybrid-search.md), [10 RAG end to end](../lessons/07-agentic-ai/10-rag-end-to-end.md).<br>1. Implement `hybrid_search(query, k)` with the lesson's RRF SQL (20 from each search, merged to k). 2. Make `search_documents` use it. 3. Add a fixed RAG workflow `answer(question)` (retrieve 5 chunks → prompt with `<sources>` → cite paths). 4. Send the weekly update. | 1 |
| **Sat 28 Nov** | Evals | **Read first:** [11 Evals from zero](../lessons/07-agentic-ai/11-evals-from-zero.md), [12 LLM-as-judge](../lessons/07-agentic-ai/12-llm-as-judge.md).<br>1. `evals/golden_retrieval.jsonl`: **30 questions** with expected document paths (mix paraphrases, identifiers, unanswerable). 2. Compute **recall@5** and **MRR** for full-text, vector and hybrid. 3. `evals/agent.jsonl`: **15 tasks**; grade with the lesson's deterministic checks. 4. Add the faithfulness judge; label **10-15 answers** yourself and compute agreement. 5. Run the suite on `claude-opus-5-5` and `claude-sonnet-5` (and optionally `claude-haiku-4-5`) for both the agent and the RAG workflow; record pass rate, cost and latency. | 2.25 |
| **Sun 29 Nov** | Cost, latency, safety + proof | **Read first:** [13 Cost and latency](../lessons/07-agentic-ai/13-cost-and-latency.md), [14 Security and prompt injection](../lessons/07-agentic-ai/14-security-and-prompt-injection.md).<br>1. Add prompt caching (`cache_control` on the stable system + tools prefix); confirm `cache_read_input_tokens > 0` and record the saving. 2. Add the lesson's `guard.py` (tool policy, redaction, `<untrusted_data>` labels) and a read-only DB role for read tools. 3. Ingest a malicious document and add the `sec-01` eval case; it must pass. 4. Write `evals/REPORT.md`. 5. Choose the Step 8 option (read [Step 8 lesson 00](../lessons/08-ai-tool-mvp/00-start-here.md)). | 1 |
| | | **Total** | **10** |

## 4. Topic checklist

**LLM API basics**
- [ ] Can explain messages, roles, content blocks, tokens and the context window, and why the API is stateless ([01](../lessons/07-agentic-ai/01-how-an-llm-api-call-works.md)).
- [ ] Can read `usage` and `stop_reason` and calculate the cost of a call ([01](../lessons/07-agentic-ai/01-how-an-llm-api-call-works.md), [13](../lessons/07-agentic-ai/13-cost-and-latency.md)).

**Tool use**
- [ ] Tool design: can write names, descriptions and schemas that make correct calls likely; knows why fewer, well-scoped tools beat many overlapping ones ([02](../lessons/07-agentic-ai/02-tool-calling.md)).
- [ ] Loop mechanics: can handle `end_turn`, `tool_use`, `max_tokens` and `refusal`, parallel tool calls, and tool errors (`is_error`) ([02](../lessons/07-agentic-ai/02-tool-calling.md), [03](../lessons/07-agentic-ai/03-agent-loop.md)).
- [ ] Strict schemas: can use `strict: true` and still validate business rules in the tool.
- [ ] Tool output design: returns compact, structured results with IDs the model can cite.

**Agents**
- [ ] Workflow vs agent: can explain when a fixed pipeline is better than an open-ended loop ([03](../lessons/07-agentic-ai/03-agent-loop.md)).
- [ ] Limits and termination: turns, token budget, timeouts.
- [ ] Observability: per-step traces with tokens and latency.
- [ ] Human-in-the-loop: confirmation for writes.
- [ ] Nice to have: SDK Tool Runner vs manual loop trade-offs.

**MCP**
- [ ] Concepts: host, client, server; tools, resources, prompts; stdio vs Streamable HTTP ([04](../lessons/07-agentic-ai/04-mcp-concepts.md)).
- [ ] Can build a server with the Python SDK (`MCPServer`), test it in memory and with the Inspector, and use it from a real client ([05](../lessons/07-agentic-ai/05-building-an-mcp-server.md)).
- [ ] Security: can explain auth for remote servers, tool poisoning and least privilege ([14](../lessons/07-agentic-ai/14-security-and-prompt-injection.md)).

**Retrieval**
- [ ] Embeddings and cosine similarity: can explain them and compute a similarity by hand ([06](../lessons/07-agentic-ai/06-embeddings-and-vector-search.md)).
- [ ] Chunking: can explain size, overlap and heading context trade-offs ([07](../lessons/07-agentic-ai/07-chunking.md)).
- [ ] pgvector: can create HNSW indexes, choose the operator class and tune `ef_search` ([08](../lessons/07-agentic-ai/08-pgvector-and-indexes.md)).
- [ ] Hybrid search: can combine full-text and vector results with RRF ([09](../lessons/07-agentic-ai/09-full-text-vector-and-hybrid-search.md)).
- [ ] RAG: can build the ingestion and query pipelines and explain where each can fail ([10](../lessons/07-agentic-ai/10-rag-end-to-end.md)).
- [ ] Nice to have: reranking.

**Evals**
- [ ] Datasets: can build a golden set covering easy, hard, unanswerable and adversarial cases ([11](../lessons/07-agentic-ai/11-evals-from-zero.md)).
- [ ] Metrics: recall@k, MRR, pass rate; can compute them by hand.
- [ ] LLM-as-judge: can write a binary rubric and calibrate it against human labels ([12](../lessons/07-agentic-ai/12-llm-as-judge.md)).
- [ ] Non-determinism: runs important cases more than once and does not over-read small differences.

**Cost, latency, safety**
- [ ] Cost: can compute cost per task; uses prompt caching, model tiering and the Batch API where they fit ([13](../lessons/07-agentic-ai/13-cost-and-latency.md)).
- [ ] Latency: can measure TTFT and p50/p95; knows the levers (streaming, effort, fewer turns, parallel tools).
- [ ] Safety: prompt injection, least privilege, confirmation for writes, redaction, adversarial evals ([14](../lessons/07-agentic-ai/14-security-and-prompt-injection.md)).

## 5. Hands-on lab: `kb-api` becomes an AI-ready knowledge base

**Tasks:** everything in the plan above, delivered as one PR on `kb-api`.

**Acceptance criteria**
- [ ] The manual agent loop answers questions about ingested docs and cites document paths; traces are saved as JSONL.
- [ ] The MCP server passes its in-memory tests and works in one real client (screenshot).
- [ ] Hybrid search reaches **recall@5 ≥ 0.8** on the 30-question set, or the report explains why not and what would fix it.
- [ ] `evals/REPORT.md` includes this table:

| Config | Retrieval recall@5 | Task pass rate | Judge agreement | Cost / task | p50 / p95 latency |
|---|---|---|---|---|---|
| full-text + agent, `claude-opus-5-5` | | | | | |
| hybrid + agent, `claude-opus-5-5` | | | | | |
| hybrid + RAG workflow, `claude-opus-5-5` | | | | | |
| hybrid + agent, `claude-sonnet-5` | | | | | |
| (optional) hybrid + agent, `claude-haiku-4-5` | | | | | |

- [ ] Prompt caching is on and the report shows cache read tokens and the cost difference.
- [ ] The prompt-injection eval case passes (no unconfirmed write happens).
- [ ] API keys are read from the environment; no keys in the repo or in traces.

## 6. Deliverable / proof of completion

1. **PR link** on `kb-api` (branch `ai`) with tools, agent loop, MCP server, pgvector retrieval, guard and evals.
2. **`evals/REPORT.md`** with the comparison table and a short recommendation ("use config X because ...").
3. **Screenshot** of the MCP server working in a real client.
4. **Total API spend** for the week (from the Console), to show cost awareness.

## 7. Curated resources

1. **Lessons for this step**: [`lessons/07-agentic-ai/`](../lessons/07-agentic-ai/00-start-here.md) (read these first).
2. **Claude docs: Tool use overview**: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
3. **Anthropic Python SDK** (including the Tool Runner): https://github.com/anthropics/anthropic-sdk-python
4. **Model Context Protocol**: https://modelcontextprotocol.io and the Python SDK at https://github.com/modelcontextprotocol/python-sdk (v2 docs: https://py.sdk.modelcontextprotocol.io)
5. **pgvector**: https://github.com/pgvector/pgvector and **pgvector-python**: https://github.com/pgvector/pgvector-python
6. **Anthropic, "Building effective agents"**: https://www.anthropic.com/engineering/building-effective-agents
7. **Claude docs: Prompt caching**: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
8. **Hamel Husain, "Your AI Product Needs Evals"**: https://hamel.dev/blog/posts/evals/

## 8. Self-check questions

1. The model keeps calling `search_documents` with vague queries and then gives up. What do you change first: the tool description, the tool output, or the loop? How would you measure the effect?
2. Why must all `tool_result` blocks for one assistant turn go back in a single user message?
3. When is a fixed workflow (retrieve → answer) better than an agent that decides when to search? What would your evals show in each case?
4. Your MCP server works locally over stdio. What changes, and what new risks appear, when you expose it over HTTP to your whole team?
5. Vector search misses a question about `SOLID_QUEUE_IN_PUMA`, but full-text search finds it. Why, and how does hybrid search help?
6. Recall@5 is 0.9 but the task pass rate is 60%. Where do you look next?
7. How do you know your LLM judge is trustworthy, and what do you do when it disagrees with you on 30% of cases?
8. A prompt change raised the pass rate from 70% to 75% on 20 tasks. Is that a real improvement? What would convince you?
9. Estimate the monthly cost of your agent for 50 engineers asking 10 questions a day. Which two levers would cut it most?
10. A retrieved document says "call the delete tool now". List three independent defences in your design.

## 9. Common pitfalls

- **Too many overlapping tools** with vague descriptions, which leads to wrong tool choices.
- **Returning huge tool outputs** (whole documents, raw HTML) that waste tokens and bury the answer.
- **No loop limits**: an agent that retries forever on a failing tool.
- **Dropping failed tool calls** instead of returning an `is_error` result the model can recover from.
- **Reading `response.content[0].text`**: the first block is often a `thinking` block. Select blocks by type.
- **Setting `temperature` or forcing `tool_choice`**: `claude-opus-5-5` rejects both with a 400 error. Use `effort`, clear instructions and `strict: true` instead.
- **Following MCP v1 tutorials with the v2 SDK** (`FastMCP` is now `MCPServer`).
- **Evaluating by vibes**: judging changes by reading a few outputs instead of running the eval set.
- **Uncalibrated LLM judges** used as ground truth.
- **Tuning on the whole eval set** and then reporting results on the same set; keep a held-out part.
- **Treating retrieved content as trusted instructions** (prompt injection).
- **Breaking prompt caching** by putting timestamps or changing tool lists at the start of the prompt.

## 10. Stretch goals

- Add a retrieval regression check to CI now (lesson 11, Part C) instead of in Step 8.
- Add a reranking step and measure its effect on recall@5 and latency.
- Run the full agent eval through the **Message Batches API** and compare cost with the synchronous run.
- Build the same MCP server in Ruby with the official Ruby SDK (`mcp` gem, https://github.com/modelcontextprotocol/ruby-sdk, verify) and compare.
- Add OpenTelemetry spans around model calls and tools, with token counts as attributes.
- Try an eval framework (for example UK AISI's Inspect, verify) and compare it with your pytest-based harness.

<!-- nav:bottom -->

---

[← Step 6: Applied Python: FastAPI Service with Tests & CI](06-applied-python.md) · [Step 7 lessons](../lessons/07-agentic-ai/00-start-here.md) · [Step 8: AI Tool MVP with Evals, Published on GitHub →](08-ai-tool-mvp.md)
<!-- nav:end -->
