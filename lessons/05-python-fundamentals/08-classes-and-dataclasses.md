# 08 · Classes and dataclasses

## 1. In one sentence

Python classes work much like Ruby's, but `self` is written explicitly as the first parameter, attributes are public by default, **dunder methods** (`__init__`, `__repr__`, `__eq__`, `__len__`...) hook your objects into language features, and **`@dataclass`** writes the boilerplate for simple data objects.

## 2. Why it exists

You will model data everywhere: an `Order`, a `Book`, a `Chunk`, a tool result. Writing `__init__`, `__repr__` and `__eq__` by hand for each is repetitive and error-prone, just as writing `initialize`, `inspect` and `==` by hand in Ruby would be. Python gives you:

- **plain classes** for objects with behaviour,
- **`@dataclass`** for objects that are mostly data (like Ruby's `Struct` or `Data.define`),
- **dunder methods** so your objects work with `len()`, `for`, `==`, `sorted()`, `print()`.

## 3. Rails analogy

| Ruby | Python |
|---|---|
| `class Order ... end` | `class Order:` + indented body |
| `def initialize(id, total)` | `def __init__(self, id, total):` |
| `@total = total` | `self.total = total` |
| `attr_reader :total` | nothing needed: attributes are public; or `@property` for computed values |
| `def to_s` / `def inspect` | `def __str__(self)` / `def __repr__(self)` |
| `def ==(other)` / `include Comparable` + `<=>` | `def __eq__(self, other)` / `__lt__` (or `@dataclass(order=True)`) |
| `def self.from_csv(row)` | `@classmethod def from_csv(cls, row):` |
| `include Enumerable` + `def each` | `def __iter__(self)` (and `__len__` for `len()`) |
| `class Admin < User` + `super` | `class Admin(User):` + `super().__init__(...)` |
| `private` methods | `_name` by convention (not enforced) |
| `Struct.new(:x, :y, keyword_init: true)` | `@dataclass class Point: x: int; y: int` |
| `Data.define(:x, :y)` (immutable) | `@dataclass(frozen=True)` |
| Duck typing | Duck typing (and `Protocol` for static checks, lesson 10) |

Where the analogy breaks: there is no `method_missing`-driven style, no open classes you are expected to reopen, and far less metaprogramming. Python code is intentionally explicit.

## 4. How it works

### `self` is explicit

```python
class Order:
    def __init__(self, id: int, total_cents: int) -> None:
        self.id = id
        self.total_cents = total_cents

    def with_discount(self, percent: int) -> int:
        return self.total_cents * (100 - percent) // 100
```

`order.with_discount(10)` is really `Order.with_discount(order, 10)`: the instance is passed as the first argument, named `self` by convention. Forgetting `self` in the parameter list is a common early error.

### Dunder ("double underscore") methods

Python calls these for you when you use built-in syntax:

| You write | Python calls | Ruby equivalent |
|---|---|---|
| `Order(1, 500)` | `__init__` | `initialize` |
| `repr(order)`, the REPL, debuggers | `__repr__` | `inspect` |
| `str(order)`, `print(order)`, f-strings | `__str__` (falls back to `__repr__`) | `to_s` |
| `a == b` | `__eq__` | `==` |
| `a < b`, `sorted(...)` | `__lt__` | `<=>` via Comparable |
| `len(basket)` | `__len__` | `size` |
| `for item in basket` | `__iter__` | `each` via Enumerable |
| `sku in basket` | `__contains__` | `include?` |
| `hash(obj)`, set/dict keys | `__hash__` | `hash` + `eql?` |

### Properties

A `@property` is a method you access like an attribute, like a Ruby reader method that computes something:

```python
@property
def total_cents(self) -> int:
    return sum(line.subtotal for line in self.lines)
```

### Class methods and static methods

- `@classmethod` receives the class as `cls`: use it for alternative constructors (`Order.from_row(row)`), like `def self.from_row`.
- `@staticmethod` receives nothing special: a plain function that lives in the class namespace. Often a module-level function is simpler.

### Dataclasses

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Money:
    cents: int
    currency: str = "GBP"
```

This generates `__init__(self, cents, currency="GBP")`, a readable `__repr__`, and `__eq__` comparing fields. `frozen=True` makes instances immutable (and hashable, so usable as dict keys). For a mutable default such as a list, use `field(default_factory=list)` (lesson 04's mutable default problem again).

### Inheritance vs composition

Inheritance works as in Ruby (`class Admin(User):`, `super().__init__(...)`). As in Rails, prefer **composition** (an object that has another object) over deep hierarchies. For "anything that has a `price_for(...)` method", Python uses duck typing, and `typing.Protocol` lets mypy check it (lesson 10).

## 5. Minimal working example

Create `shop.py`:

```python
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Money:
    cents: int
    currency: str = "GBP"

    def __add__(self, other: "Money") -> "Money":
        if other.currency != self.currency:
            raise ValueError("currency mismatch")
        return Money(self.cents + other.cents, self.currency)

    def __str__(self) -> str:
        return f"£{self.cents / 100:,.2f}"


@dataclass
class LineItem:
    sku: str
    unit: Money
    quantity: int = 1

    @property
    def subtotal(self) -> Money:
        return Money(self.unit.cents * self.quantity, self.unit.currency)


@dataclass
class Basket:
    lines: list[LineItem] = field(default_factory=list)  # a new list per basket

    def add(self, sku: str, unit_cents: int, quantity: int = 1) -> "Basket":
        self.lines.append(LineItem(sku, Money(unit_cents), quantity))
        return self

    @property
    def total(self) -> Money:
        total = Money(0)
        for line in self.lines:
            total = total + line.subtotal
        return total

    def __len__(self) -> int:
        return sum(line.quantity for line in self.lines)

    def __iter__(self):
        return iter(self.lines)

    def __contains__(self, sku: str) -> bool:
        return any(line.sku == sku for line in self.lines)

    @classmethod
    def from_pairs(cls, pairs: list[tuple[str, int]]) -> "Basket":
        basket = cls()
        for sku, cents in pairs:
            basket.add(sku, cents)
        return basket


basket = Basket().add("book", 1250, 2).add("pen", 199)
print(basket.lines[0])                          # dataclass __repr__
print(len(basket), "items, total", basket.total)  # __len__, __str__
print("pen" in basket, "mug" in basket)         # __contains__
print([line.sku for line in basket])            # __iter__
print(Money(100) == Money(100), Money(100) is Money(100))  # __eq__ vs identity
print(Basket.from_pairs([("mug", 800)]).total)  # classmethod constructor

try:
    basket.lines[0].unit.cents = 1  # frozen dataclass
except Exception as error:
    print(type(error).__name__, "-", error)
```

```bash
uv run python shop.py
```

Output:

```
LineItem(sku='book', unit=Money(cents=1250, currency='GBP'), quantity=2)
3 items, total £26.99
True False
['book', 'pen']
True False
£8.00
FrozenInstanceError - cannot assign to field 'cents'
```

Every line of output comes from a dunder method you wrote or `@dataclass` generated: `__repr__`, `__len__`, `__str__`, `__contains__`, `__iter__`, `__eq__`, and the frozen check in `__setattr__`.

## 6. Key terms

- **Class / instance**: the blueprint / an object made from it.
- **`self` / `cls`**: the instance / the class, passed explicitly.
- **Dunder method**: `__name__` methods that plug into language syntax.
- **`@property`**: a computed attribute.
- **`@classmethod` / `@staticmethod`**: receives the class / receives nothing extra.
- **`@dataclass`**: generates `__init__`, `__repr__`, `__eq__` from annotated fields.
- **`frozen=True`**: immutable instances.
- **`field(default_factory=...)`**: a fresh default per instance.
- **Composition**: building objects from other objects instead of inheriting.

## 7. Common mistakes

- **Forgetting `self`** in a method definition or when accessing attributes (`total` instead of `self.total`).
- **Class attributes used as instance state**: `class Basket: lines = []` shares one list across all baskets.
- **Mutable dataclass defaults** (`lines: list = []`): use `field(default_factory=list)` (Python raises an error for this one).
- **Getters and setters** (`get_total()`, `set_total()`): use plain attributes, and `@property` when you need computation.
- **Only defining `__str__`**: define `__repr__` first; it is what you see while debugging.
- **Deep inheritance trees**: prefer composition and small classes.

## 8. Check your understanding

1. What does `@dataclass` generate for you, and what does `frozen=True` add?
2. How do you make `len(basket)` and `for line in basket` work?
3. Why is `class Basket: lines = []` a bug?
4. What is the difference between `@classmethod` and `@staticmethod`, and when do you use a classmethod?
5. Translate `class Admin < User; def initialize(name) super(name); @admin = true; end; end`.

<details>
<summary>Answers</summary>

1. `__init__`, `__repr__` and `__eq__` from the annotated fields (optionally ordering methods). `frozen=True` makes instances immutable and hashable.
2. Define `__len__` (returning an int) and `__iter__` (returning an iterator).
3. `lines` is a class attribute: one list shared by every instance, so items added to one basket appear in all.
4. A classmethod receives the class (`cls`) and is used for alternative constructors; a staticmethod receives nothing extra and is just a namespaced function.
5. `class Admin(User):` with `def __init__(self, name): super().__init__(name); self.admin = True`.

</details>

## 9. Go deeper (optional)

- The Python Tutorial: [Classes](https://docs.python.org/3/tutorial/classes.html).
- Python docs: [`dataclasses`](https://docs.python.org/3/library/dataclasses.html) and the [data model](https://docs.python.org/3/reference/datamodel.html) (the full list of dunder methods).
- *Fluent Python*, 2nd ed., chapter 1 ("The Python Data Model"), chapter 5 ("Data Class Builders") and chapter 11 ("A Pythonic Object").
