from quartz.gen.data import BasicManager, Reference
from quartz.db.sqlite import Database
from quartz.error import Error
from abc import abstractmethod


class Table:

    def __init__(self, name:str, db:Database):
        self._name = name
        self._db = db

    @property
    def db(self):
        return self._db

    @abstractmethod
    def create(self, x, ref = True):
        return None

    def clear(self):
        self.exec(f'@{self._table}/delete')

    @abstractmethod
    def ref(self, x = None) -> Reference:
        return None

    @abstractmethod
    def refs(self, x = None) -> list[Reference]:
        return []

    @abstractmethod
    def get(self, x = None) -> object:
        return None

    @abstractmethod
    def all(self, x = None) -> list[object]:
        return []


class Manager(BasicManager):

    # def __init__(self, tbl):
    #     if not isinstance(tbl, Table): Error.invalid("table", tbl)
    #     self._table = tbl

    def __init__(self, table:str, db:Database):
        self._table = table
        self._db = db

    @property
    def table(self):
        return self._table

    @property
    def db(self):
        return self._db

    @property
    def table(self):
        return self._table

    def clear(self):
        self.db.exec(f'@{self.table}/delete')

    def has(self, x = None) -> bool:
        return (self.ref(x) is not None)

    def ref(self, x = None) -> Reference:
        row = self._ref(x)
        if (isinstance(row, tuple) or isinstance(row, list)) and (len(row) > 0):
            return self._reference(row)
        return None

    def refs(self, x = None) -> list[Reference]:
        rows = self._refs(x)
        if (isinstance(rows, tuple) or isinstance(rows, list)) and (len(rows) > 0):
            return [ self._reference(row) for row in rows ]
        return []

    def one(self, x = None) -> object:
        row = self._one(x)
        if (isinstance(row, tuple) or isinstance(row, list)) and (len(row) > 0):
            return self._instance(row)
        return None

    def all(self, x = None) -> list[object]:
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

    @abstractmethod
    def _ref(self, x = None) -> Reference:
        return None

    @abstractmethod
    def _refs(self, x = None) -> list[Reference]:
        return []

    @abstractmethod
    def _one(self, x = None) -> object:
        return None

    @abstractmethod
    def _all(self, x = None) -> list[object]:
        return []
