import ds.base.book as _base
from ds.base._core import Submanager
from ds.model._reference import *


class Book(_base.Book):

    class Publisher(Submanager):

        def get(self):
            return None if (self._.publisher_id is None) else self.api.publishers.one(self._.publisher_id)

        def set(self, x:_base.PublisherRef):
            _base.PublisherRef.valid(x)
            self._.publisher_id = int(x)
            self.api.books.set(x)

    class Genres(Submanager):

        def add(self, x, rank=1):
            return self.api.books.add(BookGenreRef(self._, int(x)))

        def remove(self, x):
            return self.api.books.remove(BookGenreRef(self._, int(x)))

        def all(self):
            return self.api.authors.all(BookRef(self._))

    class Authors(Submanager):

        def add(self, x, rank=1):
            return self.api.books.add(BookAuthor(self._, int(x), rank))

        def remove(self, x):
            return self.api.books.remove(BookAuthorRef(self._, int(x)))

        def all(self):
            return self.api.genres.all(BookRef(self._))

    def __init__(self, publisher_id=None, title=None, year=None, id=None, api=None):
        super().__init__(publisher_id, title, year, id, api)
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


class BookManager(_base.BookManager):

    def _create(self, x):
        return Book(id=x[0], publisher_id=x[1], title=x[2], year=x[3]).attach(self.api)
