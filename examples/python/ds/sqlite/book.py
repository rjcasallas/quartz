from ds.model._data import *
from quartz.gen.data import Reference
from quartz.gen.sqlite import Manager
from quartz.error import Error


class BookSqliteManager(Dataset.Books, Manager):

    def __init__(self, ds, db):
        Dataset.Books.__init__(self, ds)
        Manager.__init__(self, 'book', db)


    def add(self, x:Book):
        b = Book.valid(x)
        if x.id is None:
            x.id = self.db.exec('@book/insert', [ x.publisher_id, x.title, x.year ])
        else:
            self.db.exec('@book/insert_id', [ x.id, x.publisher_id, x.title, x.year ])
        return b


    def update(self, x):
        b = Book.valid(x)
        self.db.exec('@book/update', [ x.publisher_id, x.title, x.year, x.id ])
        return b


    def remove(self, x):
        if isinstance(x, int) or isinstance(x, BookRef):
            return self.db.exec('@book/delete_id', [ int(x) ])
        if isinstance(x, str):
            return self.db.exec('@book/delete_title', [ x ])
        Error.missing(f"remove 'book': {type(x)}")


    def link(self, x, y):
        if not (isinstance(x, int) or isinstance(x, BookRef)):
            Error.invalid("book link base", x)
        if not isinstance(x, Reference):
            Error.invalid("book link target", x)
        return self._link(int(x), y)

    def unlink(self, x, y):
        if not (isinstance(x, int) or isinstance(x, BookRef)):
            Error.invalid("book link base", x)
        if not isinstance(x, Reference):
            Error.invalid("book link target", x)
        return self._unlink(int(x), y)


    def _reference(self, x):
        return BookRef(x[0])


    def _instance(self, x):
        return Book(id=x[0], publisher_id=x[1], title=x[2], year=x[3])


    def _link(self, base_id, x):
        # "book_author" book.id → author.id
        if isinstance(x, AuthorRef):
            return self.db.exec('@book/insert_author', [ base_id, int(x) ])
        # "book_genre" book.id → genre.id
        if isinstance(x, GenreRef):
            return self.db.exec('@book/insert_genre', [ base_id, int(x) ])
        Error.invalid("book link target", x)


    def _unlink(self, base_id, x):
        # "book_author" book.id → author.id
        if isinstance(x, AuthorRef):
            return self.db.exec('@book/delete_author', [ base_id, int(x) ])
        # "book_genre" book.id → genre.id
        if isinstance(x, GenreRef):
            return self.db.exec('@book/delete_genre', [ base_id, int(x) ])
        Error.invalid("book link target", x)


    def _ref(self, x = None) -> int:
        if x is None:
            sql = self.db.sql('@book/select_ref', 'LIMIT 1')
            return self.db.one(sql)
        if isinstance(x, int) or isinstance(x, BookRef):
            return self.db.one('@book/select_ref_by_pk', [ int(x) ])
        if isinstance(x, str):
            return self.db.one('@book/select_ref_by_title', [ x ])
        Error.missing(f"select 'book' ref: {type(x)}")


    def _refs(self, x = None) -> list[int]:
        if x is None:
            return self.db.all('@book/select_ref')
        Error.missing(f"select 'book' refs: {type(x)}")


    def _one(self, x = None) -> Book:
        if x is None:
            sql = self.db.sql('@book/select_all', 'LIMIT 1')
            return self.db.one(sql)
        if isinstance(x, int) or isinstance(x, BookRef):
            return self.db.one('@book/select_all_by_pk', [ int(x) ])
        if isinstance(x, str):
            return self.db.one('@book/select_all_by_title', [ x ])
        Error.missing(f"select 'book' get: {type(x)}")


    def _all(self, x = None) -> list[Book]:
        if x is None:
            return self.db.all('@book/select_all')
        Error.missing(f"select 'book' all: {type(x)}")