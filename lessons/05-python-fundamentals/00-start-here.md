# Step 5 lessons: start here

<!-- nav:top -->
[Course home](../../README.md) › [Step 5 plan](../../steps/05-python-fundamentals.md) · [Glossary](../../GLOSSARY.md)
<!-- nav:end -->

These lessons teach Python from the fundamentals, **for someone who already programs well in Ruby**. Every lesson compares Python with Ruby, so you learn the differences rather than re-learning programming. They move fast on what is the same, and slow down on what trips Rubyists up.

**How to use this folder:** every day in [the Step 5 plan](../../steps/05-python-fundamentals.md) starts with **"Read first:"** links. Read the lesson (20-40 minutes), type and run its example yourself (do not copy-paste; typing builds the habits), then do the day's tasks.

## The lessons

| # | Lesson | Day |
|---|---|---|
| 01 | [Tooling: uv, ruff, mypy](01-tooling-uv-ruff-mypy.md) | Mon 26 Oct |
| 02 | [Values, strings, truthiness and equality](02-values-and-truthiness.md) | Mon 26 Oct |
| 03 | [Collections and comprehensions](03-collections-and-comprehensions.md) | Tue 27 Oct |
| 04 | [Functions, arguments and closures](04-functions-and-closures.md) | Wed 28 Oct |
| 05 | [Modules, packages and imports](05-modules-packages-and-imports.md) | Thu 29 Oct |
| 06 | [Testing with pytest](06-testing-with-pytest.md) | Thu 29 Oct |
| 07 | [Errors, files and `with`](07-errors-files-and-with.md) | Fri 30 Oct |
| 08 | [Classes and dataclasses](08-classes-and-dataclasses.md) | Sat 31 Oct |
| 09 | [Iterators and generators](09-iterators-and-generators.md) | Mon 2 Nov |
| 10 | [Type hints and mypy](10-type-hints-and-mypy.md) | Tue 3 Nov |
| 11 | [Decorators and context managers](11-decorators-and-context-managers.md) | Wed 4 Nov |
| 12 | [Pattern matching and enums](12-pattern-matching-and-enums.md) | Thu 5 Nov |

The [Ruby-to-Python translation table](../../steps/05-python-fundamentals.md#41-ruby-to-python-translation-table) in the step plan is your quick reference; these lessons explain each row properly.

## The mental model: what is really different

Most of Python will feel familiar. These are the differences that matter most, in order of how often they cause bugs for Rubyists:

| # | Ruby habit | Python reality | Lesson |
|---|---|---|---|
| 1 | The last expression is returned | You must write `return`; otherwise the function returns `None` | [04](04-functions-and-closures.md) |
| 2 | Only `nil` and `false` are falsy | `0`, `""`, `[]`, `{}` and `None` are also falsy | [02](02-values-and-truthiness.md) |
| 3 | Blocks everywhere (`map { }`, `each { }`) | Comprehensions and `for` loops; lambdas are one expression only | [03](03-collections-and-comprehensions.md), [04](04-functions-and-closures.md) |
| 4 | `yield` calls the block | `yield` turns a function into a **generator** | [09](09-iterators-and-generators.md) |
| 5 | Autoloading (Zeitwerk) | Every name must be imported explicitly | [05](05-modules-packages-and-imports.md) |
| 6 | `File.open { }` closes the file | `with open(...) as f:` does the same, and works for any resource | [07](07-errors-files-and-with.md) |
| 7 | Default arguments are evaluated per call | Defaults are evaluated **once**, when the function is defined | [04](04-functions-and-closures.md) |
| 8 | Methods are public unless `private` | Nothing is enforced; `_name` means "internal, please do not use" | [08](08-classes-and-dataclasses.md) |
| 9 | `method_missing`, open classes, DSLs | Used far less; explicit code is the norm | [08](08-classes-and-dataclasses.md) |
| 10 | Indentation is style | **Indentation is syntax**: it defines blocks (no `end`) | [02](02-values-and-truthiness.md) |

## The Zen of Python in one table

Python's culture values explicitness. Run `python -c "import this"` to see its design principles. The ones that explain most Python code:

| Principle | What it means in practice |
|---|---|
| Explicit is better than implicit. | Explicit imports, explicit `return`, explicit `self`. |
| Readability counts. | Prefer a clear loop to a clever one-liner. |
| There should be one obvious way to do it. | Less "there's more than one way" than Ruby; linters enforce idioms. |
| Errors should never pass silently. | Catch specific exceptions; do not swallow errors. |

## Glossary

| Term | Meaning | Lesson |
|---|---|---|
| **Interpreter** | The program that runs Python code (`python3.13`), like `ruby`. | [01](01-tooling-uv-ruff-mypy.md) |
| **REPL** | The interactive prompt (`python` or `uv run python`), like `irb`. | [01](01-tooling-uv-ruff-mypy.md) |
| **Virtual environment (venv)** | A project-local folder (`.venv`) with its own Python and packages, like a Bundler-managed gem set per project. | [01](01-tooling-uv-ruff-mypy.md) |
| **uv** | A fast tool that manages Python versions, virtual environments, dependencies and lockfiles (rbenv + Bundler in one). | [01](01-tooling-uv-ruff-mypy.md) |
| **`pyproject.toml` / `uv.lock`** | Project metadata and dependencies / exact resolved versions (like `Gemfile` / `Gemfile.lock`). | [01](01-tooling-uv-ruff-mypy.md) |
| **PyPI** | The Python package registry, like RubyGems.org. | [01](01-tooling-uv-ruff-mypy.md) |
| **ruff** | Linter and formatter (RuboCop + a formatter). | [01](01-tooling-uv-ruff-mypy.md) |
| **mypy** | Static type checker (like Sorbet or Steep). | [10](10-type-hints-and-mypy.md) |
| **Truthiness** | Whether a value counts as true in `if`. | [02](02-values-and-truthiness.md) |
| **Identity vs equality** | `is` (same object) vs `==` (equal value). | [02](02-values-and-truthiness.md) |
| **Mutable / immutable** | Can be changed in place (list, dict) or not (str, tuple, int). | [02](02-values-and-truthiness.md) |
| **f-string** | `f"Hi {name}"`: string interpolation. | [02](02-values-and-truthiness.md) |
| **list / tuple / dict / set** | Array / frozen array / Hash / Set. | [03](03-collections-and-comprehensions.md) |
| **Slicing** | `items[1:3]`, `text[::-1]`: taking parts of sequences. | [03](03-collections-and-comprehensions.md) |
| **Comprehension** | `[x * 2 for x in xs if x > 0]`: Python's `map` + `select` in one expression. | [03](03-collections-and-comprehensions.md) |
| **Positional / keyword argument** | Passed by position / by name (`f(1, limit=5)`). | [04](04-functions-and-closures.md) |
| **`*args` / `**kwargs`** | Collect extra positional / keyword arguments (Ruby's `*args` / `**opts`). | [04](04-functions-and-closures.md) |
| **Closure** | A function that remembers variables from where it was defined. | [04](04-functions-and-closures.md) |
| **lambda** | A one-expression anonymous function. | [04](04-functions-and-closures.md) |
| **Module / package** | A `.py` file / a folder of modules. | [05](05-modules-packages-and-imports.md) |
| **`__name__ == "__main__"`** | True when a file is run directly, not imported (like `if __FILE__ == $0`). | [05](05-modules-packages-and-imports.md) |
| **`src` layout** | Keeping package code under `src/` so tests import the installed package. | [05](05-modules-packages-and-imports.md) |
| **pytest / fixture / parametrize** | Test runner / reusable setup (like `let`) / run one test with many inputs. | [06](06-testing-with-pytest.md) |
| **Exception / `raise ... from`** | Error object / raising a new error while keeping the original as its cause. | [07](07-errors-files-and-with.md) |
| **Context manager / `with`** | An object that sets up and tears down a resource around a block. | [07](07-errors-files-and-with.md), [11](11-decorators-and-context-managers.md) |
| **`pathlib.Path`** | Object-oriented file paths (like Ruby's `Pathname`). | [07](07-errors-files-and-with.md) |
| **`self`** | The instance, passed explicitly as the first parameter of methods. | [08](08-classes-and-dataclasses.md) |
| **Dunder method** | "Double underscore" methods such as `__init__`, `__repr__`, `__eq__` that hook into language features. | [08](08-classes-and-dataclasses.md) |
| **`@property`** | A method used like an attribute (like a Ruby reader method). | [08](08-classes-and-dataclasses.md) |
| **Dataclass** | `@dataclass`: generates `__init__`, `__repr__`, `__eq__` from fields (like `Struct` / `Data.define`). | [08](08-classes-and-dataclasses.md) |
| **Iterator / iterable** | An object you can loop over / an object that produces an iterator. | [09](09-iterators-and-generators.md) |
| **Generator** | A function with `yield` that produces values lazily (like a Ruby `Enumerator`). | [09](09-iterators-and-generators.md) |
| **Type hint / annotation** | `def f(x: int) -> str:`, optional types checked by tools, not at runtime. | [10](10-type-hints-and-mypy.md) |
| **`Protocol`** | A type describing "anything with these methods" (duck typing, checked statically). | [10](10-type-hints-and-mypy.md) |
| **`TypedDict`** | A type for dicts with known keys. | [10](10-type-hints-and-mypy.md) |
| **Decorator** | `@something` above a function: a function that wraps another function. | [11](11-decorators-and-context-managers.md) |
| **Structural pattern matching** | `match value: case {...}:` (like Ruby's `case ... in`). | [12](12-pattern-matching-and-enums.md) |
| **Enum** | A fixed set of named constants (instead of Ruby symbols). | [12](12-pattern-matching-and-enums.md) |

<!-- nav:bottom -->

---

[← Step 4 lessons](../04-open-source/00-start-here.md) · [Step 5 plan](../../steps/05-python-fundamentals.md) · [First lesson: 01 · Tooling: uv, ruff and mypy →](01-tooling-uv-ruff-mypy.md) · [Step 6 lessons →](../06-applied-python/00-start-here.md)
<!-- nav:end -->
