# 12 · Pattern matching and enums

## 1. In one sentence

`match`/`case` (Python 3.10+) matches a value against **shapes** (literal values, sequences, dicts, objects) and pulls out parts of it, like Ruby's `case ... in`, and **enums** give you a fixed set of named values where Ruby would use symbols.

## 2. Why it exists

You will handle a lot of structured data: webhook payloads, API responses, tool calls from a model (`{"type": "tool_use", "name": ..., "input": {...}}`), CLI commands. Long chains of `if isinstance(...) and "key" in data and data["key"] == ...` are hard to read. Pattern matching expresses "if it looks like **this**, take out **these** parts" directly.

Enums solve a different Ruby habit. Python has no symbols, and plain strings like `"pendng"` (a typo) fail silently. An enum makes the set of valid values explicit, gives autocomplete, and lets mypy check exhaustiveness.

## 3. Rails analogy

| Ruby | Python |
|---|---|
| `case event in { type: "order.paid", data: { id: } }` | `match event: case {"type": "order.paid", "data": {"id": id}}:` |
| `in [first, *rest]` | `case [first, *rest]:` |
| `in Integer => n if n > 10` | `case int(n) if n > 10:` |
| `in Order(status: "paid")` (with `deconstruct_keys`) | `case Order(status="paid"):` (dataclasses support this automatically) |
| `else` | `case _:` |
| `:pending`, `:paid` symbols | `class Status(StrEnum): PENDING = "pending"` |
| `enum status: { pending: 0, paid: 1 }` (Active Record) | `Enum` / `StrEnum` in code; store the `.value` in the database |

Where the analogy breaks: a dict pattern like `{"type": "x"}` matches dicts that have **at least** those keys (extra keys are fine), the same as Ruby's hash patterns. But a bare name in a pattern **captures** a value; it does not compare against a variable (see the mistakes section).

## 4. How it works

### Pattern kinds

```python
match value:
    case 0 | 1:                      # literals, with | for "or"
        ...
    case [x, y]:                     # a sequence of exactly two items
        ...
    case [first, *rest]:             # first item, then the rest
        ...
    case {"type": "order.paid", "data": {"id": order_id}}:   # dict shape; captures order_id
        ...
    case Order(status="refunded", total_cents=cents):         # object attributes
        ...
    case str() as text if len(text) > 100:                    # type check + guard
        ...
    case _:                          # anything else (like else)
        ...
```

Cases are tried **top to bottom**; the first match wins, so put specific patterns before general ones.

### Enums

```python
from enum import StrEnum

class Status(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    REFUNDED = "refunded"

Status("paid")          # Status.PAID   (from a database or JSON value)
Status.PAID == "paid"   # True: a StrEnum is also a str
[s.value for s in Status]
```

`StrEnum` (Python 3.11+) members are also strings, so they serialise to JSON and compare with strings naturally. Use plain `Enum` when the values should not be mixed with strings.

## 5. Minimal working example

Create `events.py`. It routes webhook-style events and uses an enum for statuses:

```python
from dataclasses import dataclass
from enum import StrEnum


class Status(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    REFUNDED = "refunded"


@dataclass
class Order:
    id: int
    status: Status
    total_cents: int


def describe(event: object) -> str:
    match event:
        case {"type": "order.paid", "data": {"id": order_id, "total_cents": cents}}:
            return f"order {order_id} paid £{cents / 100:.2f}"
        case {"type": "order.refunded", "data": {"id": order_id}}:
            return f"order {order_id} refunded"
        case {"type": str(kind)}:
            return f"ignored event type {kind!r}"
        case Order(status=Status.REFUNDED, id=order_id):
            return f"Order object {order_id} is refunded"
        case Order(total_cents=cents) if cents > 100_000:
            return "large order, needs review"
        case [first, *rest]:
            return f"batch: {describe(first)} (+{len(rest)} more)"
        case _:
            return "unknown"


events = [
    {"type": "order.paid", "data": {"id": 7, "total_cents": 4200}, "meta": {"retry": 0}},
    {"type": "order.refunded", "data": {"id": 8}},
    {"type": "customer.created", "data": {}},
    Order(9, Status.REFUNDED, 900),
    Order(10, Status.PAID, 250_000),
    [{"type": "order.refunded", "data": {"id": 11}}, {"type": "x"}],
    42,
]
for event in events:
    print(describe(event))

print(Status("paid") is Status.PAID, Status.PAID == "paid", [s.value for s in Status])
try:
    Status("pendng")
except ValueError as error:
    print("ValueError:", error)
```

```bash
uv run python events.py
```

Output:

```
order 7 paid £42.00
order 8 refunded
ignored event type 'customer.created'
Order object 9 is refunded
large order, needs review
batch: order 11 refunded (+1 more)
unknown
True True ['pending', 'paid', 'refunded']
ValueError: 'pendng' is not a valid Status
```

Look at the first event: it has an extra `"meta"` key and still matches, because dict patterns only require the listed keys. And the typo `"pendng"` fails loudly, instead of flowing through the app as an invalid string.

## 6. Key terms

- **Structural pattern matching**: `match`/`case` on the shape of data.
- **Capture pattern**: a bare name in a pattern that binds a value (`id`).
- **Wildcard `_`**: matches anything; used as the default case.
- **Guard**: `if` condition on a case.
- **Class pattern**: `Order(status=...)`, matching object attributes.
- **Enum / `StrEnum`**: a fixed set of named constants / one whose members are also strings.
- **`.value`**: the underlying value of an enum member (for storage and JSON).

## 7. Common mistakes

- **Using a variable to compare**: `case expected_status:` does **not** compare with `expected_status`; it captures anything into a new variable with that name. Compare with dotted names (`Status.PAID`), literals, or a guard (`case x if x == expected_status:`).
- **General cases before specific ones**, so the specific ones never run.
- **Forgetting `case _:`**, so unexpected input silently does nothing.
- **Plain strings for statuses** across the codebase; use an enum in code and store `.value`.
- **`match` for simple two-way checks**: `if/else` is clearer for those.

## 8. Check your understanding

1. Translate `case event in { type: "order.paid", data: { id: } }` into Python.
2. Why does the first event in the example match even though it has a `"meta"` key?
3. What is wrong with `case PAID_STATUS:` where `PAID_STATUS = "paid"`?
4. What is the advantage of `Status("paid")` over passing the string `"paid"` around?
5. When would you choose plain `Enum` over `StrEnum`?

<details>
<summary>Answers</summary>

1. `match event: case {"type": "order.paid", "data": {"id": id}}:`
2. Dict patterns check only the listed keys; extra keys are allowed.
3. A bare name is a capture pattern: it matches anything and assigns it to `PAID_STATUS`. Use a dotted name (`Status.PAID`), the literal `"paid"`, or a guard.
4. Invalid values fail immediately with a `ValueError`, typos are impossible in code (autocomplete, mypy), and the set of valid statuses is documented in one place.
5. When enum members should not be equal to (or mixed up with) plain strings, for example for internal states that must never be compared with user input.

</details>

## 9. Go deeper (optional)

- [PEP 636: Structural Pattern Matching tutorial](https://peps.python.org/pep-0636/).
- Python docs: [`enum` HOWTO](https://docs.python.org/3/howto/enum.html).
- *Fluent Python*, 2nd ed., chapter 18 ("with, match, and else Blocks") for pattern matching in depth.
