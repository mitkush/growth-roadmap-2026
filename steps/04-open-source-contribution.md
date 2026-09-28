# Step 4: Open-Source Contribution to the Ruby Ecosystem

| Weight | Dates | Hours |
|---|---|---|
| 10% | Mon 19 Oct - Sun 25 Oct 2026 (scouting starts in W1) | ~10 h (+ ~1 h scouting in W1-W3) |

## What you will learn this step

This week you make a real contribution to a Ruby project you have used (Solid Queue, Kamal, Rails and others): choosing an issue that fits, getting an unfamiliar project's test suite running, reproducing the bug with a failing test, making a small fix and writing a PR that maintainers can review quickly, then handling their feedback. The one lesson for this step, [The contribution workflow](../lessons/04-open-source/01-contribution-workflow.md), walks through each stage and includes a worked example of setting up and running Solid Queue's own test suite, including the setup errors you are likely to hit.

## 1. Objective

By the end of this week you will be able to:

- Find an issue in a well-known Ruby project that fits your skills and time, and confirm with maintainers that a fix is wanted.
- Set up a project's development environment and test suite, reproduce the bug with a failing test, and fix it the way the project expects.
- Write a PR that is easy to review and likely to be merged: small, tested, well described and following the contribution guide.
- Handle review feedback professionally and follow the PR to merge.
- If no upstream PR is possible in time, ship your own small gem or internal tool with the same quality bar.

## 2. Why it matters

- Reading and changing a large, well-maintained codebase quickly is a core senior skill. Open-source code is the best free training ground.
- A merged PR in Rails, RuboCop, Solid Queue or Kamal is public, verifiable proof of skill.
- You learn how top maintainers review code, which improves your own reviews at work.
- It meets the "1-2 open-source or internal tool contributions" success criterion.

## 3. Day-by-day plan

### Before this week: scouting (W1-W3, Sundays, 20 min each)

| When | Task |
|---|---|
| Sun 4 Oct | **Read first:** [01 The contribution workflow](../lessons/04-open-source/01-contribution-workflow.md) (sections 1-4).<br>Star the 8 projects below. Read `CONTRIBUTING.md` for 3 of them. |
| Sun 11 Oct | **Read first:** [01 The contribution workflow](../lessons/04-open-source/01-contribution-workflow.md), "Issue fit checks".<br>Browse `good first issue`, `help wanted` and recent bug issues in `rails/solid_queue` and `basecamp/kamal` (you used both in Step 2). Save 5 candidates. |
| Sun 18 Oct | **Read first:** section 5.2 below (issue fit checks).<br>Narrow to a **shortlist of 3** using the "issue fit" checks below. Comment on your top pick: "I'd like to work on this; my plan is X. Does that sound right?" |

### Week 4

| Day | Topic | Concrete tasks | Hours |
|---|---|---|---|
| **Mon 19 Oct** | Choose + set up | **Read first:** [00 Start here](../lessons/04-open-source/00-start-here.md), [01 The contribution workflow](../lessons/04-open-source/01-contribution-workflow.md) ("Git setup for a fork" and section 5).<br>1. Read maintainer replies; choose the issue (or switch to #2 on the shortlist). 2. Fork, clone and run the full test suite locally (or in the project's devcontainer). 3. Note how long the suite takes and how to run one test file. | 1.5 |
| **Tue 20 Oct** | Reproduce | **Read first:** [01 The contribution workflow](../lessons/04-open-source/01-contribution-workflow.md) ("Finding your way in unfamiliar code").<br>1. Write a **failing test** that reproduces the issue (for Rails: start from the bug report templates in `guides/bug_report_templates`). 2. Find the code path with `git grep`, the debugger (`ruby/debug`, `binding.b`) and `git log -S`. 3. Read the last 3 merged PRs that touched those files. | 1.5 |
| **Wed 21 Oct** | Fix | **Read first:** [01 The contribution workflow](../lessons/04-open-source/01-contribution-workflow.md) (section 7, "Common mistakes").<br>1. Make the smallest change that makes the test pass. 2. Run the related test files and the linter (RuboCop/Standard). 3. Check edge cases: nil, empty, multiple DB adapters, older Ruby versions supported by the project. | 1.5 |
| **Thu 22 Oct** | Polish + open PR | **Read first:** [01 The contribution workflow](../lessons/04-open-source/01-contribution-workflow.md) ("A PR description that gets reviewed") and section 5.4 below.<br>1. Add a CHANGELOG entry if the project wants one. 2. Squash into one clean commit with a clear message. 3. Open the PR using the PR template below. 4. Link the issue. | 1.25 |
| **Fri 23 Oct** | Blog post #1 | **Read first:** [`templates/blog-post-outline.md`](../templates/blog-post-outline.md).<br>1. Draft Blog post #1 from Steps 1-2 results (the PR is now waiting for review). 2. Send the weekly update with the PR link. | 1 |
| **Sat 24 Oct** | Review loop or second contribution | **Read first:** [01 The contribution workflow](../lessons/04-open-source/01-contribution-workflow.md) ("Handling review").<br>1. Answer review comments within 24 h; push fixes as new commits unless asked to squash. 2. If there is no review yet: start a **second, smaller contribution** (a docs fix, or another issue from your shortlist), or start the fallback below if the first PR is blocked. 3. Finish and publish Blog post #1. | 2.5 |
| **Sun 25 Oct** | Proof | **Read first:** the glossary in [00 Start here](../lessons/04-open-source/00-start-here.md); re-answer lesson 01's "Check your understanding".<br>1. Write `contribution-notes.md`: issue, root cause, fix, what you learned from the codebase. 2. Self-check questions. 3. Update the README tracker. | 0.75 |
| | | **Total** | **10** |

## 4. Topic checklist

- [ ] Can find issues using labels, GitHub search and recent bug reports, and judge whether an issue is a good fit (see checks below).
- [ ] Can read `CONTRIBUTING.md`, the PR template, CI config and CODEOWNERS, and follow them exactly.
- [ ] Can set up the dev environment and run a single test file in the project.
- [ ] Can reproduce a bug as a minimal failing test before changing code.
- [ ] Can navigate an unfamiliar codebase using `git grep`, `git log -S`, `git blame` and the debugger.
- [ ] Can write a PR description that states problem, cause, fix, testing and trade-offs.
- [ ] Can respond to review feedback without taking it personally, and knows when to push back politely with evidence.
- [ ] Knows the project's licence and any contributor agreement requirements.
- [ ] Knows how to follow up on a stale PR (one polite ping after ~1-2 weeks).

## 5. Hands-on lab: the contribution playbook

### 5.1 Where to look

| Source | How to use it |
|---|---|
| **Labels** | Search `label:"good first issue"`, `label:"help wanted"`, `label:bug` with `is:open no:assignee`. |
| **GitHub search** | `is:issue is:open label:"good first issue" language:Ruby` sorted by recently updated. |
| **Your own experience** | Bugs or missing docs you hit in Steps 1-3 (Solid Queue, Kamal, strong_migrations) are the best candidates: you already have context. |
| **Docs** | Wrong or outdated docs and guides are welcome in almost every project and are quick to review. |
| **Deprecation warnings** | Warnings in your app's logs from a gem often point to small, useful fixes. |

### 5.2 Issue fit checks (all should be "yes")

- [ ] Updated in the last 3 months, and a maintainer has commented or labelled it.
- [ ] No one is assigned or has an open PR for it.
- [ ] You can reproduce it in under 1 hour.
- [ ] The fix is likely under ~100 lines, including tests.
- [ ] The project merged outside PRs in the last month (check "Pull requests → Closed").

### 5.3 Shortlist of projects

| Project | Repo | Why it is a good fit for you |
|---|---|---|
| **Solid Queue** | `rails/solid_queue` | You studied it in Step 2; smaller codebase than Rails; active issues about adapters, recurring tasks and docs. |
| **Kamal** | `basecamp/kamal` | You deployed with it in Step 2; clear command structure; many issues are CLI edge cases or docs. |
| **Rails** | `rails/rails` | Highest profile. Best entry points: Rails Guides and API docs fixes, bugs with a reproduction script, Active Record edge cases. Reviews can be slow, so start early. |
| **RuboCop / rubocop-rails** | `rubocop/rubocop`, `rubocop/rubocop-rails` | Each cop is small and well tested; false-positive bug reports are ideal first issues; very responsive maintainers. |
| **factory_bot** | `thoughtbot/factory_bot` | Used in almost every Rails app; readable codebase; clear contribution guide. |
| **Faker** | `faker-ruby/faker` | Uses `good first issue` often; easy setup; good for a quick second contribution. |
| **Pagy** | `ddnexus/pagy` | Popular pagination gem; active maintainer; small, focused code. |
| **ankane's gems** | e.g. `ankane/strong_migrations`, `ankane/pghero` | Postgres-focused (matches Step 2); fast responses; very small, clean codebases. |

Before choosing, check each repo's recent activity yourself: maintainers and activity change over time.

### 5.4 How to write a PR that gets merged

1. **Ask first** for anything bigger than a typo: comment on the issue with your plan.
2. **One change per PR.** No drive-by refactors or formatting changes.
3. **Test first:** the failing test should be the first thing a reviewer reads.
4. **Match the house style**: naming, comment density, CHANGELOG format, commit message style.
5. **Make CI green** before asking for review.
6. **Describe it well** with this template:

```markdown
### Problem
<What is wrong, with a link to the issue and a minimal reproduction.>

### Cause
<One or two sentences on the root cause, with a file/line link.>

### Fix
<What you changed and why this approach. Mention the alternatives you rejected.>

### Testing
<New/changed tests. Commands you ran. Adapters/Ruby versions covered.>
```

7. **Be patient and responsive**: reply within a day, thank reviewers, ping once after 1-2 weeks of silence.

### 5.5 Fallback plan (decide by Wed 21 Oct)

If no suitable issue is confirmed by Wednesday, or the project is unresponsive, switch to **one** of these. Both count as "internal tool contribution" in the success criteria.

| Option | What to build | Quality bar |
|---|---|---|
| **A. Your own gem** | A small tool from Steps 1-2, for example: a Rake task that reads `pg_stat_statements`, runs `EXPLAIN` on the top N queries and flags sequential scans on large tables; or a RuboCop custom cop for a rule your team keeps repeating in reviews. Check RubyGems first so you do not duplicate an existing gem. | Published on RubyGems, README with usage, tests, CI, semantic versioning, `CHANGELOG.md`. |
| **B. Internal dev tool** | A tool for your team at work: a `bin/` script, a CI check, a generator or a shared RuboCop config. | Merged into the team repo, with docs and at least one other engineer using it. |

**Acceptance criteria (for either path)**
- [ ] Upstream path: PR opened with a failing-then-passing test, CI green and at least one maintainer interaction by 25 Oct.
- [ ] Fallback path: gem released as `v0.1.0` on RubyGems, or internal tool merged, by 25 Oct.
- [ ] `contribution-notes.md` explains the root cause and what you learned.

## 6. Deliverable / proof of completion

1. **Upstream PR link** (open with review activity counts as done; track merge in the README until 15 Dec).
   **or** a **RubyGems link + GitHub repo** (fallback A) **or** an **internal PR link** (fallback B).
2. `contribution-notes.md` (half a page).
3. **Blog post #1 link** (published this week).

## 7. Curated resources

1. **Course lesson for this step**: [The contribution workflow](../lessons/04-open-source/01-contribution-workflow.md) (with a worked example of running Solid Queue's test suite).
2. **Rails: Contributing to Ruby on Rails guide**: https://guides.rubyonrails.org/contributing_to_ruby_on_rails.html
3. **GitHub docs: Finding ways to contribute to open source**: https://docs.github.com/en/get-started/exploring-projects-on-github/finding-ways-to-contribute-to-open-source-on-github
4. **Open Source Guides: How to Contribute to Open Source**: https://opensource.guide/how-to-contribute/
5. **RuboCop: Development docs** (how cops are built and tested): https://docs.rubocop.org/rubocop/development.html
6. **Bundler guide: Creating a gem** (for the fallback): https://bundler.io/guides/creating_gem.html
7. **ruby/debug** (the standard debugger for exploring unfamiliar code): https://github.com/ruby/debug

## 8. Self-check questions

1. What did you check to decide that the issue was worth your time, and what would have made you drop it?
2. Why is a failing test the most valuable part of a bug-fix PR for a maintainer?
3. How did you find the code path responsible for the bug? What would you do faster next time?
4. What edge cases did you consider, and which supported Ruby/Rails versions or DB adapters could behave differently?
5. A maintainer asks for a completely different approach. How do you respond?
6. What did you learn about the project's design that you could apply at work?
7. When is it better to open an issue or discussion instead of a PR?
8. If you published a gem, how did you choose its public API and version number, and what would count as a breaking change?

## 9. Common pitfalls

- **Picking an issue that is too big** or that maintainers have not agreed to fix.
- **Starting without reading CONTRIBUTING.md**, then failing CI on style or missing CHANGELOG.
- **Mixing refactors with the fix**, which makes review slow and risky.
- **Not running the test suite for all supported adapters or Ruby versions** when the project needs it.
- **Going silent after review comments**, or arguing without evidence.
- **Treating "not merged by the due date" as failure.** Merge timing is outside your control; quality and engagement are the goal.

## 10. Stretch goals

- Make a **second contribution** to a different project from the shortlist.
- Review someone else's open PR in the same project (helpful reviews are valued contributions).
- Write a short "How I fixed X in Y" section in your blog or team wiki.
- If you published a gem: add a GitHub Actions matrix for Ruby 3.3, 3.4 and 4.0, and automate releases with a trusted publisher on RubyGems (verify setup docs).
