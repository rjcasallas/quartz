import ds.data._base as _base
import ds.model._dataset as _model
from quartz.error import Error


class Author(_base.Author):

    def __init__(self, name=None, id:int=None):
        _base.Author.__init__(self, name, id)
        _base.Entity.__init__(self)

    def add(self, x):
        if isinstance(x, _base.Engine):
            return x.authors.add(self)

    def remove(self):
        self.data.ds.authors.remove(self)
        self.id = None

    def link(self, x):
        return self.data.authors.link(self, x)

    def unlink(self, x):
        return self.data.authors.unlink(self, x)


class AuthorManager(_base.AuthorManager):

    def add(self, x: Author):
        return self.data.ds.authors.add(x)

    def update(self, x: Author):
        return self.data.ds.authors.update(x)

    def remove(self, x: _model.AuthorRef):
        return self.data.ds.authors.remove(x)

    def clear(self):
        self.data.ds.authors.clear()

    def has(self, x = None) -> bool:
        return self.data.ds.authors.has(x)

    def fetch(self, x: object, id:int = None) -> Author:
        x_ = str(x)
        a = self.one(x_)
        if a is None:
            a = self.add(Author(x_, id))
        return a

    def ref(self, x = None) -> _model.AuthorRef:
        return self.data.ds.authors.ref(x)

    def refs(self, x = None) -> list[_model.AuthorRef]:
        return self.data.ds.authors.refs(x)

    def one(self, x = None) -> Author:
        return self.data.ds.authors.one(x)

    def all(self, x = None) -> list[Author]:
        return self.data.ds.authors.all(x)
