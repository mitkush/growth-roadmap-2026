# shop-lab performance results

Machine: <CPU, RAM> · Ruby <version> · Rails <version> · PostgreSQL <version> · seed scale <1.0>
Load tool: `oha -z 30s -c 16 --no-tui <url>` after a 10 s warm-up · RAILS_ENV=production

## Step 1: runtime

| Change | Endpoint | req/s | p50 | p95 | p99 | RSS (MB) | Notes |
|---|---|---|---|---|---|---|---|
| Baseline | /products | | | | | | |
| Baseline | /reports/sales | | | | | | |
| Baseline | /slow_io | | | | | | |

## Step 2: database

| Query (short) | Before: mean ms | After: mean ms | Change | Plan change |
|---|---|---|---|---|
