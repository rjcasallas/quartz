from ds.model._base import *
import ds.model.author as _core
import ds.data._base as _base
from abc import abstractmethod


class Author(_core.Author, _base.Entity):

    def __init__(self, name=None, id=None, api=None):
        super().__init__(name, id)
        self.api = api

    def add(self, x):
        if isinstance(x, _base.Engine):
            return x.authors.add(self)

    def remove(self):
        self.api.ds.authors.remove(self)
        self.id = None

    def push(self, x:Fields=None):
        return self.api.ds.authors.set(self if (x is None) else (self, x))

    def pull(self, x:Fields=None):
        return self.api.ds.authors.get(self, x)


class AuthorManager(_base.AuthorManager):

    def add(self, x, debug=False):
        if isinstance(x, Author):
            x.attach(self.api)
        return self.api.ds.authors.add(x, debug)

    def set(self, x, debug=False):
        if isinstance(x, Author):
            x.attach(self.api)
        return self.api.ds.authors.set(x, debug)

    def get(self, x:Author, field:Fields=None, debug=False):
        if isinstance(x, Author):
            x.attach(self.api)
            return self.api.ds.authors.get(x, field, debug)

    def remove(self, x: AuthorRef, debug=False):
        return self.api.ds.authors.remove(x, debug)

    def clear(self, debug=False):
        self.api.ds.authors.clear(debug)

    def has(self, x=None, debug=False) -> bool:
        return self.api.ds.authors.has(x, debug)

    def ref(self, x=None, order=None, debug=False) -> AuthorRef:
        return self.api.ds.authors.ref(x, order, debug)

    def refs(self, x=None, order=None, debug=False) -> list[AuthorRef]:
        return self.api.ds.authors.refs(x, order, debug)

    def one(self, x=None, order=None, debug=False) -> Author:
        return self.api.ds.authors.find(x, "full", self._create, True, order, debug)

    def all(self, x=None, order=None, debug=False) -> list[Author]:
        return self.api.ds.authors.find(x, "full", self._create, False, order, debug)

    def fetch(self, x: object, id:int=None, debug=False) -> Author:
        x_ = str(x)
        a = self.one(x_)
        if a is None:
            a = self._create([ id, x_ ])
            self.add(a, debug)
        return a

    @abstractmethod
    def _create(self, x):
        return None

