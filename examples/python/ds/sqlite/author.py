from ds.core import *
from ds.model._dataset import Dataset
from quartz.gen.sqlite import Table


class AuthorManager(Dataset.Authors):

    def __init__(self, ds, db):
        super().__init__(ds)
        self._table = Table("author", db, AuthorFilter())

    def add(self, x, debug=False):
        if isinstance(x, Author) and (x.id is None):
            x.id = self._table.insert(x, debug)
        else:
            self._table.insert(x, debug)
        return x

    def set(self, x, debug=False):
        # "author_book" book.id → author.id
        if isinstance(x, BookAuthorRef):
            if (x.book_id is None) or (x.author_id is None):
                return self._table.delete(x, debug)
        # Fields
        if isinstance(x, tuple) and isinstance(x[0], Author) and isinstance(x[1], Fields):
            o, f = x
            if f == Fields.Name:
                x = Table.Update("author", [ "name", "id" ], [ o.name, o.id ], 1)
        return self._table.update(x, debug)

    def get(self, x:Author, field:Fields=None, debug=False):
        if field is None:
            row = self._table.select(Table.Select("author", [ "name", "id" ], [ x.id ], 1), one=True, debug=debug)
            x.name = row[0]
        elif field == Fields.Name:
            x.name = self._table.select(Table.Select("author", [ "name", "id" ], [ x.id ], 1), one=True, debug=debug)[0]
    def remove(self, x, debug=False):
        return self._table.delete(x, debug)

    def has(self, x, debug=False) -> bool:
        return self._table.contains(x, debug)

    def clear(self, debug=False):
        self._table.deleteAll(debug)

    def find(self, x=None, tag:str="full", builder=None, one=False, order=None, debug=False) -> list[object]:
        return self._table.select(x, tag, builder, one, order, debug)

    def ref(self, x=None, order=None, debug=False) -> AuthorRef:
        return self._table.select(x, "pk", self._reference, True, order, debug)

    def refs(self, x=None, order=None, debug=False) -> list[AuthorRef]:
        return self._table.select(x, "pk", self._reference, False, order, debug)

    def one(self, x=None, order=None, debug=False) -> Author:
        return self._table.select(x, "full", self._create, True, order, debug)

    def all(self, x=None, order=None, debug=False) -> list[Author]:
        return self._table.select(x, "full", self._create, False, order, debug)

    def _reference(self, x):
        return AuthorRef(id=x[0])

    def _create(self, x):
        return Author(id=x[0], name=x[1])


class AuthorFilter(Table.Filter):

    def insert(self, x):
        # author
        if isinstance(x, Author):
            return Table.Insert("author", False, [ x.id, x.name ])
        # "author_book" book.id → author.id
        if isinstance(x, BookAuthorRef):
            return Table.Insert("book_author", True, [ x.book_id, x.author_id, x.rank ])

    def update(self, x):
        # author
        if isinstance(x, Author):
            return Table.Update("author", False, [ x.name, x.id ])
        # "author_book" book.id → author.id
        if isinstance(x, BookAuthorRef):
            return Table.Update("book_author", True, [x.rank, x.book_id, x.author_id ])

    def delete(self, x):
        # "author_book" book.id → author.id
        if isinstance(x, BookAuthorRef):
            return Table.Delete("book_author", [ "book_id", "author_id" ], [ x.book_id, x.author_id ])
        # pk
        if isinstance(x, int) or isinstance(x, AuthorRef):
            return Table.Delete("author", "pk", [ int(x) ])
        # name
        if isinstance(x, str):
            return Table.Delete("author", "name", [ x ])

    def select(self, x=None) -> tuple:
        # "author_book" book.id → author.id 
        if isinstance(x, BookRef):
            return Table.Select("author", "book", [ int(x) ])
        # pk
        if isinstance(x, int) or isinstance(x, AuthorRef):
            return Table.Select("author", "pk", [ int(x) ])
        # name (lookup)
        if isinstance(x, str):
            return Table.Select("author", "name", [ x ])
        # all
        if x is None:
            return Table.Select("author")

