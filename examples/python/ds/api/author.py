import ds.api._core as _core
import ds.model.author as _model
from ds.model._reference import *
from abc import abstractmethod


class Author(_model.Author, _core.Entity):

    def __init__(self, name=None, rank:int=None, id=None, api=None):
        super().__init__(name, id)
        self.api = api
        self.rank = rank

    @property
    def rank(self):
        return self._rank
    @rank.setter
    def rank(self, x):
        self._rank = int(x) if isinstance(x, int) else None

    def add(self, x):
        if isinstance(x, _core.Engine):
            return x.authors.add(self)

    def remove(self):
        self.api.authors.remove(self)
        self.id = None

    def push(self, x:Fields=None):
        return self.api.authors.set(self if (x is None) else (self, x))

    def pull(self, x:Fields=None):
        return self.api.authors.get(self, x)


class AuthorManager(_core.AuthorManager):

    def fetch(self, x: object, id:int=None, debug=False) -> Author:
        x_ = str(x)
        a = self.one(x_)
        if a is None:
            a = Author(id=id, name=x_, api=self.api)
            self.add(a, debug)
        return a

    def _create(self, x):
        return Author(id=x[0], name=x[1], api=self.api)
