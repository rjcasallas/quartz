from ds.core import *
from ds.model._dataset import Dataset
from quartz.gen.sqlite import Table


class BookManager(Dataset.Books):

    def __init__(self, ds, db):
        super().__init__(ds)
        self._table = Table("book", db, BookFilter())

    def add(self, x, debug=False):
        if isinstance(x, Book) and (x.id is None):
            x.id = self._table.insert(x, debug)
        else:
            self._table.insert(x, debug)
        return x

    def set(self, x, debug=False):
        # "book_author" author.id → book.id
        if isinstance(x, BookAuthorRef):
            if (x.book_id is None) or (x.author_id is None):
                return self._table.delete(x, debug)
        # "book_genre" genre.id → book.id
        if isinstance(x, BookGenreRef):
            if (x.book_id is None) or (x.genre_id is None):
                return self._table.delete(x, debug)
        # Fields
        if isinstance(x, tuple) and isinstance(x[0], Book) and isinstance(x[1], Fields):
            o, f = x
            if f == Fields.Publisher:
                x = Table.Update("book", [ "publisher_id", "id" ], [ o.publisher_id, o.id ], 1)
            if f == Fields.Title:
                x = Table.Update("book", [ "title", "id" ], [ o.title, o.id ], 1)
            if f == Fields.Year:
                x = Table.Update("book", [ "year", "id" ], [ o.year, o.id ], 1)
        return self._table.update(x, debug)

    def get(self, x:Book, field:Fields=None, debug=False):
        if field is None:
            row = self._table.select(Table.Select("book", [ "publisher_id", "title", "year", "id" ], [ x.id ], 1), one=True, debug=debug)
            x.publisher_id = row[0]
            x.title = row[1]
            x.year = row[2]
        elif field == Fields.Publisher:
            x.publisher_id = self._table.select(Table.Select("book", [ "publisher", "id" ], [ x.id ], 1), one=True, debug=debug)[0]
        elif field == Fields.Title:
            x.title = self._table.select(Table.Select("book", [ "title", "id" ], [ x.id ], 1), one=True, debug=debug)[0]
        elif field == Fields.Year:
            x.year = self._table.select(Table.Select("book", [ "year", "id" ], [ x.id ], 1), one=True, debug=debug)[0]
    def remove(self, x, debug=False):
        return self._table.delete(x, debug)

    def has(self, x, debug=False) -> bool:
        return self._table.contains(x, debug)

    def clear(self, debug=False):
        self._table.deleteAll(debug)

    def find(self, x=None, tag:str="full", builder=None, one=False, order=None, debug=False) -> list[object]:
        return self._table.select(x, tag, builder, one, order, debug)

    def ref(self, x=None, order=None, debug=False) -> BookRef:
        return self._table.select(x, "pk", self._reference, True, order, debug)

    def refs(self, x=None, order=None, debug=False) -> list[BookRef]:
        return self._table.select(x, "pk", self._reference, False, order, debug)

    def one(self, x=None, order=None, debug=False) -> Book:
        return self._table.select(x, "full", self._create, True, order, debug)

    def all(self, x=None, order=None, debug=False) -> list[Book]:
        return self._table.select(x, "full", self._create, False, order, debug)

    def _reference(self, x):
        return BookRef(id=x[0])

    def _create(self, x):
        return Book(id=x[0], publisher_id=x[1], title=x[2], year=x[3])


class BookFilter(Table.Filter):

    def insert(self, x):
        # book
        if isinstance(x, Book):
            return Table.Insert("book", False, [ x.id, x.publisher_id, x.title, x.year ])
        # "book_author" author.id → book.id
        if isinstance(x, BookAuthorRef):
            return Table.Insert("book_author", True, [ x.book_id, x.author_id, x.rank ])
        # "book_genre" genre.id → book.id
        if isinstance(x, BookGenreRef):
            return Table.Insert("book_genre", True, [ x.book_id, x.genre_id ])

    def update(self, x):
        # book
        if isinstance(x, Book):
            return Table.Update("book", False, [ x.publisher_id, x.title, x.year, x.id ])
        # "book_author" author.id → book.id
        if isinstance(x, BookAuthorRef):
            return Table.Update("book_author", True, [x.rank, x.book_id, x.author_id ])
        # "book_genre" genre.id → book.id
        if isinstance(x, BookGenreRef):
            return Table.Update("book_genre", True, [x.book_id, x.genre_id ])

    def delete(self, x):
        # "book_author" author.id → book.id
        if isinstance(x, BookAuthorRef):
            return Table.Delete("book_author", [ "book_id", "author_id" ], [ x.book_id, x.author_id ])
        # "book_genre" genre.id → book.id
        if isinstance(x, BookGenreRef):
            return Table.Delete("book_genre", [ "book_id", "genre_id" ], [ x.book_id, x.genre_id ])
        # pk
        if isinstance(x, int) or isinstance(x, BookRef):
            return Table.Delete("book", "pk", [ int(x) ])
        # title
        if isinstance(x, str):
            return Table.Delete("book", "title", [ x ])

    def select(self, x=None) -> tuple:
        # "book_author" author.id → book.id 
        if isinstance(x, AuthorRef):
            return Table.Select("book", "author", [ int(x) ])
        # "book_genre" genre.id → book.id 
        if isinstance(x, GenreRef):
            return Table.Select("book", "genre", [ int(x) ])
        # pk
        if isinstance(x, int) or isinstance(x, BookRef):
            return Table.Select("book", "pk", [ int(x) ])
        # title (lookup)
        if isinstance(x, str):
            return Table.Select("book", "title", [ x ])
        # publisher (foreign)
        if isinstance(x, PublisherRef):
            return Table.Select("book", "publisher", [ int(x) ])
        # all
        if x is None:
            return Table.Select("book")

