from ds.model._dataset import *
import quartz.gen.sqlite as _sqlite
from quartz.error import Error


class PublisherManager(Dataset.Publishers, _sqlite.Table):

    def __init__(self, ds, db):
        Dataset.Publishers.__init__(self, ds)
        _sqlite.Table.__init__(self, "publisher", db)

    def add(self, x: Publisher):
        return self._add(x)

    def remove(self, x):
        return self._remove(x)

    def has(self, x) -> bool:
        return self.contains(x)

    def clear(self):
        self.deleteAll()

    def update(self, x: Publisher):
        Publisher.valid(x)
        _sqlite.Table.update(self, [ x.parent_id, x.name, x.id ])
        return x

    def ref(self, x = None) -> PublisherRef:
        return self.selectRef(x)

    def one(self, x = None) -> Publisher:
        return self.selectOne(x)

    def refs(self, x = None) -> list[PublisherRef]:
        return self.selectRefs(x)

    def all(self, x = None) -> list[Publisher]:
        return self.selectAll(x)

    def _reference(self, x):
        return PublisherRef(id=x[0])

    def _instance(self, x):
        return Publisher(id=x[0], parent_id=x[1], name=x[2])

    def _add(self, x):
        # publisher
        if isinstance(x, Publisher):
            if x.id is None:
                x.id = self.insert([ x.parent_id, x.name ], auto=True)
            else:
                self.insert([ x.id, x.parent_id, x.name ])
            return x
        # "publisher_book" book.publisher_id → publisher.id
        if isinstance(x, PublisherRef):
            return self.db.exec("@publisher/replace", [ x.id, x.parent_id, x.name ])
        # "parent_publisher" publisher.parent_id → publisher.id (self-referencing)
        if isinstance(x, PublisherRef):
            return self.db.exec("@publisher/replace", [ x.id, x.parent_id, x.name ])
        return Error.invalid("publisher", x)

    def _remove(self, x):
        # publisher
        if isinstance(x, PublisherRef):
            return self.db.exec("@publisher/delete_pk", [ int(x) ])
        if isinstance(x, str):
            return self.db.exec("@publisher/delete_name", [ x ])
        # "publisher_book" book.publisher_id → publisher.id
        if isinstance(x, PublisherRef):
            return self.db.exec("@publisher/delete_pk", [ x.id, x.parent_id, x.name ])
        # "parent_publisher" publisher.parent_id → publisher.id (self-referencing)
        if isinstance(x, PublisherRef):
            return self.db.exec("@publisher/delete_pk", [ x.id, x.parent_id, x.name ])

        return self.delete(x)

    def _ref(self, x = None) -> PublisherRef:
        # "parent_publisher" publisher.parent_id → publisher.id (self-referencing)
        if isinstance(x, ParentPublisherRef):
            return self.db.one("@publisher/select_ref_by_parent", [ int(x) ])
        # "publisher_book" book.publisher_id → publisher.id 
        if isinstance(x, BookRef):
            return self.db.one("@publisher/select_ref_by_book", [ int(x) ])
        # pk
        if isinstance(x, int) or isinstance(x, PublisherRef):
            return self.db.one("@publisher/select_ref_by_pk", [ int(x) ])
        # name
        if isinstance(x, str):
            return self.db.one("@publisher/select_ref_by_name", [ x ])
        return super()._ref(x)

    def _one(self, x = None) -> Publisher:
        # "parent_publisher" publisher.parent_id → publisher.id (self-referencing)
        if isinstance(x, ParentPublisherRef):
            return self.db.one("@publisher/select_all_by_parent", [ int(x) ])
        # "publisher_book" book.publisher_id → publisher.id 
        if isinstance(x, BookRef):
            return self.db.one("@publisher/select_all_by_book", [ int(x) ])
        # pk
        if isinstance(x, int) or isinstance(x, PublisherRef):
            return self.db.one("@publisher/select_all_by_pk", [ int(x) ])
        # name
        if isinstance(x, str):
            return self.db.one("@publisher/select_all_by_name", [ x ])
        return super()._one(x)

    def _refs(self, x = None) -> list[PublisherRef]:
        # "parent_publisher" publisher.parent_id → publisher.id (self-referencing)
        if isinstance(x, ParentPublisherRef):
            return self.db.all("@publisher/select_ref_by_parent", [ int(x) ])
        # "publisher_book" book.publisher_id → publisher.id 
        if isinstance(x, BookRef):
            return self.db.all("@publisher/select_ref_by_book", [ int(x) ])
        return super()._refs(x)

    def _all(self, x = None) -> list[Publisher]:
        # "parent_publisher" publisher.parent_id → publisher.id (self-referencing)
        if isinstance(x, ParentPublisherRef):
            return self.db.all("@publisher/select_all_by_parent", [ int(x) ])
        # "publisher_book" book.publisher_id → publisher.id 
        if isinstance(x, BookRef):
            return self.db.all("@publisher/select_all_by_book", [ int(x) ])
        return super()._all(x)