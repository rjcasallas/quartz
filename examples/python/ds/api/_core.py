import ds.dataset as _ds
import quartz.data.base as _base
from quartz.error import Error
from quartz.log import Log
from abc import ABC, abstractmethod

#
# Entities
#

class Entity(ABC):

    def __init__(self, x=None):
        self._en = x

    @property
    def _en(self):
        if self.__e is None:
            Error.fail(f"Detached {self}")
        return self.__e
    @_en.setter
    def _en(self, x):
        self.__e = Engine.valid(x, nullable=True)

    @property
    def _ds(self):
        return self._en._ds

    def attach(self, x:Engine):
        self.__e = Engine.valid(x)
        return self

    def detach(self):
        self._en = self._ds = None
        return self

    @staticmethod
    def valid(x, nullable=False, dettached=True):
        if nullable and (x is None):
            return None
        if isinstance(x, Entity):
            if dettached or x.id:
                return x
        Error.invalid("entity", x)


class Manager:

    def __init__(self, en, ds):
        self.__e = Engine.valid(en)
        self.__d = _ds.Dataset.valid(ds)

    @property
    def _en(self):
        if self.__e is None:
            Error.fail("Detached")
        return self.__e

    @property
    def _ds(self):
        if self.__d is None:
            Error.fail("Detached")
        return self.__d


class Submanager:

    def __init__(self, e:Entity):
        self.__ = Entity.valid(e)

    @property
    def _(self):
        return self.__

    @property
    def _en(self):
        return self.__._en

    @property
    def _ds(self):
        return self.__._en._ds

#
# Engine
#

class Engine:

    def __init__(self):
        self._authors = None
        self._books = None
        self._genres = None
        self._publishers = None

    @property
    def authors(self) -> Manager:
        if self._authors: return self._authors
        Error.missing(f"Authors")

    @property
    def books(self) -> Manager:
        if self._books: return self._books
        Error.missing(f"Books")

    @property
    def genres(self) -> Manager:
        if self._genres: return self._genres
        Error.missing(f"Genres")

    @property
    def publishers(self) -> Manager:
        if self._publishers: return self._publishers
        Error.missing(f"Publishers")

    def print(self):
        self.ds.print()

    @staticmethod
    def valid(x, nullable=False):
        if nullable and (x is None):
            return None
        if isinstance(x, Engine):
            return x
        Error.invalid("engine", x)