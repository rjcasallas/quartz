import ds.data._base as _base
import ds.model._dataset as _model
from quartz.error import Error


class Book(_base.Book):

    def __init__(self, publisher=None, title=None, year=None, id:int=None):
        _base.Book.__init__(self, None, title, year, id)
        _base.Entity.__init__(self)
        self.publisher = publisher

    @property
    def publisher_id(self):
        return self._publisher.id if self._publisher else None
    @publisher_id.setter
    def publisher_id(self, x):
        pass

    @property
    def publisher(self):
        return self._publisher
    @publisher.setter
    def publisher(self, x):
        self._publisher = _base.Publisher.valid(x, True, False)

    def add(self, x):
        if isinstance(x, _base.Engine):
            return x.books.add(self)

    def remove(self):
        self.data.ds.books.remove(self)
        self.id = None

    def link(self, x):
        return self.data.books.link(self, x)

    def unlink(self, x):
        return self.data.books.unlink(self, x)


class BookManager(_base.BookManager):

    def add(self, x: Book):
        return self.data.ds.books.add(x)

    def update(self, x: Book):
        return self.data.ds.books.update(x)

    def remove(self, x: _model.BookRef):
        return self.data.ds.books.remove(x)

    def clear(self):
        self.data.ds.books.clear()

    def has(self, x = None) -> bool:
        return self.data.ds.books.has(x)

    def fetch(self, x: object, id:int = None) -> Book:
        x_ = str(x)
        b = self.one(x_)
        if b is None:
            b = self.add(Book(x_, id))
        return b

    def ref(self, x = None) -> _model.BookRef:
        return self.data.ds.books.ref(x)

    def refs(self, x = None) -> list[_model.BookRef]:
        return self.data.ds.books.refs(x)

    def one(self, x = None) -> Book:
        return self.data.ds.books.one(x)

    def all(self, x = None) -> list[Book]:
        return self.data.ds.books.all(x)
