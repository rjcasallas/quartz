import sqlite3
import os
import re
from quartz.db.meta import Schema, Table, Column
from quartz.log import Log
from quartz.file import Paths
from quartz.error import Error
from quartz.db.query import Queries


class Database:

    def __init__(self, schema: str, path: str = None):
        self._schema = schema
        self._db = None
        self._path = path
        # Queries
        self._queries = Queries()
        self._load_queries()

    @property
    def path(self):
        return self._path

    def open(self, reset: bool = False):
        if self._path is None:
            return self.open(os.getcwd(), reset)
        # Close
        self.close()
        # Directory?
        if os.path.isdir(self._path):
            Log.warning(f"Opening directory: {self._path}")
            return self.open(os.path.join(self._path, self._defaultName()), reset)
        # Path exists?
        path = Paths.normalize(self._path)
        exists = os.path.isfile(path)
        if exists and reset:
            # Reset existing file
            Log.warning(f"RESET: {path}")
            os.remove(path)
            exists = False
        if exists:
            # Existing file
            self._connect(path)
        else:
            # Path doesn't exist
            _, ext = os.path.splitext(path)
            if ext:
                # Treat as file
                os.makedirs(os.path.dirname(path), exist_ok=True)
                self._create(path)
            else:
                # Treat as directory
                os.makedirs(path, exist_ok=True)
                self._create(os.path.join(path, self._defaultName()))
        # self._queries.print()

    def close(self):
        if self._db is not None:
            self._path = None
            self._db.close()
            self._db = None
            self._queries = None

    def isOpen(self):
        return self._db is not None

    def print(self):
        meta = self.meta()
        # meta.print()
        for t in meta.tables:
            Log.list(t, 1)
            rows = self.all(f"SELECT * FROM `{t}`")
            for r in rows:
                Log.list(str(r), 2)


    def sql(self, query, append=None):
        if query.startswith("@"):
            name = query[1:]
            query = self._queries[name]
        return query + (append and f"\n{append}" or "")

    def exec(self, query, params=[], debug: bool = False):
        self._validateOpen()
        sql = self.sql(query)
        if debug:
            self._debug(query, sql, params)
        cur = self._db.cursor()
        cur.execute(sql, params)
        self._db.commit()
        return cur.lastrowid

    def one(self, query, params=None, debug=False, limit: bool = False):
        self._validateOpen()
        sql = self.sql(query)
        if limit:
            sql += f" LIMIT 1"
        params = params or []
        if debug:
            self._debug(query, sql, params)
        cur = self._db.cursor()
        res = cur.execute(sql, params)
        return res.fetchone()

    def all(self, query: str, params: tuple = None, debug: bool = False) -> list:
        self._validateOpen()
        sql = self.sql(query)
        if debug:
            self._debug(query, sql, params)
        cur = self._db.cursor()
        cur.execute(sql, params or ())
        return cur.fetchall()

    def meta(self):
        schema = Schema("SQLite", self._schema)
        # First pass: create all tables and columns
        for row in self.all("SELECT name, sql FROM sqlite_master WHERE type='table';"):
            tbl_name = row[0]
            create_sql = row[1] or ""
            table = Table(tbl_name)

            # Get column information
            for col in self.all(f"PRAGMA table_info('{tbl_name}');"):
                col_name = col[1]
                # Check if column is autoincrement
                pattern = rf"\b{re.escape(col_name)}\s+[^,)]+\bAUTOINCREMENT\b"
                autoincrement = bool(re.search(pattern, create_sql, re.IGNORECASE))
                # Create column
                column = Column(
                    table=table,
                    name=col_name,
                    type_=col[2],
                    notnull=bool(col[3]),
                    default=col[4],
                    pk=bool(col[5]),
                    auto=autoincrement,
                )
                table.add(column)

            # Get index information
            for idx_row in self.all(f"PRAGMA index_list('{tbl_name}');"):
                idx_name = idx_row[1]
                idx_unique = bool(idx_row[2])
                # Get columns in this index
                for idx_info in self.all(f"PRAGMA index_info('{idx_name}');"):
                    column = table.find(idx_info[2])
                    column.index(indexed=True, unique=idx_unique)
            # Add table to schema
            schema.add(table)

        # Second pass: resolve foreign key references to actual Column instances
        for table in schema.tables.values():
            for row in self.all(f"PRAGMA foreign_key_list('{table.name}');"):
                from_col = table.find(row[3])  # 'from' column
                into_table = schema.find(row[2])  # referenced table
                into_column = into_table.find(row[4])  # 'to' column
                from_col.into = into_column

        return schema.compile()

    def _defaultName(self):
        _, n, _ = Paths.split(self._schema)
        return f"{n}.db"

    def _validateOpen(self):
        if not self.isOpen():
            Error.fail(f"Database not open")

    def _connect(self, path):
        Log.list(f"{path}", 0, "💾")
        self._path = path
        self._db = sqlite3.connect(path)
        return self._db

    def _create(self, path):
        if not os.path.exists(self._schema):
            Error.missing(self._schema)
        db = self._connect(path)
        with open(self._schema, "r") as f:
            db.executescript(f.read())
        db.commit()
        return db

    def _load_queries(self):
        # Try schema.yaml
        path = Paths.replacex(self._schema, ".yaml")
        if os.path.isfile(path):
            self._queries.load(path)
        # Try schema/queries/*.yaml
        path = os.path.join(os.path.dirname(self._schema), "queries")
        if os.path.isdir(path):
            self._queries.load(path)

    def _debug(self, query, sql, params):
        if query.startswith("@"):
            Log.debug("[{}]\n{}\n{}".format(query[1:], sql, params))
        else:
            Log.debug("\nQ:\n{}\n{}".format(sql, params))
