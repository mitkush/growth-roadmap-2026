# 10 · Type hints and mypy

## 1. In one sentence

**Type hints** (`def total(prices: list[int]) -> int:`) describe what types a function expects and returns; Python **ignores them at runtime**, but **mypy** (and your editor) checks them before you run anything, catching a whole class of bugs early.

## 2. Why it exists

Ruby has optional typing too (RBS with Steep, or Sorbet), but most Rails code is untyped. In Python, type hints are mainstream: FastAPI and Pydantic (Step 6) **use them at runtime** to validate requests, the Anthropic and MCP SDKs are fully typed, and your editor's autocomplete depends on them.

Type hints help you:

- catch `None` bugs ("`Optional[str]` has no attribute `upper`") before production,
- document what a function takes and returns without extra comments,
- refactor safely: rename a field and mypy lists every place that breaks,
- get precise autocomplete in the editor.

## 3. Rails analogy

| Ruby (Sorbet / RBS) | Python |
|---|---|
| `sig { params(x: Integer).returns(String) }` | `def f(x: int) -> str:` |
| `T.nilable(String)` | `str \| None` |
| `T::Array[Integer]` / `T::Hash[String, Integer]` | `list[int]` / `dict[str, int]` |
| `T.any(Integer, String)` | `int \| str` |
| `T.untyped` | `Any` (avoid) |
| An interface / duck type | `typing.Protocol` |
| A hash with known keys (`T::Struct` is closer to a dataclass) | `typing.TypedDict` |
| `srb tc` in CI | `mypy --strict src` in CI |
| Types are not checked at runtime by default | Same: hints are **not** enforced at runtime |

## 4. How it works

### The everyday annotations

```python
def find_order(order_id: int) -> Order | None: ...       # may return None
def totals(orders: list[Order]) -> dict[str, int]: ...    # built-in generics (Python 3.9+)
def apply(fn: Callable[[int], int], values: list[int]) -> list[int]: ...
def lines(path: Path) -> Iterator[str]: ...               # a generator
Status = Literal["pending", "paid", "shipped"]            # only these strings
MAX_RETRIES: Final = 3                                     # constant
```

`X | None` means "X or None" (older code writes `Optional[X]`). mypy then forces you to handle the `None` case before using the value, which is exactly the `NoMethodError: undefined method for nil` bug you know from Ruby.

### Narrowing

mypy follows your checks:

```python
order = find_order(7)          # type: Order | None
if order is None:
    raise LookupError("no order 7")
order.total_cents              # OK here: mypy knows order is Order now
```

### `TypedDict`: dicts with known keys

For JSON-like data where you want key checking without a class:

```python
class OrderRow(TypedDict):
    id: int
    status: Status
    total_cents: int
```

### `Protocol`: typed duck typing

A `Protocol` says "anything with these methods fits", without inheritance. It is duck typing that mypy can check:

```python
class PricingRule(Protocol):
    def price(self, unit_cents: int, quantity: int) -> int: ...

def checkout(rule: PricingRule, unit: int, qty: int) -> int:
    return rule.price(unit, qty)   # any object with a matching price() is accepted
```

### Generics

Type variables make reusable functions keep precise types. Python 3.12+ has a compact syntax:

```python
def first[T](items: list[T]) -> T | None:
    return items[0] if items else None
```

### mypy `--strict`

`--strict` turns on all checks: every function must be annotated, no implicit `Any`, and so on. Start new code in strict mode (it is easy from the beginning and painful to add later). Use `# type: ignore[code]` sparingly and always with the specific error code.

## 5. Minimal working example

Create `pricing_types.py`:

```python
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal, Protocol, TypedDict

Status = Literal["pending", "paid", "refunded"]


class OrderRow(TypedDict):
    id: int
    status: Status
    total_cents: int


class PricingRule(Protocol):
    def price(self, unit_cents: int, quantity: int) -> int: ...


@dataclass
class PercentOff:
    percent: int

    def price(self, unit_cents: int, quantity: int) -> int:
        return unit_cents * quantity * (100 - self.percent) // 100


@dataclass
class ThreeForTwo:
    def price(self, unit_cents: int, quantity: int) -> int:
        return unit_cents * (quantity - quantity // 3)


def checkout(rule: PricingRule, unit_cents: int, quantity: int) -> int:
    return rule.price(unit_cents, quantity)


def find(rows: Iterable[OrderRow], order_id: int) -> OrderRow | None:
    return next((row for row in rows if row["id"] == order_id), None)


def first[T](items: list[T]) -> T | None:
    return items[0] if items else None


rows: list[OrderRow] = [
    {"id": 1, "status": "paid", "total_cents": 1250},
    {"id": 2, "status": "pending", "total_cents": 300},
]

print(checkout(PercentOff(10), 1000, 3), checkout(ThreeForTwo(), 1000, 3))
found = find(rows, 2)
if found is not None:  # narrowing: after this check, found is an OrderRow
    print(found["status"], found["total_cents"])
print(first(["a", "b"]), first([]))
```

Create `mistakes.py` (it imports the file above and makes typical mistakes):

```python
from pricing_types import OrderRow, PercentOff, checkout, find, rows


class Coupon:
    def discount(self, cents: int) -> int:  # wrong method name: not a PricingRule
        return cents - 100


order = find(rows, 1)
print(order["total_cents"])  # order may be None

bad_row: OrderRow = {"id": 3, "status": "shipped", "total_cents": "12.50"}

checkout(Coupon(), 1000, 1)
checkout(PercentOff("10"), 1000, 1)
```

Run the correct file, then type-check both:

```bash
uv run python pricing_types.py
```

```
2700 2000
pending 300
a None
```

```bash
uv run mypy --strict pricing_types.py mistakes.py
```

```
mistakes.py:10: error: Value of type "OrderRow | None" is not indexable  [index]
mistakes.py:12: error: Incompatible types (expression has type "Literal['shipped']", TypedDict item "status" has type "Literal['pending', 'paid', 'refunded']")  [typeddict-item]
mistakes.py:12: error: Incompatible types (expression has type "str", TypedDict item "total_cents" has type "int")  [typeddict-item]
mistakes.py:14: error: Argument 1 to "checkout" has incompatible type "Coupon"; expected "PricingRule"  [arg-type]
mistakes.py:15: error: Argument 1 to "PercentOff" has incompatible type "str"; expected "int"  [arg-type]
```

Every error above would be a runtime crash or a wrong result in production: a `None` subscript, a status that is not allowed, a price stored as a string, an object that does not fit the pricing protocol, and a percentage passed as a string. mypy found them without running anything.

## 6. Key terms

- **Type hint / annotation**: a type written after `:` or `->`.
- **`X | None`**: "X or None" (also written `Optional[X]`).
- **Narrowing**: mypy refining a type after checks like `is None`.
- **`Literal`**: only specific values allowed.
- **`TypedDict`**: a dict type with known keys and value types.
- **`Protocol`**: a structural interface (duck typing with checking).
- **Generic / type variable**: `list[T]`, `def first[T](...)`: types that keep precision.
- **`Any`**: "anything"; disables checking for that value.
- **`--strict`**: mypy's strictest mode.

## 7. Common mistakes

- **Thinking hints are enforced at runtime.** Plain Python ignores them (FastAPI and Pydantic are exceptions: they validate on purpose).
- **`Any` everywhere** to make errors go away.
- **Not handling `None`** from functions that return `X | None`.
- **Old syntax from tutorials** (`List[int]`, `Optional[str]` from `typing`): it still works, but modern code uses `list[int]` and `str | None`.
- **Blanket `# type: ignore`** without an error code.
- **Adding types only at the end of a project.** Start strict from the first file.

## 8. Check your understanding

1. Does `def f(x: int) -> int` stop someone calling `f("a")` at runtime?
2. How do you tell mypy that `find_order` can return nothing, and what does it then force you to do?
3. When would you use a `TypedDict` instead of a dataclass?
4. What does `Protocol` give you that a base class does not?
5. What does `mypy --strict` add over plain `mypy`?

<details>
<summary>Answers</summary>

1. No. Python runs it (and may fail later); only mypy (or a runtime validator such as Pydantic) would flag it.
2. Annotate the return as `Order | None`. mypy then requires a check (for example `if order is None: ...`) before you use `order`'s attributes.
3. For dict-shaped data you keep as a dict (JSON payloads, rows from a library) where you want key and value types checked without converting to objects.
4. Structural typing: any class with matching methods fits, without inheriting from anything (checked duck typing).
5. It requires annotations on every function and turns on many extra checks (no implicit `Any`, no untyped calls, and more).

</details>

## 9. Go deeper (optional)

- [mypy cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html) and "Getting started".
- Python docs: [`typing`](https://docs.python.org/3/library/typing.html) (Protocol, TypedDict, Literal, generics).
- *Fluent Python*, 2nd ed., chapter 8 ("Type Hints in Functions") and chapter 15 ("More About Type Hints").
