from ds.core import *
from ds.model._dataset import Dataset
from quartz.gen.sqlite import Table


class PublisherManager(Dataset.Publishers):

    def __init__(self, ds, db):
        super().__init__(ds)
        self._table = Table("publisher", db, PublisherFilter())

    def add(self, x, debug=False):
        if isinstance(x, Publisher) and (x.id is None):
            x.id = self._table.insert(x, debug)
        else:
            self._table.insert(x, debug)
        return x

    def set(self, x, debug=False):
        # Fields
        if isinstance(x, tuple) and isinstance(x[0], Publisher) and isinstance(x[1], Fields):
            o, f = x
            if f == Fields.Parent:
                x = Table.Update("publisher", [ "parent_id", "id" ], [ o.parent_id, o.id ], 1)
            if f == Fields.Name:
                x = Table.Update("publisher", [ "name", "id" ], [ o.name, o.id ], 1)
        return self._table.update(x, debug)

    def get(self, x:Publisher, field:Fields=None, debug=False):
        if field is None:
            row = self._table.select(Table.Select("publisher", [ "parent_id", "name", "id" ], [ x.id ], 1), one=True, debug=debug)
            x.parent_id = row[0]
            x.name = row[1]
        elif field == Fields.Parent:
            x.parent_id = self._table.select(Table.Select("publisher", [ "parent", "id" ], [ x.id ], 1), one=True, debug=debug)[0]
        elif field == Fields.Name:
            x.name = self._table.select(Table.Select("publisher", [ "name", "id" ], [ x.id ], 1), one=True, debug=debug)[0]
    def remove(self, x, debug=False):
        return self._table.delete(x, debug)

    def has(self, x, debug=False) -> bool:
        return self._table.contains(x, debug)

    def clear(self, debug=False):
        self._table.deleteAll(debug)

    def find(self, x=None, tag:str="full", builder=None, one=False, order=None, debug=False) -> list[object]:
        return self._table.select(x, tag, builder, one, order, debug)

    def ref(self, x=None, order=None, debug=False) -> PublisherRef:
        return self._table.select(x, "pk", self._reference, True, order, debug)

    def refs(self, x=None, order=None, debug=False) -> list[PublisherRef]:
        return self._table.select(x, "pk", self._reference, False, order, debug)

    def one(self, x=None, order=None, debug=False) -> Publisher:
        return self._table.select(x, "full", self._create, True, order, debug)

    def all(self, x=None, order=None, debug=False) -> list[Publisher]:
        return self._table.select(x, "full", self._create, False, order, debug)

    def _reference(self, x):
        return PublisherRef(id=x[0])

    def _create(self, x):
        return Publisher(id=x[0], parent_id=x[1], name=x[2])


class PublisherFilter(Table.Filter):

    def insert(self, x):
        # publisher
        if isinstance(x, Publisher):
            return Table.Insert("publisher", False, [ x.id, x.parent_id, x.name ])

    def update(self, x):
        # publisher
        if isinstance(x, Publisher):
            return Table.Update("publisher", False, [ x.parent_id, x.name, x.id ])

    def delete(self, x):
        # "parent_publisher" publisher.parent_id → publisher.id (recursive)
        if isinstance(x, ParentPublisherRef):
            return Table.Delete("publisher", [ "parent" ], [ int(x) ])
        # pk
        if isinstance(x, int) or isinstance(x, PublisherRef):
            return Table.Delete("publisher", "pk", [ int(x) ])
        # name
        if isinstance(x, str):
            return Table.Delete("publisher", "name", [ x ])

    def select(self, x=None) -> tuple:
        # "parent_publisher" publisher.parent_id → publisher.id (recursive)
        if isinstance(x, ParentPublisherRef):
            return Table.Select("publisher", "parent", [ int(x) ])
        # pk
        if isinstance(x, int) or isinstance(x, PublisherRef):
            return Table.Select("publisher", "pk", [ int(x) ])
        # name (lookup)
        if isinstance(x, str):
            return Table.Select("publisher", "name", [ x ])
        # all
        if x is None:
            return Table.Select("publisher")

