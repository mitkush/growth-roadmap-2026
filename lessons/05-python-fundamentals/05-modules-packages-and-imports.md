# 05 · Modules, packages and imports

<!-- nav:top -->
[Course home](../../README.md) › [Step 5 plan](../../steps/05-python-fundamentals.md) › [Step 5 lessons](00-start-here.md) · [Glossary](../../GLOSSARY.md)
<!-- nav:end -->

## 1. In one sentence

Every `.py` file is a **module**, a folder of modules is a **package**, and nothing is loaded automatically: each file **imports** exactly the names it uses, which replaces Rails autoloading and Ruby's `require`.

## 2. Why it exists

In Rails you rarely write `require`: Zeitwerk autoloads `app/models/order.rb` when you first mention `Order`. Python has no autoloading. That feels verbose at first, but it has benefits you will come to like:

- Every file says **where each name comes from**; you can read a file on its own.
- Tools (ruff, mypy, your editor) know exactly what exists.
- There are no load-order surprises.

The trade-offs to learn: how to lay out a project so imports work, the `__name__ == "__main__"` idiom, and how to avoid **circular imports**.

## 3. Rails analogy

| Ruby / Rails | Python |
|---|---|
| A file `lib/pricing.rb` defining `module Pricing` | A file `pricing.py`: the file **is** the module |
| A folder `lib/katas/` with files | A package folder `katas/` (optionally with `__init__.py`) |
| `require "json"` / `require_relative "pricing"` | `import json` / `from katas import pricing` |
| Zeitwerk autoloading | None: explicit imports everywhere |
| `Katas::Pricing.total` | `from katas.pricing import total` then `total(...)` |
| `if __FILE__ == $PROGRAM_NAME` | `if __name__ == "__main__":` |
| `exe/katas` in a gem (with `OptionParser`) | `[project.scripts]` entry point (with `argparse`) |
| `ruby -Ilib script.rb` | `uv run python -m katas.cli` (run a module by name) |

## 4. How it works

### The three import forms

```python
import json                          # the module; use json.dumps(...)
from pathlib import Path             # one name from a module; use Path(...)
from katas.pricing import total as price_total   # rename on import (for clashes)
```

Avoid `from module import *`: it hides where names come from (ruff flags it).

### Where Python looks for modules

When you write `import katas`, Python searches a list of folders (`sys.path`): the folder of the script you ran, the installed packages in `.venv`, and the standard library. With uv's `--package` layout, your own package is **installed** into `.venv` in editable mode, so `import katas` works from anywhere in the project, including tests.

### The `src` layout

```
python-katas/
├── pyproject.toml
├── src/
│   └── katas/              # the package (import katas)
│       ├── __init__.py     # marks the package; runs on import; often empty
│       ├── pricing.py      # module katas.pricing
│       └── cli.py          # module katas.cli
└── tests/
    └── test_pricing.py     # from katas.pricing import total
```

Putting the package under `src/` means tests import the **installed** package, not whatever happens to be in the current folder: it catches packaging mistakes early. `uv init --package` creates this layout for you.

### `__name__ == "__main__"`

When Python runs a file directly, that module's `__name__` is `"__main__"`; when the file is imported, `__name__` is its module name (`"katas.cli"`). So:

```python
def main() -> None:
    ...

if __name__ == "__main__":   # only when run as a script, not when imported by tests
    main()
```

### Command-line tools with `argparse`

`argparse` (standard library) parses `sys.argv`, generates `--help`, and validates types, like Ruby's `OptionParser`. To install a command, add an entry point:

```toml
[project.scripts]
katas = "katas.cli:main"   # command name = "module:function"
```

After `uv sync`, `uv run katas --help` works.

### Circular imports

If `a.py` imports `b.py` and `b.py` imports `a.py` at the top, one of them sees a half-initialised module and fails with `ImportError: cannot import name ...`. Fixes, in order of preference: move the shared code into a third module; import inside the function that needs it; rethink the dependency (often a sign of a missing boundary, as in Step 3).

## 5. Minimal working example

Create these files (the `src` layout above). The package here is called `katas`; if you created your project with `uv init --package python-katas`, uv named the package folder `src/python_katas/`, so either rename it to `katas` (and update `[project.scripts]`) or use `python_katas` in the imports below.

Create `src/katas/__init__.py`:

```python
"""Small Python exercises for Rubyists."""
```

Create `src/katas/pricing.py`:

```python
"""Pricing helpers. Amounts are integer cents, as in a Rails app."""

VAT_RATE = 0.20


def total_cents(unit_cents: int, quantity: int, *, with_vat: bool = False) -> int:
    subtotal = unit_cents * quantity
    return round(subtotal * (1 + VAT_RATE)) if with_vat else subtotal


def format_cents(cents: int) -> str:
    return f"£{cents / 100:,.2f}"
```

Create `src/katas/cli.py`:

```python
import argparse

from katas.pricing import format_cents, total_cents


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="katas", description="Price calculator")
    parser.add_argument("unit_cents", type=int, help="price of one item in cents")
    parser.add_argument("quantity", type=int, help="number of items")
    parser.add_argument("--vat", action="store_true", help="add 20%% VAT")
    args = parser.parse_args(argv)
    print(format_cents(total_cents(args.unit_cents, args.quantity, with_vat=args.vat)))


if __name__ == "__main__":
    main()
```

Run the module by name (the `-m` flag runs `katas/cli.py` as `__main__`):

```bash
uv run python -m katas.cli --help
```

```
usage: katas [-h] [--vat] unit_cents quantity

Price calculator

positional arguments:
  unit_cents  price of one item in cents
  quantity    number of items

options:
  -h, --help  show this help message and exit
  --vat       add 20% VAT
```

```bash
uv run python -m katas.cli 1250 3 --vat
```

```
£45.00
```

And a bad argument, handled by `argparse` for free:

```bash
uv run python -m katas.cli twelve 3
```

```
usage: katas [-h] [--vat] unit_cents quantity
katas: error: argument unit_cents: invalid int value: 'twelve'
```

Add `katas = "katas.cli:main"` under `[project.scripts]` in `pyproject.toml`, run `uv sync`, and the same tool is available as `uv run katas 1250 3`.

## 6. Key terms

- **Module**: one `.py` file.
- **Package**: a folder of modules (with `__init__.py` for a regular package).
- **`import` / `from ... import`**: bring a module / specific names into scope.
- **`sys.path`**: the folders Python searches for imports.
- **`src` layout**: package code under `src/`, installed in editable mode.
- **`__name__ == "__main__"`**: true when the file is run directly.
- **`python -m`**: run a module by its dotted name.
- **Entry point (`[project.scripts]`)**: installs a command that calls a function.
- **Circular import**: two modules importing each other at load time.

## 7. Common mistakes

- **Naming your file like a standard library module** (`json.py`, `random.py`, `re.py`). It shadows the real module and breaks imports in confusing ways.
- **Running `python src/katas/cli.py` directly.** Relative paths and imports then behave differently; use `python -m katas.cli`.
- **`from x import *`.**
- **Putting logic at module top level** that runs on import (database connections, network calls). Put it in functions.
- **Circular imports** between modules that should have a clearer boundary.
- **Relative imports everywhere** (`from ..utils import x`); prefer absolute imports (`from katas.utils import x`).

## 8. Check your understanding

1. What is the Python equivalent of `if __FILE__ == $PROGRAM_NAME`, and why is it useful for tests?
2. Why does the `src` layout make tests more trustworthy?
3. A teammate creates `tests/json.py` and suddenly `import json` fails in other tests. Why?
4. How do you turn `katas.cli:main` into a command called `katas`?
5. Module `orders.py` imports `customers.py`, which imports `orders.py`. What error do you expect, and how would you fix it?

<details>
<summary>Answers</summary>

1. `if __name__ == "__main__":`. Tests can import the module (to test `main` or other functions) without triggering the script's behaviour.
2. Tests import the installed package, exactly as users will, instead of accidentally importing files from the current folder.
3. Their `json.py` is found first on the import path and shadows the standard library `json` module.
4. Add `katas = "katas.cli:main"` under `[project.scripts]` in `pyproject.toml` and run `uv sync`.
5. An `ImportError` (cannot import name ... partially initialised module). Move the shared code to a third module, import inside a function, or remove the two-way dependency.

</details>

## 9. Go deeper (optional)

- The Python Tutorial: [Modules](https://docs.python.org/3/tutorial/modules.html).
- Python docs: [`argparse` tutorial](https://docs.python.org/3/howto/argparse.html).
- uv docs: [Creating projects](https://docs.astral.sh/uv/concepts/projects/init/) (application vs packaged application layouts).

<!-- nav:bottom -->

---

[← 04 · Functions, arguments and closures](04-functions-and-closures.md) · [Step 5 lessons](00-start-here.md) · [06 · Testing with pytest →](06-testing-with-pytest.md)
<!-- nav:end -->
