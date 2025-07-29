# chquery: Async ClickHouse Python Client

`chquery` is an async Python client and query builder for ClickHouse, built on top of [asynch](https://github.com/long2ice/asynch). It provides a simple, high-level API for querying ClickHouse asynchronously, with a convenient query builder. Used by myself for most of my data analytics since the beginning of 2025.

## Features
- Async connection pool management
- High-level query builder (select, filters, order, limit, insert, etc.)
- Raw SQL execution
- Custom error handling
- Batch insert and async iteration for large result sets
- Type hints and docstrings for easy development

## Installation

Install `chquery`:

```bash
pip install git+https://github.com/filipnyquist/chquery.git
```

## Usage Example

```python
import asyncio
from chquery import CHDriver, DbError

async def main():
    driver = CHDriver(dsn="clickhouse://user:pass@localhost/default")
    await driver.startup()
    try:
        # Simple query
        rows = await driver.fetch_all("SELECT * FROM my_table LIMIT 10")
        print(rows)

        # Using the query builder
        qb = driver.qb("my_table").fields(["id", "name"]).filters({"id[gt]": 10}).order_by(["-id"]).limit(5)
        results = await qb.all()
        print(results)

        # Insert data
        await driver.qb("my_table").insert({"id": 123, "name": "Alice"})

        # Check if a row exists
        exists = await driver.qb("my_table").filters({"id[eq]": 123}).exists()
        print("Exists:", exists)

        # Count rows
        count = await driver.qb("my_table").count()
        print("Count:", count)

        # Async iteration for large results
        async for row in driver.qb("my_table").all_iter(batch_size=100):
            print(row)
    except DbError as e:
        print("Database error:", e)
    finally:
        await driver.shutdown()

asyncio.run(main())
```

## API Overview

### CHDriver
- `startup()` / `shutdown()` / `close()`
- `fetch_all(query, *args)` / `fetch_one(query, *args)`
- `insert_many(query, data)`
- `raw(query, *args, fetch='all')`
- `ping()`
- `qb(table)` — returns a `CHQueryBuilder`

### CHQueryBuilder
- `fields(list)`
- `filters(dict)` — supports `[eq]`, `[ne]`, `[lt]`, `[lte]`, `[gt]`, `[gte]`, `[in]`, `[like]`, `[isnull]`
- `order_by(list)`
- `limit(n)` / `offset(n)`
- `all()` / `one()` / `count()` / `exists()`
- `all_iter(batch_size=1000)` — async generator
- `insert(data)`
- `reset()`

## License
MIT
