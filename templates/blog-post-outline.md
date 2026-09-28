# Blog post outline template

Use this for both posts (Blog post #1 after Steps 1-2, Blog post #2 after Step 8). Target length: **1,200-2,000 words**, with at least one table or chart of real numbers. Plan about 3 hours: 1 h outline, 1.5 h draft, 0.5 h edit.

## Before you write

- [ ] **One-sentence takeaway:** what should the reader remember? _<write it here>_
- [ ] **Reader:** who is it for? (e.g. "Rails developers who run Puma in production")
- [ ] **Evidence:** which numbers, screenshots or code do you have? List them.
- [ ] **Permission:** remove company names, internal code and data unless you have approval.

## Structure

### 1. Title
Specific and honest. Include the result if you can.
_Example: "What YJIT, Puma threads and one missing index did to a Rails 8 app (with numbers)"_

### 2. Hook (1 paragraph)
The problem or surprise that started this. A symptom the reader has seen too.

### 3. Context (1-2 paragraphs)
- The setup: app size, data size, versions (Ruby, Rails, Postgres / Python, model).
- What "good" looks like: the metric you cared about.

### 4. Method (short)
- How you measured (tools, commands, warm-up, number of runs).
- Link to the repository so others can reproduce it.

### 5. What I did and what happened (main body, 3-5 sections)
For each change:
- **Change:** what you did (with a short code snippet).
- **Result:** before/after numbers (table).
- **Why:** the mechanism behind the result.

| Change | Metric before | Metric after | Notes |
|---|---|---|---|

### 6. What did not work
One or two things that did not help, or made things worse. This builds trust.

### 7. Lessons (3-5 bullets)
Practical advice the reader can apply tomorrow.

### 8. Limits and next steps
What your results do not show, and what you would test next.

### 9. Links
Repository, docs you relied on, and related posts.

## Suggested outlines

**Blog post #1 (publish by 25 Oct):** Measuring before tuning in a Rails 8 app
- Hook: "Our p95 was fine until it wasn't."
- Sections: baseline method → Puma threads vs workers (Step 1) → YJIT cost/benefit → the allocation fix found with Vernier → the missing index found with `pg_stat_statements` (Step 2) → safe migration to add it.
- Takeaway: measure, change one thing, measure again.

**Blog post #2 (publish 15 Dec):** Building (and evaluating) an MCP server for Rails codebases
- Hook: "The AI assistant invented a column that does not exist."
- Sections: problem → design (read-only, live vs static introspection) → tools that worked and tools that did not → how the evals were built (ground truth from Rails itself) → results with vs without the tool → cost, latency and safety → what's next.
- Takeaway: evals turn an AI demo into a tool people can trust.

## Final checklist

- [ ] Every number has a source (repo link, command or screenshot).
- [ ] Code snippets run as written.
- [ ] No confidential data or names.
- [ ] Read it aloud once; cut 10%.
- [ ] Share the link in the weekly update and in the README tracker.
