import ds.core as _core
import ds.data.author as _base
from ds.data._base import Submanager


class Author(_base.Author):

    def __init__(self, name=None, rank:int=None, id=None, api=None):
        super().__init__(name, id, api)
        self.rank = rank

    @property
    def rank(self):
        return self._rank
    @rank.setter
    def rank(self, x):
        self._rank = int(x) if isinstance(x, int) else None


class AuthorManager(_base.AuthorManager):

    def _create(self, x):
        return Author(id=x[0], name=x[1], rank=[2]).attach(self.api)
