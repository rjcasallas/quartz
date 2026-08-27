import ds.data._base as _base
import ds.model._dataset as _model
from quartz.error import Error


class Genre(_base.Genre):

    def __init__(self, name=None, id:int=None):
        _base.Genre.__init__(self, name, id)
        _base.Entity.__init__(self)

    def add(self, x):
        if isinstance(x, _base.Engine):
            return x.genres.add(self)

    def remove(self):
        self.data.ds.genres.remove(self)
        self.id = None

    def link(self, x):
        return self.data.genres.link(self, x)

    def unlink(self, x):
        return self.data.genres.unlink(self, x)


class GenreManager(_base.GenreManager):

    def add(self, x: Genre):
        return self.data.ds.genres.add(x)

    def update(self, x: Genre):
        return self.data.ds.genres.update(x)

    def remove(self, x: _model.GenreRef):
        return self.data.ds.genres.remove(x)

    def clear(self):
        self.data.ds.genres.clear()

    def has(self, x = None) -> bool:
        return self.data.ds.genres.has(x)

    def fetch(self, x: object, id:int = None) -> Genre:
        x_ = str(x)
        g = self.one(x_)
        if g is None:
            g = self.add(Genre(x_, id))
        return g

    def ref(self, x = None) -> _model.GenreRef:
        return self.data.ds.genres.ref(x)

    def refs(self, x = None) -> list[_model.GenreRef]:
        return self.data.ds.genres.refs(x)

    def one(self, x = None) -> Genre:
        return self.data.ds.genres.one(x)

    def all(self, x = None) -> list[Genre]:
        return self.data.ds.genres.all(x)
