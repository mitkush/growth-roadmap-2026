# 08 · pgvector and vector indexes

<!-- nav:top -->
[Course home](../../README.md) › [Step 7 plan](../../steps/07-agentic-ai-engineering.md) › [Step 7 lessons](00-start-here.md) · [Glossary](../../GLOSSARY.md)
<!-- nav:end -->

## 1. In one sentence

**pgvector** is a Postgres extension that adds a `vector` column type, distance operators (such as `<=>` for cosine distance) and special indexes (**HNSW**) that make "find the nearest vectors" fast, so you can do vector search inside the database you already use.

## 2. Why it exists

After lessons 06-07 you have thousands of chunks, each with a 384-number embedding. You need to:

- store them next to the documents they belong to,
- find the 5 closest to a question vector,
- do it in milliseconds, with filters ("only runbooks", "only this source"),
- keep it transactional with the rest of your data.

Dedicated vector databases exist, but for most apps (and certainly for `kb-api`) **Postgres + pgvector** is enough, and you already know how to run, back up and migrate Postgres. No new infrastructure.

## 3. Rails analogy

pgvector is to vectors what the built-in `tsvector` + GIN index is to full-text search, or what PostGIS is to map coordinates: **a Postgres extension that adds a column type, operators and an index type**.

```ruby
# In Rails, it would look like this (with the neighbor gem, verify):
enable_extension "vector"
add_column :chunks, :embedding, :vector, limit: 384
add_index :chunks, :embedding, using: :hnsw, opclass: :vector_cosine_ops
```

Where it breaks: a B-tree index gives **exact** answers. Vector indexes (HNSW) are **approximate**: they are very fast and *almost* always return the true nearest neighbours, but not guaranteed. That is a deliberate trade-off.

## 4. How it works

### The column and the operators

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE chunks (
  id           bigserial PRIMARY KEY,
  document_id  bigint NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  position     int NOT NULL,
  heading_path text NOT NULL,
  body         text NOT NULL,
  embedding    vector(384) NOT NULL        -- dimension must match the model
);
```

| Operator | Distance | Use with |
|---|---|---|
| `<=>` | **Cosine distance** (1 − cosine similarity) | Text embeddings (the usual choice) |
| `<->` | Euclidean (L2) distance | Some image/geometry uses |
| `<#>` | Negative inner product | Normalised vectors, when you want max speed |

A vector search is just `ORDER BY distance LIMIT k`:

```sql
SELECT id, heading_path, embedding <=> $1 AS distance
FROM chunks
ORDER BY embedding <=> $1
LIMIT 5;
```

### Exact search vs an index

Without an index, Postgres computes the distance to **every row**, then sorts: exact, but slower as the table grows. On this course's test machine, with 20,000 rows of 384 dimensions:

```
Limit (actual time=14.637..14.641 rows=5 loops=1)
  ->  Sort (actual time=14.634..14.635 rows=5 loops=1)
        Sort Key: ((demo_vectors.embedding <=> $0))
        Sort Method: top-N heapsort  Memory: 25kB
        ->  Seq Scan on demo_vectors (actual time=0.007..12.835 rows=20000 loops=1)
Execution Time: 14.677 ms
```

Read it bottom-up: a **Seq Scan** read all 20,000 rows (12.8 ms), then a **Sort** kept the top 5. Now with an HNSW index:

```
Limit (actual time=2.398..2.411 rows=5 loops=1)
  ->  Index Scan using demo_vectors_hnsw on demo_vectors (actual time=2.397..2.407 rows=5 loops=1)
        Order By: (embedding <=> $0)
Execution Time: 2.433 ms
```

An **Index Scan** found the 5 nearest directly: 6× faster here, and the gap grows with table size (exact search time grows with the number of rows; HNSW grows very slowly).

### How HNSW works (intuition)

**HNSW** stands for *Hierarchical Navigable Small World*. Think of how you would find a street in an unfamiliar country:

1. Start on the **motorway network** (few roads, long jumps): get to the right region quickly.
2. Switch to **main roads**: get to the right town.
3. Switch to **local streets**: find the exact house.

HNSW builds exactly this: several **layers** of a graph in which each vector is linked to some of its near neighbours. The top layer has few vectors with long links; the bottom layer has every vector with short links.

```mermaid
flowchart TB
  subgraph L2["Layer 2 (few points, long links)"]
    A2((A)) --- F2((F))
  end
  subgraph L1["Layer 1"]
    A1((A)) --- C1((C)) --- F1((F)) --- H1((H))
  end
  subgraph L0["Layer 0 (every point, short links)"]
    A0((A)) --- B0((B)) --- C0((C)) --- D0((D)) --- E0((E)) --- F0((F)) --- G0((G)) --- H0((H))
  end
  A2 -.-> A1
  F2 -.-> F1
  A1 -.-> A0
  C1 -.-> C0
  F1 -.-> F0
  H1 -.-> H0
```

A search starts at the top, greedily moves to whichever neighbour is closer to the query, drops a layer, and repeats. It checks a few hundred vectors instead of all of them. Because it is greedy, it can occasionally miss a true neighbour: that is the "approximate" part.

### The settings that matter

| Setting | When | Default | Effect |
|---|---|---|---|
| `m` | Index build | 16 | Links per node. Higher = better recall, bigger index. |
| `ef_construction` | Index build | 64 | Candidates considered while building. Higher = better index, slower build. |
| `hnsw.ef_search` | Query time (`SET hnsw.ef_search = 100`) | 40 | Candidates checked per query. Higher = better recall, slower query. **Must be ≥ your LIMIT.** |

Start with the defaults. If your retrieval eval shows the index missing results that exact search finds, raise `ef_search`.

**The index must match the operator.** An index built with `vector_cosine_ops` is used only for `<=>`. On the same table, a query with `<->` (L2) ignores it and falls back to a Seq Scan (16.3 ms on the test machine). The operator classes are `vector_cosine_ops` (`<=>`), `vector_l2_ops` (`<->`) and `vector_ip_ops` (`<#>`).

### IVFFlat, the other index type

pgvector also has **IVFFlat**, which groups vectors into clusters and searches only the nearest clusters. It builds faster and uses less memory, but it needs data in the table before you create it and usually gives lower recall. **Use HNSW** unless you have a specific reason not to.

### Filters and approximate search

`WHERE source_id = 3 ORDER BY embedding <=> $1 LIMIT 5` can return **fewer than 5 rows** with HNSW: the index finds the nearest `ef_search` candidates first, then the filter removes some. If you filter heavily, raise `ef_search`, or enable iterative index scans in pgvector 0.8+ (`SET hnsw.iterative_scan = relaxed_order`, verify for your version).

## 5. Minimal working example

Start Postgres with pgvector (the same image your Step 6 `compose.yaml` uses):

```bash
docker run -d --name pgv -e POSTGRES_PASSWORD=postgres -p 5433:5432 pgvector/pgvector:pg17
```

### Part A: SQL you can paste into `psql`

```bash
docker exec -it pgv psql -U postgres
```

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE toy_chunks (id bigserial PRIMARY KEY, body text NOT NULL, embedding vector(3));
INSERT INTO toy_chunks (body, embedding) VALUES
 ('Solid Queue stores background jobs in PostgreSQL', '[0.9, 0.1, 0.0]'),
 ('Retrying failed jobs with Solid Queue',            '[0.8, 0.3, 0.1]'),
 ('Kamal deploys Docker containers to your servers',  '[0.1, 0.9, 0.2]'),
 ('Set SOLID_QUEUE_IN_PUMA to run jobs inside Puma',  '[0.5, 0.5, 0.1]');

CREATE INDEX ON toy_chunks USING hnsw (embedding vector_cosine_ops);

SELECT id, left(body, 40) AS body,
       round((embedding <=> '[0.85, 0.2, 0.05]')::numeric, 4) AS cosine_distance
FROM toy_chunks
ORDER BY embedding <=> '[0.85, 0.2, 0.05]'
LIMIT 3;
```

Output:

```
 id |                   body                   | cosine_distance
----+------------------------------------------+-----------------
  1 | Solid Queue stores background jobs in Po |          0.0089
  2 | Retrying failed jobs with Solid Queue    |          0.0098
  4 | Set SOLID_QUEUE_IN_PUMA to run jobs insi |          0.1515
```

(With 4 rows, Postgres will not bother using the index; it only pays off on bigger tables, as the 20,000-row plans above show.)

### Part B: the same thing from Python with SQLAlchemy (async)

The `pgvector` Python package adds a `Vector` column type and distance methods to SQLAlchemy. Create `pgvector_demo.py`:

```python
import asyncio

from pgvector.sqlalchemy import Vector
from sqlalchemy import BigInteger, Index, Text, select, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5433/postgres"


class Base(DeclarativeBase):
    pass


class DemoChunk(Base):
    __tablename__ = "demo_chunks"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    body: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(Vector(3))  # use Vector(384) for bge-small

    __table_args__ = (
        Index(
            "ix_demo_chunks_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )


async def main() -> None:
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with Session() as session:
        session.add_all([
            DemoChunk(body="Solid Queue stores jobs in PostgreSQL", embedding=[0.9, 0.1, 0.0]),
            DemoChunk(body="Kamal deploys Docker containers", embedding=[0.1, 0.9, 0.2]),
        ])
        await session.commit()

        query_vector = [0.85, 0.2, 0.05]
        distance = DemoChunk.embedding.cosine_distance(query_vector)  # renders as <=>
        stmt = select(DemoChunk.body, distance.label("distance")).order_by(distance).limit(2)
        for body, dist in (await session.execute(stmt)).all():
            print(f"{dist:.4f}  {body}")
    await engine.dispose()


asyncio.run(main())
```

```bash
uv run python pgvector_demo.py
```

Output:

```
0.0089  Solid Queue stores jobs in PostgreSQL
0.6610  Kamal deploys Docker containers
```

In `kb-api` you will put the `CREATE EXTENSION` and the table/index in an **Alembic migration** rather than `create_all` (Step 6, lesson on Alembic).

## 6. Key terms

- **pgvector**: Postgres extension for vectors.
- **`vector(n)`**: column type holding n-dimension vectors.
- **`<=>`, `<->`, `<#>`**: cosine distance, L2 distance, negative inner product.
- **Exact (brute-force) search**: compare against every row; always correct.
- **ANN (approximate nearest neighbour)**: fast search that may occasionally miss a true neighbour.
- **HNSW**: layered-graph ANN index; pgvector's recommended index.
- **IVFFlat**: cluster-based ANN index; faster to build, usually lower recall.
- **Operator class** (`vector_cosine_ops`): tells the index which distance it serves.
- **`m`, `ef_construction`, `ef_search`**: HNSW build and query settings.

## 7. Common mistakes

- **Index and query use different operators** (`vector_cosine_ops` index, `<->` query): the index is ignored.
- **Wrong dimension**: `vector(1536)` with a 384-dimension model fails on insert.
- **Testing on 10 rows** and concluding "the index is not used". Postgres correctly prefers a Seq Scan on tiny tables.
- **`ef_search` lower than `LIMIT`**: you can get fewer rows than you asked for.
- **Heavy `WHERE` filters with HNSW** returning too few results; raise `ef_search` or use iterative scans.
- **Forgetting `CREATE EXTENSION vector`** in migrations, or using a Postgres image without pgvector installed.
- **Building the index row by row during a huge import.** For big backfills, load data first, then create the index.

## 8. Check your understanding

1. In the two plans above, what replaced the `Seq Scan` + `Sort`, and why is it faster?
2. What does "approximate" mean for HNSW, and which setting improves accuracy at query time?
3. Your index uses `vector_cosine_ops`. A teammate writes `ORDER BY embedding <-> $1`. What happens?
4. Why might `WHERE source_id = 3 ... LIMIT 5` return 3 rows with an HNSW index?
5. Why is Postgres + pgvector a good default for `kb-api` instead of a separate vector database?

<details>
<summary>Answers</summary>

1. An `Index Scan using demo_vectors_hnsw` with `Order By: (embedding <=> $0)`. It walks the HNSW graph and checks a small number of candidates instead of computing the distance to every row.
2. It can occasionally miss a true nearest neighbour because the graph search is greedy. `hnsw.ef_search` (more candidates per query) improves recall at some speed cost.
3. The index is not used (it only serves `<=>`); Postgres does a sequential scan with L2 distance, which is slower and ranks by a different measure.
4. The index returns the nearest `ef_search` candidates first; the filter then removes those from other sources, leaving fewer than 5.
5. It keeps vectors next to the documents, transactional, with filters and joins, using infrastructure and skills you already have; at this scale it is fast enough.

</details>

## 9. Go deeper (optional)

- [pgvector README](https://github.com/pgvector/pgvector): operators, HNSW/IVFFlat options, filtering, performance tuning.
- [pgvector-python](https://github.com/pgvector/pgvector-python): SQLAlchemy, psycopg and asyncpg integration.
- Paper (optional, advanced): Malkov & Yashunin, "Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs" (2016).

<!-- nav:bottom -->

---

[← 07 · Chunking](07-chunking.md) · [Step 7 lessons](00-start-here.md) · [09 · Full-text, vector and hybrid search →](09-full-text-vector-and-hybrid-search.md)
<!-- nav:end -->
