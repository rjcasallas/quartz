from ds.model._reference import *
from ds.model.publisher import *
import quartz.gen.data as _data
from quartz.error import Error
from quartz.util import Parse

#
# Entity
#

class Publisher(PublisherRef):

    def __init__(self, parent_id = None, name = None, id = None):
        super().__init__(id)
        self.parent_id = parent_id
        self.name = name

    def __str__(self):
        return self._name

    def __repr__(self):
        ref = super().__repr__()
        parent_id = Parse.string(self._parent_id)
        name = Parse.string(self._name)
        return "{}(parent_id:{}, name:{})".format(ref, parent_id, name)

    def _validRef(self, x):
        if isinstance(x, PublisherRef):
            return x

    @property
    def parent_id(self):
        return self._parent_id
    @parent_id.setter
    def parent_id(self, x):
        self._parent_id = PublisherRef.valid(x, True)

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, x):
        self._name = x

    def copy(self, x):
        if isinstance(x, Publisher):
            super().copy(x)
            self.parent_id = x.parent_id
            self.name = x.name
        return self

    @staticmethod
    def valid(x, nullable = False):
        if nullable and (x is None):
            return None
        if isinstance(x, Publisher):
            return x
        Error.invalid("publisher", x)

#
# Manager
#

class PublisherManager(_data.EntityManager):

    def fetch(self, x, id = None):
        x_ = str(x)
        p = self.one(x_)
        if p is None:
            p = self.add(Publisher(x_, id))
        return p
