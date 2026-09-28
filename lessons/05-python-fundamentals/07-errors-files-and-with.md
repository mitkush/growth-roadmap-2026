# 07 · Errors, files and `with`

<!-- nav:top -->
[Course home](../../README.md) › [Step 5 plan](../../steps/05-python-fundamentals.md) › [Step 5 lessons](00-start-here.md) · [Glossary](../../GLOSSARY.md)
<!-- nav:end -->

## 1. In one sentence

Python raises and catches **exceptions** with `try/except/else/finally` (Ruby's `begin/rescue/else/ensure`), and uses **`with` blocks** to open and reliably close files and other resources, while `pathlib.Path` handles file paths.

## 2. Why it exists

Real programs read files, parse data and call services; things fail. You need to:

- raise errors that **say what went wrong** and can be caught specifically,
- keep the **original cause** when you convert a low-level error into a domain error,
- **always release resources** (files, connections, locks), even when an exception is raised.

Ruby solves the last one with blocks (`File.open(path) { |f| ... }`). Python solves it with `with`, which works for files, database transactions, locks, timers and anything else that needs setup and cleanup (lesson 11 shows how to write your own).

## 3. Rails analogy

| Ruby | Python |
|---|---|
| `begin ... rescue ArgumentError => e ... ensure ... end` | `try: ... except ValueError as e: ... finally: ...` |
| `rescue => e` (StandardError) | `except Exception as e:` (never bare `except:`) |
| `else` (no exception) | `else:` (same) |
| `raise ArgumentError, "bad"` | `raise ValueError("bad")` |
| `raise MyError, "x"` inside a `rescue` (Ruby keeps `cause` automatically) | `raise MyError("x") from error` (explicit chaining) |
| `class OutOfStock < StandardError; end` | `class OutOfStock(Exception): pass` |
| `ActiveRecord::RecordNotFound` | `KeyError` / `LookupError` or your own exception |
| `retry` | a loop around `try` (no `retry` keyword) |
| `File.open(p) { \|f\| f.read }` | `with open(p) as f: f.read()` |
| `File.read(p)` / `File.write(p, s)` | `Path(p).read_text()` / `Path(p).write_text(s)` |
| `Pathname.new("a") + "b"` | `Path("a") / "b"` |
| `JSON.parse(s)` / `obj.to_json` | `json.loads(s)` / `json.dumps(obj)` |
| `CSV.foreach(p, headers: true)` | `csv.DictReader(open(p))` |

Common built-in exceptions and their Ruby cousins: `ValueError` (ArgumentError for bad values), `TypeError` (wrong type), `KeyError` (Hash#fetch KeyError), `IndexError`, `FileNotFoundError` (Errno::ENOENT), `ZeroDivisionError`.

## 4. How it works

### `try` / `except` / `else` / `finally`

```python
try:
    data = json.loads(text)          # code that may fail
except json.JSONDecodeError as error:
    log.warning("bad JSON: %s", error)
    data = {}
else:
    log.info("parsed %d keys", len(data))   # runs only if no exception
finally:
    cleanup()                        # always runs, like ensure
```

Catch the **most specific** exception you can handle. Let the rest propagate.

### Your own exception hierarchy

```python
class InventoryError(Exception):
    """Base class for inventory errors: callers can catch all of them at once."""

class OutOfStock(InventoryError):
    def __init__(self, sku: str, requested: int, available: int):
        super().__init__(f"{sku}: requested {requested}, only {available} left")
        self.sku = sku
```

### Chaining with `raise ... from`

When you catch a low-level error and raise a domain error, keep the original:

```python
try:
    price = int(row["price_cents"])
except (KeyError, ValueError) as error:
    raise InvalidRow(f"row {n} has no valid price") from error
```

The traceback then shows both errors: "The above exception was the direct cause of the following exception". Ruby does this automatically via `cause`; Python makes you say it (and ruff's rule `B904` reminds you).

### `with` and context managers

```python
with open("orders.csv", newline="") as f:   # f is closed at the end of the block,
    for row in csv.DictReader(f):           # even if an exception is raised inside
        ...
```

Always pass `encoding="utf-8"` (or rely on `pathlib`'s methods with an explicit encoding) when reading text you did not create, so behaviour does not depend on the machine.

### `pathlib`

```python
from pathlib import Path

root = Path("data")
report = root / "reports" / "2026-11.csv"   # / joins paths (Pathname-style)
report.parent.mkdir(parents=True, exist_ok=True)
report.exists(), report.suffix, report.stem  # True/False, ".csv", "2026-11"
for path in root.glob("**/*.csv"): ...       # like Dir.glob
```

## 5. Minimal working example

Create `import_orders.py`. It reads a CSV, converts bad rows into a domain error with the cause kept, and writes a JSON summary:

```python
import csv
import json
from pathlib import Path


class OrderImportError(Exception):  # not "ImportError": that name is a Python built-in
    """Base class for order-import errors."""


class InvalidRow(OrderImportError):
    pass


def parse_row(line_no: int, row: dict[str, str]) -> dict[str, object]:
    try:
        return {"id": int(row["id"]), "total_cents": int(row["total_cents"])}
    except (KeyError, ValueError) as error:
        raise InvalidRow(f"line {line_no}: {row}") from error


def import_orders(csv_path: Path, out_path: Path) -> dict[str, int]:
    good, bad = [], 0
    with csv_path.open(newline="", encoding="utf-8") as f:
        for line_no, row in enumerate(csv.DictReader(f), start=2):  # line 1 is the header
            try:
                good.append(parse_row(line_no, row))
            except InvalidRow as error:
                bad += 1
                print(f"skipped {error} (cause: {error.__cause__!r})")
    summary = {"imported": len(good), "skipped": bad, "total_cents": sum(o["total_cents"] for o in good)}
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    data = Path("data")
    data.mkdir(exist_ok=True)
    (data / "orders.csv").write_text("id,total_cents\n1,1250\n2,abc\n3,4200\n", encoding="utf-8")

    print(import_orders(data / "orders.csv", data / "summary.json"))
    print((data / "summary.json").read_text())

    try:
        import_orders(data / "missing.csv", data / "x.json")
    except FileNotFoundError as error:
        print("FileNotFoundError:", error.filename)
```

```bash
uv run python import_orders.py
```

Output:

```
skipped line 3: {'id': '2', 'total_cents': 'abc'} (cause: ValueError("invalid literal for int() with base 10: 'abc'"))
{'imported': 2, 'skipped': 1, 'total_cents': 5450}
{
  "imported": 2,
  "skipped": 1,
  "total_cents": 5450
}
FileNotFoundError: data/missing.csv
```

Notice `error.__cause__`: because of `raise ... from error`, the domain error still carries the original `ValueError`.

## 6. Key terms

- **Exception**: an object representing an error; raised with `raise`, handled with `except`.
- **`try/except/else/finally`**: handle / no-error branch / always-run cleanup.
- **Exception hierarchy**: your own base class with specific subclasses.
- **Exception chaining (`raise ... from`)**: keep the original error as `__cause__`.
- **Context manager / `with`**: guaranteed setup and cleanup around a block.
- **`pathlib.Path`**: object-oriented paths; `/` joins them.
- **Encoding**: how text is turned into bytes; say `utf-8` explicitly.

## 7. Common mistakes

- **Bare `except:`**, which also catches `KeyboardInterrupt` and `SystemExit`. Use `except Exception` at most, and prefer specific types.
- **Swallowing errors** (`except Exception: pass`).
- **Losing the cause**: raising a new error inside `except` without `from error`.
- **Opening files without `with`**, so they stay open on errors.
- **Building paths with string concatenation** (`"data/" + name`); use `Path`.
- **Naming your exception like a built-in** (`ImportError`, `TimeoutError`) and shadowing it.
- **Catching too early**: handle errors where you can do something useful; let the rest propagate.

## 8. Check your understanding

1. Translate `begin ... rescue ArgumentError => e ... ensure close end` into Python.
2. When does the `else:` block of a `try` run?
3. What does `raise InvalidRow(...) from error` add to the traceback, and why is it useful?
4. Why is `with open(p) as f:` better than `f = open(p)` followed by `f.close()`?
5. How do you catch "any inventory error" but not unrelated errors?

<details>
<summary>Answers</summary>

1. `try: ... except ValueError as e: ... finally: close()`
2. Only when the `try` block completed without raising an exception.
3. It records the original exception as the cause and shows both tracebacks; you see the domain meaning and the root cause.
4. The file is closed even if an exception happens inside the block, and the code is shorter.
5. Define a base class (`InventoryError`), make specific errors subclass it, and `except InventoryError:`.

</details>

## 9. Go deeper (optional)

- The Python Tutorial: [Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html) and [Reading and Writing Files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files).
- Python docs: [`pathlib`](https://docs.python.org/3/library/pathlib.html), [`csv`](https://docs.python.org/3/library/csv.html), [`json`](https://docs.python.org/3/library/json.html).
- *Fluent Python*, 2nd ed., chapter 18 ("with, match, and else Blocks").

<!-- nav:bottom -->

---

[← 06 · Testing with pytest](06-testing-with-pytest.md) · [Step 5 lessons](00-start-here.md) · [08 · Classes and dataclasses →](08-classes-and-dataclasses.md)
<!-- nav:end -->
