import ds.data._base as _base
import ds.model._dataset as _model
from quartz.error import Error


class Publisher(_base.Publisher):

    def __init__(self, parent=None, name=None, id:int=None):
        _base.Publisher.__init__(self, None, name, id)
        _base.Entity.__init__(self)
        self.parent = parent

    @property
    def parent_id(self):
        return self._parent.id if self._parent else None
    @parent_id.setter
    def parent_id(self, x):
        pass

    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self, x):
        self._parent = _base.Publisher.valid(x, True, False)

    def add(self, x):
        if isinstance(x, _base.Engine):
            return x.publishers.add(self)

    def remove(self):
        self.data.ds.publishers.remove(self)
        self.id = None

    def link(self, x):
        return self.data.publishers.link(self, x)

    def unlink(self, x):
        return self.data.publishers.unlink(self, x)


class PublisherManager(_base.PublisherManager):

    def add(self, x: Publisher):
        return self.data.ds.publishers.add(x)

    def update(self, x: Publisher):
        return self.data.ds.publishers.update(x)

    def remove(self, x: _model.PublisherRef):
        return self.data.ds.publishers.remove(x)

    def clear(self):
        self.data.ds.publishers.clear()

    def has(self, x = None) -> bool:
        return self.data.ds.publishers.has(x)

    def fetch(self, x: object, id:int = None) -> Publisher:
        x_ = str(x)
        p = self.one(x_)
        if p is None:
            p = self.add(Publisher(x_, id))
        return p

    def ref(self, x = None) -> _model.PublisherRef:
        return self.data.ds.publishers.ref(x)

    def refs(self, x = None) -> list[_model.PublisherRef]:
        return self.data.ds.publishers.refs(x)

    def one(self, x = None) -> Publisher:
        return self.data.ds.publishers.one(x)

    def all(self, x = None) -> list[Publisher]:
        return self.data.ds.publishers.all(x)
