# Step 8 lessons: start here

<!-- nav:top -->
[Course home](../../README.md) › [Step 8 plan](../../steps/08-ai-tool-mvp.md) · [Glossary](../../GLOSSARY.md)
<!-- nav:end -->

Step 8 is where everything comes together: you build a small but real AI tool, prove it works with evals, and publish it. This page explains the **three project options in plain language**, with a walkthrough of what each one looks like to a user, so you can choose with confidence. The other lessons in this folder teach what you need to build the recommended option.

**How to use this folder:** read this page on Sun 29 Nov (the last day of Step 7) and choose your option. Then follow the "Read first:" links in [the Step 8 plan](../../steps/08-ai-tool-mvp.md) each day.

## The lessons

| # | Lesson | Needed for |
|---|---|---|
| 00 | This page: the three options, how to choose, glossary | Choosing |
| 01 | [Rails introspection with `bin/rails runner`](01-rails-introspection-with-rails-runner.md) | Option A (core) |
| 02 | [Static mode: parsing `schema.rb` without booting Rails](02-static-mode-parsing-schema-rb.md) | Option A |
| 03 | [Building the rails-lens MCP server](03-building-the-rails-lens-server.md) | Option A |
| 04 | [Evaluating your tool: ground truth and A/B evals](04-evaluating-your-tool.md) | All options |
| 05 | [Packaging and releasing a tool others can install](05-packaging-and-releasing.md) | All options |
| 06 | [Writing an eval report](06-writing-an-eval-report.md) | All options |
| 07 | [Building blocks for Options B and C (GitHub Actions bots)](07-github-bots-for-options-b-and-c.md) | Options B and C only |

Everything from Step 7 is reused (these numbers are Step 7's lessons, in [`lessons/07-agentic-ai/`](../07-agentic-ai/00-start-here.md)): tool design (Step 7 lesson 02), the agent loop (03), MCP servers (04-05), evals and judges (11-12), cost (13) and security (14).

## The three options in plain language

### Option A (recommended): `rails-lens-mcp`, give AI assistants an accurate map of a Rails app

**What it does for a user:** a Rails developer adds `rails-lens` to Claude Code (or Cursor, or Claude Desktop). From then on, when they ask about their app, the assistant can look up **facts from the real app** (models, associations, validations, callbacks, routes, jobs) instead of guessing from grep results.

**Without the tool** (what happens today):

```text
You:    Add a "refunded" status to orders. What else do I need to change?
Claude: [greps for "status" and gets 140 matches across the app]
        [reads 6 files, spends about 40k tokens]
        You'll need to add "refunded" to the STATUSES constant in Order...
        I don't see any callbacks that depend on status.        ← wrong: it missed one
```

**With `rails-lens`:**

```text
You:    Add a "refunded" status to orders. What else do I need to change?
Claude: [calls describe_model("Order")]
          → table orders; status: string, nullable
          → validates status inclusion in: pending, paid, shipped
          → callbacks: before_validation :set_default_status, after_commit :send_receipt
          → belongs_to :customer; has_many :line_items; has_many :products (through line_items)
        [calls find_routes("orders")]
          → GET /orders (orders#index), GET /orders/:id (orders#show), POST /orders (orders#create)
        You need to:
        1. Add "refunded" to Order::STATUSES (the inclusion validation uses it). [app/models/order.rb]
        2. Check send_receipt: it runs after every commit, so a refund would also trigger
           ReceiptEmailJob. You probably want to skip it for refunds.
        3. There is no route for refunds yet; add PATCH /orders/:id/refund if needed.
```

The second answer is more accurate, cheaper (fewer tokens) and faster, because the tool gives precise facts. **That difference is what your evals will measure.**

**How it gets the facts:** it runs a small Ruby script inside the app with `bin/rails runner` ("live mode"), which asks Rails itself for its models and routes (lesson 01). If the app cannot boot, it falls back to reading `db/schema.rb` ("static mode", lesson 02).

**Why it is recommended:**
- It builds directly on Steps 1-3 (Rails internals) and Step 7 (MCP).
- **Ground truth is free and exact:** Rails tells you the real associations, so you can generate hundreds of eval questions automatically and score them without a judge.
- It is **read-only**, so the security surface is small.
- Your team can use it on day one.

### Option B: `rails-pr-reviewer`, an AI reviewer for risky Rails changes

**What it does for a user:** it runs as a GitHub Action on every pull request. It checks the diff for risky Rails patterns (unsafe migrations, missing indexes on new foreign keys, N+1-prone code) and posts **a few precise review comments**.

**Walkthrough:** a developer opens a PR that contains:

```ruby
class AddStatusToOrders < ActiveRecord::Migration[8.1]
  def change
    add_column :orders, :status, :string, null: false, default: "pending"
    add_index :orders, :status
  end
end
```

A minute later, a review comment appears on the `add_index` line:

```text
rails-pr-reviewer · warning · migration safety
`add_index :orders, :status` runs without `algorithm: :concurrently`. On a large `orders` table
this blocks writes while the index builds.
Suggested fix: add `disable_ddl_transaction!` to the migration and use
`add_index :orders, :status, algorithm: :concurrently`.
Evidence: schema.rb shows orders is a core table; this PR adds no batching.
```

**The hard part:** being **useful without being noisy**. A reviewer that posts 15 vague comments per PR gets turned off within a week. Your key metric is **false positives per PR**.

**Why not recommended first:** labelled ground truth is harder to get (you must label diffs by hand), and precision tuning takes time. It is a great choice if your team's biggest pain is risky PRs.

### Option C: `ci-triage-agent`, explain why a build failed

**What it does for a user:** when a CI run fails, it reads the logs, extracts the failing tests, checks whether those tests also fail on `main` or pass on retry (**flaky**), classifies the failure, and posts a short summary on the PR.

**Walkthrough:**

```text
ci-triage-agent · build #4812 failed
Classification: FLAKY (confidence: high)
- Failing test: spec/system/checkout_spec.rb:42 "completes checkout"
- It failed 3 times and passed 11 times on main in the last 7 days; it passed on retry here.
- Error: Capybara::ElementNotFound (a timing-sensitive wait).
Suggested next step: re-run the job; track this test in the flaky-tests issue #311.
Not related to your changes (files changed in this PR: app/models/invoice.rb).
```

**The hard part:** you need **history** (a store of past test results) and labelled examples of real failures.

**Why not recommended first:** it needs access to CI logs and history (often restricted at work), and building the history store adds scope. It is a great choice if your team loses a lot of time to flaky tests.

## How to choose

| Question | If yes, lean to |
|---|---|
| Do you want the fastest route to credible evals? | **A** (automatic ground truth) |
| Is your team's biggest pain risky PRs reaching production? | **B** |
| Does your team lose hours every week to red builds and flaky tests? | **C** |
| Can you access your company's CI logs and history for the pilot? | C is possible; otherwise A or B |
| Do you want the tool usable by your teammates on day one, with no org-level setup? | **A** (runs locally, read-only) |

If you are unsure, choose **A**. The plan, milestones and most lessons in this folder assume it.

## Glossary for Step 8

| Term | Meaning | Lesson |
|---|---|---|
| **Introspection** | A program asking a running system to describe itself (for example, asking Rails for all models and their associations). | [01](01-rails-introspection-with-rails-runner.md) |
| **`bin/rails runner`** | Runs a Ruby script inside a booted Rails app, with all models loaded. | [01](01-rails-introspection-with-rails-runner.md) |
| **Reflection (Active Record)** | Rails APIs that describe models, such as `reflect_on_all_associations` and `validators`. | [01](01-rails-introspection-with-rails-runner.md) |
| **Eager loading (code)** | Loading every class at boot (`Rails.application.eager_load!`) so lists like `ApplicationRecord.descendants` are complete. Not the same as `includes`. | [01](01-rails-introspection-with-rails-runner.md) |
| **Live mode / static mode** | Getting facts by booting the app (accurate, needs a working app) vs by parsing files such as `schema.rb` (always works, less complete). | [01](01-rails-introspection-with-rails-runner.md), [02](02-static-mode-parsing-schema-rb.md) |
| **Codebase index** | The JSON snapshot of models, routes and jobs that the tools answer from. | [03](03-building-the-rails-lens-server.md) |
| **Cache key (Git SHA)** | The commit ID used to decide whether the index is still up to date. | [03](03-building-the-rails-lens-server.md) |
| **Path allowlist** | The rule that a tool may only read files inside the app directory, and never secret files. | [03](03-building-the-rails-lens-server.md) |
| **Ground truth** | The known-correct answers you score against. | [04](04-evaluating-your-tool.md) |
| **A/B eval (with vs without)** | Running the same tasks with and without your tool to measure its effect. | [04](04-evaluating-your-tool.md) |
| **Baseline** | The result you compare against (here: the agent without your tool). | [04](04-evaluating-your-tool.md) |
| **Package / wheel** | An installable bundle of your Python project (`.whl` file). | [05](05-packaging-and-releasing.md) |
| **Entry point / console script** | A command created when your package is installed (like a gem's `exe/` file). | [05](05-packaging-and-releasing.md) |
| **`uvx`** | Runs a command from a Python package without installing it permanently (like `npx`). | [05](05-packaging-and-releasing.md) |
| **Semantic versioning (SemVer)** | `MAJOR.MINOR.PATCH` version numbers that signal breaking changes. | [05](05-packaging-and-releasing.md) |
| **PyPI / trusted publishing** | The Python package registry (like RubyGems.org); publishing from GitHub Actions without storing a password. | [05](05-packaging-and-releasing.md) |
| **Eval report** | The document (`EVALS.md`) that explains how you measured and what you found, including limits. | [06](06-writing-an-eval-report.md) |
| **GitHub Action / workflow trigger** | Automation that runs on events such as `pull_request` or `workflow_run`. | [07](07-github-bots-for-options-b-and-c.md) |
| **False positive (review bot)** | A comment about a problem that is not real. The metric that decides whether people keep a bot. | [07](07-github-bots-for-options-b-and-c.md) |
| **Flaky test** | A test that sometimes passes and sometimes fails without code changes. | [07](07-github-bots-for-options-b-and-c.md) |

All Step 7 terms (tool, agent, MCP, embedding, recall@k, LLM-as-judge and so on) are in the [Step 7 glossary](../07-agentic-ai/00-start-here.md#glossary).

<!-- nav:bottom -->

---

[← Step 7 lessons](../07-agentic-ai/00-start-here.md) · [Step 8 plan](../../steps/08-ai-tool-mvp.md) · [First lesson: 01 · Rails introspection with `bin/rails runner` →](01-rails-introspection-with-rails-runner.md)
<!-- nav:end -->
