from ds.base import *
from quartz.error import Error
from quartz.util import Parse

#
# Entity
#

class BookAuthor(BookAuthorRef):

    def __init__(self, book_id=None, author_id=None, rank=None):
        super().__init__(book_id, author_id)
        self.rank = rank

    def __repr__(self):
        ref = super().__repr__()
        rank = Parse.string(self._rank)
        return "{}(rank:{})".format(ref, rank)

    def _validateRef(self, x):
        if isinstance(x, int) or isinstance(x, BookAuthorRef):
            return int(x)   

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
    def valid(x):
        if isinstance(x, BookAuthor):
            return x
        Error.invalid("BookAuthor", x)
