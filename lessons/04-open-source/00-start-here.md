# Step 4 lessons: start here

<!-- nav:top -->
[Course home](../../README.md) › [Step 4 plan](../../steps/04-open-source-contribution.md) · [Glossary](../../GLOSSARY.md)
<!-- nav:end -->

This step is mostly **doing**: finding an issue, fixing it and getting a pull request merged in a real Ruby project. There is less new theory than in other steps, so there is one main lesson: the contribution workflow from fork to merge, with a worked example of setting up and running a real project's test suite (Solid Queue, which you studied in Step 2).

**How to use this folder:** read [01 The contribution workflow](01-contribution-workflow.md) before the scouting Sundays in Weeks 1-3 and again on Mon 19 Oct. Each day in [the Step 4 plan](../../steps/04-open-source-contribution.md) starts with **"Read first:"** links to the relevant section.

## The lessons

| # | Lesson | Day |
|---|---|---|
| 01 | [The contribution workflow: fork, test suite, PR, review](01-contribution-workflow.md) | Sun 4 Oct (first read), Mon 19 Oct - Sat 24 Oct |

## Glossary

| Term | Meaning | Lesson |
|---|---|---|
| **Upstream** | The original project repository you want to contribute to. | [01](01-contribution-workflow.md) |
| **Fork** | Your own copy of the upstream repository on GitHub, where you push branches. | [01](01-contribution-workflow.md) |
| **Remote (`origin`, `upstream`)** | Git's names for the repositories your clone talks to: your fork and the original. | [01](01-contribution-workflow.md) |
| **Rebase** | Replaying your commits on top of the latest upstream branch. | [01](01-contribution-workflow.md) |
| **`CONTRIBUTING.md`** | The project's rules for contributors (setup, style, tests, changelog). | [01](01-contribution-workflow.md) |
| **Good first issue / help wanted** | Labels maintainers use for issues suitable for new contributors. | [01](01-contribution-workflow.md) |
| **Reproduction (repro)** | The smallest code or test that shows the bug. | [01](01-contribution-workflow.md) |
| **Failing test first** | Writing a test that fails because of the bug before fixing it. | [01](01-contribution-workflow.md) |
| **CI** | Continuous integration: the project's automated tests and linters that run on every PR. | [01](01-contribution-workflow.md) |
| **Flaky / environmental failure** | A test that fails for reasons unrelated to your change (timing, missing service). | [01](01-contribution-workflow.md) |
| **`git log -S` / `git blame`** | Find commits that added or removed a string / who last changed each line and why. | [01](01-contribution-workflow.md) |
| **CHANGELOG** | The file listing user-visible changes per release. | [01](01-contribution-workflow.md) |
| **Squash** | Combining several commits into one. | [01](01-contribution-workflow.md) |
| **CLA / DCO** | Contributor License Agreement / Developer Certificate of Origin: legal sign-offs some projects require. | [01](01-contribution-workflow.md) |
| **CODEOWNERS** | A file mapping paths to the maintainers who review them. | [01](01-contribution-workflow.md) |
| **Devcontainer** | A Docker-based, ready-made development environment defined in `.devcontainer/` (used by VS Code and Codespaces). | [01](01-contribution-workflow.md) |
| **Bug report template** | A single-file Rails script (in `guides/bug_report_templates/`) that reproduces a bug with an in-memory database. | [01](01-contribution-workflow.md) |

<!-- nav:bottom -->

---

[← Step 3 lessons](../03-architecture/00-start-here.md) · [Step 4 plan](../../steps/04-open-source-contribution.md) · [First lesson: 01 · The contribution workflow: fork, test suite, PR, review →](01-contribution-workflow.md) · [Step 5 lessons →](../05-python-fundamentals/00-start-here.md)
<!-- nav:end -->
