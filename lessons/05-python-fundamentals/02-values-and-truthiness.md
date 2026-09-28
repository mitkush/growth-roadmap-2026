# 02 · Values, strings, truthiness and equality

## 1. In one sentence

Python's basic values (numbers, strings, `None`, booleans) look like Ruby's, but **truthiness**, **equality vs identity**, **integer division** and **indentation as syntax** work differently enough to cause real bugs.

## 2. Why it exists

Most early Python bugs from Rubyists are not about big concepts. They are small, silent differences:

- `if user.orders_count:` is false when the count is `0` (in Ruby, `0` is truthy).
- `x == None` works but is wrong; `x is None` is the idiom.
- `7 / 2` is `3.5`, not `3`.
- Forgetting a colon or mis-indenting a line changes which block the code belongs to.

Learning these on day one saves hours later.

## 3. Rails analogy

| Ruby | Python | Note |
|---|---|---|
| `nil` | `None` | A single object; compare with `is` |
| `true` / `false` | `True` / `False` | Capitalised |
| `"Hi #{name}"` | `f"Hi {name}"` | f-string; any expression inside `{}` |
| `name.upcase`, `.strip`, `.split(",")` | `name.upper()`, `.strip()`, `.split(",")` | Methods need `()` in Python |
| `name.empty?` | `not name` or `len(name) == 0` | No `?` methods |
| `"abc".frozen?` | strings are **always** immutable | |
| `7 / 2 # => 3` | `7 / 2 # 3.5`, `7 // 2 # 3` | `//` is floor division |
| `a.equal?(b)` | `a is b` | Same object |
| `a == b` | `a == b` | Equal value |
| `if x ... end` | `if x:` + indented block | No `end`; indentation is the block |
| `# comment` | `# comment` | Same |
| `puts x` / `p x` | `print(x)` / `print(repr(x))` | |

## 4. How it works

### Indentation is syntax

```python
if count > 10:
    print("many")   # inside the if (4 spaces)
    notify()        # still inside
print("done")       # outside: runs always
```

There is no `end`. The block is whatever is indented under the line ending in `:`. Use 4 spaces (ruff format does this for you).

### Truthiness

In Ruby, only `nil` and `false` are falsy. In Python, **empty and zero values are falsy** too:

| Value | Ruby | Python |
|---|---|---|
| `nil` / `None` | falsy | falsy |
| `false` / `False` | falsy | falsy |
| `0`, `0.0` | **truthy** | **falsy** |
| `""` | **truthy** | **falsy** |
| `[]`, `{}` | **truthy** | **falsy** |
| `"0"`, `" "`, `[0]` | truthy | truthy |

This makes `if items:` a neat way to say "if the list is not empty". It also creates bugs when `0` or `""` is a valid value:

```python
def discount_label(percent: int | None) -> str:
    if percent:              # BUG: 0 is treated like "no discount given"
        return f"{percent}% off"
    return "no discount"

def discount_label_fixed(percent: int | None) -> str:
    if percent is not None:  # only None means "missing"
        return f"{percent}% off"
    return "no discount"
```

### Equality vs identity

- `==` compares **values** (calls `__eq__`, like Ruby's `==`).
- `is` compares **identity**: is it the very same object (like Ruby's `equal?`).
- Use `is` only for singletons: `None`, `True`, `False`. For everything else, use `==`.

### Mutable vs immutable, and names

Python variables are **names that point to objects**, exactly as in Ruby. Assignment never copies:

```python
a = [1, 2]
b = a        # b points to the same list
b.append(3)
print(a)     # [1, 2, 3]
```

Some types are **immutable**: `int`, `float`, `str`, `tuple`, `frozenset`, `bool`, `None`. "Changing" them creates a new object. Others are **mutable**: `list`, `dict`, `set` and most objects you create.

### Numbers

- `int` has no size limit (like Ruby's Integer).
- `/` always returns a `float`; `//` is floor division; `%` is modulo; `**` is power.
- For money, do not use `float`: use integer cents (as in Rails) or `decimal.Decimal`.

### Strings

- Single and double quotes are the same: `'hi' == "hi"`.
- f-strings support formatting: `f"{price:.2f}"`, `f"{count:,}"`, `f"{name!r}"` (the `repr`, like Ruby's `inspect`).
- Triple quotes `"""..."""` make multi-line strings (like a heredoc).
- Strings are immutable, and there are no `!` bang methods: `s.upper()` returns a new string.

## 5. Minimal working example

Create `basics.py`:

```python
from decimal import Decimal

# 1. Truthiness: the values Ruby treats as true but Python treats as false.
for value in [None, False, 0, 0.0, "", [], {}, "0", [0]]:
    print(f"{value!r:>6} -> {'truthy' if value else 'falsy'}")

# 2. The classic bug and its fix.
def discount_label(percent: int | None) -> str:
    if percent is not None:
        return f"{percent}% off"
    return "no discount"

print(discount_label(0), "|", discount_label(None))

# 3. == vs is.
a = [1, 2]
b = [1, 2]
print("a == b:", a == b, "| a is b:", a is b, "| a is a:", a is a)

# 4. Names point to objects; assignment does not copy.
c = a
c.append(3)
print("a after c.append(3):", a)

# 5. Numbers.
print(7 / 2, 7 // 2, 7 % 2, 2**100)
print(0.1 + 0.2, Decimal("0.1") + Decimal("0.2"))

# 6. Strings and f-string formatting.
name, price, visits = "  Solid Queue ", 1234.5, 1234567
print(f"[{name.strip().upper()}] £{price:,.2f} visits={visits:,} repr={name!r}")
```

```bash
uv run python basics.py
```

Output:

```
  None -> falsy
 False -> falsy
     0 -> falsy
   0.0 -> falsy
    '' -> falsy
    [] -> falsy
    {} -> falsy
   '0' -> truthy
   [0] -> truthy
0% off | no discount
a == b: True | a is b: False | a is a: True
a after c.append(3): [1, 2, 3]
3.5 3 1 1267650600228229401496703205376
0.30000000000000004 0.3
[SOLID QUEUE] £1,234.50 visits=1,234,567 repr='  Solid Queue '
```

Before moving on, explain each line to yourself. For example: `0.1 + 0.2` is not exactly `0.3` (like in Ruby); `Decimal` fixes that; `2**100` just works because `int` has no size limit.

## 6. Key terms

- **`None`**: Python's `nil`.
- **Truthiness**: whether a value counts as true in a condition.
- **`is` / `==`**: identity / equality.
- **Mutable / immutable**: can / cannot be changed in place.
- **f-string**: formatted string literal, `f"..."`.
- **`repr`**: the developer-facing representation (`!r` in f-strings), like `inspect`.
- **Floor division (`//`)**: division rounded down to an integer.

## 7. Common mistakes

- **`if count:` when `0` is a valid value.** Use `if count is not None:`.
- **`x == None`.** Use `x is None` (ruff rule `E711`).
- **Using `is` to compare strings or numbers.** It may appear to work for small values and then fail.
- **Expecting `/` to give an integer.**
- **Floats for money.**
- **Mixing tabs and spaces**, or wrong indentation after an `if`.
- **Forgetting `()`**: `name.upper` is the method object, not the result.

## 8. Check your understanding

1. Which of these are falsy in Python: `0`, `"0"`, `[]`, `[None]`, `" "`, `{}`?
2. Why is `if percent:` a bug for a discount that can be 0%?
3. What does `a is b` check, and when should you use `is`?
4. What do `9 / 4`, `9 // 4` and `9 % 4` return?
5. After `x = [1]; y = x; y += [2]`, what is `x`? Why?

<details>
<summary>Answers</summary>

1. `0`, `[]`, `{}`. (`"0"`, `[None]` and `" "` are non-empty, so truthy.)
2. `0` is falsy, so a real 0% discount is treated as "no discount". Use `is not None`.
3. Whether both names point to the very same object. Use it for `None`, `True`, `False` only.
4. `2.25`, `2`, `1`.
5. `[1, 2]`. `y` and `x` point to the same list, and `+=` on a list modifies it in place.

</details>

## 9. Go deeper (optional)

- The Python Tutorial: [An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html) and [More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html).
- Python docs: [Truth Value Testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing).
- *Fluent Python*, 2nd ed., chapter 6 ("Object References, Mutability, and Recycling").
