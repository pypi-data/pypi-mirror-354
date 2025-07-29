import pytest
from chquery import CHDriver

DSN = "clickhouse://default@localhost/default"


def log(msg):
    print(f"[TEST LOG] {msg}")


@pytest.mark.asyncio
async def test_create_and_delete_table():
    driver = CHDriver(dsn=DSN)
    await driver.startup()
    try:
        await driver.delete_table("test_table")
        await driver.create_table(
            "test_table",
            {"id": "Int32", "name": "String"},
            engine="MergeTree() ORDER BY id",
        )
        await driver.qb("test_table").insert({"id": 1, "name": "Alice"})
        log("test_create_and_delete_table passed")
    finally:
        await driver.delete_table("test_table")
        await driver.shutdown()


@pytest.mark.asyncio
async def test_insert_and_fetch():
    driver = CHDriver(dsn=DSN)
    await driver.startup()
    try:
        await driver.delete_table("test_table")
        await driver.create_table(
            "test_table",
            {"id": "Int32", "name": "String"},
            engine="MergeTree() ORDER BY id",
        )
        await driver.qb("test_table").insert({"id": 1, "name": "Alice"})
        await driver.qb("test_table").insert({"id": 2, "name": "Bob"})
        await driver.qb("test_table").insert(
            [{"id": 3, "name": "Charlie"}, {"id": 4, "name": "David"}]
        )
        rows = await driver.fetch_all("SELECT name FROM test_table LIMIT 5")
        assert len(rows) == 4
        names = {row["name"] for row in rows}
        assert {"Alice", "Bob", "Charlie", "David"}.issubset(names)
        log("test_insert_and_fetch passed")
    finally:
        await driver.delete_table("test_table")
        await driver.shutdown()


@pytest.mark.asyncio
async def test_querybuilder_select_and_limit():
    driver = CHDriver(dsn=DSN)
    await driver.startup()
    try:
        await driver.delete_table("test_table")
        await driver.create_table(
            "test_table",
            {"id": "Int32", "name": "String"},
            engine="MergeTree() ORDER BY id",
        )
        await driver.qb("test_table").insert(
            [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"},
                {"id": 3, "name": "Charlie"},
                {"id": 4, "name": "David"},
            ]
        )
        qb = driver.qb("test_table").fields(["id", "name"]).limit(3)
        results = await qb.all()
        assert len(results) == 3
        log("test_querybuilder_select_and_limit passed")
    finally:
        await driver.delete_table("test_table")
        await driver.shutdown()


@pytest.mark.asyncio
async def test_querybuilder_count_exists_one():
    driver = CHDriver(dsn=DSN)
    await driver.startup()
    try:
        await driver.delete_table("test_table")
        await driver.create_table(
            "test_table",
            {"id": "Int32", "name": "String"},
            engine="MergeTree() ORDER BY id",
        )
        await driver.qb("test_table").insert(
            [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"},
                {"id": 3, "name": "Charlie"},
                {"id": 4, "name": "David"},
            ]
        )
        count = await driver.qb("test_table").count()
        assert count == 4
        exists = await driver.qb("test_table").filters({"name[eq]": "Alice"}).exists()
        assert exists is True
        one = await driver.qb("test_table").filters({"id[eq]": 2}).one()
        assert one is not None and one["name"] == "Bob"
        log("test_querybuilder_count_exists_one passed")
    finally:
        await driver.delete_table("test_table")
        await driver.shutdown()


@pytest.mark.asyncio
async def test_querybuilder_filters():
    driver = CHDriver(dsn=DSN)
    await driver.startup()
    try:
        await driver.delete_table("test_table")
        await driver.create_table(
            "test_table",
            {
                "id": "Int32",
                "name": "String",
                "score": "Int32",
                "desc": "Nullable(String)",
            },
            engine="MergeTree() ORDER BY id",
        )
        await driver.qb("test_table").insert(
            [
                {"id": 1, "name": "Alice", "score": 10, "desc": None},
                {"id": 2, "name": "Bob", "score": 20, "desc": "B"},
                {"id": 3, "name": "Charlie", "score": 30, "desc": "C"},
                {"id": 4, "name": "David", "score": 40, "desc": None},
            ]
        )
        # eq
        res = await driver.qb("test_table").filters({"score[eq]": 20}).all()
        assert len(res) == 1 and res[0]["name"] == "Bob"
        # ne
        res = await driver.qb("test_table").filters({"score[ne]": 20}).all()
        assert all(r["score"] != 20 for r in res)
        # lt
        res = await driver.qb("test_table").filters({"score[lt]": 25}).all()
        assert {r["name"] for r in res} == {"Alice", "Bob"}
        # lte
        res = await driver.qb("test_table").filters({"score[lte]": 20}).all()
        assert {r["name"] for r in res} == {"Alice", "Bob"}
        # gt
        res = await driver.qb("test_table").filters({"score[gt]": 20}).all()
        assert {r["name"] for r in res} == {"Charlie", "David"}
        # gte
        res = await driver.qb("test_table").filters({"score[gte]": 20}).all()
        assert {r["name"] for r in res} == {"Bob", "Charlie", "David"}
        # in
        res = (
            await driver.qb("test_table")
            .filters({"name[in]": ["Alice", "David"]})
            .all()
        )
        assert {r["name"] for r in res} == {"Alice", "David"}
        # like
        res = await driver.qb("test_table").filters({"name[like]": "%ar%"}).all()
        assert {r["name"] for r in res} == {"Charlie"}
        # isnull True
        res = await driver.qb("test_table").filters({"desc[isnull]": True}).all()
        assert {r["name"] for r in res} == {"Alice", "David"}
        # isnull False
        res = await driver.qb("test_table").filters({"desc[isnull]": False}).all()
        assert {r["name"] for r in res} == {"Bob", "Charlie"}
        log("test_querybuilder_filters passed")
    finally:
        await driver.delete_table("test_table")
        await driver.shutdown()


@pytest.mark.asyncio
async def test_querybuilder_pagination():
    driver = CHDriver(dsn=DSN)
    await driver.startup()
    try:
        await driver.delete_table("test_table")
        await driver.create_table(
            "test_table",
            {"id": "Int32", "name": "String"},
            engine="MergeTree() ORDER BY id",
        )
        await driver.qb("test_table").insert(
            [{"id": i, "name": f"Name{i}"} for i in range(1, 21)]
        )
        # Page 1: limit 5, offset 0
        page1 = (
            await driver.qb("test_table")
            .fields(["id", "name"])
            .limit(5)
            .offset(0)
            .all()
        )
        assert len(page1) == 5
        assert page1[0]["id"] == 1
        # Page 2: limit 5, offset 5
        page2 = (
            await driver.qb("test_table")
            .fields(["id", "name"])
            .limit(5)
            .offset(5)
            .all()
        )
        assert len(page2) == 5
        assert page2[0]["id"] == 6
        # Page 3: limit 5, offset 10
        page3 = (
            await driver.qb("test_table")
            .fields(["id", "name"])
            .limit(5)
            .offset(10)
            .all()
        )
        assert len(page3) == 5
        assert page3[0]["id"] == 11
        # Page 4: limit 5, offset 15
        page4 = (
            await driver.qb("test_table")
            .fields(["id", "name"])
            .limit(5)
            .offset(15)
            .all()
        )
        assert len(page4) == 5
        assert page4[0]["id"] == 16
        # Page 5: limit 5, offset 20 (should be empty)
        page5 = (
            await driver.qb("test_table")
            .fields(["id", "name"])
            .limit(5)
            .offset(20)
            .all()
        )
        assert len(page5) == 0
        log("test_querybuilder_pagination passed")
    finally:
        await driver.delete_table("test_table")
        await driver.shutdown()
