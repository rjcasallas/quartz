from quartz.gen.data import Reference
from quartz.error import Error
from quartz.util import Parse
from quartz.log import Log

#
# Entities
#

class AuthorRef(Reference):

    @staticmethod
    def valid(x, nullable = False):
        if nullable and x is None:
            return None
        if isinstance(x, int) or isinstance(x, AuthorRef):
            return int(x)
        Error.invalid("author reference", x)


class BookRef(Reference):

    @staticmethod
    def valid(x, nullable = False):
        if nullable and x is None:
            return None
        if isinstance(x, int) or isinstance(x, BookRef):
            return int(x)
        Error.invalid("book reference", x)


class GenreRef(Reference):

    @staticmethod
    def valid(x, nullable = False):
        if nullable and x is None:
            return None
        if isinstance(x, int) or isinstance(x, GenreRef):
            return int(x)
        Error.invalid("genre reference", x)


class PublisherRef(Reference):

    @staticmethod
    def valid(x, nullable = False):
        if nullable and x is None:
            return None
        if isinstance(x, int) or isinstance(x, PublisherRef):
            return int(x)
        Error.invalid("publisher reference", x)

#
# Aggregates
#

class BookAuthorRef:

    def __init__(self, book_id, author_id):
        self.book_id = book_id
        self.author_id = author_id

    def __repr__(self):
        book_id = Parse.string(self._book_id)
        author_id = Parse.string(self._author_id)
        return "book_author(book_id:{}, author_id:{})".format(book_id, author_id)

    @property
    def book_id(self):
        return self._book_id
    @book_id.setter
    def book_id(self, x):
        self._book_id = BookRef.valid(x, True)

    @property
    def author_id(self):
        return self._author_id
    @author_id.setter
    def author_id(self, x):
        self._author_id = AuthorRef.valid(x, True)

    def copy(self, x):
        if isinstance(x, BookAuthorRef):
            self.book_id = x.book_id
            self.author_id = x.author_id
        return self

    @staticmethod
    def valid(x, nullable = False):
        if nullable and (x is None):
            return None
        if isinstance(x, BookAuthorRef):
            return x
        Error.invalid("book_author reference", x)


