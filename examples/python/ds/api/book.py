import ds.api._core as _core
import ds.model.book as _model
from ds.model._reference import *
from abc import abstractmethod


class Book(_model.Book, _core.Entity):

    class Publisher(_core.Submanager):

        def get(self):
            return None if (self._.publisher_id is None) else self.api.publishers.one(self._.publisher_id)

        def set(self, x:_core.PublisherRef):
            _core.PublisherRef.valid(x)
            self._.publisher_id = int(x)
            self.api.books.set(x)

    class Genres(_core.Submanager):

        def add(self, x, rank=1):
            return self.api.books.add(BookGenreRef(self._, int(x)))

        def remove(self, x):
            return self.api.books.remove(BookGenreRef(self._, int(x)))

        def all(self):
            return self.api.authors.all(BookRef(self._))

    class Authors(_core.Submanager):

        def add(self, x, rank=1):
            return self.api.books.add(BookAuthor(self._, int(x), rank))

        def remove(self, x):
            return self.api.books.remove(BookAuthorRef(self._, int(x)))

        def all(self):
            return self.api.genres.all(BookRef(self._))

    def __init__(self, publisher_id=None, title=None, year=None, id=None, api=None):
        super().__init__(publisher_id, title, year, id)
        self.api = api
        self._publisher = Book.Publisher(self)
        self._genres = Book.Genres(self)
        self._authors = Book.Authors(self)

    @property
    def publisher(self):
        return self._publisher

    @property
    def genres(self):
        return self._genres

    @property
    def authors(self):
        return self._authors

    def add(self, x):
        if isinstance(x, _core.Engine):
            return x.books.add(self)

    def remove(self):
        self.api.books.remove(self)
        self.id = None

    def push(self, x:Fields=None):
        return self.api.books.set(self if (x is None) else (self, x))

    def pull(self, x:Fields=None):
        return self.api.books.get(self, x)


class BookManager(_core.BookManager):

    def fetch(self, x: object, id:int=None, debug=False) -> Book:
        x_ = str(x)
        b = self.one(x_)
        if b is None:
            b = Book(id=id, title=x_, api=self.api)
            self.add(b, debug)
        return b

    def _create(self, x):
        return Book(id=x[0], publisher_id=x[1], title=x[2], year=x[3], api=self.api)
