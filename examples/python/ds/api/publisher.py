import ds.api._core as _core
import ds.model.publisher as _model
from ds.model._reference import *
from abc import abstractmethod


class Publisher(_model.Publisher, _core.Entity):

    class Parent(_core.Submanager):

        def get(self):
            return self.api.publishers.one(self._.parent_id) if self._.parent_id else None

        def set(self, x):
            self._.parent_id = PublisherRef.valid(x)
            return self.api.publishers.set((self._, Fields.Parent))

    def __init__(self, parent_id=None, name=None, id=None, api=None):
        super().__init__(parent_id, name, id)
        self.api = api
        self._parent = Publisher.Parent(self)

    @property
    def parent(self):
        return self._parent

    def add(self, x):
        if isinstance(x, _core.Engine):
            return x.publishers.add(self)

    def remove(self):
        self.api.publishers.remove(self)
        self.id = None

    def push(self, x:Fields=None):
        return self.api.publishers.set(self if (x is None) else (self, x))

    def pull(self, x:Fields=None):
        return self.api.publishers.get(self, x)


class PublisherManager(_core.PublisherManager):

    def fetch(self, x: object, id:int=None, debug=False) -> Publisher:
        x_ = str(x)
        p = self.one(x_)
        if p is None:
            p = Publisher(id=id, name=x_, api=self.api)
            self.add(p, debug)
        return p

    def _create(self, x):
        return Publisher(id=x[0], parent_id=x[1], name=x[2], api=self.api)
