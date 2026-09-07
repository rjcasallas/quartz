from quartz.db.sqlite import Database
from quartz.log import Log
from quartz.error import Error
from abc import abstractmethod


class Table:

    class Info:
        def __init__(self, table:str, args:list[str]=None, n_keys=1):
            self.table = table
            self.args = args or []
            self.n_keys=n_keys

        def __str__(self):
            return f'"{self.table}" {self.args}'

    class Insert(Info):
        def __init__(self, table:str, replace=False, args:list[str]=None, n_keys=1):
            super().__init__(table, args, n_keys)
            self.replace = replace

    class Update(Insert):
        def __init__(self, table:str, replace=False, args:list[str]=None, n_keys=1):
            super().__init__(table, replace, args, n_keys)

    class Tagged(Info):
        def __init__(self, table:str, tag=None, args:list[str]=None, n_keys=1):
            super().__init__(table, args, n_keys)
            self.tag = tag

    class Delete(Tagged):
        pass

    class Select(Tagged):
        pass

    class Filter:

        def insert(self, x) -> Table.Insert:
            return None

        def update(self, x) -> Table.Update:
            return None

        def delete(self, x) -> Table.Delete:
            return None

        def select(self, x) -> Table.Select:
            return None

    def __init__(self, name:str, db:Database, filter:Table.Filter):
        if not isinstance(name, str): Error.invalid("table name")
        if not isinstance(db, Database): Error.invalid("table database")
        self._name = name
        self._db = db
        self._filter = filter

    @property
    def name(self):
        return self._name

    @property
    def db(self):
        return self._db

    def insert(self, x, debug=False):
        info = x if isinstance(x, Table.Insert) else self._filter.insert(x)
        if not isinstance(info, Table.Insert): Error.invalid(f'insert "{self.name}"', x)
        if info.replace:
            query = f"@{info.table}/replace"
        elif (len(info.args) < 1) or (info.args[0] is None):
            query = f"@{info.table}/insert"
            info.args.pop(0)
        else:
            query = f"@{info.table}/insert_id"
        return self.db.exec(query, info.args, debug)

    def update(self, x, debug=False):
        info = x if isinstance(x, Table.Update) else self._filter.update(x)
        if not isinstance(info, Table.Update): Error.invalid(f'update "{self.name}"', x)
        if isinstance(info.replace, bool):
            # Built-in update
            query = f"@{info.table}/{'replace' if info.replace else 'update'}"
            self.db.exec(query, info.args, debug)
        elif isinstance(info.replace, list):
            # Custom update (e.g: UPDATE `book` SET `title`=?, `year`=? WHERE `id`=?)
            columns = info.replace[:info.n_keys]
            keys = info.replace[-info.n_keys:]
            sets = ", ".join([ f"`{c}`=?" for c in columns ])
            where = " AND ".join([ f"`{k}`=?" for k in keys ])
            query = f"UPDATE `{info.table}` SET {sets} WHERE {where}"
            self.db.exec(query, info.args, debug)
        return x

    def delete(self, x, debug=False):
        info = x if isinstance(x, Table.Delete) else self._filter.delete(x)
        if not isinstance(info, Table.Delete): Error.invalid(f'delete "{self.name}"', x)
        if isinstance(info.tag, str):
            # Built-in delete
            query = f"@{info.table}/delete_{info.tag}"
            self.db.exec(query, info.args, debug)
        elif isinstance(info.tag, list):
            # Custom delete
            query = f"DELETE FROM `{info.table}`"
            where = []
            args = []
            for i in range(len(info.tag)):
                if info.args[i] is not None:
                    where.append(f"{info.tag[i]}=?")
                    args.append(info.args[i])
            if len(args) > 0:
                query += " WHERE " + " AND ".join(where)
                self.db.exec(query, args, debug)
        return x

    def deleteAll(self, debug=False):
        self.db.exec(f"@{self.table}/delete", [], debug)

    def contains(self, x=None, debug=False) -> bool:
        return (self.select(x, ref=True, one=True, debug=debug) is not None)

    def select(self, x=None, kind:str = "full", builder=None, one=False, order=None, debug=False) -> list[object]:
        info = x if isinstance(x, Table.Select) else self._filter.select(x)
        if not isinstance(info, Table.Select): Error.invalid(f'select "{self.name}"', x)
        tag = info.tag if info.tag else "all"
        query = f"@{info.table}/select_{tag}-{kind}"
        tail = f"ORDER BY {order}" if order else ""
        if isinstance(info.tag, list):
            # Custom select (e.g: SELECT `title`, `year` FROM `book` WHERE `id`=?)
            cols = info.tag[:len(info.tag)-info.n_keys]
            keys = info.tag[-info.n_keys:]
            columns = ", ".join([ f"`{c}`" for c in cols ])
            where = " AND ".join([ f"`{k}`=?" for k in keys ])
            query = f"SELECT {columns} FROM `{info.table}` WHERE {where}"
            fn = self.db.one if one else self.db.all
            return fn(query, info.args, tail, debug)
        elif one:
            tail += " LIMIT 1"
            row = self.db.one(query, info.args, tail, debug)
            if isinstance(row, tuple) and (len(row) > 0):
                return row if (builder is None) else builder(row)
            return None
        else:
            rows = self.db.all(query, info.args, tail, debug)
            if isinstance(rows, list) and (len(rows) > 0):
                return rows if (builder is None) else [ builder(row) for row in rows ]
            return []

