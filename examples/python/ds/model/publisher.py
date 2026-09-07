from ds.model._reference import *
from quartz.error import Error
from quartz.util import Parse

#
# Entity
#

class Publisher(PublisherRef):

    def __init__(self, parent_id=None, name=None, id=None):
        super().__init__(id)
        self.parent_id = parent_id
        self.name = name

    def __str__(self):
        return Parse.string(self._name)

    def __repr__(self):
        ref = super().__repr__()
        parent_id = Parse.string(self._parent_id)
        name = Parse.string(self._name)
        return "{}(parent_id:{}, name:{})".format(ref, parent_id, name)

    def _validateRef(self, x):
        if isinstance(x, int) or isinstance(x, PublisherRef):
            return int(x)   

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
