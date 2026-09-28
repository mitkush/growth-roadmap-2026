# Step 1: Advanced Ruby: Concurrency, YJIT & Profiling

| Weight | Dates | Hours |
|---|---|---|
| 10% | Mon 28 Sep - Sun 4 Oct 2026 | ~10 h |

**Versions:** Ruby 3.4 (notes for Ruby 4.0 where relevant), Rails 8.x, Puma 6+ (or whatever your work app uses).

## What you will learn this step

This week you look underneath your Rails apps: how Ruby runs threads (and why some endpoints get faster with more Puma threads while others do not), what Fibers and Ractors are for, what YJIT and the garbage collector do, and how to find exactly where time and memory go with profilers. Everything is measured on a sample app with realistic data, [`shop-lab`](../starters/shop-lab/README.md), so every claim you make ends with a before/after number. The lessons in [`lessons/01-advanced-ruby/`](../lessons/01-advanced-ruby/00-start-here.md) explain each concept with Rails examples and real output.

## 1. Objective

By the end of this week you will be able to:

- Explain exactly what the GVL does and does not protect, and predict whether threads, Fibers, processes or Ractors will speed up a given workload.
- Choose Puma worker and thread counts (and the matching DB pool size) from measurements, not rules of thumb.
- Turn YJIT on, confirm it is working with runtime stats, and measure its CPU and memory cost on a real app.
- Read `GC.stat`, reduce allocations in a hot path, and decide when GC tuning or jemalloc is worth it.
- Profile CPU, wall time and memory of a Rails endpoint with Vernier, stackprof and memory_profiler, and turn the result into a fix with before/after numbers.

## 2. Why it matters

- Most Rails performance work is **I/O wait, allocation and configuration**, not clever algorithms. Engineers who can measure and explain this are rare and valuable.
- Wrong Puma/pool settings cause real incidents: connection pool timeouts, memory bloat and poor p99 latency.
- YJIT is on by default in new Rails apps on Ruby 3.3+. You should be able to prove its value (or its memory cost) on your own app.
- Profiling skills carry over to Python (Step 5-6) and to AI tools (Step 7-8), where latency and cost are central.

## 3. Day-by-day plan

Set up the sample app on Monday with the **[shop-lab starter kit](../starters/shop-lab/README.md)** (models, seed data for 2.8M rows, the three endpoints, a slow upstream server, a load generator and a production-like `benchmark` environment). If you can use a staging copy of your work app, use it instead for the measurements; the tasks stay the same.

| Day | Topic | Concrete tasks | Hours |
|---|---|---|---|
| **Mon 28 Sep** | Setup + GVL model | **Read first:** [00 Start here](../lessons/01-advanced-ruby/00-start-here.md), [01 GVL and threads](../lessons/01-advanced-ruby/01-gvl-threads-and-thread-safety.md) (sections 1-4).<br>1. Build `shop-lab` with the [starter kit](../starters/shop-lab/README.md) (about 15 minutes, including full-size seeding). 2. Run the lesson's `gvl_demo.rb` (CPU vs I/O with 1 and 4 threads) and record the timings. 3. Read the Ruby docs for `Thread` and `Thread::Queue`. | 1.5 |
| **Tue 29 Sep** | Threads in practice | **Read first:** [01 GVL and threads](../lessons/01-advanced-ruby/01-gvl-threads-and-thread-safety.md) (section 5, Part B, and "Common mistakes").<br>1. Run `race_demo.rb`; then write your own race (unsynchronised `@counter += 1`, lazy `@cache \|\|=`) and fix it with `Mutex` and `Concurrent::Map`. 2. Build a producer/consumer with `Thread::Queue` and a fixed pool of 4 workers. 3. Write 5 lines in your log: "What the GVL protects and what it does not". | 1.5 |
| **Wed 30 Sep** | Fibers, scheduler, Ractors | **Read first:** [02 Fibers and Ractors](../lessons/01-advanced-ruby/02-fibers-and-ractors.md).<br>1. Run `fibers_demo.rb` against `script/slow_server.rb`; compare sequential, threads and `async` fibers. 2. Run `ractor_demo.rb` on your Ruby version and compare with the lesson's result. 3. Note 3 limits of Ractors (shareable objects, gem support, experimental status). | 1.25 |
| **Thu 1 Oct** | Puma + baseline benchmark | **Read first:** [03 Puma and benchmarking](../lessons/01-advanced-ruby/03-puma-and-benchmarking.md).<br>1. Start `ruby script/slow_server.rb` and `RAILS_ENV=benchmark bin/rails server`. 2. Load test each endpoint (`/products`, `/reports/sales`, `/slow_io`) with `oha -z 30s -c 16` (or the kit's `ruby script/load.rb URL 16 30`) after a 10 s warm-up; record req/s, p50, p95, p99 and RSS in `perf/results.md`. This is your **baseline**. 3. Check one result against Little's Law. | 1.25 |
| **Fri 2 Oct** | YJIT | **Read first:** [04 YJIT](../lessons/01-advanced-ruby/04-yjit.md).<br>1. Confirm YJIT state: `RubyVM::YJIT.enabled?` in `bin/rails runner`. 2. Benchmark the 3 endpoints with `YJIT=0` and with YJIT on (the kit's benchmark environment reads `YJIT`). 3. Collect `RubyVM::YJIT.runtime_stats` after warm-up and note the ratio in YJIT and code memory. 4. Send the weekly update. | 1 |
| **Sat 3 Oct** | Profiling lab + GC + memory | **Read first:** [06 Profiling](../lessons/01-advanced-ruby/06-profiling.md), [05 GC and memory](../lessons/01-advanced-ruby/05-gc-and-memory.md).<br>1. Profile `/reports/sales` with Vernier; open it in the Firefox Profiler and find the top 3 hot frames (compare with the lesson's stackprof report). 2. Profile allocations with `memory_profiler`; find the top allocation sites. 3. Fix the hot path (the lesson's `pluck` version is a first step; aggregating in SQL is better). 4. Tune Puma: test (workers × threads) = (2×3), (2×5), (4×3) on `/slow_io` and `/reports/sales`; set the DB pool to match. 5. Try `MALLOC_ARENA_MAX=2` (or jemalloc); record RSS after 5 min of load. Re-run all benchmarks. | 2.5 |
| **Sun 4 Oct** | Consolidate + proof | **Read first:** [05 GC and memory](../lessons/01-advanced-ruby/05-gc-and-memory.md), "`GC.stat`: your dashboard" (review).<br>1. Run `GC.stat` before/after a load test; note minor/major GC counts and time (`GC.stat(:time)`, in milliseconds). 2. Finish `perf/results.md` (tables + 3 conclusions). 3. Answer the self-check questions in writing. 4. 20 min: OSS issue scouting (see Step 4). | 1 |
| | | **Total** | **10** |

## 4. Topic checklist

**Concurrency model**
- [ ] GVL: can explain when it is released (blocking I/O, `sleep`, some C extensions) and show a CPU vs I/O benchmark that proves it.
- [ ] Thread safety: can reproduce and fix a race on shared state; knows why `||=` memoisation in class-level state is unsafe.
- [ ] `Mutex`, `Thread::Queue`, `ConditionVariable`: can use each correctly in a small program.
- [ ] concurrent-ruby basics (`Concurrent::Map`, thread pools): knows it is already a Rails dependency and when to use it.
- [ ] Fibers and the Fiber scheduler: can explain cooperative scheduling and demonstrate the `async` gem for concurrent I/O.
- [ ] Ractors: can explain isolation and shareable objects, run a demo, and state why they are not used in Rails apps today.
- [ ] Processes vs threads: can explain copy-on-write, Puma cluster mode and why workers bypass the GVL.

**Runtime and memory**
- [ ] Puma sizing: can choose `WEB_CONCURRENCY` and `RAILS_MAX_THREADS` from measurements and explain the latency vs throughput trade-off.
- [ ] DB pool: can explain why pool size must be ≥ threads per process and how total connections = processes × pool.
- [ ] YJIT: can enable it, read `runtime_stats`, and report its CPU gain and memory cost.
- [ ] GC: can read `GC.stat` (`count`, `minor_gc_count`, `major_gc_count`, `heap_live_slots`, `total_allocated_objects`) and explain generational GC.
- [ ] Allocation reduction: can find allocation hot spots and cut them (frozen strings, avoiding intermediate arrays, `pluck`/SQL instead of loading objects).
- [ ] Memory fragmentation: can explain why RSS grows without a Ruby leak and demonstrate the effect of jemalloc or `MALLOC_ARENA_MAX`.
- [ ] Nice to have: GC env vars (`RUBY_GC_HEAP_*`) and the `autotuner` gem's suggestions.

**Profiling and measurement**
- [ ] Benchmark method: warm-up, fixed duration, percentiles, same machine, one change at a time.
- [ ] `benchmark-ips` for micro-benchmarks: can compare two implementations with confidence intervals.
- [ ] Vernier: can capture a profile and read GVL/GC activity on the timeline.
- [ ] stackprof: can produce a flamegraph and compare `:cpu` vs `:wall` mode.
- [ ] memory_profiler: can read "allocated by location" and "retained" reports.
- [ ] rack-mini-profiler (dev) and derailed_benchmarks (`derailed bundle:mem`): knows when each is the right tool.

## 5. Hands-on lab: "Make `shop-lab` faster, and prove it"

**Setup:** `shop-lab` (or a staging copy of your work app) with seeded data and the 3 endpoints from Thursday.

**Tasks**
1. Record a baseline for all 3 endpoints: req/s, p50, p95, p99 and RSS after 5 minutes of load.
2. Apply changes **one at a time**, re-measuring after each:
   - YJIT on vs off.
   - Puma: at least 3 worker × thread combinations.
   - Hot-path fix in `/reports/sales` found with Vernier/memory_profiler.
   - jemalloc or `MALLOC_ARENA_MAX=2`.
3. Record every run in `perf/results.md` using this table:

| Change | Endpoint | req/s | p50 | p95 | p99 | RSS (MB) | Notes |
|---|---|---|---|---|---|---|---|

4. Add a `perf/README.md` with exact commands, machine specs, Ruby/Rails versions and the seed size, so anyone can reproduce the results.

**Acceptance criteria**
- [ ] Baseline and final numbers exist for all 3 endpoints, with commands to reproduce.
- [ ] `/reports/sales` p95 improves by **at least 30%** or allocations per request drop by **at least 40%** (show the memory_profiler totals before and after).
- [ ] You can explain, in two sentences each, why `/slow_io` scales with threads and `/reports/sales` does not.
- [ ] A Vernier profile screenshot (before and after) is in the repo.
- [ ] The chosen Puma config is committed with a comment explaining the numbers behind it.

## 6. Deliverable / proof of completion

Send your manager:
1. **Link to a PR** in `shop-lab` (or an internal PR on your work app) containing `perf/results.md`, the Puma config change and the hot-path fix.
2. **A 5-line summary** in the weekly update: the biggest win (with numbers), the YJIT result, the chosen Puma config and one recommendation for the work app.
3. Optional but strong: one ticket raised for the work app based on a finding (for example "enable jemalloc in the Docker image").

## 7. Curated resources

1. **Lessons for this step**: [`lessons/01-advanced-ruby/`](../lessons/01-advanced-ruby/00-start-here.md) and the [shop-lab starter kit](../starters/shop-lab/README.md) (start here).
2. **Ruby docs: `Thread`, `Thread::Queue`, `Fiber`, `Ractor`**: https://docs.ruby-lang.org/en/3.4/ (use the class pages; Ractor guide: `ractor.md` in the same docs).
3. **YJIT documentation** (options, stats, memory): https://github.com/ruby/ruby/blob/master/doc/jit/yjit.md
4. **Vernier** (sampling profiler with GVL/GC markers): https://github.com/jhawthorn/vernier
5. **memory_profiler**: https://github.com/SamSaffron/memory_profiler and **stackprof**: https://github.com/tmm1/stackprof
6. **Puma docs: deployment and threads/workers**: https://github.com/puma/puma/blob/main/docs/deployment.md
7. **Nate Berkopec, *The Complete Guide to Rails Performance*** (sections on memory, Puma and profiling). Paid book; chapter names vary by edition (verify).
8. **Jean Boussier (byroot) blog**, posts on the GVL and Puma/thread sizing: https://byroot.github.io/ (verify the specific post titles).
9. **derailed_benchmarks**: https://github.com/zombocom/derailed_benchmarks

## 8. Self-check questions

1. A job calls three external APIs, each taking 300 ms. Would threads, Fibers or processes cut its time most, and why? What changes if each call also does 200 ms of JSON parsing?
2. Your app has 4 Puma workers with 5 threads each, and Solid Queue with 3 workers × 5 threads. How many Postgres connections can it open at peak? What happens when the DB `max_connections` is 100?
3. Why can raising Puma threads **lower** p99 latency for one endpoint but **raise** it for another?
4. YJIT made the app 15% faster but RSS grew by 60 MB per worker. How do you decide whether to keep it?
5. What is the difference between "allocated" and "retained" objects in memory_profiler, and which one matters for GC pressure?
6. Why can a Ruby process's RSS keep growing even though `GC.stat[:heap_live_slots]` is flat?
7. When would a CPU profile (`:cpu`) and a wall-time profile (`:wall`) of the same endpoint show different hot spots?
8. Give two reasons why Ractors are not a drop-in way to use all CPU cores in a Rails app.
9. How would you prove that a performance improvement is real and not noise?
10. Where in a Rails app is class-level memoisation (`@@cache ||=` or `class << self; @x ||=`) a thread-safety risk, and how would you fix it?

## 9. Common pitfalls

- **Benchmarking in development mode** (code reloading, no eager loading). Always use `RAILS_ENV=production` with `config.eager_load = true`.
- **Changing several things at once**, so you cannot tell which change helped.
- **Reporting averages instead of percentiles.** Users feel p95/p99.
- **Forgetting warm-up.** YJIT needs to compile hot code first; the first seconds are slower.
- **Raising threads without raising the DB pool**, which moves the bottleneck to `ActiveRecord::ConnectionTimeoutError`.
- **Assuming "thread-safe because of the GVL".** The GVL does not make `+=` or `||=` atomic in your code.
- **Tuning GC env vars before cutting allocations.** Fewer allocations beat any GC setting.
- **Profiling with the profiler's own overhead in the numbers.** Profile to find hot spots; benchmark without the profiler to measure gains.

## 10. Stretch goals

- Try **ZJIT** (experimental in Ruby 4.0) on the same benchmark and compare with YJIT (`ruby --zjit` or `RubyVM::ZJIT.enable`; see [lesson 04](../lessons/01-advanced-ruby/04-yjit.md)).
- Run the `autotuner` gem (Shopify) against `shop-lab` under load and evaluate its GC suggestions.
- Serve `shop-lab` with **Falcon** (Fiber-based server) and compare `/slow_io` throughput with Puma.
- Take a heap dump with `ObjectSpace.dump_all` and find the largest retained object types.
- Measure GVL wait time per request with the `gvltools` gem (Shopify; Ruby 3.2+): `GVLTools::LocalTimer.enable` once, then compare `GVLTools::LocalTimer.monotonic_time` (nanoseconds this thread waited for the GVL) before and after a request. High wait time means threads are queueing for the GVL ([lesson 01](../lessons/01-advanced-ruby/01-gvl-threads-and-thread-safety.md)).
