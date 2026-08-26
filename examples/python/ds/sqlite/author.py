from ds.model._data import *
from quartz.gen.data import Reference
from quartz.gen.sqlite import Manager
from quartz.error import Error


class AuthorSqliteManager(Dataset.Authors, Manager):

    def __init__(self, ds, db):
        Dataset.Authors.__init__(self, ds)
        Manager.__init__(self, 'author', db)


    def add(self, x:Author):
        a = Author.valid(x)
        if x.id is None:
            x.id = self.db.exec('@author/insert', [ x.name ])
        else:
            self.db.exec('@author/insert_id', [ x.id, x.name ])
        return a


    def update(self, x):
        a = Author.valid(x)
        self.db.exec('@author/update', [ x.name, x.id ])
        return a


    def remove(self, x):
        if isinstance(x, int) or isinstance(x, AuthorRef):
            return self.db.exec('@author/delete_id', [ int(x) ])
        if isinstance(x, str):
            return self.db.exec('@author/delete_name', [ x ])
        Error.missing(f"remove 'author': {type(x)}")


    def link(self, x, y):
        if not (isinstance(x, int) or isinstance(x, AuthorRef)):
            Error.invalid("author link base", x)
        if not isinstance(x, Reference):
            Error.invalid("author link target", x)
        return self._link(int(x), y)

    def unlink(self, x, y):
        if not (isinstance(x, int) or isinstance(x, AuthorRef)):
            Error.invalid("author link base", x)
        if not isinstance(x, Reference):
            Error.invalid("author link target", x)
        return self._unlink(int(x), y)


    def _reference(self, x):
        return AuthorRef(x[0])


    def _instance(self, x):
        return Author(id=x[0], name=x[1])


    def _link(self, base_id, x):
        # "author_book" author.id → book.id
        if isinstance(x, BookRef):
            return self.db.exec('@author/insert_book', [ base_id, int(x) ])
        Error.invalid("author link target", x)


    def _unlink(self, base_id, x):
        # "author_book" author.id → book.id
        if isinstance(x, BookRef):
            return self.db.exec('@author/delete_book', [ base_id, int(x) ])
        Error.invalid("author link target", x)


    def _ref(self, x = None) -> int:
        if x is None:
            sql = self.db.sql('@author/select_ref', 'LIMIT 1')
            return self.db.one(sql)
        if isinstance(x, int) or isinstance(x, AuthorRef):
            return self.db.one('@author/select_ref_by_pk', [ int(x) ])
        if isinstance(x, str):
            return self.db.one('@author/select_ref_by_name', [ x ])
        Error.missing(f"select 'author' ref: {type(x)}")


    def _refs(self, x = None) -> list[int]:
        if x is None:
            return self.db.all('@author/select_ref')
        Error.missing(f"select 'author' refs: {type(x)}")


    def _one(self, x = None) -> Author:
        if x is None:
            sql = self.db.sql('@author/select_all', 'LIMIT 1')
            return self.db.one(sql)
        if isinstance(x, int) or isinstance(x, AuthorRef):
            return self.db.one('@author/select_all_by_pk', [ int(x) ])
        if isinstance(x, str):
            return self.db.one('@author/select_all_by_name', [ x ])
        Error.missing(f"select 'author' get: {type(x)}")


    def _all(self, x = None) -> list[Author]:
        if x is None:
            return self.db.all('@author/select_all')
        Error.missing(f"select 'author' all: {type(x)}")