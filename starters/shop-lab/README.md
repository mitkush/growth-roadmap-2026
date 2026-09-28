# shop-lab starter kit (Steps 1-3)

`shop-lab` is a small Rails 8 API with **realistic data volumes** and three deliberately slow endpoints, so Steps 1-3 have something real to measure and fix. This folder does not contain a whole Rails app; it contains the files to **add to a fresh `rails new` app**, plus the exact commands.

Tested with Ruby 3.3, Rails 8.1 and PostgreSQL 16. Full-size seeding took about 40 seconds on the test machine.

## What you get

| Piece | Purpose | Used in |
|---|---|---|
| 5 models: `Customer`, `Product`, `Order`, `LineItem`, `Event` | A small shop plus an analytics table | Steps 1-3 |
| `db/seeds.rb` | 20k customers, 20k products, 200k orders, 600k line items, 2M events (via SQL `generate_series`: fast) | Steps 1-2 |
| `GET /products` | Has an **N+1** (a `SUM` query per product) | Steps 1-2 |
| `GET /reports/sales` | **CPU- and allocation-heavy** Ruby aggregation over 50k rows | Step 1 (profiling) |
| `GET /slow_io` | Calls a slow upstream service (**I/O-bound**, releases the GVL) | Step 1 (threads) |
| `script/slow_server.rb` | The slow upstream: answers every request after 100 ms | Step 1 |
| `script/load.rb` | A small load generator (req/s, p50/p95/p99) if you do not have `oha` or `wrk` | Steps 1-2 |
| `config/environments/benchmark.rb` | Production-like settings over plain HTTP with one database, for local benchmarks | Steps 1-2 |
| `perf/results.md` | The results table to fill in | Steps 1-2 |

Deliberately **missing indexes** (on `orders.status`, `orders.placed_at`, `events.occurred_at`) are part of the Step 2 exercise.

## Set up (about 15 minutes)

```bash
# 1. A new Rails 8 API app with PostgreSQL
rails new shop-lab --api -d postgresql
cd shop-lab

# 2. Models (the generators create migrations; the kit's model files replace the generated ones)
bin/rails g model Customer name:string email:string:uniq
bin/rails g model Product name:string sku:string:uniq price_cents:integer category:string
bin/rails g model Order customer:references status:string total_cents:integer placed_at:datetime
bin/rails g model LineItem order:references product:references quantity:integer unit_price_cents:integer
bin/rails g model Event name:string payload:jsonb occurred_at:datetime

# 3. Copy the kit's files over the app (adjust the path to where you cloned the roadmap)
cp -r ~/code/growth-roadmap-2026/starters/shop-lab/files/. .

# 4. Profiling and benchmarking gems (development and benchmark only)
bundle add memory_profiler vernier stackprof benchmark-ips --group "development, benchmark"

# 5. Database and data
bin/rails db:create db:migrate
bin/rails db:seed                    # or SEED_SCALE=0.1 bin/rails db:seed for a quick 10% version
```

Then add a `benchmark` environment to two config files (the kit already contains `config/environments/benchmark.rb`):

```yaml
# Append to config/database.yml
benchmark:
  <<: *default
  database: shop_lab_development

# Append to config/cable.yml
benchmark:
  adapter: async
```

## Run it

Three terminals:

```bash
# Terminal 1: the slow upstream service
ruby script/slow_server.rb

# Terminal 2: the app, production-like (eager loading, no reloading), 3 Puma threads (Rails' default)
RAILS_ENV=benchmark bin/rails server

# Terminal 3: check the endpoints, then load test
curl -s localhost:3000/products | head -c 200
curl -s localhost:3000/reports/sales | head -c 200
curl -s localhost:3000/slow_io
ruby script/load.rb http://127.0.0.1:3000/slow_io 16 15
```

With [oha](https://github.com/hatoo/oha) installed, the equivalent load test is `oha -z 15s -c 16 --no-tui http://127.0.0.1:3000/slow_io`.

## Results from the test machine

For orientation only (4 cores, Ruby 3.3.6, Rails 8.1.4, PostgreSQL 16, full seed). Your numbers will differ; the **shape** of the results is what matters.

```
== RAILS_MAX_THREADS=3
/slow_io  c=16  10s  requests=294  errors=0  req/s=29.4  p50=557.4ms  p95=657.0ms  p99=668.4ms
/reports/sales  c=4  15s  requests=12  errors=0  req/s=0.8  p50=5616.3ms  p95=7837.2ms  p99=11151.9ms
== RAILS_MAX_THREADS=16
/slow_io  c=16  10s  requests=1465  errors=0  req/s=146.5  p50=108.2ms  p95=118.7ms  p99=128.2ms
/reports/sales  c=4  15s  requests=12  errors=0  req/s=0.8  p50=6583.9ms  p95=7705.6ms  p99=9253.9ms
```

More threads made the I/O-bound endpoint 5× faster and did nothing for the CPU-bound one. [Step 1 lesson 01](../../lessons/01-advanced-ruby/01-gvl-threads-and-thread-safety.md) explains why.

## Notes

- The data is random but reproducible in shape; re-running `db:seed` truncates and re-creates everything.
- Do not deploy the `benchmark` environment; it exists only for local measurement.
- In Step 3 you move models into packs (`packs/catalog`, `packs/ordering`); see [Step 3 lesson 01](../../lessons/03-architecture/01-bounded-contexts-and-packwerk.md).
