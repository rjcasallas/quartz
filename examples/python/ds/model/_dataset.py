from ds.model._base import *
from ds.model.author import *
from ds.model.book import *
from ds.model.book_author import *
from ds.model.genre import *
from ds.model.publisher import *
import quartz.gen.data as _base
from quartz.error import Error
from quartz.log import Log

#
# Manager
#

class Manager:
    def __init__(self, x):
        if isinstance(x, Dataset):
            self._ds = x
        else: Error.invalid("dataset")

    @property
    def ds(self):
        return self._ds

#
# Dataset
#

class Dataset:

    class Authors(Manager, _base.EntityManager):
        pass

    class Books(Manager, _base.EntityManager):
        pass

    class BookAuthors(Manager, _base.EntityManager):
        pass

    class BookGenres(Manager, _base.BasicManager):
        pass

    class Genres(Manager, _base.EntityManager):
        pass

    class Publishers(Manager, _base.EntityManager):
        pass

    class Subgenres(Manager, _base.BasicManager):
        pass

    def __init__(self):
        self._authors = None
        self._books = None
        self._book_authors = None
        self._book_genres = None
        self._genres = None
        self._publishers = None
        self._subgenres = None

    @property
    def authors(self) -> Authors:
        if self._authors is None: Error.fail(f"Not initialized: authors.")
        return self._authors

    @property
    def books(self) -> Books:
        if self._books is None: Error.fail(f"Not initialized: books.")
        return self._books

    @property
    def book_authors(self) -> BookAuthors:
        if self._book_authors is None: Error.fail(f"Not initialized: book_authors.")
        return self._book_authors

    @property
    def book_genres(self) -> BookGenres:
        if self._book_genres is None: Error.fail(f"Not initialized: book_genres.")
        return self._book_genres

    @property
    def genres(self) -> Genres:
        if self._genres is None: Error.fail(f"Not initialized: genres.")
        return self._genres

    @property
    def publishers(self) -> Publishers:
        if self._publishers is None: Error.fail(f"Not initialized: publishers.")
        return self._publishers

    @property
    def subgenres(self) -> Subgenres:
        if self._subgenres is None: Error.fail(f"Not initialized: subgenres.")
        return self._subgenres

    def print(self, level = 0):
        # authors
        authors = self.authors.all()
        Log.list("authors({})".format(len(authors)), level + 1)
        for a in authors:
            Log.list(str(a), level + 2)
        # books
        books = self.books.all()
        Log.list("books({})".format(len(books)), level + 1)
        for b in books:
            Log.list(str(b), level + 2)
        # genres
        genres = self.genres.all()
        Log.list("genres({})".format(len(genres)), level + 1)
        for g in genres:
            Log.list(str(g), level + 2)
        # publishers
        publishers = self.publishers.all()
        Log.list("publishers({})".format(len(publishers)), level + 1)
        for p in publishers:
            Log.list(str(p), level + 2)
