# Step 5: Python Fundamentals for Rubyists

<!-- nav:top -->
[Course home](../README.md) · Step 5 of 8 · [Step 5 lessons](../lessons/05-python-fundamentals/00-start-here.md) · [Glossary](../GLOSSARY.md)
<!-- nav:end -->

| Weight | Dates | Hours |
|---|---|---|
| 15% | Mon 26 Oct - Sun 8 Nov 2026 (2 weeks) | ~20 h |

**Versions and tools:** Python 3.13 (3.14 is fine too), **uv** (Python versions, venvs, dependencies), **ruff** (lint + format), **mypy** (type checking), **pytest**.

## What you will learn this step

You will learn Python from the ground up, but at the speed of an experienced Rubyist: every lesson shows the Ruby you already know next to the Python equivalent, and spends its time on the differences that cause real bugs (explicit `return`, truthiness, default arguments, Python's very different `yield`, explicit imports). You will set up projects the modern way with uv, lint with ruff, type-check with mypy and test with pytest from day one. By the end you will have solved five practice problems and ported a Ruby utility, all with tests and CI, and you will write Python that reads like Python, not like Ruby. The lessons are in [`lessons/05-python-fundamentals/`](../lessons/05-python-fundamentals/00-start-here.md); start with the overview.

## 1. Objective

This step starts from fundamentals but moves fast. By the end of these two weeks you will be able to:

- Write idiomatic Python (not "Ruby with Python syntax") using the core data structures, comprehensions, generators, context managers, decorators and dataclasses.
- Set up a project with uv, `pyproject.toml` and a lockfile; lint and format with ruff; type-check with mypy; test with pytest.
- Explain the main differences from Ruby (truthiness, explicit `return`, mutability, `yield`, modules and imports) and avoid the common traps.
- Solve 5 specified practice problems with tests and type hints.
- Port a small Ruby utility to a Python CLI with tests and CI.

## 2. Why it matters

- Python is the main language for AI engineering (Steps 7-8): SDKs, MCP servers, eval tools and data libraries are Python-first.
- Learning the idioms early prevents slow, fragile code later. Reviewers notice un-Pythonic code quickly.
- Modern tooling (uv, ruff, type hints) is now standard in serious Python projects, and it will feel familiar coming from Bundler and RuboCop.
- Knowing two ecosystems well makes you a stronger engineer in both: you start to see which ideas are universal and which are language habits.

## 3. Day-by-day plan

Create one repo, `python-katas`, for the whole step (`uv init python-katas`, `src/` layout, `tests/`).

### Week 1 (26 Oct - 1 Nov): core language and tooling

| Day | Topic | Concrete tasks | Hours |
|---|---|---|---|
| **Mon 26 Oct** | Tooling + basics | **Read first:** [00 Start here](../lessons/05-python-fundamentals/00-start-here.md), [01 Tooling](../lessons/05-python-fundamentals/01-tooling-uv-ruff-mypy.md), [02 Values and truthiness](../lessons/05-python-fundamentals/02-values-and-truthiness.md).<br>1. Install uv; `uv python install 3.13`; `uv init --package python-katas`; `uv add --dev pytest ruff mypy`. 2. In the REPL: numbers, strings, f-strings, `None`, truthiness (`0`, `""`, `[]`, `{}` are falsy). 3. Write the first test `tests/test_basics.py` and run `uv run pytest`. | 1.5 |
| **Tue 27 Oct** | Collections | **Read first:** [03 Collections and comprehensions](../lessons/05-python-fundamentals/03-collections-and-comprehensions.md).<br>1. `list`, `tuple`, `dict`, `set`: create, slice, copy, mutate. 2. Rewrite 10 Ruby one-liners you use often (`map`, `select`, `reject`, `group_by`, `each_with_object`, `tally`, `sort_by`, `zip`, `each_with_index`, `sum`) as comprehensions and built-ins. 3. Use `collections.Counter` and `defaultdict`. | 1.5 |
| **Wed 28 Oct** | Functions | **Read first:** [04 Functions and closures](../lessons/05-python-fundamentals/04-functions-and-closures.md).<br>1. Positional, keyword, default, keyword-only (`*`), `*args`, `**kwargs`. 2. Reproduce the **mutable default argument** bug and fix it. 3. Closures, `nonlocal`, `lambda`, passing functions as arguments; `functools.partial` and `lru_cache`. | 1.25 |
| **Thu 29 Oct** | Modules, packages, pytest | **Read first:** [05 Modules and imports](../lessons/05-python-fundamentals/05-modules-packages-and-imports.md), [06 Testing with pytest](../lessons/05-python-fundamentals/06-testing-with-pytest.md).<br>1. Split code into `src/katas/<module>.py`; understand `__init__.py`, absolute imports and `if __name__ == "__main__":`. 2. pytest: fixtures (like `let`), `@pytest.mark.parametrize` (like shared examples with data), `pytest.raises`, `tmp_path`. | 1.25 |
| **Fri 30 Oct** | Errors, files, `with` | **Read first:** [07 Errors, files and `with`](../lessons/05-python-fundamentals/07-errors-files-and-with.md).<br>1. `try/except/else/finally`, custom exception classes, `raise ... from ...`. 2. `pathlib.Path`, `open()` in a `with` block, `json` and `csv` modules. 3. Send the weekly update. | 1 |
| **Sat 31 Oct** | OOP + problems 1-2 | **Read first:** [08 Classes and dataclasses](../lessons/05-python-fundamentals/08-classes-and-dataclasses.md).<br>1. Classes, `__init__`, `__repr__`, `__eq__`, `@property`, `@classmethod`, `@staticmethod`, inheritance and `super()`. 2. `@dataclass` (and `frozen=True`, `field(default_factory=...)`). 3. Solve **Problem 1** and **Problem 2** with tests. | 2.5 |
| **Sun 1 Nov** | Tooling config + review | **Read first:** [01 Tooling](../lessons/05-python-fundamentals/01-tooling-uv-ruff-mypy.md), the ruff and mypy sections (review).<br>1. Configure ruff (`[tool.ruff]` with rules `E`, `F`, `I`, `B`, `UP`, `SIM`) and `ruff format`. 2. Run `mypy src` and fix errors. 3. Fill in your own notes column in the translation table below. | 1 |
| | | **Week 1 total** | **10** |

### Week 2 (2 Nov - 8 Nov): idioms, types, practice and the port

| Day | Topic | Concrete tasks | Hours |
|---|---|---|---|
| **Mon 2 Nov** | Iterators + generators | **Read first:** [09 Iterators and generators](../lessons/05-python-fundamentals/09-iterators-and-generators.md).<br>1. The iterator protocol (`__iter__`, `__next__`); generator functions and expressions; `itertools` (`islice`, `groupby`, `chain`, `batched` on 3.12+). 2. Note: Python `yield` makes a **generator**; it is not Ruby's `yield` to a block. 3. Start **Problem 5**. | 1.5 |
| **Tue 3 Nov** | Type hints | **Read first:** [10 Type hints and mypy](../lessons/05-python-fundamentals/10-type-hints-and-mypy.md).<br>1. Annotate all katas: `list[str]`, `dict[str, int]`, `X \| None`, `Callable`, `Iterator`, `TypedDict`, `Literal`, `Protocol`. 2. Turn on `mypy --strict` for `src/` and fix errors. 3. Finish Problem 5. | 1.5 |
| **Wed 4 Nov** | Decorators + context managers | **Read first:** [11 Decorators and context managers](../lessons/05-python-fundamentals/11-decorators-and-context-managers.md).<br>1. Write a timing decorator with `functools.wraps`. 2. Write a context manager with a class (`__enter__`/`__exit__`) and with `contextlib.contextmanager`. 3. Solve **Problem 3**. | 1.25 |
| **Thu 5 Nov** | `match`, enums, problem 4 | **Read first:** [12 Pattern matching and enums](../lessons/05-python-fundamentals/12-pattern-matching-and-enums.md).<br>1. Structural pattern matching (`match/case`) on dicts and dataclasses. 2. `enum.Enum` / `StrEnum` instead of Ruby symbols. 3. Solve **Problem 4**. | 1.25 |
| **Fri 6 Nov** | Port: plan | **Read first:** [05 Modules and imports](../lessons/05-python-fundamentals/05-modules-packages-and-imports.md), the `argparse` and entry-point sections (review).<br>1. Choose the Ruby utility (see lab). 2. List its behaviours as test cases. 3. Build the CLI skeleton with `argparse` and a `[project.scripts]` entry point. 4. Send the weekly update. | 1 |
| **Sat 7 Nov** | Port: build + CI | **Read first:** [06 Testing with pytest](../lessons/05-python-fundamentals/06-testing-with-pytest.md) (review) and the CI workflow in [Step 6 lesson 12](../lessons/06-applied-python/12-github-actions-ci.md).<br>1. Implement the port with tests for every behaviour. 2. Add GitHub Actions: `astral-sh/setup-uv`, then `uv run ruff check`, `uv run ruff format --check`, `uv run mypy src`, `uv run pytest`. | 2.5 |
| **Sun 8 Nov** | Consolidate + proof | **Read first:** [00 Start here](../lessons/05-python-fundamentals/00-start-here.md), "The mental model" table (review, then write your own `NOTES.md`).<br>1. Repo README with a table of problems and how to run them. 2. Self-check questions. 3. Write "10 things that surprised me coming from Ruby" in `NOTES.md`. | 1 |
| | | **Week 2 total** | **10** |

## 4. Topic checklist

### 4.1 Ruby-to-Python translation table

| Concept | Ruby | Python | Watch out |
|---|---|---|---|
| Version manager | rbenv / asdf / `.ruby-version` | `uv python install`, `.python-version` | |
| Dependencies | Bundler, `Gemfile`, `Gemfile.lock` | uv, `pyproject.toml`, `uv.lock` | `pip` + `requirements.txt` is the older way; still common in docs. |
| Run in project env | `bundle exec rspec` | `uv run pytest` | uv creates `.venv` automatically. |
| Package / registry | gem / RubyGems | package / PyPI | Import name can differ from package name. |
| Lint + format | RuboCop / Standard | ruff (`ruff check`, `ruff format`) | |
| Types | RBS + Steep, Sorbet | type hints + mypy (or pyright) | Hints are not enforced at runtime. |
| Tests | RSpec / Minitest | pytest | Plain `assert`; no `describe` needed. |
| `let` / `before` | `let(:user) { ... }` | `@pytest.fixture` | Fixture scope: function, module, session. |
| Shared examples | `it_behaves_like` | `@pytest.mark.parametrize` | |
| Expect error | `expect { }.to raise_error(X)` | `with pytest.raises(X):` | |
| Debugger | `binding.irb`, `debug` gem | `breakpoint()` (pdb) | |
| Nothing | `nil` | `None` | Compare with `is None`, not `== None`. |
| Truthiness | only `nil` and `false` are falsy | `0`, `""`, `[]`, `{}`, `None`, `False` are falsy | Very common bug source. |
| Symbols | `:active` | strings or `Enum` | |
| Array / Hash / Set | `[]`, `{}`, `Set` | `list`, `dict`, `set`; `tuple` for immutable | Dicts keep insertion order (like Ruby). |
| Blocks + Enumerable | `users.select(&:active?).map(&:email)` | `[u.email for u in users if u.active]` | Prefer comprehensions over `map`/`filter` with `lambda`. |
| Lazy enumerator | `(1..).lazy.map { }.first(5)` | generator expression + `itertools.islice` | |
| `yield` | calls the block | turns the function into a generator | Different meaning entirely. |
| Block for resources | `File.open(p) { \|f\| ... }` | `with open(p) as f:` | Context managers. |
| Lambdas / procs | `->(x) { x * 2 }` | `lambda x: x * 2` | Python lambdas are one expression only; use `def` otherwise. |
| Implicit return | last expression is returned | must write `return` | Missing `return` gives `None`. |
| Module as namespace | `module Billing` | a module file / package directory | |
| Mixins | `include Comparable` | multiple inheritance, `functools.total_ordering`, `Protocol` | |
| Accessors | `attr_accessor :name` | plain attributes, `@property`, `@dataclass` | No getters/setters by default. |
| Value objects | `Struct`, `Data.define` | `@dataclass(frozen=True)`, `NamedTuple` | |
| String repr | `to_s` / `inspect` | `__str__` / `__repr__` | |
| Metaprogramming | `method_missing`, `define_method` | `__getattr__`, `setattr`, decorators | Use much less than in Ruby. |
| Visibility | `private` | `_name` convention | Not enforced. |
| Exceptions | `begin/rescue/ensure`, `raise` | `try/except/finally`, `raise` | `except Exception`, never bare `except:`. |
| `case/when` | `case x in {status:}` | `match x: case {"status": s}:` | |
| Safe navigation | `user&.email` | `user.email if user else None` | No built-in operator. |
| Interpolation | `"Hi #{name}"` | `f"Hi {name}"` | |
| Imports | `require`, autoloading (Zeitwerk) | explicit `import` | No autoloading. |
| Tasks | Rake | `[project.scripts]`, Makefile, or `uv run python -m ...` | |
| GVL | GVL in CRuby | GIL in CPython | Free-threaded builds exist (3.13+) but are optional. |

### 4.2 Checklist

- [ ] uv project workflow: can create, add dependencies, lock, run and reproduce a project on a clean machine.
- [ ] Core types and truthiness: can predict the output of truthiness and equality (`==` vs `is`) checks.
- [ ] Collections: can choose between list, tuple, dict and set and explain mutability and copying (shallow vs deep).
- [ ] Comprehensions: can write list, dict, set comprehensions and generator expressions, and knows when a loop is clearer.
- [ ] Functions: can use keyword-only args, `*args/**kwargs`, closures, and avoid mutable defaults.
- [ ] Modules and packages: can structure a `src/` package and fix circular import problems.
- [ ] OOP: can write classes with dunder methods and properties, and use dataclasses.
- [ ] Iterators and generators: can write a generator that processes a large file in constant memory.
- [ ] Decorators and context managers: can write both from scratch.
- [ ] Exceptions: can define an exception hierarchy and chain exceptions.
- [ ] Type hints: can type a module to pass `mypy --strict`, including `Protocol` and `TypedDict`.
- [ ] pytest: can use fixtures, parametrize, `tmp_path`, `monkeypatch` and `pytest.raises`.
- [ ] ruff: can configure rules and fix or suppress findings deliberately.
- [ ] Nice to have: `match` statements and `enum`.

## 5. Hands-on lab

### 5.1 The 5 practice problems

Each problem lives in `src/katas/pN_<name>.py` with tests in `tests/`. All must pass `ruff`, `mypy --strict` and `pytest`.

| # | Problem | Specification | Skills practised |
|---|---|---|---|
| **P1** | **Rails log analyser** | Read a Rails `production.log` (create a 5,000-line sample). For each `Controller#action`, output request count, p50/p95 duration and error rate (5xx), sorted by total time. Print a table and `--json` output. | regex, `dict`/`Counter`, `statistics.quantiles`, file I/O, `argparse` |
| **P2** | **Bookshop inventory** | Model `Book`, `Inventory` and pricing rules (percentage discount, buy-2-get-1). `Inventory` supports `add`, `remove` (raises `OutOfStock`), `total_value()`, iteration and `len()`. Pricing rules follow a `Protocol`. | classes, dataclasses, dunder methods, custom exceptions, `Protocol` |
| **P3** | **Token-bucket rate limiter** | `TokenBucket(capacity, refill_rate, clock=time.monotonic)`, `allow() -> bool`. Plus a `@rate_limited(bucket)` decorator that raises `RateLimited`. Tests use a fake clock (no `sleep`). | classes, closures, decorators, dependency injection, testing time |
| **P4** | **Config deep-merge + flatten** | `deep_merge(base, override)` for nested dicts (lists replaced, not merged) and `flatten({"db": {"host": "x"}}) == {"db.host": "x"}` and back (`unflatten`). Handle a `None` override as "delete key". | recursion, dict comprehensions, `match`, `TypedDict`, edge-case tests |
| **P5** | **Streaming top-K** | Read a text file of any size line by line and return the top K words (case-insensitive, ignoring a stop-word list) using constant memory for the input. Include a `timed()` context manager that reports duration. Test with a generated 200 MB file. | generators, `heapq.nlargest`, `Counter`, context managers |

### 5.2 Port a Ruby utility

Port a small Ruby script or Rake task **you wrote at work** (100-300 lines), removing anything confidential. If you have none, port this:

> **`lockfile-report`**: read a `Gemfile.lock`, and print (a) gems grouped by source (`GEM`, `GIT`, `PATH`), (b) the dependency tree depth for each top-level gem, and (c) gems pinned to Git refs. Support `--format table|json`.

**Acceptance criteria**
- [ ] P1-P5 each have at least 5 tests, including edge cases (empty input, invalid input).
- [ ] The port has a test for every behaviour of the Ruby original (write the list first) and a CLI entry point (`uv run lockfile-report path/to/Gemfile.lock`).
- [ ] `ruff check`, `ruff format --check`, `mypy --strict src` and `pytest` all pass in GitHub Actions.
- [ ] No Ruby-isms left: no manual index loops where `enumerate`/`zip` fit, no `== None`, no mutable defaults (ruff rule `B006` helps).
- [ ] `NOTES.md` lists 10 differences from Ruby that surprised you.

## 6. Deliverable / proof of completion

1. **Link to the `python-katas` repo** with a green GitHub Actions run.
2. The **README table** listing P1-P5 and the port, with commands to run each.
3. **Side-by-side snippet** (Ruby original vs Python port) of the most interesting function, in the weekly update.

## 7. Curated resources

1. **Lessons for this step**: [`lessons/05-python-fundamentals/`](../lessons/05-python-fundamentals/00-start-here.md) (read these first).
2. **The Python Tutorial** (official): https://docs.python.org/3/tutorial/ (sections 3-9; skim what you already know).
3. **Luciano Ramalho, *Fluent Python*, 2nd edition** (O'Reilly, 2022): ch. 2-3 (sequences, dicts), ch. 5 (data class builders), ch. 7 and 9 (functions, decorators, closures), ch. 17 (iterators and generators).
4. **uv docs**: https://docs.astral.sh/uv/ (Projects guide and "Working on projects").
5. **ruff docs**: https://docs.astral.sh/ruff/
6. **pytest docs: Getting started, fixtures, parametrize**: https://docs.pytest.org/en/stable/
7. **mypy: type hints cheat sheet**: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
8. **Exercism Python track** (extra practice with mentoring): https://exercism.org/tracks/python

## 8. Self-check questions

1. Why does `def add(item, items=[])` behave differently from Ruby's `def add(item, items = [])`? How do you fix it?
2. When is a generator better than a list comprehension, and what happens if you iterate a generator twice?
3. What is the difference between `==` and `is`, and why must you use `is None`?
4. How would you express Ruby's `File.open(path) { |f| ... }` pattern for your own resource (e.g. a DB transaction) in Python?
5. What does `@dataclass(frozen=True)` give you, and when would you choose `NamedTuple` instead?
6. How do `pyproject.toml` and `uv.lock` compare with `Gemfile` and `Gemfile.lock`? What should be committed for an app vs a library?
7. Type hints are not checked at runtime. So why use them, and where would you add runtime validation?
8. Write the Python version of `orders.group_by(&:status).transform_values(&:count)` in two different ways. Which is more readable?
9. How does Python's import system differ from Rails autoloading, and what problems does that cause (and prevent)?
10. When should a class implement `__eq__` and `__hash__` together?

## 9. Common pitfalls

- **Writing Ruby in Python**: long `map(lambda ...)` chains, manual index loops, getters/setters.
- **Forgetting `return`**, which silently returns `None`.
- **Relying on Ruby truthiness**: `if count:` is `False` when `count == 0`.
- **Mutable default arguments** and shared mutable class attributes.
- **Installing packages globally with `pip`** instead of inside the project environment.
- **Catching bare `except:`** (also catches `KeyboardInterrupt` and `SystemExit`).
- **Using `Any` everywhere** to make mypy quiet, which removes the value of types.
- **Confusing Python `yield` with Ruby `yield`.**

## 10. Stretch goals

- Solve 10 more Exercism Python exercises and ask for mentor feedback on 2.
- Rewrite P1 with `polars` or `pandas` and compare code length and speed.
- Try **pyright** (or Astral's `ty` type checker, verify its status) alongside mypy and compare the errors.
- Add property-based tests to P4 with **Hypothesis**.
- Package the port and publish it to TestPyPI.

<!-- nav:bottom -->

---

[← Step 4: Open-Source Contribution to the Ruby Ecosystem](04-open-source-contribution.md) · [Step 5 lessons](../lessons/05-python-fundamentals/00-start-here.md) · [Step 6: Applied Python: FastAPI Service with Tests & CI →](06-applied-python.md)
<!-- nav:end -->
