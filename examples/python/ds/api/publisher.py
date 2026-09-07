import ds.base.publisher as _base
from ds.base._core import Submanager
from ds.model._reference import *


class Publisher(_base.Publisher):

    class Parent(Submanager):

        def get(self):
            return self.api.publishers.one(self._.parent_id) if self._.parent_id else None

        def set(self, x):
            self._.parent_id = PublisherRef.valid(x)
            return self.api.publishers.set((self._, Fields.Parent))

    def __init__(self, parent_id=None, name=None, id=None, api=None):
        super().__init__(parent_id, name, id, api)
        self._parent = Publisher.Parent(self)

    @property
    def parent(self):
        return self._parent


class PublisherManager(_base.PublisherManager):

    def _create(self, x):
        return Publisher(id=x[0], parent_id=x[1], name=x[2]).attach(self.api)
