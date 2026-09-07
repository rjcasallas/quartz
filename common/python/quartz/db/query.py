from quartz.log import Log
from quartz.error import Error
import yaml
import re
import os
import pathlib

# Manages SQL queries loaded from YAML files.
#
# Queries are stored with keys in the format 'table_name/query_name' and
# supports reference resolution using @table/query_name syntax.
class Queries:

    def __init__(self, path: str = None):
        self._queries = {}
        self.load(path)

    def __str__(self):
        return str(self._queries)

    def __getitem__(self, key: str):
        if key not in self._queries:
            Error.missing(key)
        sql = self._queries[key]
        return self._compile(sql)

    def __setitem__(self, key: str, value: str):
        self._queries[key] = value

    def __delitem__(self, key: str):
        del self._queries[key]

    # Load queries from a YAML file.
    def load(self, path):
        if path is None:
            return
        if isinstance(path, str):
            return self.load(pathlib.Path(path))
        if isinstance(path, pathlib.Path):
            if path.is_dir():
                return self._loadDir(path)
        Error.invalid("path", path)

    def _loadDir(self, path):
        for table in sorted(list(path.glob("*"))):
            if table.is_dir():
                # Load auto-generated queries
                for file in sorted(list(table.glob("*.sql"))):
                    if not file.stem.startswith("+"):
                        self._loadSql(table, file)
                # Load manual queries
                for file in sorted(list(table.glob("+*.sql"))):
                    self._loadSql(table, file)

    def _loadSql(self, dir, file):
        table = dir.name
        query = file.stem[1:] if file.stem.startswith("+") else file.stem
        sql = file.read_text()
        key = f"{table}/{query}"
        # Log.debug(f"{key}")
        self._queries[key] = sql.strip()

    # Resolve @table/query_name references in query text.
    def _compile(self, sql: str, visited: set = None) -> str:
        if not isinstance(sql, str):
            return sql
        visited = visited or set()

        def _replace(match):
            table = match.group(1)
            query = match.group(2)
            key = f"{table}/{query}"
            if key in visited:
                return match.group(0)
            if key in self._queries:
                visited.add(key)
                resolved = self._compile(self._queries[key], visited)
                return resolved
            else:
                return match.group(0)

        # Pattern to match @table/query_name references
        pattern = r"@([a-zA-Z_][a-zA-Z0-9_]*)/([a-zA-Z0-9_-]*)"
        return re.sub(pattern, _replace, sql)

    def print(self, level: int = 0):
        for name, sql in self._queries.items():
            full = self._compile(sql)
            Log.list(f"\n{name}:\n{full}", level, "▪︎")
