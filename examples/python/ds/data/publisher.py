from ds.model._base import *
import ds.model.publisher as _core
import ds.data._base as _base
from ds.data.publisher import *
from abc import abstractmethod


class Publisher(_core.Publisher, _base.Entity):

    def __init__(self, parent_id=None, name=None, id=None, api=None):
        super().__init__(parent_id, name, id)
        self.api = api

    def add(self, x):
        if isinstance(x, _base.Engine):
            return x.publishers.add(self)

    def remove(self):
        self.api.ds.publishers.remove(self)
        self.id = None

    def push(self, x:Fields=None):
        return self.api.ds.publishers.set(self if (x is None) else (self, x))

    def pull(self, x:Fields=None):
        return self.api.ds.publishers.get(self, x)


class PublisherManager(_base.PublisherManager):

    def add(self, x, debug=False):
        if isinstance(x, Publisher):
            x.attach(self.api)
        return self.api.ds.publishers.add(x, debug)

    def set(self, x, debug=False):
        if isinstance(x, Publisher):
            x.attach(self.api)
        return self.api.ds.publishers.set(x, debug)

    def get(self, x:Publisher, field:Fields=None, debug=False):
        if isinstance(x, Publisher):
            x.attach(self.api)
            return self.api.ds.publishers.get(x, field, debug)

    def remove(self, x: PublisherRef, debug=False):
        return self.api.ds.publishers.remove(x, debug)

    def clear(self, debug=False):
        self.api.ds.publishers.clear(debug)

    def has(self, x=None, debug=False) -> bool:
        return self.api.ds.publishers.has(x, debug)

    def ref(self, x=None, order=None, debug=False) -> PublisherRef:
        return self.api.ds.publishers.ref(x, order, debug)

    def refs(self, x=None, order=None, debug=False) -> list[PublisherRef]:
        return self.api.ds.publishers.refs(x, order, debug)

    def one(self, x=None, order=None, debug=False) -> Publisher:
        return self.api.ds.publishers.find(x, "full", self._create, True, order, debug)

    def all(self, x=None, order=None, debug=False) -> list[Publisher]:
        return self.api.ds.publishers.find(x, "full", self._create, False, order, debug)

    def fetch(self, x: object, id:int=None, debug=False) -> Publisher:
        x_ = str(x)
        p = self.one(x_)
        if p is None:
            p = self._create([ id, None, x_ ])
            self.add(p, debug)
        return p

    @abstractmethod
    def _create(self, x):
        return None

