import quartz.data.base as _base
from quartz.error import Error
from quartz.log import Log

#
# Dataset
#

class Dataset:

    class Authors(_base.EntitySubset):
        pass

    class Books(_base.EntitySubset):
        pass

    class BookAuthors(_base.EntitySubset):
        pass

    class Genres(_base.EntitySubset):
        pass

    class Publishers(_base.EntitySubset):
        pass

    def __init__(self):
        self._authors = None
        self._books = None
        self._book_authors = None
        self._genres = None
        self._publishers = None

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
    def genres(self) -> Genres:
        if self._genres is None: Error.fail(f"Not initialized: genres.")
        return self._genres

    @property
    def publishers(self) -> Publishers:
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
        # book_authors
        book_authors = self.book_authors.all()
        Log.list("book_authors({})".format(len(book_authors)), level + 1)
        for ba in book_authors:
            Log.list(str(ba), level + 2)
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
