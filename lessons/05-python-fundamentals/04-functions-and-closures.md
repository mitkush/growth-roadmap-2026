# 04 · Functions, arguments and closures

## 1. In one sentence

Python functions are defined with `def`, must `return` explicitly, take positional and keyword arguments (with `*` and `**` for extras), and are ordinary objects you can pass around, which is how Python does most of what Ruby does with blocks.

## 2. Why it exists

Functions are where Ruby habits bite hardest:

- A Ruby method returns its last expression; a Python function without `return` returns `None`.
- Ruby evaluates default arguments on every call; Python evaluates them **once**, so `def f(items=[])` shares one list across all calls.
- Ruby passes a block to almost everything; Python has no blocks. You pass a **function** instead (a named `def`, or a one-line `lambda`).

## 3. Rails analogy

| Ruby | Python |
|---|---|
| `def total(items) items.sum end` | `def total(items): return sum(items)` |
| `def search(query, limit: 10)` | `def search(query, *, limit=10):` (`*` makes `limit` keyword-only) |
| `def log(*args, **opts)` | `def log(*args, **kwargs):` |
| `search("x", limit: 5)` | `search("x", limit=5)` |
| `items.each { \|i\| ... }` | `for i in items: ...` |
| `retry_with(3) { call_api }` | `retry_with(3, call_api)`: pass the function itself |
| `->(x) { x * 2 }` | `lambda x: x * 2` (one expression only) |
| `method(:puts)` | `print` (functions are already objects) |
| `memoize` / `@x \|\|= ...` | `@functools.cache` / `@functools.lru_cache` |

## 4. How it works

### Kinds of parameters

```python
def search(query, limit=10, *, include_archived=False, **filters):
    ...
```

| Part | Name | How it is passed |
|---|---|---|
| `query` | positional-or-keyword | `search("x")` or `search(query="x")` |
| `limit=10` | with a default | optional |
| `*` | separator | everything after it is **keyword-only** |
| `include_archived=False` | keyword-only | must be `include_archived=True`, never positional |
| `**filters` | extra keyword arguments | collected into a dict, like Ruby's `**opts` |

Use keyword-only arguments for boolean flags: `search("x", True)` is unreadable; `search("x", include_archived=True)` is clear.

### Defaults are evaluated once

```python
def add_tag(tag, tags=[]):   # the [] is created ONCE, when the function is defined
    tags.append(tag)
    return tags

add_tag("a")  # ['a']
add_tag("b")  # ['a', 'b']  ← surprise: same list
```

The fix is the `None` idiom:

```python
def add_tag(tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags
```

ruff's rule `B006` catches this for you.

### Functions are objects (instead of blocks)

Any function can be stored in a variable, passed as an argument, or returned from another function. This replaces most block usage:

```python
def retry(times, action):
    for attempt in range(1, times + 1):
        try:
            return action()
        except ConnectionError:
            if attempt == times:
                raise

retry(3, fetch_orders)                   # pass a named function (no parentheses!)
retry(3, lambda: fetch_orders(page=2))   # or a lambda for a small inline call
```

A `lambda` is limited to **one expression**. When you need statements, write a small `def` with a name, even inside another function.

### Closures and `nonlocal`

A function defined inside another function **remembers** the outer variables (a closure), like a Ruby lambda:

```python
def make_counter():
    count = 0
    def increment():
        nonlocal count      # needed to *assign* to the outer variable
        count += 1
        return count
    return increment
```

Reading an outer variable works without anything special. **Assigning** to it needs `nonlocal` (otherwise Python creates a new local variable).

### Scope in one rule

Python looks up names in this order: **L**ocal → **E**nclosing functions → **G**lobal (module) → **B**uilt-ins ("LEGB"). There is no block scope: a variable assigned inside an `if` or `for` is visible after it in the same function.

## 5. Minimal working example

Create `functions.py`:

```python
from functools import lru_cache, partial


# 1. Explicit return (and what happens without it).
def total_with_return(prices):
    return sum(prices)


def total_without_return(prices):
    sum(prices)  # computed, then thrown away


print(1, total_with_return([1, 2]), total_without_return([1, 2]))


# 2. Keyword-only flags and **kwargs.
def search(query, limit=10, *, include_archived=False, **filters):
    return f"q={query!r} limit={limit} archived={include_archived} filters={filters}"


print(2, search("kamal", 5, include_archived=True, team="infra"))


# 3. The mutable default bug, and the fix.
def add_tag_buggy(tag, tags=[]):  # noqa: B006  (deliberate bug for the demo)
    tags.append(tag)
    return tags


def add_tag(tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags


print(3, add_tag_buggy("a"), add_tag_buggy("b"), "| fixed:", add_tag("a"), add_tag("b"))


# 4. Passing functions instead of blocks.
def apply_to_all(values, transform):
    return [transform(v) for v in values]


print(4, apply_to_all(["ruby", "rails"], str.upper), apply_to_all([1, 2, 3], lambda n: n * 10))


# 5. A closure with nonlocal.
def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment


counter = make_counter()
print(5, counter(), counter(), counter())

# 6. partial: pre-fill arguments (like currying).
search_infra = partial(search, team="infra", limit=3)
print(6, search_infra("deploy"))


# 7. Memoisation with a decorator (lesson 11 explains decorators).
@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print(7, fib(80), fib.cache_info().hits)
```

```bash
uv run python functions.py
```

Output:

```
1 3 None
2 q='kamal' limit=5 archived=True filters={'team': 'infra'}
3 ['a', 'b'] ['a', 'b'] | fixed: ['a'] ['b']
4 ['RUBY', 'RAILS'] [10, 20, 30]
5 1 2 3
6 q='deploy' limit=3 archived=False filters={'team': 'infra'}
7 23416728348467685 78
```

Line 3 is the one to remember: the buggy version prints `['a', 'b']` **twice**. Both calls appended to, and returned, the **same** default list, so by the time `print` shows them, that one list holds both tags. The fixed version creates a new list per call.

## 6. Key terms

- **Positional / keyword argument**: passed by position / by name.
- **Keyword-only parameter**: after `*`, must be passed by name.
- **`*args` / `**kwargs`**: extra positional arguments as a tuple / extra keyword arguments as a dict.
- **Default argument**: evaluated once, at definition time.
- **First-class function**: a function used as a value.
- **lambda**: an anonymous one-expression function.
- **Closure / `nonlocal`**: an inner function that remembers outer variables / the keyword to assign to them.
- **LEGB**: the name lookup order.

## 7. Common mistakes

- **Forgetting `return`.**
- **Mutable defaults** (`[]`, `{}`, `set()`) as parameter defaults.
- **Calling the function you meant to pass:** `retry(3, fetch_orders())` runs it immediately; pass `fetch_orders`.
- **Long lambdas.** If it needs more than one short expression, use `def`.
- **Assigning to an outer variable without `nonlocal`**, which raises `UnboundLocalError`.
- **Boolean positional flags** (`send(msg, True, False)`). Make them keyword-only.

## 8. Check your understanding

1. What does a Python function return if it has no `return` statement?
2. Rewrite `def notify(user, urgent=False)` so that `notify(u, True)` is an error but `notify(u, urgent=True)` works.
3. Why does `def f(x, seen=set())` misbehave, and how do you fix it?
4. How would you pass "a block" to a Python function that retries an API call?
5. In `make_counter`, what happens if you remove the `nonlocal count` line?

<details>
<summary>Answers</summary>

1. `None`.
2. `def notify(user, *, urgent=False):`
3. The `set()` is created once and shared by every call, so items "leak" between calls. Use `seen=None` and create a new set inside when it is `None`.
4. Pass a function object: `retry(3, fetch_orders)` or `retry(3, lambda: client.get("/orders"))`.
5. `count += 1` makes `count` a local variable of `increment`, so reading it before assignment raises `UnboundLocalError`.

</details>

## 9. Go deeper (optional)

- The Python Tutorial: [Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions) and "More on Defining Functions".
- Python docs: [`functools`](https://docs.python.org/3/library/functools.html) (`partial`, `lru_cache`, `cache`, `wraps`).
- *Fluent Python*, 2nd ed., chapter 7 ("Functions as First-Class Objects") and chapter 9 ("Decorators and Closures").
