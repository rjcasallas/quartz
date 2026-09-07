from ds.model._reference import *
from quartz.error import Error
from quartz.util import Parse

#
# Entity
#

class Genre(GenreRef):

    def __init__(self, name=None, id=None):
        super().__init__(id)
        self.name = name

    def __str__(self):
        return Parse.string(self._name)

    def __repr__(self):
        ref = super().__repr__()
        name = Parse.string(self._name)
        return "{}(name:{})".format(ref, name)

    def _validateRef(self, x):
        if isinstance(x, int) or isinstance(x, GenreRef):
            return int(x)   

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
