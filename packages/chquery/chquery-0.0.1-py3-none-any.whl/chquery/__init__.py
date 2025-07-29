import asynch
from asynch.cursors import DictCursor


class DbError(Exception):
    """Custom database error for query builder and driver."""

    pass


class CHDriver:
    """
    Async ClickHouse driver with connection pool and query builder.
    """

    def __init__(self, dsn: str, minsize: int = 1, maxsize: int = 10, **kwargs):
        self.pool = asynch.Pool(
            dsn=dsn, minsize=minsize, maxsize=maxsize, **kwargs, echo=True
        )

    async def startup(self) -> None:
        """Start the connection pool."""
        try:
            await self.pool.startup()
        except Exception as e:
            raise DbError(f"Failed to start connection pool: {e}") from e

    async def shutdown(self) -> None:
        """Shutdown the connection pool."""
        try:
            await self.pool.shutdown()
        except Exception as e:
            raise DbError(f"Failed to shutdown connection pool: {e}") from e

    async def close(self) -> None:
        """Alias for shutdown."""
        await self.shutdown()

    async def ping(self) -> bool:
        """Check if the connection to ClickHouse is alive."""
        try:
            await self.fetch_one("SELECT 1")
            return True
        except Exception:
            return False

    async def fetch_all(self, query: str, *args, cursor_class=DictCursor) -> list:
        """Fetch all rows for a query."""
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor(cursor=cursor_class) as cursor:
                    await cursor.execute(query, *args)
                    result = await cursor.fetchall()
                    return result if result is not None else []
        except Exception as e:
            raise DbError(f"fetch_all error: {e}") from e

    async def fetch_one(self, query: str, *args, cursor_class=DictCursor):
        """Fetch a single row for a query."""
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor(cursor=cursor_class) as cursor:
                    await cursor.execute(query, *args)
                    return await cursor.fetchone()
        except Exception as e:
            raise DbError(f"fetch_one error: {e}") from e

    async def insert_many(self, query: str, data, cursor_class=DictCursor):
        """Insert many rows using executemany."""
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor(cursor=cursor_class) as cursor:
                    return await cursor.executemany(query, data)
        except Exception as e:
            raise DbError(f"insert_many error: {e}") from e

    def qb(self, table: str) -> "CHQueryBuilder":
        """Return a query builder for a table."""
        return CHQueryBuilder(self, table)

    async def raw(self, query: str, *args, fetch: str = "all", cursor_class=DictCursor):
        """
        Execute a raw SQL query.

        Args:
            query (str): The SQL query to execute.
            *args: Parameters for the query.
            fetch (str): 'all', 'one', or None for fetchall, fetchone, or no fetch (DDL).
            cursor_class: Cursor class to use (default DictCursor).
        Returns:
            Query result or None.
        """
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor(cursor=cursor_class) as cursor:
                    await cursor.execute(query, *args)
                    if fetch == "all":
                        return await cursor.fetchall()
                    elif fetch == "one":
                        return await cursor.fetchone()
                    else:
                        return None
        except Exception as e:
            raise DbError(f"raw error: {e}") from e

    async def __aenter__(self):
        await self.startup()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.shutdown()

    def __repr__(self) -> str:
        return f"<CHDriver dsn={getattr(self.pool, 'dsn', None)} pool={self.pool}>"

    async def delete_table(self, table: str) -> None:
        """
        Drop a table if it exists.
        Args:
            table (str): The table name to drop.
        Raises:
            DbError: For any database-related error.
        """
        query = f"DROP TABLE IF EXISTS {table}"
        try:
            await self.raw(query, fetch="none")
        except Exception as e:
            raise DbError(f"Failed to drop table {table}: {e}") from e

    async def create_table(
        self, table: str, columns: dict, engine: str = "MergeTree() ORDER BY tuple()"
    ) -> None:
        """
        Create a table with the given columns and engine.
        Args:
            table (str): The table name to create.
            columns (dict): Column definitions, e.g. {"id": "Int32", "name": "String"}
            engine (str): Table engine definition (default: MergeTree() ORDER BY tuple()).
        Raises:
            DbError: For any database-related error.
        """
        cols_sql = ", ".join(f"{name} {type_}" for name, type_ in columns.items())
        query = f"CREATE TABLE IF NOT EXISTS {table} ({cols_sql}) ENGINE = {engine}"
        try:
            await self.raw(query, fetch="none")
        except Exception as e:
            raise DbError(f"Failed to create table {table}: {e}") from e


class CHQueryBuilder:
    """
    A simple async query builder for CHDriver.

    Usage example:
        await driver.qb("table").fields(["col1", "col2"]).filters({"col1[eq]": value}).all()
    """

    def __init__(self, driver: CHDriver, table):
        """
        Initialize the CHQueryBuilder.

        Args:
            driver: The CHDriver instance.
            table (str): The table name to query.
        """
        self.driver = driver
        self.table = table
        self._filters = []
        self._params = {}
        self._fields = None

    def __repr__(self) -> str:
        return (
            f"<CHQueryBuilder table={self.table} fields={self._fields} filters={self._filters} "
            f"order_by={getattr(self, '_order_by', None)} limit={getattr(self, '_limit', None)} offset={getattr(self, '_offset', None)}>"
        )

    def fields(self, fields_list: list[str]) -> "CHQueryBuilder":
        """
        Specify which fields/columns to select.

        Args:
            fields_list (list): List of column names to select.
        Returns:
            self (CHQueryBuilder): For method chaining.
        """
        self._fields = fields_list
        return self

    def order_by(self, fields: list[str]) -> "CHQueryBuilder":
        """
        Specify the ORDER BY clause.

        Args:
            fields (list): List of field names. Prefix with '-' for DESC, e.g. ['name', '-age']
        Returns:
            self (CHQueryBuilder): For method chaining.
        """
        self._order_by = []
        for f in fields:
            if f.startswith("-"):
                self._order_by.append(f"{f[1:]} DESC")
            else:
                self._order_by.append(f"{f} ASC")
        return self

    def limit(self, n: int) -> "CHQueryBuilder":
        """
        Specify the LIMIT clause.

        Args:
            n (int): Maximum number of rows to return.
        Returns:
            self (CHQueryBuilder): For method chaining.
        """
        self._limit = n
        return self

    def offset(self, n: int) -> "CHQueryBuilder":
        """
        Specify the OFFSET clause.

        Args:
            n (int): Number of rows to skip.
        Returns:
            self (CHQueryBuilder): For method chaining.
        """
        self._offset = n
        return self

    def _build_where(self):
        return f"WHERE {' AND '.join(self._filters)}" if self._filters else ""

    def _build_order_by(self):
        return (
            f"ORDER BY {', '.join(self._order_by)}"
            if hasattr(self, "_order_by") and self._order_by
            else ""
        )

    def _build_limit(self):
        return (
            f"LIMIT {self._limit}"
            if hasattr(self, "_limit") and self._limit is not None
            else ""
        )

    def _build_offset(self):
        return (
            f"OFFSET {self._offset}"
            if hasattr(self, "_offset") and self._offset is not None
            else ""
        )

    def filters(self, filters_dict: dict) -> "CHQueryBuilder":
        """
        Add filters to the query. Supports [eq], [ne], [lt], [lte], [gt], [gte], [in], [like], [isnull] operators.

        Args:
            filters_dict (dict): Dictionary of filters, e.g. {"col[eq]": value, "col[gt]": 5}
        Returns:
            self (CHQueryBuilder): For method chaining.
        """
        for key, value in filters_dict.items():
            if "[" in key and key.endswith("]"):
                field, op = key[:-1].split("[", 1)
            else:
                field, op = key, "eq"
            param_name = f"param_{len(self._params)}"
            if op == "eq":
                self._filters.append(f"{field} = %({param_name})s")
                self._params[param_name] = value
            elif op == "ne":
                self._filters.append(f"{field} != %({param_name})s")
                self._params[param_name] = value
            elif op == "lt":
                self._filters.append(f"{field} < %({param_name})s")
                self._params[param_name] = value
            elif op == "lte":
                self._filters.append(f"{field} <= %({param_name})s")
                self._params[param_name] = value
            elif op == "gt":
                self._filters.append(f"{field} > %({param_name})s")
                self._params[param_name] = value
            elif op == "gte":
                self._filters.append(f"{field} >= %({param_name})s")
                self._params[param_name] = value
            elif op == "in":
                in_params = []
                for i, v in enumerate(value):
                    pname = f"{param_name}_{i}"
                    in_params.append(f"%({pname})s")
                    self._params[pname] = v
                self._filters.append(f"{field} IN ({', '.join(in_params)})")
            elif op == "like":
                self._filters.append(f"{field} LIKE %({param_name})s")
                self._params[param_name] = value
            elif op == "isnull":
                if value:
                    self._filters.append(f"{field} IS NULL")
                else:
                    self._filters.append(f"{field} IS NOT NULL")
            else:
                raise ValueError(f"Unsupported filter operator: {op}")
        return self

    async def all(self) -> list[dict]:
        """
        Execute the built query and return all results.

        Returns:
            List of rows (dicts by default).
        Raises:
            DbError: For any database-related error, with a clear message.
        """
        where = self._build_where()
        order_by = self._build_order_by()
        limit = self._build_limit()
        offset = self._build_offset()
        fields = ", ".join(self._fields) if self._fields else "*"
        query = f"SELECT {fields} FROM {self.table} {where} {order_by} {limit} {offset}".strip()
        try:
            return await self.driver.fetch_all(query, self._params)
        except Exception as e:
            msg = str(e)
            raise DbError(f"Database error: {msg}") from e

    async def one(self) -> dict | None:
        """
        Execute the built query and return a single result (LIMIT 1).

        Returns:
            Single row (dict by default) or None if not found.
        Raises:
            DbError: For any database-related error, with a clear message.
        """
        where = self._build_where()
        order_by = self._build_order_by()
        limit = "LIMIT 1"
        offset = self._build_offset()
        fields = ", ".join(self._fields) if self._fields else "*"
        query = f"SELECT {fields} FROM {self.table} {where} {order_by} {limit} {offset}".strip()
        try:
            result = await self.driver.fetch_one(query, self._params)
            if not result:
                return None
            return result
        except Exception as e:
            msg = str(e)
            raise DbError(f"Database error: {msg}") from e

    async def count(self) -> int:
        """
        Return the count of rows matching the current query filters, respecting limit/offset/order if set.
        """
        where = self._build_where()
        order_by = self._build_order_by()
        limit = self._build_limit()
        offset = self._build_offset()
        # If limit/offset/order_by is set, wrap in subquery
        if limit or offset or order_by:
            fields = ", ".join(self._fields) if self._fields else "*"
            inner_query = f"SELECT {fields} FROM {self.table} {where} {order_by} {limit} {offset}".strip()
            query = f"SELECT count() as count FROM ({inner_query})"
        else:
            query = f"SELECT count() as count FROM {self.table} {where}".strip()
        try:
            result = await self.driver.fetch_one(query, self._params)
            return result["count"] if result else 0
        except Exception as e:
            raise DbError(f"Database error: {e}") from e

    async def exists(self) -> bool:
        """
        Return True if any row matches the current query filters.
        """
        where = self._build_where()
        query = f"SELECT 1 FROM {self.table} {where} LIMIT 1".strip()
        try:
            result = await self.driver.fetch_one(query, self._params)
            return result is not None
        except Exception as e:
            raise DbError(f"Database error: {e}") from e

    async def all_iter(self, batch_size: int = 1000):
        """
        Async generator yielding rows in batches for large result sets.
        """
        offset = 0
        while True:
            qb = CHQueryBuilder(self.driver, self.table)
            qb._fields = self._fields
            qb._filters = self._filters.copy()
            qb._params = self._params.copy()
            if hasattr(self, "_order_by"):
                qb._order_by = self._order_by.copy()
            qb._limit = batch_size
            qb._offset = offset
            batch = await qb.all()
            if not batch:
                break
            for row in batch:
                yield row
            if len(batch) < batch_size:
                break
            offset += batch_size

    async def insert(self, data: dict | list[dict]) -> int:
        """
        Insert one or many rows into the table.

        Args:
            data (dict or list of dict): Row or rows to insert.
        Returns:
            Number of rows inserted.
        Raises:
            DbError: For any database-related error.
        """
        if isinstance(data, dict):
            data = [data]
        if not data:
            raise DbError("No data provided for insert.")
        columns = list(data[0].keys())
        cols_sql = ", ".join(columns)
        query = f"INSERT INTO {self.table} ({cols_sql}) VALUES"
        print(query)
        print(data)
        try:
            await self.driver.insert_many(query, data)
            return len(data)
        except Exception as e:
            raise DbError(f"Database insert error: {e}") from e

    async def delete(self) -> int:
        """
        Delete rows matching the current filters.
        Returns:
            Number of rows deleted (if supported).
        Raises:
            DbError: For any database-related error.
        """
        where = self._build_where()
        query = f"ALTER TABLE {self.table} DELETE {where}".strip()
        try:
            await self.driver.raw(query, fetch="none")
            # ClickHouse does not return affected rows for DELETE
            return 0
        except Exception as e:
            raise DbError(f"Database delete error: {e}") from e

    async def upsert(self, data: dict | list[dict], key_columns: list[str]) -> int:
        """
        Upsert (insert or update) rows into the table. (Emulates ON CONFLICT DO UPDATE)
        Args:
            data (dict or list of dict): Row or rows to upsert.
            key_columns (list[str]): Columns to use as unique key.
        Returns:
            Number of rows upserted.
        Raises:
            DbError: For any database-related error.
        Note: ClickHouse does not support true upserts, so this is a best-effort emulation.
        """
        if isinstance(data, dict):
            data = [data]
        if not data:
            raise DbError("No data provided for upsert.")
        columns = list(data[0].keys())
        values = [tuple(row[col] for col in columns) for row in data]
        cols_sql = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        query = f"INSERT INTO {self.table} ({cols_sql}) VALUES ({placeholders})"
        try:
            await self.driver.insert_many(query, values)
            return len(values)
        except Exception as e:
            # If duplicate key error, ignore (ClickHouse may not error, depending on table engine)
            if "Code: 242" in str(e):  # Code 242: Duplicate
                return 0
            raise DbError(f"Database upsert error: {e}") from e
