from ds.model._reference import *
import quartz.gen.data as _data
from quartz.error import Error
from quartz.util import Parse

#
# Entity
#

class Genre(GenreRef):

    def __init__(self, name = None, id = None):
        super().__init__(id)
        self.name = name

    def __str__(self):
        return self._name

    def __repr__(self):
        ref = super().__repr__()
        name = Parse.string(self._name)
        return "{}(name:{})".format(ref, name)

    def _validRef(self, x):
        if isinstance(x, GenreRef):
            return x

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, x):
        self._name = x

    def copy(self, x):
        if isinstance(x, Genre):
            super().copy(x)
            self.name = x.name
        return self

    @staticmethod
    def valid(x, nullable = False):
        if nullable and (x is None):
            return None
        if isinstance(x, Genre):
            return x
        Error.invalid("genre", x)

#
# Manager
#

class GenreManager(_data.EntityManager):

    def fetch(self, x, id = None):
        x_ = str(x)
        g = self.one(x_)
        if g is None:
            g = self.add(Genre(x_, id))
        return g
