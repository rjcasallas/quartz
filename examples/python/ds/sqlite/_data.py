from ds.model._data import *
from ds.sqlite.author import *
from ds.sqlite.book import *
from ds.sqlite.book_author import *
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
# Tables
#

class AuthorSqliteManager(AuthorSqliteManager):

    def _link(self, base_id, x):
        # "author_book" author.id → book.id
        if isinstance(x, BookRef):
            return self.db.exec('@book_author/insert', [ base_id, int(x) ])
        return super()._link(x)

    def _unlink(self, base_id, x):
        # "author_book" author.id → book.id
        if isinstance(x, BookRef):
            return self.db.exec('@book_author/delete', [ base_id, int(x) ])
        return super()._unlink(x)

    def _refs(self, x = None) -> list[int]:
        if isinstance(x, BookRef) or isinstance(x, Book):
            return self.db.all('@author/select_ref_by_book', [ int(x) ])
        return super()._refs(x)


class BookSqliteManager(BookSqliteManager):

    def _link(self, base_id, x):
        # "book_author" book.id → author.id
        if isinstance(x, AuthorRef):
            return self.db.exec('@book_author/replace', [ base_id, int(x), 1 ]) # TODO
        # "book_genre" book.id → genre.id
        if isinstance(x, GenreRef):
            return self.db.exec('@book_genre/replace', [ base_id, int(x) ])
        return super()._link(x)

    def _unlink(self, base_id, x):
        # "book_author" book.id → author.id
        if isinstance(x, AuthorRef):
            return self.db.exec('@book_author/delete_id', [ base_id, int(x) ])
        # "book_genre" book.id → genre.id
        if isinstance(x, GenreRef):
            return self.db.exec('@book_genre/delete_id', [ base_id, int(x) ])
        return super()._unlink(x)

    def _refs(self, x = None) -> list[int]:
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


class BookAuthorSqliteManager(BookAuthorSqliteManager):
        pass


class GenreSqliteManager(GenreSqliteManager):

    def _refs(self, x = None) -> list[int]:
        if isinstance(x, BookRef) or isinstance(x, Book):
            return self.db.all('@genre/select_ref_by_book', [ int(x) ])
        return super()._refs(x)

    def _all(self, x = None) -> list[Genre]:
        if isinstance(x, BookRef) or isinstance(x, Book):
            return self.db.all('@genre/select_all_by_book', [ int(x) ])
        return super()._all(x)


class PublisherSqliteManager(PublisherSqliteManager):
        pass


#
# Dataset
#

class Dataset(Dataset):

    def __init__(self, schema_path):
        super().__init__()
        self._db = _sqlite.Database(schema_path)
        self._authors = AuthorSqliteManager(self, self._db)
        self._books = BookSqliteManager(self, self._db)
        self._book_authors = BookAuthorSqliteManager(self, self._db)
        self._genres = GenreSqliteManager(self, self._db)
        self._publishers = PublisherSqliteManager(self, self._db)

    @property
    def path(self):
        return self._db.path

    def open(self, path:str, reset: bool = False):
        self._db.open(path, reset)

    def isOpen(self):
        return self._db.isOpen()
