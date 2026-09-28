# Step 2: Rails at Scale: PostgreSQL, Solid Queue & Kamal

<!-- nav:top -->
[Course home](../README.md) · Step 2 of 8 · [Step 2 lessons](../lessons/02-rails-at-scale/00-start-here.md) · [Glossary](../GLOSSARY.md)
<!-- nav:end -->

| Weight | Dates | Hours |
|---|---|---|
| 10% | Mon 5 Oct - Sun 11 Oct 2026 | ~10 h |

**Versions:** PostgreSQL 16+ (17 or 18 preferred), Rails 8.x, Solid Queue 1.x, Kamal 2.x.

## What you will learn this step

This week is about the database, which is the real bottleneck in most Rails apps. You will find the queries that cost the most with `pg_stat_statements`, read their `EXPLAIN ANALYZE` plans line by line, fix them with the right index, and remove N+1 queries. Then you look at locks: why a 50 ms migration can take a site down, and how to write migrations that cannot. Finally you meet the Rails 8 infrastructure around Postgres: partitioning and read replicas, Solid Queue (jobs stored in the database, claimed with `SKIP LOCKED`) and Kamal (deploying containers to your own server). The lessons in [`lessons/02-rails-at-scale/`](../lessons/02-rails-at-scale/00-start-here.md) explain each concept with real plans and output from `shop-lab`.

## 1. Objective

By the end of this week you will be able to:

- Find the most expensive queries with `pg_stat_statements`, read `EXPLAIN (ANALYZE, BUFFERS)` output, and fix them with the right index or query change, with before/after timings.
- Explain Postgres row locks, lock queues and deadlocks, and write migrations that do not block production traffic.
- Choose between pessimistic locks, optimistic locking and `SKIP LOCKED` for a given concurrency problem.
- Set up read replicas with Rails multi-DB and automatic role switching, and explain when sharding (and partitioning) is and is not worth it.
- Run Solid Queue in production shape (separate DB, recurring jobs, concurrency limits, dashboard) and deploy a Rails 8 app with Kamal 2.

## 2. Why it matters

- In most Rails apps, **the database is the bottleneck**. Fixing one query often beats any Ruby-level optimisation.
- Blocking migrations and lock contention are among the most common causes of Rails outages.
- Rails 8's "Solid" stack and Kamal remove Redis and PaaS dependencies. Teams are adopting them now, and someone has to understand their failure modes.
- These skills are expected of senior Rails engineers and come up in every system design discussion.

## 3. Day-by-day plan

Continue in `shop-lab` from Step 1 (or your work app's staging copy). The [starter kit](../starters/shop-lab/README.md) already seeds the `events` table (2M rows) for the partitioning task and leaves out the indexes you will add.

| Day | Topic | Concrete tasks | Hours |
|---|---|---|---|
| **Mon 5 Oct** | Find slow queries | **Read first:** [00 Start here](../lessons/02-rails-at-scale/00-start-here.md), [01 Finding slow queries and EXPLAIN](../lessons/02-rails-at-scale/01-finding-slow-queries-and-explain.md).<br>1. Enable `pg_stat_statements` (`shared_preload_libraries`, `CREATE EXTENSION`). 2. Run the Step 1 load test, then list the top 10 queries by `total_exec_time`. 3. For the top 3, run `EXPLAIN (ANALYZE, BUFFERS)` and paste the plans into explain.dalibo.com. 4. For each, note: scan type, estimated vs actual rows, buffers read vs hit. | 1.5 |
| **Tue 6 Oct** | Indexes + N+1 | **Read first:** [02 Indexes, N+1 and batching](../lessons/02-rails-at-scale/02-indexes-and-n-plus-one.md).<br>1. Fix the top 3 queries: one composite index (column order matters), one partial index (e.g. `WHERE status = 'pending'`), one covering index (`INCLUDE`). Use `algorithm: :concurrently` with `disable_ddl_transaction!`. 2. Record timings before/after. 3. Turn on `strict_loading` for `Order` in dev; fix the N+1s it finds with `includes`/`preload`; count queries per request before/after. | 1.5 |
| **Wed 7 Oct** | Locking + safe migrations | **Read first:** [03 Locks and safe migrations](../lessons/02-rails-at-scale/03-locks-and-safe-migrations.md).<br>1. In two `rails console` sessions, reproduce: a row lock wait (`with_lock`), a deadlock (two rows locked in opposite order) and an optimistic lock conflict (`lock_version`). 2. Reproduce a **lock queue**: open a long transaction, run `ALTER TABLE ... ADD COLUMN ... DEFAULT` in another session, then a simple `SELECT` in a third; watch `pg_locks`/`pg_stat_activity`. 3. Add `strong_migrations`; set `lock_timeout` and `statement_timeout` for migrations. | 1.5 |
| **Thu 8 Oct** | Partitioning + multi-DB | **Read first:** [04 Partitioning, replicas and sharding](../lessons/02-rails-at-scale/04-partitioning-and-multi-db.md).<br>1. Create `events_partitioned` with range partitioning by month (SQL migration, switch to `structure.sql`); copy data; compare `EXPLAIN` for a one-month query (look for partition pruning). 2. Run `bin/rails g active_record:multi_db`; configure a `primary_replica` (use a read-only DB user on the same DB, or a real replica via Docker if you have time); enable automatic role switching; prove reads go to the replica in logs. | 1.25 |
| **Fri 9 Oct** | Solid Queue (and Solid Cache/Cable) | **Read first:** [05 Solid Queue internals](../lessons/02-rails-at-scale/05-solid-queue-internals.md).<br>1. Confirm the `queue` DB in `config/database.yml`; run `bin/jobs`. 2. Add one recurring job in `config/recurring.yml` and one job with `limits_concurrency`. 3. Mount Mission Control – Jobs (API-only apps also need `propshaft`; see lesson 05); trigger failures and retry them. 4. Enqueue jobs before starting `bin/jobs` and inspect the `solid_queue_*` tables, then kill a worker mid-job and find the failed execution (lesson 05, section 5). 5. Skim Solid Cache and Solid Cable configs. 6. Send the weekly update. | 1 |
| **Sat 10 Oct** | Kamal deploy lab | **Read first:** [06 Kamal architecture](../lessons/02-rails-at-scale/06-kamal-architecture.md).<br>1. Get a small VPS (any provider, ~2 GB RAM) or a local VM. 2. Fill `config/deploy.yml` and `.kamal/secrets`; add Postgres as an **accessory**. 3. `kamal setup`, then `kamal deploy`. 4. Run Solid Queue inside Puma (`SOLID_QUEUE_IN_PUMA`) or as a separate role. 5. Do a second deploy with a migration and observe zero-downtime switching by kamal-proxy. 6. Run a short load test against the deployed app. | 2.5 |
| **Sun 11 Oct** | Consolidate + proof | **Read first:** the glossary in [00 Start here](../lessons/02-rails-at-scale/00-start-here.md); re-read the "Check your understanding" sections of lessons 01-06.<br>1. Finish `perf/db-report.md` (query table, lock experiments, partition result). 2. Self-check questions. 3. 20 min: OSS scouting (look at `rails/solid_queue` and `basecamp/kamal` issues). | 0.75 |
| | | **Total** | **10** |

## 4. Topic checklist

**PostgreSQL performance**
- [ ] `pg_stat_statements`: can find top queries by total and mean time and explain why total time matters more.
- [ ] `EXPLAIN (ANALYZE, BUFFERS)`: can read node types (Seq Scan, Index Scan, Index Only Scan, Bitmap Heap Scan, Nested Loop, Hash Join), spot bad row estimates and explain buffer hits vs reads.
- [ ] Index design: can choose column order for composite indexes, and use partial, covering (`INCLUDE`) and GIN indexes appropriately.
- [ ] Knows index costs: write amplification, bloat, unused indexes (`pg_stat_user_indexes`).
- [ ] Statistics: can explain `ANALYZE`, autovacuum and why stale stats cause bad plans.

**Active Record at scale**
- [ ] N+1: can use `strict_loading`, and explain `includes` vs `preload` vs `eager_load`.
- [ ] Batching: `in_batches`, `insert_all`/`upsert_all`, and when callbacks/validations are skipped.
- [ ] `load_async`: can explain when parallel queries help and how they use the pool.
- [ ] Connection pooling: can explain PgBouncer transaction mode and its caveats (prepared statements, session state, advisory locks).

**Locking and migrations**
- [ ] Row locks (`lock`, `with_lock`), optimistic locking (`lock_version`) and `SKIP LOCKED`: can choose the right one for a scenario.
- [ ] Deadlocks: can reproduce one and explain how consistent lock ordering prevents it.
- [ ] Lock queues: can explain why a waiting `ACCESS EXCLUSIVE` lock blocks later reads.
- [ ] Safe migrations: `CREATE INDEX CONCURRENTLY`, `lock_timeout`, adding columns and constraints safely (`NOT VALID` then `VALIDATE`), backfilling in batches; uses `strong_migrations`.

**Scaling data**
- [ ] Multi-DB: can configure replicas with `connects_to` and automatic role switching, and explain replica lag risks.
- [ ] Partitioning: can create a range-partitioned table and show partition pruning in a plan.
- [ ] Sharding: can explain Rails horizontal sharding (`connects_to shards:`) and when it is justified. Nice to have: demo in stretch goals.

**Rails 8 infrastructure**
- [ ] Solid Queue: can explain its tables, polling, `SKIP LOCKED`, recurring tasks, concurrency controls and how to monitor it.
- [ ] Solid Cache / Solid Cable: can explain their trade-offs vs Redis (disk-backed, bigger cache, higher latency per read).
- [ ] Kamal 2: can explain kamal-proxy, roles, accessories, secrets and how a zero-downtime deploy works.

## 5. Hands-on lab: "A tuned, safely migrated, deployed `shop-lab`"

**Tasks**
1. Tune the 3 slowest queries from `pg_stat_statements`, one change at a time.
2. Write one risky migration (e.g. adding an index and a `NOT NULL` column on `orders`) and rewrite it in a safe form that passes `strong_migrations`.
3. Partition `events` by month and show the query-time change for a one-month query.
4. Configure a replica and prove that GET requests read from it.
5. Deploy with Kamal, with Solid Queue running a recurring job in production.

**Record results in `perf/db-report.md`:**

| Query (short) | Before: mean ms | After: mean ms | Change | Plan change (e.g. Seq Scan → Index Only Scan) |
|---|---|---|---|---|

**Acceptance criteria**
- [ ] At least 3 queries improved; at least one improved by **≥ 10×** (common for a missing index on a large table).
- [ ] Queries per request on `/products` reduced (show the count before/after).
- [ ] The safe migration runs without blocking a concurrent `SELECT` loop (show the loop output).
- [ ] Partition pruning is visible in the `EXPLAIN` output.
- [ ] The app is reachable on the deployed URL; `kamal app logs` shows the recurring job running.
- [ ] `perf/db-report.md` includes commands, data sizes and Postgres version.

## 6. Deliverable / proof of completion

1. **PR link** in `shop-lab` with indexes, the safe migration, partitioning, multi-DB config, Solid Queue config and `config/deploy.yml` (no secrets).
2. **`perf/db-report.md`** with the before/after table.
3. **Deployed URL** (or a screenshot of `kamal deploy` and Mission Control if you shut the server down to save cost).
4. One recommendation for the work app (for example "add `strong_migrations`" or "these 2 indexes are unused").

## 7. Curated resources

1. **Course lessons for this step**: [`lessons/02-rails-at-scale/`](../lessons/02-rails-at-scale/00-start-here.md) (start here; each lesson ends with its own "Go deeper" links).
2. **PostgreSQL docs: Using EXPLAIN**: https://www.postgresql.org/docs/current/using-explain.html
3. **PostgreSQL docs: Explicit Locking** (table and row lock modes): https://www.postgresql.org/docs/current/explicit-locking.html
4. **PostgreSQL docs: Table Partitioning**: https://www.postgresql.org/docs/current/ddl-partitioning.html
5. **Andrew Atkinson, *High Performance PostgreSQL for Rails*** (Pragmatic Bookshelf, 2024): chapters on indexes, query optimisation and migrations.
6. **Rails Guides: Multiple Databases with Active Record**: https://guides.rubyonrails.org/active_record_multiple_databases.html
7. **Solid Queue README** (architecture, configuration, concurrency controls): https://github.com/rails/solid_queue
8. **Kamal docs**: https://kamal-deploy.org
9. **strong_migrations** (safe-migration rules and explanations): https://github.com/ankane/strong_migrations

## 8. Self-check questions

1. `EXPLAIN ANALYZE` shows an estimated 10 rows and 400,000 actual rows at a nested loop. What went wrong, and what are your first two actions?
2. You have `WHERE customer_id = ? AND created_at > ? ORDER BY created_at DESC`. What index do you create and why in that column order?
3. Why can adding an index make the whole app slower?
4. A migration that normally takes 50 ms caused a 2-minute outage. Explain the lock queue that made this happen and how `lock_timeout` prevents it.
5. Two workers process the same order at the same time. When would you use `with_lock`, `lock_version` or `SKIP LOCKED`?
6. With automatic role switching, a user updates their profile and immediately sees the old data. Why, and how does Rails mitigate this?
7. When does partitioning make queries **slower**?
8. What does Solid Queue do with a job whose worker process was killed mid-job?
9. You move from Redis cache to Solid Cache. What gets better, what gets worse, and what would you measure?
10. How does Kamal achieve zero-downtime deploys, and what can still break during a deploy (think migrations)?

## 9. Common pitfalls

- **Running `EXPLAIN ANALYZE` on an empty dev DB.** Plans depend on data size and statistics; use realistic data.
- **Forgetting that `EXPLAIN ANALYZE` executes the query**: wrap `UPDATE`/`DELETE` in a transaction and roll back.
- **Adding an index for every slow query** without checking existing indexes and write cost.
- **Using `CREATE INDEX CONCURRENTLY` inside a transaction** (it fails); in Rails you need `disable_ddl_transaction!`.
- **Backfilling in the same migration** that changes the schema, holding locks for the whole backfill.
- **Assuming `includes` always uses one query**: it switches between `preload` and `eager_load` based on references.
- **Sizing Solid Queue threads without counting DB connections**, especially with PgBouncer.
- **Committing Kamal secrets** or registry passwords; use `.kamal/secrets` with env vars or a password manager.

## 10. Stretch goals

- Set up **horizontal sharding** with two shard databases and `connected_to(shard:)`; route by tenant ID.
- Add **PgHero** (ankane) to `shop-lab` and compare its suggestions with your own analysis.
- Add **PgBouncer** in transaction mode in front of Postgres and fix what breaks.
- Try UUIDv7 primary keys (`uuidv7()` is built into PostgreSQL 18) and compare index size with random UUIDs. UUIDv7 values start with a timestamp, so new keys land at the end of the B-tree index like `bigint` ids, while random (v4) UUIDs land anywhere and cause more page splits and a larger, less cache-friendly index ([lesson 02](../lessons/02-rails-at-scale/02-indexes-and-n-plus-one.md) explains B-trees).
- Benchmark Solid Cache vs Redis for your top cached fragment.

<!-- nav:bottom -->

---

[← Step 1: Advanced Ruby: Concurrency, YJIT & Profiling](01-advanced-ruby.md) · [Step 2 lessons](../lessons/02-rails-at-scale/00-start-here.md) · [Step 3: Rails Architecture: Modular Monolith & Observability →](03-architecture-system-design.md)
<!-- nav:end -->
