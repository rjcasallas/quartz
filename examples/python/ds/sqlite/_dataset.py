import ds.model._dataset as _base
from ds.sqlite.author import *
from ds.sqlite.book import *
from ds.sqlite.genre import *
from ds.sqlite.publisher import *
import quartz.db.sqlite as _sqlite

#
# Filters
#

class YearFilter:

    def __init__(self, year):
        self._year = year

    @property
    def year(self):
        return self._year

#
# Managers
#

class AuthorManager(AuthorManager):

    def _refs(self, x = None) -> list[AuthorRef]:
        if isinstance(x, BookRef) or isinstance(x, Book):
            return self.db.all('@author/select_ref_by_book', [ int(x) ])
        return super()._refs(x)


class BookManager(BookManager):

    def _refs(self, x = None) -> list[BookRef]:
        if isinstance(x, AuthorRef) or isinstance(x, Author):
            return self.db.all('@book/select_ref_by_author', [ int(x) ])
        if isinstance(x, GenreRef) or isinstance(x, Genre):
            return self.db.all('@book/select_ref_by_genre', [ int(x) ])
        if isinstance(x, YearFilter):
            return self.db.all('@book/select_ref_by_year', [ x.year ])
        return super()._refs(x)

    def _all(self, x = None) -> list[Book]:
        if isinstance(x, AuthorRef) or isinstance(x, Author):
            return self.db.all('@book/select_all_by_author', [ int(x) ])
        if isinstance(x, GenreRef) or isinstance(x, Genre):
            return self.db.all('@book/select_all_by_genre', [ int(x) ])
        if isinstance(x, YearFilter):
            return self.db.all('@book/select_all_by_year', [ x.year ])
        return super()._all(x)


class GenreManager(GenreManager):

    def _refs(self, x = None) -> list[GenreRef]:
        if isinstance(x, BookRef) or isinstance(x, Book):
            return self.db.all('@genre/select_ref_by_book', [ int(x) ])
        return super()._refs(x)

    def _all(self, x = None) -> list[Genre]:
        if isinstance(x, BookRef) or isinstance(x, Book):
            return self.db.all('@genre/select_all_by_book', [ int(x) ])
        return super()._all(x)


class PublisherManager(PublisherManager):
    pass


#
# Dataset
#

class Dataset(_base.Dataset):

    def __init__(self, schema_path, file_path:str):
        super().__init__()
        self._db = _sqlite.Database(schema_path, file_path)
        self._authors = AuthorManager(self, self._db)
        self._books = BookManager(self, self._db)
        self._genres = GenreManager(self, self._db)
        self._publishers = PublisherManager(self, self._db)

    @property
    def path(self):
        return self._db.path

    def open(self, reset: bool = False):
        self._db.open(reset)

    def isOpen(self):
        return self._db.isOpen()
