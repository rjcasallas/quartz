from ds.model._base import *
import ds.model.book as _core
import ds.data._base as _base
from ds.data.publisher import *
from abc import abstractmethod


class Book(_core.Book, _base.Entity):

    class Publisher(_base.Submanager):

        def get(self):
            return None if (self._.publisher_id is None) else self.api.publishers.one(self._.publisher_id)

        def set(self, x:_base.PublisherRef):
            _base.PublisherRef.valid(x)
            self._.publisher_id = int(x)
            self.api.books.set(x)

    def __init__(self, publisher_id=None, title=None, year=None, id=None, api=None):
        super().__init__(publisher_id, title, year, id)
        self.api = api
        self._publisher = Book.Publisher(self)

    @property
    def publisher(self):
        return self._publisher

    def add(self, x):
        if isinstance(x, _base.Engine):
            return x.books.add(self)

    def remove(self):
        self.api.ds.books.remove(self)
        self.id = None

    def push(self, x:Fields=None):
        return self.api.ds.books.set(self if (x is None) else (self, x))

    def pull(self, x:Fields=None):
        return self.api.ds.books.get(self, x)


class BookManager(_base.BookManager):

    def add(self, x, debug=False):
        if isinstance(x, Book):
            x.attach(self.api)
        return self.api.ds.books.add(x, debug)

    def set(self, x, debug=False):
        if isinstance(x, Book):
            x.attach(self.api)
        return self.api.ds.books.set(x, debug)

    def get(self, x:Book, field:Fields=None, debug=False):
        if isinstance(x, Book):
            x.attach(self.api)
            return self.api.ds.books.get(x, field, debug)

    def remove(self, x: BookRef, debug=False):
        return self.api.ds.books.remove(x, debug)

    def clear(self, debug=False):
        self.api.ds.books.clear(debug)

    def has(self, x=None, debug=False) -> bool:
        return self.api.ds.books.has(x, debug)

    def ref(self, x=None, order=None, debug=False) -> BookRef:
        return self.api.ds.books.ref(x, order, debug)

    def refs(self, x=None, order=None, debug=False) -> list[BookRef]:
        return self.api.ds.books.refs(x, order, debug)

    def one(self, x=None, order=None, debug=False) -> Book:
        return self.api.ds.books.find(x, "full", self._create, True, order, debug)

    def all(self, x=None, order=None, debug=False) -> list[Book]:
        return self.api.ds.books.find(x, "full", self._create, False, order, debug)

    def fetch(self, x: object, id:int=None, debug=False) -> Book:
        x_ = str(x)
        b = self.one(x_)
        if b is None:
            b = self._create([ id, None, x_, None ])
            self.add(b, debug)
        return b

    @abstractmethod
    def _create(self, x):
        return None

