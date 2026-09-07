import ds.api._core as _core
import ds.model.book as _model
from ds.model.book_author import *
from ds.base import *


class Book(_model.Book, _core.Entity):

    class Publisher(_core.Submanager):

        def pull(self):
            if self._.publisher_id is None: return None
            return self._en.publishers.one(self._.publisher_id)

        def push(self, x:_core.PublisherRef):
            self._.publisher_id = _core.PublisherRef.valid(x)
            self._en.books.push(self._, Fields.Publisher)

    class Genres(_core.Submanager):

        def add(self, x):
            return self._ds.books.add(BookGenreRef(self._, int(x)))

        def remove(self, x):
            return self._ds.books.remove(BookGenreRef(self._, int(x)))

        def all(self):
            return self._ds.authors.all(BookRef(self._))

    class Authors(_core.Submanager):

        def add(self, x, rank=1):
            return self._ds.book_authors.add(BookAuthor(int(self._), int(x), rank))

        def remove(self, x):
            return self._ds.book_authors.remove(BookAuthorRef(self._, int(x)))

        def all(self):
            return self._ds.genres.all(BookRef(self._))

    def __init__(self, publisher_id=None, title=None, year=None, id=None, api=None):
        super().__init__(publisher_id, title, year, id)
        self._en = api
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
            return x._ds.books.add(self.attach(x))

    def remove(self):
        self._ds.books.remove(self)
        self.id = None

    def push(self, field:Fields=None, api=None):
        if api: self.attach(api)
        return self._ds.books.push(self, field)

    def pull(self, field:Fields=None, api=None):
        if api: self.attach(api)
        return self._ds.books.pull(self, field)

    @staticmethod
    def valid(x):
        if isinstance(x, Book):
            return x
        Error.invalid("Book", x)


class BookManager(_core.Manager):

    def add(self, x):
        if isinstance(x, str):
            y = Book(title=x, api=self._en)
        else:
            Book.valid(x).attach(api=self._en)
        return self._ds.books.add(y)

    def remove(self, x):
        return self._ds.books.remove(x)

    def fetch(self, x:object, id:int=None) -> Book:
        s = str(x)
        o = self._ds.books.one(s)
        if o is None:
            o = Book(id=id, title=s, api=self._en)
            self._ds.books.add(o)
        return o

    def ref(self, x=None, order:list[str]=None, limit:str=None):
        return self._ds.books.ref(x, order, limit)

    def refs(self, x=None, order:list[str]=None, limit:str=None):
        return self._ds.books.refs(x, order, limit)

    def one(self, x=None, order:list[str]=None, limit:str=None):
        return self._ds.books.one(x, self._create, 'full', order, limit)

    def all(self, x=None, order:list[str]=None, limit:str=None):
        return self._ds.books.all(x, self._create, 'full', order, limit)

    def _create(self, x):
        return Book(id=x[0], publisher_id=x[1], title=x[2], year=x[3], api=self._en)
