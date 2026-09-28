# 01 · HTTP clients: requests and httpx

<!-- nav:top -->
[Course home](../../README.md) › [Step 6 plan](../../steps/06-applied-python.md) › [Step 6 lessons](00-start-here.md) · [Glossary](../../GLOSSARY.md)
<!-- nav:end -->

## 1. In one sentence

**`requests`** is the classic, simple, synchronous HTTP client for Python (like Faraday or HTTParty), and **`httpx`** is its modern successor with the same feel plus **async support**, HTTP/2 and a built-in way to test apps in memory; `kb-api` uses httpx.

## 2. Why it exists

`kb-api` ingests documents from GitHub, and in Step 7 your agent talks to model APIs. Every such call can be slow, fail, or be rate-limited. You need a client that:

- reuses connections (a **client object**, not one-off calls),
- has **timeouts** (the default in `requests` is to wait forever),
- can make **many requests concurrently** without threads (httpx with `async`),
- is easy to **mock in tests** (respx for httpx, lesson 10).

You will still meet `requests` in scripts, tutorials and older code, so you should know both.

## 3. Rails analogy

| Ruby | requests | httpx |
|---|---|---|
| `Faraday.get(url)` | `requests.get(url, timeout=10)` | `httpx.get(url, timeout=10)` |
| `conn = Faraday.new(url:, headers:)` (reused) | `requests.Session()` | `httpx.Client(base_url=..., headers=...)` |
| `response.status` / `response.body` | `r.status_code` / `r.text` | same |
| `JSON.parse(response.body)` | `r.json()` | same |
| `raise_error` middleware | `r.raise_for_status()` | same |
| Concurrent requests with threads / `async` gem | threads | `httpx.AsyncClient` + `asyncio.gather` |
| WebMock | `responses` library | `respx` |

## 4. How it works

### Use a client object, and always set a timeout

```python
import httpx

with httpx.Client(
    base_url="https://api.github.com",
    headers={"Authorization": f"Bearer {token}", "X-GitHub-Api-Version": "2022-11-28"},
    timeout=httpx.Timeout(10.0, connect=5.0),
) as client:
    response = client.get("/repos/rails/solid_queue/contents/")
    response.raise_for_status()            # raise httpx.HTTPStatusError on 4xx/5xx
    files = [f for f in response.json() if f["name"].endswith(".md")]
```

A client keeps a **connection pool**: calls to the same host reuse TCP/TLS connections, which is much faster than new connections per request. The `with` block closes the pool at the end.

### Errors you must handle

| Situation | What you get | What to do |
|---|---|---|
| Slow server | `httpx.TimeoutException` | Retry a few times with backoff, then give up |
| Network down, DNS failure | `httpx.ConnectError` / `httpx.TransportError` | Retry, then report |
| 404 | status 404 (`raise_for_status` raises `HTTPStatusError`) | Usually not retryable; skip or report |
| 403 / 429 rate limit (GitHub) | status 403/429 with `x-ratelimit-remaining: 0`, `x-ratelimit-reset` or `retry-after` headers | Wait until the reset time, or slow down |
| 5xx | status 500-599 | Retry with backoff |

### Sync vs async

- **Sync** (`httpx.Client`, `requests`): each call blocks until the response arrives. Fine for scripts and for one call at a time.
- **Async** (`httpx.AsyncClient`): `await client.get(...)` pauses only that task; other tasks run meanwhile. With `asyncio.gather` you can have many requests in flight at once, in **one thread** (lesson 02 explains how).

Limit concurrency with an `asyncio.Semaphore`: without it, fetching 500 files starts 500 requests at once, which trips rate limits.

## 5. Minimal working example

This example downloads the READMEs of eight Rails-ecosystem repositories three ways and compares the time. It uses `raw.githubusercontent.com`, which needs no token.

Create `fetch_readmes.py`:

```python
import asyncio
import time

import httpx
import requests

REPOS = [
    "rails/solid_queue", "rails/solid_cache", "rails/solid_cable", "basecamp/kamal",
    "rails/propshaft", "rails/importmap-rails", "hotwired/turbo-rails", "rails/mission_control-jobs",
]
URL = "https://raw.githubusercontent.com/{repo}/main/README.md"


def with_requests() -> int:
    total = 0
    with requests.Session() as session:  # reuse connections
        for repo in REPOS:
            response = session.get(URL.format(repo=repo), timeout=10)
            response.raise_for_status()
            total += len(response.text)
    return total


def with_httpx_sync() -> int:
    with httpx.Client(timeout=10) as client:
        return sum(len(client.get(URL.format(repo=r)).raise_for_status().text) for r in REPOS)


async def with_httpx_async(max_in_flight: int = 4) -> int:
    limit = asyncio.Semaphore(max_in_flight)  # never more than 4 requests at once

    async with httpx.AsyncClient(timeout=10) as client:

        async def fetch(repo: str) -> int:
            async with limit:
                response = await client.get(URL.format(repo=repo))
                response.raise_for_status()
                return len(response.text)

        sizes = await asyncio.gather(*(fetch(repo) for repo in REPOS))
    return sum(sizes)


for label, run in [
    ("requests, sequential", with_requests),
    ("httpx sync, sequential", with_httpx_sync),
    ("httpx async, 4 at a time", lambda: asyncio.run(with_httpx_async())),
]:
    started = time.perf_counter()
    characters = run()
    print(f"{label:<26} {characters:>7,} characters in {time.perf_counter() - started:.2f}s")
```

```bash
uv add requests httpx
uv run python fetch_readmes.py
```

Output from one real run (timings depend on your network; the character count depends on the current READMEs):

```
requests, sequential       149,804 characters in 1.19s
httpx sync, sequential     149,804 characters in 0.73s
httpx async, 4 at a time   149,804 characters in 0.61s
```

This run was on a fast, low-latency connection, so the async gain is small. The async version wins because up to four downloads wait on the network **at the same time**, so the gain grows with the number of calls and with how slow each one is. On a typical laptop connection to GitHub, or with 100 files, expect a much bigger difference. That is exactly the situation of `kb-api`'s ingestion and of Step 7's model calls (each takes seconds). Try `max_in_flight=1` and `8` and compare.

In `kb-api`, put the GitHub calls in `services/github_client.py`, with one `httpx.AsyncClient` created at startup (in the app's `lifespan`) and reused for every request.

## 6. Key terms

- **HTTP client**: a library for making HTTP requests.
- **Session / client object**: a reusable client with a connection pool and shared settings.
- **Connection pool**: open connections kept for reuse.
- **Timeout**: how long to wait before giving up; set it on every client.
- **`raise_for_status()`**: turns 4xx/5xx responses into exceptions.
- **Rate limit**: a cap on requests per period; respect the headers.
- **`AsyncClient`**: httpx's async client, used with `await`.
- **Semaphore**: a counter that limits how many tasks enter a block at once.

## 7. Common mistakes

- **No timeout.** `requests.get(url)` without `timeout=` can hang forever.
- **A new client per request.** You lose connection reuse; create one client and share it.
- **Ignoring status codes.** A 404 page is still a "successful" HTTP call unless you check.
- **Unbounded concurrency** (`gather` over 1,000 URLs) that triggers rate limits or bans.
- **Using `requests` inside `async def`** code: it blocks the event loop (lesson 02). Use `httpx.AsyncClient`.
- **Hard-coding tokens** in code; read them from settings (lesson 05).

## 8. Check your understanding

1. Why should you create one `httpx.Client` and reuse it instead of calling `httpx.get` in a loop?
2. What happens with `requests.get(url)` if the server never answers?
3. Why was the async version faster, even though it used one thread?
4. GitHub returns 403 with `x-ratelimit-remaining: 0`. What should your ingestion do?
5. Why is calling `requests.get` inside an `async def` route a problem?

<details>
<summary>Answers</summary>

1. The client keeps a connection pool (reusing TCP/TLS connections) and shared configuration (base URL, headers, timeout), which is faster and less error-prone.
2. It waits indefinitely, because `requests` has no default timeout.
3. While one request waited for the network, the event loop started or finished others; four downloads overlapped instead of running one after another.
4. Stop, wait until the time in `x-ratelimit-reset`, then continue (or fail the sync with a clear message), and reduce concurrency.
5. `requests` blocks the thread, which freezes the event loop, so no other request to your API can be served until it finishes.

</details>

## 9. Go deeper (optional)

- [HTTPX docs](https://www.python-httpx.org/): Quickstart, Clients, Async Support, Timeouts.
- [Requests docs](https://requests.readthedocs.io/): Quickstart and "Advanced Usage" (Sessions, timeouts).
- GitHub docs: [Rate limits for the REST API](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api).

<!-- nav:bottom -->

---

[← Step 6 lessons: start here](00-start-here.md) · [Step 6 lessons](00-start-here.md) · [02 · asyncio basics →](02-asyncio-basics.md)
<!-- nav:end -->
