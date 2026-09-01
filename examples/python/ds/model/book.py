from ds.model._base import *
from quartz.error import Error
from quartz.util import Parse

#
# Entity
#

class Book(BookRef):

    def __init__(self, publisher_id=None, title=None, year=None, id=None):
        super().__init__(id)
        self.publisher_id = publisher_id
        self.title = title
        self.year = year

    def __str__(self):
        return Parse.string(self._title)

    def __repr__(self):
        ref = super().__repr__()
        publisher_id = Parse.string(self._publisher_id)
        title = Parse.string(self._title)
        year = Parse.string(self._year)
        return "{}(publisher_id:{}, title:{}, year:{})".format(ref, publisher_id, title, year)

    def _validRef(self, x):
        if isinstance(x, BookRef):
            return x

    @property
    def publisher_id(self):
        return self._publisher_id
    @publisher_id.setter
    def publisher_id(self, x):
        self._publisher_id = PublisherRef.valid(x, True)

    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, x):
        self._title = x

    @property
    def year(self):
        return self._year
    @year.setter
    def year(self, x):
        self._year = x

    @staticmethod
    def valid(x, nullable = False):
        if nullable and (x is None):
            return None
        if isinstance(x, Book):
            return x
        Error.invalid("book", x)
