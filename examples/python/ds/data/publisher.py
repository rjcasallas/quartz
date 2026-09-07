from ds.base import *
from ds.model.publisher import *
from ds.model._dataset import Dataset
from quartz.data.table import Table


class PublisherData(Dataset.Publishers):

    def __init__(self, db):
        self._table = PublisherTable("publisher", db)

    def add(self, x, debug:bool=False):
        if isinstance(x, Publisher) and (x.id is None):
            x.id = self._table.insert(x, debug)
            return x
        elif self._replace(x, debug):
            return x
        self._table.insert(x, debug)
        return x

    def remove(self, x, debug:bool=False):
        return self._table.delete(x, debug)

    def push(self, x, field:Fields=None, debug:bool=False):
        if self._replace(x, True, debug):
            return x
        if isinstance(x, Publisher) and isinstance(field, Fields):
            match field:
                case Fields.Parent:
                    x = Table.Info("publisher", [ ("id", x.id), ("parent_id", x.parent_id) ], 1)
                case Fields.Name:
                    x = Table.Info("publisher", [ ("id", x.id), ("name", x.name) ], 1)
                case _:
                    x = None
        return self._table.update(x, debug) if (x is not None) else None

    def pull(self, x:Publisher, field:Fields=None, debug:bool=False):
        match field:
            case None:
                row = self._table.one(Table.Info("publisher", [ ("id", x.id), ("parent_id", None), ("name", None) ], 1), debug=debug)
                if (isinstance(row, tuple) or isinstance(row, list)) and (len(row) > 0):
                    x.parent_id = row[0]
                    x.name = row[1]
            case Fields.Parent:
                row = self._table.one(Table.Info("publisher", [ ("id", x.id), ("parent_id", None) ], 1), debug=debug)
                if (isinstance(row, tuple) or isinstance(row, list)) and (len(row) > 0):
                    x.parent_id = row[0]
            case Fields.Name:
                row = self._table.one(Table.Info("publisher", [ ("id", x.id), ("name", None) ], 1), debug=debug)
                if (isinstance(row, tuple) or isinstance(row, list)) and (len(row) > 0):
                    x.name = row[0]
        return x

    def has(self, x, debug:bool=False) -> bool:
        return self.ref(x, debug) is not None

    def clear(self, debug:bool=False):
        self._table.deleteAll(debug)

    def refb(self, x=None, order:list[str]=None, limit:str=None, debug:bool=False):
        return self.begin(x, 'pk', order, limit, debug)

    def refn(self, cursor) -> Reference:
        return self.next(cursor, self._reference)

    def ref(self, x=None, order:list[str]=None, limit:str=None, debug:bool=False):
        return self.one(x, self._reference, 'pk', order, limit, debug)

    def refs(self, x=None, order:list[str]=None, limit:str=None, debug:bool=False):
        return self.all(x, self._reference, 'pk', order, limit, debug)

    def begin(self, x=None, columns:str='full', order:list[str]=None, limit:str=None, debug:bool=False):
        return self._table.begin(x, columns, order, limit, debug)

    def next(self, cursor, builder=None):
        fn = self._create if (builder is None) else builder
        return self._table.next(cursor, fn)

    def one(self, x=None, builder=None, columns:str='full', order:list[str]=None, limit:str=None, debug:bool=False):
        fn = self._create if (builder is None) else builder
        return self._table.one(x, fn, columns, order, limit, debug)

    def all(self, x=None, builder=None, columns:str='full', order:list[str]=None, limit:str=None, debug:bool=False):
        fn = self._create if (builder is None) else builder
        return self._table.select(x, fn, columns, order, limit, debug)

    def _replace(self, x, allow_delete=False, debug:bool=False) -> bool:
        return False

    def _reference(self, x):
        return PublisherRef(id=x[0])

    def _create(self, x):
        return Publisher(id=x[0], parent_id=x[1], name=x[2])


class PublisherTable(Table):

    def _insert(self, x):
        # publisher
        if isinstance(x, Publisher):
            return Table.Info("publisher", [ x.id, x.parent_id, x.name ], 1, tag=("insert" if (x.id is None) else "insert_id"))

    def _update(self, x):
        # publisher
        if isinstance(x, Publisher):
            return Table.Info("publisher", [ x.id, x.parent_id, x.name ], 1, tag="update")

    def _delete(self, x):
        # "parent_publisher" publisher.parent_id → publisher.id (recursive)
        if isinstance(x, ParentPublisherRef):
            return Table.Info("publisher", [ ("parent", int(x)) ])
        # pk
        if isinstance(x, int) or isinstance(x, PublisherRef):
            return Table.Info("publisher", [ int(x) ], tag="pk")
        # name
        if isinstance(x, str):
            return Table.Info("publisher", [ x ], tag="name")

    def _select(self, x=None) -> tuple:
        # "parent_publisher" publisher.parent_id → publisher.id (recursive)
        if isinstance(x, ParentPublisherRef):
            return Table.Info("publisher", [ int(x) ], tag="parent")
        # pk
        if isinstance(x, int) or isinstance(x, PublisherRef):
            return Table.Info("publisher", [ int(x) ], tag="pk")
        # name (lookup)
        if isinstance(x, str):
            return Table.Info("publisher", [ x ], tag="name")
        # all
        if x is None:
            return Table.Info("publisher", tag="all")

