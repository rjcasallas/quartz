import ds.base._core as _core
import ds.model.genre as _model
from ds.model._reference import *
from abc import abstractmethod


class Genre(_model.Genre, _core.Entity):

    def __init__(self, name=None, id=None, api=None):
        super().__init__(name, id)
        self.api = api

    def add(self, x):
        if isinstance(x, _core.Engine):
            return x.genres.add(self)

    def remove(self):
        self.api.ds.genres.remove(self)
        self.id = None

    def push(self, x:Fields=None):
        return self.api.ds.genres.set(self if (x is None) else (self, x))

    def pull(self, x:Fields=None):
        return self.api.ds.genres.get(self, x)


class GenreManager(_core.GenreManager):

    def add(self, x, debug=False):
        return self.api.ds.genres.add(x, debug)

    def set(self, x, debug=False):
        return self.api.ds.genres.set(x, debug)

    def get(self, x:Genre, field:Fields=None, debug=False):
        return self.api.ds.genres.get(x, field, debug)

    def remove(self, x: GenreRef, debug=False):
        return self.api.ds.genres.remove(x, debug)

    def clear(self, debug=False):
        self.api.ds.genres.clear(debug)

    def has(self, x=None, debug=False) -> bool:
        return self.api.ds.genres.has(x, debug)

    def ref(self, x=None, order=None, debug=False) -> GenreRef:
        return self.api.ds.genres.ref(x, order, debug)

    def refs(self, x=None, order=None, debug=False) -> list[GenreRef]:
        return self.api.ds.genres.refs(x, order, debug)

    def one(self, x=None, order=None, debug=False) -> Genre:
        return self.api.ds.genres.find(x, "full", self._create, True, order, debug)

    def all(self, x=None, order=None, debug=False) -> list[Genre]:
        return self.api.ds.genres.find(x, "full", self._create, False, order, debug)

    def fetch(self, x: object, id:int=None, debug=False) -> Genre:
        x_ = str(x)
        g = self.one(x_)
        if g is None:
            g = self._create([ id, x_ ])
            self.add(g, debug)
        return g

    @abstractmethod
    def _create(self, x):
        return None

