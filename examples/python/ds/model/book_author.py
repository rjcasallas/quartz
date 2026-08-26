from ds.model._reference import *
import quartz.gen.data as _data
from quartz.error import Error
from quartz.util import Parse

#
# Aggregate
#

class BookAuthor(BookAuthorRef):

    def __init__(self, book_id, author_id, rank):
        super().__init__(book_id, author_id)
        self.rank = rank

    def __repr__(self):
        book_id = Parse.string(self._book_id)
        author_id = Parse.string(self._author_id)
        rank = Parse.string(self._rank)
        return "book_author(book_id:{}, author_id:{}, rank:{})".format(book_id, author_id, rank)

    @property
    def rank(self):
        return self._rank
    @rank.setter
    def rank(self, x):
        self._rank = x

    def copy(self, x):
        if isinstance(x, BookAuthor):
            super().copy(x)
            self.rank = x.rank
        return self

    @staticmethod
    def valid(x, nullable = False):
        if nullable and (x is None):
            return None
        if isinstance(x, BookAuthor):
            return x
        Error.invalid("book_author", x)

#
# Manager
#

class BookAuthorManager(_data.BasicManager):
    pass