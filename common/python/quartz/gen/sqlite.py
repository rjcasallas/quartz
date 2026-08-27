import quartz.gen.data as _base
from quartz.db.sqlite import Database
from quartz.error import Error
from abc import abstractmethod


class Table:

    def __init__(self, name:str, db:Database):
        if not isinstance(name, str): Error.invalid("table name")
        if not isinstance(db, Database): Error.invalid("table database")
        self._name = name
        self._db = db

    @property
    def name(self):
        return self._name

    @property
    def db(self):
        return self._db

    def insert(self, args, auto=False):
        if auto:
            return self.db.exec(f"@{self.name}/insert", args)
        else:
            self.db.exec(f"@{self.name}/insert_id", args)
        return args[0]

    def replace(self, args):
        self.db.exec(f"@{self.name}/replace", args)
        return args[0]

    def update(self, args: list):
        self.db.exec(f"@{self.name}/update", args, True)

    def delete(self, x):
        if isinstance(x, int) or isinstance(x, _base.Reference):
            return self.db.exec(f"@{self.name}/delete_id", [ int(x) ])
        elif isinstance(x, list):
            return self.db.exec(f"@{self.name}/delete_id", x)
        Error.missing(f"remove '{self.name}': {type(x)}")

    def deleteAll(self):
        self.db.exec(f'@{self.table}/delete')

    def contains(self, x = None) -> bool:
        return (self._ref(x) is not None)

    def select(self, x = None) -> list[object]:
        rows = self._all(x)
        if (isinstance(rows, tuple) or isinstance(rows, list)) and (len(rows) > 0):
            return rows
        return []

    def selectRef(self, x = None) -> _base.Reference:
        row = self._ref(x)
        if (isinstance(row, tuple) or isinstance(row, list)) and (len(row) > 0):
            return self._reference(row)
        return None

    def selectOne(self, x = None) -> object:
        row = self._one(x)
        if (isinstance(row, tuple) or isinstance(row, list)) and (len(row) > 0):
            return self._instance(row)
        return None

    def selectRefs(self, x = None) -> list[_base.Reference]:
        rows = self._refs(x)
        if (isinstance(rows, tuple) or isinstance(rows, list)) and (len(rows) > 0):
            return [ self._reference(row) for row in rows ]
        return []

    def selectAll(self, x = None) -> list[object]:
        rows = self._all(x)
        if (isinstance(rows, tuple) or isinstance(rows, list)) and (len(rows) > 0):
            return [ self._instance(row) for row in rows ]
        return []

    @abstractmethod
    def _reference(self, x):
        return None

    @abstractmethod
    def _instance(self, x):
        return None

    def _ref(self, x = None) -> _base.Reference:
        if x is None:
            sql = self.db.sql(f"@{self.name}/select_ref", "LIMIT 1")
            return self.db.one(sql)
        Error.missing(f"select ref '{self.name}': {type(x)}")

    def _refs(self, x = None) -> list[_base.Reference]:
        if x is None:
            sql = self.db.sql(f"@{self.name}/select_ref")
            return self.db.all(sql)
        Error.missing(f"select one '{self.name}': {type(x)}")

    def _one(self, x = None) -> object:
        if x is None:
            sql = self.db.sql(f"@{self.name}/select_all", "LIMIT 1")
            return self.db.one(sql)
        Error.missing(f"select one '{self.name}': {type(x)}")

    def _all(self, x = None) -> list[object]:
        if x is None:
            sql = self.db.sql(f"@{self.name}/select_all")
            return self.db.all(sql)
        Error.missing(f"select all '{self.name}': {type(x)}")
