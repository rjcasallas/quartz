from ds.model._data import *
from quartz.gen.data import Reference
from quartz.gen.sqlite import Manager
from quartz.error import Error


class BookAuthorSqliteManager(Dataset.BookAuthors, Manager):

    def __init__(self, ds, db):
        Dataset.BookAuthors.__init__(self, ds)
        Manager.__init__(self, 'book_author', db)


    def add(self, x:BookAuthor):
        ba = BookAuthor.valid(x)
        self.db.exec('@book_author/replace', [ x.book_id, x.author_id, x.rank ])
        return ba


    def update(self, x):
        ba = BookAuthor.valid(x)
        self.db.exec('@book_author/update', [ x.rank, x.book_id, x.author_id ])
        return ba


    def remove(self, x):
        if isinstance(x, BookAuthorRef):
            return self.db.exec('@book_author/delete_id', [ x.book_id, x.author_id ])
        Error.missing(f"remove 'book_author': {type(x)}")


    def _reference(self, x):
        return BookAuthorRef(book_id=x[0], author_id=x[1])


    def _instance(self, x):
        return BookAuthor(book_id=x[0], author_id=x[1], rank=x[2])


    def _ref(self, x = None) -> BookAuthor:
        if x is None:
            sql = self.db.sql('@book_author/select_ref', 'LIMIT 1')
            return self.db.one(sql)
        if isinstance(x, BookAuthor):
            return self.db.one('@book_author/select_ref_by_pk', x.book_id, x.author_id)
        Error.missing(f"select 'book_author' ref: {type(x)}")


    def _refs(self, x = None) -> list[BookAuthor]:
        if x is None:
            return self.db.all('@book_author/select_ref')
        Error.missing(f"select 'book_author' refs: {type(x)}")


    def _one(self, x = None) -> BookAuthor:
        if x is None:
            sql = self.db.sql('@book_author/select_all', 'LIMIT 1')
            return self.db.one(sql)
        if isinstance(x, BookAuthor):
            return self.db.one('@book_author/select_all_by_pk', x.book_id, x.author_id)
        Error.missing(f"select 'book_author' get: {type(x)}")


    def _all(self, x = None) -> list[BookAuthor]:
        if x is None:
            return self.db.all('@book_author/select_all')
        Error.missing(f"select 'book_author' all: {type(x)}")