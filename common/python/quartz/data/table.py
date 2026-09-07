from quartz.data.base import Database
from quartz.log import Log
from quartz.error import Error
from abc import ABC, abstractmethod


class Table(ABC):

    class Info:
        def __init__(self, table:str, columns:list=None, n_keys:int=None, replace:bool=False, tag:str=None):
            self.table = table
            self.replace = replace
            self.tag = tag
            if columns is None: columns = []
            if (n_keys is None) or (n_keys >= len(columns)):
                self.keys = columns
                self.values = []
            else:
                self.keys = columns[:n_keys]
                self.values = columns[n_keys:]
            # c = ', '.join([ "∅" if c is None else str(c) for c in columns])
            # k = ', '.join([ "∅" if c is None else str(c) for c in self.keys])
            # v = ', '.join([ "∅" if c is None else str(c) for c in self.values])
            # Log.debug(f"[{c}] =({(n_keys is None) and '*' or str(n_keys)})=> [{k}] [{v}]")

        def __str__(self):
            k = ', '.join([ "∅" if c is None else str(c) for c in self.keys])
            v = ', '.join([ "∅" if c is None else str(c) for c in self.values])
            r = ' R' if self.replace else ''
            t = f'<{self.tag}>' if (self.tag is not None) else ''
            return f'"{self.table}"{t}[{k}][{v}]'
        
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

    def insert(self, x, debug=False):
        info = x if isinstance(x, Table.Info) else self._insert(x)
        if not isinstance(info, Table.Info):
            Error.invalid(f'"{self.name}" insert', x)
        if info.tag is None:
            # INSERT INTO book(title, year) VALUES ('Dune', 1965)
            # REPLACE INTO book(title, year) VALUES ('Dune', 1965)
            action = info.replace and "REPLACE" or "INSERT"
            columns = info.keys + info.values
            names = ", ".join([ f"`{c[0]}`" for c in columns ])
            args = [ c[1] for c in columns ]
            marks = ", ".join([ "?" ] * len(columns) )
            query = f"{action} {info.table}({names}) VALUES({marks})"
            return self.db.exec(query, args, debug)
        else:
            # @book/insert|insert_id|replace
            args = info.values if ("insert" == info.tag) else (info.keys + info.values)
            query = f"@{info.table}/{info.tag}"
            return self.db.exec(query, args, debug)

    def update(self, x, debug=False):
        info = x if isinstance(x, Table.Info) else self._update(x)
        if not isinstance(info, Table.Info):
            Error.invalid(f'"{self.name}" update', x)
        if info.tag is None:
            # UPDATE book SET year=2000 WHERE id=1
            sets = ", ".join([ f"`{c[0]}`=?" for c in info.values ])
            where = " AND ".join([ f"`{k[0]}`=?" for k in info.keys ])
            query = f"UPDATE `{info.table}` SET {sets} WHERE {where}"
            args = [ c[1] for c in info.values ] + [ c[1] for c in info.keys ]
            self.db.exec(query, args, debug)
        else:
            # @book/update|replace
            query = f"@{info.table}/{info.tag}"
            args = info.values + info.keys
            self.db.exec(query, args, debug)           
        return x

    def delete(self, x, debug=False):
        info = x if isinstance(x, Table.Info) else self._delete(x)
        if not isinstance(info, Table.Info): 
            Error.invalid(f'"{self.name}" delete', x)
        if info.tag is None:
            # DELETE FROM book WHERE year >= ? AND year <= ?
            query = f"DELETE FROM `{info.table}`"
            where = []
            args = []
            for i in range(len(info.keys)):
                if info.keys[i][1] is not None:
                    where.append(f"{info.keys[i][0]}=?")
                    args.append(info.keys[i][1])
            if len(args) > 0:
                query += " WHERE " + " AND ".join(where)
                self.db.exec(query, args, debug)
        else:
            query = f"@{info.table}/delete-{info.tag}"
            self.db.exec(query, info.keys, debug)
        return x

    def deleteAll(self, debug=False):
        self.db.exec(f"@{self.table}/delete", [], debug)

    def begin(self, x=None, columns:str='full', order:list[str]=None, limit:int=None, debug:bool=False):
        [query, args] = self.preselect(x, columns, order, limit)
        return self.db.begin(query, args, debug=debug)

    def next(self, cursor, builder=None):
        row = self.db.next(cursor)
        if ((isinstance(row, tuple) or isinstance(row, list)) and (len(row) > 0)):
            return builder(row) if builder else row
        return None
    
    def one(self, x=None, builder=None, columns:str='full', order:list[str]=None, limit:int=None, debug:bool=False):
        cur = self.begin(x, columns, order, limit, debug)
        return self.next(cur, builder)

    def select(self, x=None, builder=None, columns:str='full', order:list[str]=None, limit:int=None, debug:bool=False) -> list:
        [query, args] = self.preselect(x, columns, order, limit)
        rows = self.db.all(query, args, debug=debug)
        if (isinstance(rows, list) and (len(rows) > 0)):
            return [ builder(r) for r in rows ] if builder else rows
        return []

    def preselect(self, x=None, columns:list[str]='full', order:str=None, limit:str=None) -> list:
        info = x if isinstance(x, Table.Info) else self._select(x)
        if not isinstance(info, Table.Info): 
            Error.invalid(f'"{self.name}" select', x)
        ord = "" if (order is None) else f" ORDER BY {order}"
        lim = "" if (limit is None) else f" LIMIT {lim}"
        tail = ord + lim
        if info.tag is None:
            # SELECT id, title FROM book WHERE author = ? AND year > ?
            nonkeys = ", ".join([ f"`{c[0]}`" for c in info.values ])
            where = " AND ".join([ f"`{c[0]}`=?" for c in info.keys ])
            args = [ c[1] for c in info.keys ]
            query = f"SELECT {nonkeys} FROM `{info.table}` WHERE {where}{tail}"
            return [ query, args ]
        else:
            # @book/select_<tag>
            tag = 'all' if (info.tag is None) else info.tag
            query = self.db.sql(f"@{info.table}/select_{columns}-{tag}") + tail
            return [ query, info.keys ]

    @abstractmethod
    def _insert(self, x) -> Table.Insert:
        return None

    @abstractmethod
    def _update(self, x) -> Table.Update:
        return None

    @abstractmethod
    def _delete(self, x) -> Table.Delete:
        return None

    @abstractmethod
    def _select(self, x) -> Table.Select:
        return None
