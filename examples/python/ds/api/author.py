import ds.api._core as _core
import ds.model.author as _model
from ds.base import *


class Author(_model.Author, _core.Entity):

    def __init__(self, name=None, rank:int=None, id=None, api=None):
        super().__init__(name, id)
        self._en = api
        self.rank = rank

    @property
    def rank(self):
        return self._rank
    @rank.setter
    def rank(self, x):
        self._rank = int(x) if isinstance(x, int) else None

    def add(self, x):
        if isinstance(x, _core.Engine):
            return x._ds.authors.add(self.attach(x))

    def remove(self):
        self._ds.authors.remove(self)
        self.id = None

    def push(self, field:Fields=None, api=None):
        if api: self.attach(api)
        return self._ds.authors.push(self, field)

    def pull(self, field:Fields=None, api=None):
        if api: self.attach(api)
        return self._ds.authors.pull(self, field)

    @staticmethod
    def valid(x):
        if isinstance(x, Author):
            return x
        Error.invalid("Author", x)


class AuthorManager(_core.Manager):

    def add(self, x):
        if isinstance(x, str):
            y = Author(name=x, api=self._en)
        else:
            Author.valid(x).attach(api=self._en)
        return self._ds.authors.add(y)

    def remove(self, x):
        return self._ds.authors.remove(x)

    def fetch(self, x:object, id:int=None) -> Author:
        s = str(x)
        o = self._ds.authors.one(s)
        if o is None:
            o = Author(id=id, name=s, api=self._en)
            self._ds.authors.add(o)
        return o

    def ref(self, x=None, order:list[str]=None, limit:str=None):
        return self._ds.authors.ref(x, order, limit)

    def refs(self, x=None, order:list[str]=None, limit:str=None):
        return self._ds.authors.refs(x, order, limit)

    def one(self, x=None, order:list[str]=None, limit:str=None):
        return self._ds.authors.one(x, self._create, 'full', order, limit)

    def all(self, x=None, order:list[str]=None, limit:str=None):
        return self._ds.authors.all(x, self._create, 'full', order, limit)

    def _create(self, x):
        return Author(id=x[0], name=x[1], rank=x[2], api=self._en)
