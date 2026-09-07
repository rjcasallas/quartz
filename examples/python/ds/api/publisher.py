import ds.api._core as _core
import ds.model.publisher as _model
from ds.base import *


class Publisher(_model.Publisher, _core.Entity):

    class Parent(_core.Submanager):

        def pull(self):
            return self._ds.publishers.one(self._.parent_id) if self._.parent_id else None

        def push(self, x):
            self._.parent_id = PublisherRef.valid(x)
            return self._ds.publishers.push(self._, Fields.Parent)

    def __init__(self, parent_id=None, name=None, id=None, api=None):
        super().__init__(parent_id, name, id)
        self._en = api
        self._parent = Publisher.Parent(self)

    @property
    def parent(self):
        return self._parent

    def add(self, x):
        if isinstance(x, _core.Engine):
            return x._ds.publishers.add(self.attach(x))

    def remove(self):
        self._ds.publishers.remove(self)
        self.id = None

    def push(self, field:Fields=None, api=None):
        if api: self.attach(api)
        return self._ds.publishers.push(self, field)

    def pull(self, field:Fields=None, api=None):
        if api: self.attach(api)
        return self._ds.publishers.pull(self, field)

    @staticmethod
    def valid(x):
        if isinstance(x, Publisher):
            return x
        Error.invalid("Publisher", x)


class PublisherManager(_core.Manager):

    def add(self, x):
        if isinstance(x, str):
            y = Publisher(name=x, api=self._en)
        else:
            Publisher.valid(x).attach(api=self._en)
        return self._ds.publishers.add(y)

    def remove(self, x):
        return self._ds.publishers.remove(x)

    def fetch(self, x:object, id:int=None) -> Publisher:
        s = str(x)
        o = self._ds.publishers.one(s)
        if o is None:
            o = Publisher(id=id, name=s, api=self._en)
            self._ds.publishers.add(o)
        return o

    def ref(self, x=None, order:list[str]=None, limit:str=None):
        return self._ds.publishers.ref(x, order, limit)

    def refs(self, x=None, order:list[str]=None, limit:str=None):
        return self._ds.publishers.refs(x, order, limit)

    def one(self, x=None, order:list[str]=None, limit:str=None):
        return self._ds.publishers.one(x, self._create, 'full', order, limit)

    def all(self, x=None, order:list[str]=None, limit:str=None):
        return self._ds.publishers.all(x, self._create, 'full', order, limit)

    def _create(self, x):
        return Publisher(id=x[0], parent_id=x[1], name=x[2], api=self._en)
