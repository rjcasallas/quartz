import yaml
import re
import os
from quartz.log import Log
from quartz.error import Error


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
    def load(self, path: str):
        if path is None:
            return
        if os.path.isdir(path):
            for entry in os.listdir(path):
                if entry.endswith(".yaml"):
                    full_path = os.path.join(path, entry)
                    self.load(full_path)
        elif os.path.isfile(path):
            with open(path, "r") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                self._parse(data)
        else:
            Error.missing(path)

    # Parse YAML data into flattened queries with table_name/query_name keys.
    def _parse(self, data: dict):
        # First pass: flatten the structure
        for table, queries in data.items():
            if isinstance(queries, dict):
                for query, sql in queries.items():
                    key = f"{table}/{query}"
                    if isinstance(sql, str):
                        self._queries[key] = sql.strip()
                    else:
                        self._queries[key] = str(sql).strip()

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
        pattern = r"@([a-zA-Z_][a-zA-Z0-9_]*)/([a-zA-Z_][a-zA-Z0-9_]*)"
        return re.sub(pattern, _replace, sql)

    def print(self, level: int = 0):
        for name, sql in self._queries.items():
            full = self._compile(sql)
            Log.list(f"\n{name}:\n{full}", level, "▪︎")
