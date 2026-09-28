# Step 3: Rails Architecture: Modular Monolith & Observability

<!-- nav:top -->
[Course home](../README.md) · Step 3 of 8 · [Step 3 lessons](../lessons/03-architecture/00-start-here.md) · [Glossary](../GLOSSARY.md)
<!-- nav:end -->

| Weight | Dates | Hours |
|---|---|---|
| 10% | Mon 12 Oct - Sun 18 Oct 2026 | ~10 h |

**Versions:** Rails 8.1 (for `Rails.event`), Packwerk 3.x + packwerk-extensions, OpenTelemetry Ruby SDK.

## What you will learn this step

This week turns `shop-lab` from a fast app into a well-structured, observable one. You will split it into business modules (bounded contexts) inside the same Rails app and let Packwerk enforce the boundaries; publish events that are never lost or processed twice using the transactional outbox; design an API that behaves correctly when clients retry, page through changing data or send too much; and trace one request from HTTP through the database into a background job with OpenTelemetry. You will also write your decisions down as ADRs. The lessons in [`lessons/03-architecture/`](../lessons/03-architecture/00-start-here.md) explain each idea with tested code and real output.

## 1. Objective

By the end of this week you will be able to:

- Find domain boundaries in an existing Rails app, draw a context map, and enforce two boundaries with Packwerk.
- Design events inside a monolith that are not lost or duplicated, using the transactional outbox pattern and idempotent consumers.
- Design a JSON API that handles pagination, retries (idempotency keys), errors (RFC 9457) and rate limits correctly.
- Instrument a Rails app with OpenTelemetry so you can follow one request from HTTP through the database and into a background job, and correlate traces with logs.
- Write clear Architecture Decision Records (ADRs) and a one-page design doc.

## 2. Why it matters

- Most Rails teams do not need microservices; they need a monolith with **clear boundaries**. Knowing how to create those boundaries is a core senior/staff skill.
- Events that are lost or duplicated cause subtle production bugs (double emails, missing webhooks). The outbox pattern is the standard fix.
- Good API design reduces support load and makes clients (mobile, partners, AI agents in Step 7-8) reliable.
- Observability is what lets you debug production quickly. OpenTelemetry is the vendor-neutral standard, so the skill carries across employers and tools.
- Written design decisions (ADRs) are visible proof of senior-level thinking.

## 3. Day-by-day plan

Continue in `shop-lab`. Target contexts: **Catalog** (products), **Ordering** (orders, line items), **Billing** (payments), **Customers**.

| Day | Topic | Concrete tasks | Hours |
|---|---|---|---|
| **Mon 12 Oct** | Boundaries + ADRs | **Read first:** [00 Start here](../lessons/03-architecture/00-start-here.md), [01 Bounded contexts and Packwerk](../lessons/03-architecture/01-bounded-contexts-and-packwerk.md) (sections 1-4), [05 ADRs and design docs](../lessons/03-architecture/05-adrs-and-design-docs.md).<br>1. List every model and the models it references; draw a context map (Mermaid) with the 4 contexts. 2. Mark each cross-context call (e.g. `Order` reading `Product#price`). 3. Write `docs/adr/0001-modular-monolith-with-packwerk.md` (Context, Decision, Consequences). 4. Read the Packwerk README and "Resolving violations" docs. | 1.5 |
| **Tue 13 Oct** | Packwerk | **Read first:** [01 Bounded contexts and Packwerk](../lessons/03-architecture/01-bounded-contexts-and-packwerk.md) (section 5 onwards).<br>1. Add `packwerk` and `packwerk-extensions` (privacy checker); `bundle binstub packwerk`, then `bin/packwerk init`. 2. Move Catalog and Ordering into `packs/catalog` and `packs/ordering` (add their `app/*` paths to autoload, or use `packs-rails`). 3. Enable `enforce_dependencies` and privacy; run `bin/packwerk check`. 4. Fix 2 violations by adding a small public API (e.g. `Catalog::PriceLookup.for(product_ids)`); record the rest with `update-todo`. | 1.5 |
| **Wed 14 Oct** | Events + outbox | **Read first:** [02 Events and the transactional outbox](../lessons/03-architecture/02-events-and-outbox.md).<br>1. Emit `order.placed` with `Rails.event.notify` (Rails 8.1) and subscribe to it; compare with `ActiveSupport::Notifications`. 2. Create an `outbox_events` table; write the event **in the same transaction** as the order. 3. Add a Solid Queue job that publishes unsent rows with `FOR UPDATE SKIP LOCKED` and marks them sent. 4. Add a consumer (e.g. "reserve stock") that is idempotent via a unique `event_id` in a `processed_events` table. | 1.5 |
| **Thu 15 Oct** | API design | **Read first:** [03 API design](../lessons/03-architecture/03-api-design.md).<br>1. Build `GET /api/v1/orders` with **cursor** pagination (`created_at, id` keyset) and `POST /api/v1/orders` with an `Idempotency-Key` header (store key + response hash). 2. Return errors as RFC 9457 problem details (`type`, `title`, `status`, `detail`). 3. Add Rails `rate_limit` to `create`. 4. Document both endpoints with rswag (OpenAPI). | 1.25 |
| **Fri 16 Oct** | OpenTelemetry setup | **Read first:** [04 OpenTelemetry for Rails](../lessons/03-architecture/04-opentelemetry.md) (sections 1-5, Part A-B).<br>1. Run `grafana/otel-lgtm` (or Jaeger all-in-one) in Docker. 2. Add `opentelemetry-sdk`, `opentelemetry-exporter-otlp`, `opentelemetry-instrumentation-all`; configure in `config/initializers/opentelemetry.rb` with `c.use_all` (Active Job `propagation_style: :child` to keep jobs in the request's trace) and a service name. 3. Confirm spans for Rack, Active Record and Active Job. 4. Send the weekly update. | 1 |
| **Sat 17 Oct** | Observability lab | **Read first:** [04 OpenTelemetry for Rails](../lessons/03-architecture/04-opentelemetry.md) (Part C, and sections 6-8).<br>1. Add a custom span around the outbox publisher and consumer with attributes (`event.type`, `order.id`). 2. Confirm that one trace covers HTTP → DB → job → consumer. 3. Switch logs to structured JSON with `trace_id` and `span_id`; jump from a log line to its trace. 4. Build a small dashboard: request rate, error rate, p95 duration (RED) and outbox lag. 5. Write a one-page design doc for the event flow (use the ADR as a starting point). | 2.5 |
| **Sun 18 Oct** | Consolidate + proof | **Read first:** [05 ADRs and design docs](../lessons/03-architecture/05-adrs-and-design-docs.md) (the example ADR); the glossary in [00 Start here](../lessons/03-architecture/00-start-here.md).<br>1. Write ADR-0002 (outbox) and ADR-0003 (API conventions). 2. Self-check questions. 3. Pick your OSS issue shortlist (Step 4). 4. Outline **Blog post #1** with the template. | 0.75 |
| | | **Total** | **10** |

## 4. Topic checklist

**Modular monolith**
- [ ] Bounded contexts and context maps: can split a real app into contexts and defend the split.
- [ ] Packwerk: can set up packs, dependency and privacy checks, and a todo list for existing violations.
- [ ] Public APIs for packs: can design a small interface that hides models from other packs.
- [ ] Trade-offs: can compare Packwerk packs, Rails engines and separate services (cost, isolation, deploys).
- [ ] Nice to have: knows `packs-rails` and the "Ruby at Scale" tooling from Gusto.

**Event-driven patterns**
- [ ] In-process events: can use `ActiveSupport::Notifications` and Rails 8.1 `Rails.event`, and explain their differences.
- [ ] `after_commit` vs in-transaction publishing: can explain the dual-write problem.
- [ ] Transactional outbox: can implement it with Postgres and Solid Queue.
- [ ] Idempotent consumers: can make a handler safe to run twice.
- [ ] Delivery guarantees: can explain at-most-once, at-least-once and why "exactly once" is really "at least once + idempotency".
- [ ] Event versioning: can explain how to evolve an event schema without breaking consumers.

**API design**
- [ ] Resource modelling and status codes: can design consistent endpoints and choose correct codes (201, 202, 409, 422, 429).
- [ ] Cursor (keyset) pagination: can implement it and explain why offset pagination breaks at scale.
- [ ] Idempotency keys: can implement safe retries for `POST`.
- [ ] Errors: can return RFC 9457 problem details consistently.
- [ ] Versioning and deprecation: can explain URL vs header versioning and a deprecation process.
- [ ] Rate limiting: can use Rails `rate_limit` and explain its storage (cache store) limits.

**Observability**
- [ ] OpenTelemetry concepts: traces, spans, attributes, context propagation, exporters, OTLP, collector.
- [ ] Ruby SDK: can auto-instrument Rails and add custom spans.
- [ ] Trace propagation into background jobs: can show one trace across web and job.
- [ ] Structured logging with trace correlation.
- [ ] RED/USE metrics and SLOs: can define an SLO (e.g. "99% of `POST /orders` < 300 ms") and an alert for it.
- [ ] Sampling: can explain head vs tail sampling and cost trade-offs.

**Communication**
- [ ] ADRs: can write a short ADR with context, options, decision and consequences.

## 5. Hands-on lab: "Order placed, end to end"

**Scenario:** When an order is placed via the API, the app must reserve stock and send a confirmation email exactly once in effect, and you must be able to see the whole flow in one trace.

**Tasks**
1. `POST /api/v1/orders` with `Idempotency-Key` creates an order and an outbox row in one transaction.
2. The publisher job sends `order.placed`; two consumers (stock reservation, email) process it idempotently.
3. Packwerk shows Ordering depending on Catalog only through its public API.
4. OpenTelemetry shows one trace from the HTTP request to both consumers.
5. Chaos test: kill the job process mid-publish, restart, and confirm no event is lost or processed twice (count rows).

**Acceptance criteria**
- [ ] Sending the same `POST` twice with the same key returns the same response and creates **one** order.
- [ ] The chaos test shows 0 lost and 0 double-processed events over 100 orders.
- [ ] `bin/packwerk check` passes (with a todo file for old violations) and runs in CI.
- [ ] A trace screenshot shows HTTP, SQL, job and consumer spans linked together.
- [ ] Every log line for the request includes the `trace_id`.
- [ ] 3 ADRs and a one-page design doc are in `docs/`.

## 6. Deliverable / proof of completion

1. **PR link** in `shop-lab` with packs, outbox, API and OpenTelemetry setup.
2. **`docs/adr/`** with 3 ADRs, plus the one-page design doc (link in the weekly update).
3. **Screenshot** of the end-to-end trace and the RED dashboard.
4. **One paragraph** for your manager: which boundary or observability idea could help the work app, and a first small step.

## 7. Curated resources

1. **Course lessons for this step**: [`lessons/03-architecture/`](../lessons/03-architecture/00-start-here.md) (start here; each lesson ends with its own "Go deeper" links).
2. **Packwerk** (README, USAGE, resolving violations): https://github.com/Shopify/packwerk and **packwerk-extensions**: https://github.com/rubyatscale/packwerk-extensions
3. **Ruby at Scale** (Gusto's modularisation guides and tools): https://github.com/rubyatscale (verify current doc site)
4. **Vlad Khononov, *Learning Domain-Driven Design*** (O'Reilly, 2021): Part I, chapters 1-4 (strategic design, bounded contexts).
5. **Martin Kleppmann, *Designing Data-Intensive Applications***: chapter 7 (Transactions) and chapter 11 (Stream Processing) in the 1st edition (chapter numbers may differ in the 2nd edition, verify).
6. **Transactional outbox pattern** (Chris Richardson): https://microservices.io/patterns/data/transactional-outbox.html
7. **OpenTelemetry Ruby docs** (getting started, instrumentation, exporters): https://opentelemetry.io/docs/languages/ruby/
8. **RFC 9457, Problem Details for HTTP APIs**: https://www.rfc-editor.org/rfc/rfc9457
9. **Rails 8.1 release notes** (structured event reporting, `Rails.event`): https://guides.rubyonrails.org/8_1_release_notes.html

## 8. Self-check questions

1. How did you decide where the boundary between Ordering and Catalog goes? What evidence would make you move it?
2. Packwerk reports 300 violations in a legacy app. What is your plan for the first month?
3. Why is publishing an event in `after_commit` still not fully reliable? What does the outbox add?
4. Your consumer sends an email and then records the event as processed, but it crashes in between. What happens and how do you make it safe?
5. Why does offset pagination give wrong results when rows are inserted during paging? How does a keyset cursor fix it?
6. Two requests with the same idempotency key arrive at the same moment. How does your implementation avoid creating two orders?
7. What is the difference between a trace, a span and a log, and when is each the best tool?
8. Tracing every request is too expensive. How would you sample while still catching slow and failed requests?
9. When would you recommend extracting a service from the monolith instead of adding a pack?
10. What makes an ADR useful a year later, and what makes it useless?

## 9. Common pitfalls

- **Drawing boundaries around technical layers** (models, services) instead of business capabilities.
- **Using Packwerk as a goal** instead of a tool; a pack full of cross-pack calls is not a module.
- **Publishing events inside the transaction to an external system** (the dual-write problem), or in `after_save` instead of `after_commit`.
- **Idempotency by "check then insert"** without a unique constraint, which races under load.
- **Leaking internal models in APIs** (serialising Active Record objects directly), which freezes your schema.
- **High-cardinality attributes in metrics** (user IDs as labels), which explode metric storage cost.
- **Adding tracing without log correlation**, so engineers still search logs by timestamp.

## 10. Stretch goals

- Rebuild the order flow with **Rails Event Store** (`rails_event_store` gem: stores events in database tables and gives you publish/subscribe, event streams and asynchronous handlers) and compare it with your outbox from [lesson 02](../lessons/03-architecture/02-events-and-outbox.md).
- Add an **OpenTelemetry Collector** with tail-based sampling (keep all errors and slow traces).
- Enforce API contracts in CI by validating responses against the rswag OpenAPI file.
- Extract `packs/billing` as a Rails engine and compare the developer experience with a Packwerk pack.
- Write a short internal tech-talk from your ADRs (15 minutes).

<!-- nav:bottom -->

---

[← Step 2: Rails at Scale: PostgreSQL, Solid Queue & Kamal](02-rails-at-scale.md) · [Step 3 lessons](../lessons/03-architecture/00-start-here.md) · [Step 4: Open-Source Contribution to the Ruby Ecosystem →](04-open-source-contribution.md)
<!-- nav:end -->
