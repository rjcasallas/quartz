from quartz.error import Error
from abc import ABC, abstractmethod


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
        elif self._validateRef(x):
            self._id = int(x)
        else:
            Error.invalid("id", x)
        return self._id

    def copy(self, x):
        if isinstance(x, Reference):
            self.id = x.id
        return self

    def _validateRef(self, x):
        if isinstance(x, int):
            return x
        if isinstance(x, Reference) and (x._id is not None):
            return x


class BasicSubset(ABC):

    @abstractmethod
    def add(self, x: object):
        pass

    @abstractmethod
    def remove(self, x: object):
        pass

    @abstractmethod
    def has(self, x = None) -> bool:
        pass

    @abstractmethod
    def clear(self):
        pass


class EntitySubset(BasicSubset):

    @abstractmethod
    def set(self, x: object):
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
