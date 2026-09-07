import ds.api._core as _core
import ds.model.genre as _model
from ds.base import *


class Genre(_model.Genre, _core.Entity):

    class Parent(_core.Submanager):

        def pull(self):
            return self._ds.genres.one(ChildGenreRef(self._))

        def push(self, x):
            pr = GenreRef.valid(x, nullable=True)
            self._ds.genres.push(SubgenreRef(pr, self._))

    class Children(_core.Submanager):

        def add(self, x):
            return self._ds.genres.add(SubgenreRef(self._, int(x)))

        def all(self):
            return self._ds.genres.all(ParentGenreRef(self._))

    def __init__(self, name=None, id=None, api=None):
        super().__init__(name, id)
        self._en = api
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
            return x._ds.genres.add(self.attach(x))

    def remove(self):
        self._ds.genres.remove(self)
        self.id = None

    def push(self, field:Fields=None, api=None):
        if api: self.attach(api)
        return self._ds.genres.push(self, field)

    def pull(self, field:Fields=None, api=None):
        if api: self.attach(api)
        return self._ds.genres.pull(self, field)

    @staticmethod
    def valid(x):
        if isinstance(x, Genre):
            return x
        Error.invalid("Genre", x)


class GenreManager(_core.Manager):

    def add(self, x):
        if isinstance(x, str):
            y = Genre(name=x, api=self._en)
        else:
            Genre.valid(x).attach(api=self._en)
        return self._ds.genres.add(y)

    def remove(self, x):
        return self._ds.genres.remove(x)

    def fetch(self, x:object, id:int=None) -> Genre:
        s = str(x)
        o = self._ds.genres.one(s)
        if o is None:
            o = Genre(id=id, name=s, api=self._en)
            self._ds.genres.add(o)
        return o

    def ref(self, x=None, order:list[str]=None, limit:str=None):
        return self._ds.genres.ref(x, order, limit)

    def refs(self, x=None, order:list[str]=None, limit:str=None):
        return self._ds.genres.refs(x, order, limit)

    def one(self, x=None, order:list[str]=None, limit:str=None):
        return self._ds.genres.one(x, self._create, 'full', order, limit)

    def all(self, x=None, order:list[str]=None, limit:str=None):
        return self._ds.genres.all(x, self._create, 'full', order, limit)

    def _create(self, x):
        return Genre(id=x[0], name=x[1], api=self._en)
