import ds.api._core as _core
import ds.model.genre as _model
from ds.model._reference import *
from abc import abstractmethod


class Genre(_model.Genre, _core.Entity):

    class Parent(_core.Submanager):

        def get(self):
            return self.api.genres.one(ChildGenreRef(self._))

        def set(self, x):
            pr = GenreRef.valid(x, nullable=True)
            self.api.genres.set(SubgenreRef(pr, self._))

    class Children(_core.Submanager):

        def add(self, x):
            return self.api.genres.add(SubgenreRef(self._, int(x)))

        def all(self):
            return self.api.genres.all(ParentGenreRef(self._))

    def __init__(self, name=None, id=None, api=None):
        super().__init__(name, id)
        self.api = api
        self._parent = Genre.Parent(self)
        self._children = Genre.Children(self)

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return self._children

    def add(self, x):
        if isinstance(x, _core.Engine):
            return x.genres.add(self)

    def remove(self):
        self.api.genres.remove(self)
        self.id = None

    def push(self, x:Fields=None):
        return self.api.genres.set(self if (x is None) else (self, x))

    def pull(self, x:Fields=None):
        return self.api.genres.get(self, x)


class GenreManager(_core.GenreManager):

    def fetch(self, x: object, id:int=None, debug=False) -> Genre:
        x_ = str(x)
        g = self.one(x_)
        if g is None:
            g = Genre(id=id, name=x_, api=self.api)
            self.add(g, debug)
        return g

    def _create(self, x):
        return Genre(id=x[0], name=x[1], api=self.api)
