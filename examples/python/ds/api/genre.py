import ds.base.genre as _base
from ds.base._core import Submanager
from ds.model._reference import *


class Genre(_base.Genre):

    class Parent(Submanager):

        def get(self):
            return self.api.genres.one(ChildGenreRef(self._))

        def set(self, x):
            pr = GenreRef.valid(x, nullable=True)
            self.api.genres.set(SubgenreRef(pr, self._))

    class Children(Submanager):

        def add(self, x):
            return self.api.genres.add(SubgenreRef(self._, int(x)))

        def all(self):
            return self.api.genres.all(ParentGenreRef(self._))

    def __init__(self, name=None, id=None, api=None):
        super().__init__(name, id, api)
        self._parent = Genre.Parent(self)
        self._children = Genre.Children(self)

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return self._children


class GenreManager(_base.GenreManager):

    def _create(self, x):
        return Genre(id=x[0], name=x[1]).attach(self.api)
