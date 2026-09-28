# 03 · Collections and comprehensions

## 1. In one sentence

Python's four core collections are `list` (Array), `tuple` (frozen Array), `dict` (Hash) and `set` (Set), and instead of Ruby's block methods (`map`, `select`, `each_with_object`) you mostly use **comprehensions** and a few built-in functions.

## 2. Why it exists

In Ruby you chain `Enumerable` methods: `orders.select(&:paid?).map(&:total).sum`. Python has no `Enumerable` mixin with dozens of methods on every collection. It has:

- **comprehensions**: `[o.total for o in orders if o.paid]`, one readable expression for map + filter,
- **built-in functions** that work on any iterable: `sum`, `min`, `max`, `sorted`, `any`, `all`, `len`, `enumerate`, `zip`,
- the **`collections`** module for special cases: `Counter` (Ruby's `tally`), `defaultdict` (a Hash with a default block).

Knowing these few tools covers almost every Ruby one-liner you use daily.

## 3. Rails analogy

| Ruby | Python |
|---|---|
| `[1, 2, 3]` (Array) | `[1, 2, 3]` (`list`) |
| `[1, 2].freeze` | `(1, 2)` (`tuple`); `(1,)` for one item |
| `{ "a" => 1 }` / `{ a: 1 }` | `{"a": 1}` (`dict`; keys are usually strings) |
| `Set[1, 2]` | `{1, 2}` (`set`); empty set is `set()`, not `{}` |
| `xs.map { \|x\| x * 2 }` | `[x * 2 for x in xs]` |
| `xs.select { \|x\| x > 1 }` | `[x for x in xs if x > 1]` |
| `xs.reject(&:nil?)` | `[x for x in xs if x is not None]` |
| `xs.sum`, `xs.min`, `xs.max` | `sum(xs)`, `min(xs)`, `max(xs)` |
| `xs.sort_by { \|o\| o.total }` | `sorted(xs, key=lambda o: o.total)` |
| `xs.each_with_index` | `for i, x in enumerate(xs):` |
| `xs.zip(ys)` | `zip(xs, ys)` |
| `xs.tally` | `Counter(xs)` |
| `xs.group_by(&:status)` | `defaultdict(list)` + loop (or `itertools.groupby` on sorted data) |
| `xs.any? { ... }` / `all?` | `any(... for x in xs)` / `all(...)` |
| `h.map { \|k, v\| [k, v * 2] }.to_h` | `{k: v * 2 for k, v in h.items()}` |
| `h.fetch(:a, 0)` | `h.get("a", 0)` |
| `xs.first(3)`, `xs.last`, `xs[1..2]` | `xs[:3]`, `xs[-1]`, `xs[1:3]` |

Where the analogy breaks: Python has **no symbols**, so dict keys are usually strings (`order["status"]`), and you cannot call methods on dict keys like attributes (`order.status` only works on objects, not dicts).

## 4. How it works

### Lists, tuples, dicts, sets

```python
tags = ["ruby", "rails"]        # list: ordered, mutable
tags.append("python")           # Ruby: tags << "python"
point = (3, 4)                  # tuple: ordered, immutable; good for fixed records and dict keys
x, y = point                    # unpacking (Ruby: x, y = point)
order = {"id": 7, "status": "paid"}   # dict: insertion-ordered, mutable
order["total"] = 1250           # add a key
statuses = {"paid", "pending"}  # set: unique items, fast membership tests
"paid" in statuses              # True (Ruby: statuses.include?("paid"))
```

### Slicing

`sequence[start:stop:step]`: `stop` is **excluded** (like Ruby's `...` range, not `..`).

```python
xs = [10, 20, 30, 40, 50]
xs[1:3]    # [20, 30]
xs[:2]     # [10, 20]   first two
xs[-2:]    # [40, 50]   last two
xs[::-1]   # reversed copy
```

### Comprehensions

A comprehension is `[expression for item in iterable if condition]`. Read it left to right as "give me *expression* for each *item* where *condition*".

```python
paid_totals = [o["total"] for o in orders if o["status"] == "paid"]
by_id = {o["id"]: o for o in orders}               # dict comprehension
statuses = {o["status"] for o in orders}           # set comprehension
count = sum(1 for o in orders if o["total"] > 1000)  # generator expression inside sum()
```

If a comprehension needs more than one `for` or a long condition, **use a normal loop**: readability counts.

### Copying

`b = a` does not copy (lesson 02). To copy:

- `list(a)`, `a.copy()` or `a[:]`: a **shallow** copy (the outer list is new; inner objects are shared).
- `copy.deepcopy(a)`: copies nested structures too.

### Sorting

- `sorted(xs)` returns a **new** list; `xs.sort()` sorts **in place** and returns `None`.
- `key=` gives the value to sort by (like `sort_by`); `reverse=True` for descending.
- Sort by several keys with a tuple: `key=lambda o: (o["status"], -o["total"])`.

## 5. Minimal working example

Create `enumerable.py`. It translates ten Ruby one-liners you use every day (Ruby in the comments):

```python
from collections import Counter, defaultdict

orders = [
    {"id": 1, "customer": "ana", "status": "paid", "total": 1250},
    {"id": 2, "customer": "ben", "status": "pending", "total": 300},
    {"id": 3, "customer": "ana", "status": "paid", "total": 4200},
    {"id": 4, "customer": "cy", "status": "refunded", "total": 900},
]

# 1. orders.map { |o| o[:id] }
print(1, [o["id"] for o in orders])

# 2. orders.select { |o| o[:status] == "paid" }.map { |o| o[:total] }.sum
print(2, sum(o["total"] for o in orders if o["status"] == "paid"))

# 3. orders.reject { |o| o[:status] == "refunded" }.size
print(3, len([o for o in orders if o["status"] != "refunded"]))

# 4. orders.map { |o| o[:status] }.tally
print(4, Counter(o["status"] for o in orders))

# 5. orders.group_by { |o| o[:customer] }.transform_values { |os| os.sum { |o| o[:total] } }
totals: defaultdict[str, int] = defaultdict(int)
for o in orders:
    totals[o["customer"]] += o["total"]
print(5, dict(totals))

# 6. orders.sort_by { |o| -o[:total] }.first(2).map { |o| o[:id] }
print(6, [o["id"] for o in sorted(orders, key=lambda o: o["total"], reverse=True)[:2]])

# 7. orders.each_with_index.map { |o, i| "#{i + 1}. ##{o[:id]}" }
print(7, [f"{i}. #{o['id']}" for i, o in enumerate(orders, start=1)])

# 8. orders.index_by { |o| o[:id] }   (Rails)
by_id = {o["id"]: o for o in orders}
print(8, by_id[3]["customer"])

# 9. orders.any? { |o| o[:total] > 4000 } / orders.all? { |o| o[:total] > 0 }
print(9, any(o["total"] > 4000 for o in orders), all(o["total"] > 0 for o in orders))

# 10. orders.map { |o| o[:customer] }.uniq.sort
print(10, sorted({o["customer"] for o in orders}))

# Bonus: slicing and a copy.
ids = [o["id"] for o in orders]
print("slices:", ids[:2], ids[-1], ids[::-1])
```

```bash
uv run python enumerable.py
```

Output:

```
1 [1, 2, 3, 4]
2 5450
3 3
4 Counter({'paid': 2, 'pending': 1, 'refunded': 1})
5 {'ana': 5450, 'ben': 300, 'cy': 900}
6 [3, 1]
7 ['1. #1', '2. #2', '3. #3', '4. #4']
8 ana
9 True True
10 ['ana', 'ben', 'cy']
slices: [1, 2] 4 [4, 3, 2, 1]
```

Line 5 uses `defaultdict(int)`: a dict that creates a missing key with `int()`, which is `0`. It is Python's `Hash.new(0)`.

## 6. Key terms

- **list / tuple / dict / set**: Array / frozen Array / Hash / Set.
- **Slicing**: `seq[start:stop:step]`, stop excluded.
- **Comprehension**: `[expr for x in xs if cond]` (also `{...}` for dicts and sets).
- **Generator expression**: `(expr for x in xs)`, lazy; often passed straight to `sum()`, `any()`, `max()`.
- **Unpacking**: `a, b = pair`; `first, *rest = xs`.
- **`Counter` / `defaultdict`**: `tally` / a Hash with a default value.
- **Shallow vs deep copy**: new outer container only / everything copied.

## 7. Common mistakes

- **`{}` for an empty set.** It is an empty dict; use `set()`.
- **`xs.sort()` in an expression.** It returns `None`; use `sorted(xs)`.
- **`map(lambda ...)` / `filter(lambda ...)`** chains. Prefer comprehensions.
- **Modifying a list while looping over it.** Build a new list instead.
- **Forgetting that `stop` is excluded in slices** (`xs[1:3]` has two items).
- **Nested comprehensions nobody can read.** Use a loop.
- **Accessing a missing key with `d["x"]`** (raises `KeyError`); use `d.get("x")` when absence is normal.

## 8. Check your understanding

1. Write the Python for `users.select(&:admin?).map(&:email)` where users are dicts with `"admin"` and `"email"` keys.
2. What is the difference between `sorted(xs)` and `xs.sort()`?
3. What does `xs[-3:]` return for `xs = [1, 2, 3, 4, 5]`?
4. How do you count how many times each status appears, in one line?
5. Why is `{}` not an empty set?

<details>
<summary>Answers</summary>

1. `[u["email"] for u in users if u["admin"]]`
2. `sorted` returns a new sorted list and leaves `xs` unchanged; `xs.sort()` sorts `xs` in place and returns `None`.
3. `[3, 4, 5]`.
4. `Counter(o["status"] for o in orders)`.
5. `{}` was the empty dict long before sets had literals; use `set()`.

</details>

## 9. Go deeper (optional)

- The Python Tutorial: [Data Structures](https://docs.python.org/3/tutorial/datastructures.html).
- Python docs: [`collections`](https://docs.python.org/3/library/collections.html) (`Counter`, `defaultdict`, `deque`).
- *Fluent Python*, 2nd ed., chapter 2 ("An Array of Sequences") and chapter 3 ("Dictionaries and Sets").
