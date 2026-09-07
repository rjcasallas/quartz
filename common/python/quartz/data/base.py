from quartz.data.meta import Schema, Table, Column
from quartz.log import Log
from quartz.error import Error
from quartz.data.query import Queries
from abc import ABC, abstractmethod
import pathlib


class Reference:

    def __init__(self, id = None):
        self.id = id

    def __str__(self):
        return "∅" if self.id is None else f"⌗{self.id}"

    def __repr__(self):
        return "∅" if self.id is None else f"⌗{self.id}"

    def __eq__(self, other: 'Reference'):
        if isinstance(other, Reference):
            return self.id == other.id
        elif isinstance(other, int):
            return self.id == other
        else:
            return False

    def __int__(self):
        return self.id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, x):
        if x is None:
            self._id = None
        elif self._validateRef(x):
            self._id = int(x)
        else:
            Error.invalid("id", x)
        return self._id

    def copy(self, x):
        if isinstance(x, Reference):
            self.id = x.id
        return self

    def _validateRef(self, x):
        if isinstance(x, int):
            return x
        if isinstance(x, Reference) and (x._id is not None):
            return x


class BasicSubset(ABC):

    @abstractmethod
    def add(self, x: object):
        pass

    @abstractmethod
    def remove(self, x: object):
        pass

    @abstractmethod
    def has(self, x = None) -> bool:
        pass

    @abstractmethod
    def clear(self):
        pass


class EntitySubset(BasicSubset):

    @abstractmethod
    def ref(self, x=None, builder=None, order:list[str]=None, limit:str=None, debug:bool=False):
        return None

    @abstractmethod
    def refn(self, cursor) -> Reference:
        return None
    
    @abstractmethod
    def refs(self, x=None, builder=None, order:list[str]=None, limit:str=None, debug:bool=False):
        return []
    
    @abstractmethod
    def begin(self, x=None, builder=None, columns:str='full', order:list[str]=None, limit:str=None, debug:bool=False):
        return None
    
    @abstractmethod
    def next(self, cursor, builder=None):
        return None

    @abstractmethod
    def all(self, x=None, builder=None, columns:str='full', order:list[str]=None, limit:str=None, debug:bool=False):
        return []


class Database(ABC):

    def __init__(self, schema: str):
        self._schema = schema
        # Queries
        self._queries = Queries()
        self._load_queries()

    @abstractmethod
    def open(self, reset: bool=False):
        pass

    @abstractmethod
    def close(self):
        if self._db is not None:
            self._path = None
            self._db.close()
            self._db = None
            self._queries = None

    @abstractmethod
    def isOpen(self):
        return False

    def print(self):
        meta = self.meta()
        if meta:
            # meta.print()
            for t in meta.tables:
                Log.list(t, 1)
                rows = self.all(f"SELECT * FROM `{t}`")
                for r in rows:
                    Log.list(str(r), 2)

    def exec(self, query:str, args:list=[], debug:bool=False):
        sql =  self._sql(query, args if debug else None)
        return self._exec(sql, args)

    def begin(self, query, args:list=[], debug:bool=False):
        sql =  self._sql(query, args if debug else None)
        return self._begin(sql, args)

    def next(self, cursor):
        # if (isinstance(cursor, x)):
        return self._next(cursor)
        # s = Log.string(cursor)
        # Log.error("Invalid statement: s")

    def one(self, query, args:list=[], debug:bool=False):
        cur = self.begin(query, args, debug)
        return self.next(cur)

    def all(self, query, args:list=[], debug:bool=False):
        sql =  self._sql(query, args if debug else None)
        return self._all(sql, args)

    def sql(self, query, debug:bool=False):
        return self._sql(query, [] if debug else None)

    @abstractmethod
    def meta(self):
        return None

    @abstractmethod
    def _exec(self, sql, params=[]):
        pass

    @abstractmethod
    def _begin(self, sql, params=[]):
        return None

    @abstractmethod
    def _next(self, cursor):
        return None

    @abstractmethod
    def _all(self, sql, params=[]):
        return []

    def _validateOpen(self):
        if not self.isOpen(): Error.fail(f"Database not open")

    def _load_queries(self):
        # Try schema.yaml
        schema = pathlib.Path(self._schema)
        path = schema.with_suffix(".yaml")
        if path.is_file():
            self._queries.load(path)
        # Try schema/queries/*.yaml
        queries = path.parent / "sql"
        if queries.is_dir():
            self._queries.load(queries)

    def _sql(self, query, debug:list[str]=None):
        debug_args = ', '.join(str(a) for a in debug) if isinstance(debug, list) else None
        if (query.startswith('@')):
            key = query[1:]
            sql = self._queries[key]
            if debug_args is not None:
                Log.debug(f"[{key}]\n{sql}\n[{debug_args}]\n")
            return sql
        elif debug_args is not None:
            Log.debug(f"{query}\n[{debug_args}]\n")
        return query
