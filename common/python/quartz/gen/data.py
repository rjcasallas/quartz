from abc import ABC, abstractmethod
from quartz.log import Log
from quartz.util import Parse
from quartz.error import Error
from enum import Enum


class Reference:

    def __init__(self, id = None):
        self.id = id

    def __repr__(self):
        return "∅" if self.id is None else f"⌗{self.id}"

    def __str__(self):
        return repr(self)

    def __eq__(self, other: 'Reference'):
        if isinstance(other, Reference):
            return self.id == other.id
        elif isinstance(other, int):
            return self.id == other
        else:
            return False

    def __int__(self):
        return self.id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, x):
        if x is None:
            self._id = None
        elif isinstance(x, int):
            self._id = x
        elif self._validRef(x):
            self._id = int(x)
        else:
            Error.invalid("id", x)
        return self._id

    def copy(self, x):
        if isinstance(x, Reference):
            self.id = x.id
        return self

    def _validRef(self, x):
        if isinstance(x, Reference):
            return x


class BasicManager:

    @abstractmethod
    def add(self, x: object):
        pass

    @abstractmethod
    def update(self, x: object):
        pass

    @abstractmethod
    def remove(self, x: object):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def has(self, x = None) -> bool:
        pass

    @abstractmethod
    def ref(self, x = None) -> Reference:
        pass

    @abstractmethod
    def refs(self, x = None) -> list[Reference]:
        pass

    @abstractmethod
    def one(self, x = None) -> object:
        pass

    @abstractmethod
    def all(self, x = None) -> list[object]:
        pass


class EntityManager(BasicManager):

    @abstractmethod
    def link(self, x, y):
        pass

    @abstractmethod
    def unlink(self, x, y):
        pass

    @abstractmethod
    def fetch(self, x: object, id:int = None) -> object:
        pass

