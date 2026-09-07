from ds.core import *
from ds.model._dataset import Dataset
from quartz.gen.sqlite import Table


class BookAuthorManager(Dataset.BookAuthors):

    def __init__(self, ds, db):
        super().__init__(ds)
        self._table = Table("book_author", db, BookAuthorFilter())

    def add(self, x, debug=False):
        if isinstance(x, BookAuthor) and (x.id is None):
            x.id = self._table.insert(x, debug)
        else:
            self._table.insert(x, debug)
        return x

    def set(self, x, debug=False):
        # Fields
        if isinstance(x, tuple) and isinstance(x[0], BookAuthor) and isinstance(x[1], Fields):
            o, f = x
            if f == Fields.Rank:
                x = Table.Update("book_author", [ "rank", "book_id", "author_id" ], [ o.rank, o.book_id, o.author_id ], 2)
        return self._table.update(x, debug)

    def get(self, x:BookAuthor, field:Fields=None, debug=False):
        if field is None:
            row = self._table.select(Table.Select("book_author", [ "rank", "book_id", "author_id" ], [ x.book_id, x.author_id ], 2), one=True, debug=debug)
            x.rank = row[0]
        elif field == Fields.Rank:
            x.rank = self._table.select(Table.Select("book_author", [ "rank", "book_id", "author_id" ], [ x.book_id, x.author_id ], 2), one=True, debug=debug)[0]
    def remove(self, x, debug=False):
        return self._table.delete(x, debug)

    def has(self, x, debug=False) -> bool:
        return self._table.contains(x, debug)

    def clear(self, debug=False):
        self._table.deleteAll(debug)

    def find(self, x=None, tag:str="full", builder=None, one=False, order=None, debug=False) -> list[object]:
        return self._table.select(x, tag, builder, one, order, debug)

    def ref(self, x=None, order=None, debug=False) -> BookAuthorRef:
        return self._table.select(x, "pk", self._reference, True, order, debug)

    def refs(self, x=None, order=None, debug=False) -> list[BookAuthorRef]:
        return self._table.select(x, "pk", self._reference, False, order, debug)

    def one(self, x=None, order=None, debug=False) -> BookAuthor:
        return self._table.select(x, "full", self._create, True, order, debug)

    def all(self, x=None, order=None, debug=False) -> list[BookAuthor]:
        return self._table.select(x, "full", self._create, False, order, debug)

    def _reference(self, x):
        return BookAuthorRef(book_id=x[0], author_id=x[1])

    def _create(self, x):
        return BookAuthor(book_id=x[0], author_id=x[1], rank=x[2])


class BookAuthorFilter(Table.Filter):

    def insert(self, x):
        # book_author
        if isinstance(x, BookAuthor):
            return Table.Insert("book_author", True, [ x.book_id, x.author_id, x.rank ])

    def update(self, x):
        # book_author
        if isinstance(x, BookAuthor):
            return Table.Update("book_author", False, [ x.rank, x.book_id, x.author_id ])

    def delete(self, x):
        # pk
        if isinstance(x, BookAuthorRef):
            return Table.Delete("book_author", "pk", [x.book_id, x.author_id ])

    def select(self, x=None) -> tuple:
        # pk
        if isinstance(x, BookAuthor):
            return Table.Select("book_author", "pk", [ x.book_id, x.author_id ])
        # all
        if x is None:
            return Table.Select("book_author")

