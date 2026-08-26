from ds.model._reference import *
from ds.model.author import *
from ds.model.book import *
from ds.model.book_author import *
from ds.model.genre import *
from ds.model.publisher import *
from quartz.error import Error
from quartz.log import Log

#
# Dataset
#

class Dataset:

    class Manager:
        def __init__(self, ds):
            self._ds = ds

        @property
        def ds(self):
            return self._ds

    class Authors(Manager, AuthorManager):
        pass

    class Books(Manager, BookManager):
        pass

    class BookAuthors(Manager, BookAuthorManager):
        pass

    class Genres(Manager, GenreManager):
        pass

    class Publishers(Manager, PublisherManager):
        pass

    def __init__(self):
        self._authors = None
        self._books = None
        self._book_authors = None
        self._genres = None
        self._publishers = None

    @property
    def authors(self) -> 'Dataset.Manager':
        if self._authors is None: Error.fail(f"Not initialized: authors.")
        return self._authors

    @property
    def books(self) -> 'Dataset.Manager':
        if self._books is None: Error.fail(f"Not initialized: books.")
        return self._books

    @property
    def book_authors(self) -> 'Dataset.Manager':
        if self._book_authors is None: Error.fail(f"Not initialized: book_authors.")
        return self._book_authors

    @property
    def genres(self) -> 'Dataset.Manager':
        if self._genres is None: Error.fail(f"Not initialized: genres.")
        return self._genres

    @property
    def publishers(self) -> 'Dataset.Manager':
        if self._publishers is None: Error.fail(f"Not initialized: publishers.")
        return self._publishers

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
