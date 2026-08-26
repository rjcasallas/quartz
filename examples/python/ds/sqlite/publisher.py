from ds.model._data import *
from quartz.gen.data import Reference
from quartz.gen.sqlite import Manager
from quartz.error import Error


class PublisherSqliteManager(Dataset.Publishers, Manager):

    def __init__(self, ds, db):
        Dataset.Publishers.__init__(self, ds)
        Manager.__init__(self, 'publisher', db)


    def add(self, x:Publisher):
        p = Publisher.valid(x)
        if x.id is None:
            x.id = self.db.exec('@publisher/insert', [ x.parent_id, x.name ])
        else:
            self.db.exec('@publisher/insert_id', [ x.id, x.parent_id, x.name ])
        return p


    def update(self, x):
        p = Publisher.valid(x)
        self.db.exec('@publisher/update', [ x.parent_id, x.name, x.id ])
        return p


    def remove(self, x):
        if isinstance(x, int) or isinstance(x, PublisherRef):
            return self.db.exec('@publisher/delete_id', [ int(x) ])
        if isinstance(x, str):
            return self.db.exec('@publisher/delete_name', [ x ])
        Error.missing(f"remove 'publisher': {type(x)}")


    def _reference(self, x):
        return PublisherRef(x[0])


    def _instance(self, x):
        return Publisher(id=x[0], parent_id=x[1], name=x[2])


    def _ref(self, x = None) -> int:
        if x is None:
            sql = self.db.sql('@publisher/select_ref', 'LIMIT 1')
            return self.db.one(sql)
        if isinstance(x, int) or isinstance(x, PublisherRef):
            return self.db.one('@publisher/select_ref_by_pk', [ int(x) ])
        if isinstance(x, str):
            return self.db.one('@publisher/select_ref_by_name', [ x ])
        Error.missing(f"select 'publisher' ref: {type(x)}")


    def _refs(self, x = None) -> list[int]:
        if x is None:
            return self.db.all('@publisher/select_ref')
        Error.missing(f"select 'publisher' refs: {type(x)}")


    def _one(self, x = None) -> Publisher:
        if x is None:
            sql = self.db.sql('@publisher/select_all', 'LIMIT 1')
            return self.db.one(sql)
        if isinstance(x, int) or isinstance(x, PublisherRef):
            return self.db.one('@publisher/select_all_by_pk', [ int(x) ])
        if isinstance(x, str):
            return self.db.one('@publisher/select_all_by_name', [ x ])
        Error.missing(f"select 'publisher' get: {type(x)}")


    def _all(self, x = None) -> list[Publisher]:
        if x is None:
            return self.db.all('@publisher/select_all')
        Error.missing(f"select 'publisher' all: {type(x)}")