import ds.model._dataset as _model
import quartz.gen.data as _data
from quartz.error import Error
from quartz.log import Log
from abc import ABC, abstractmethod

#
# Entities
#

class Entity(ABC):

    def __init__(self, x=None):
        self.api = x

    @property
    def api(self):
        if self._ is None: Error.fail("Detached")
        return self._
    @api.setter
    def api(self, x):
        self._ = Engine.valid(x, nullable=True)

    def attach(self, x:Engine):
        self._ = Engine.valid(x)
        return self

    def detach(self):
        self._ = None
        return self

    @staticmethod
    def valid(x, nullable=False, dettached=True):
        if nullable and (x is None):
            return None
        if isinstance(x, Entity):
            if dettached or x.id:
                return x
        Error.invalid("entity", x)


class Submanager:

    def __init__(self, ent:Entity):
        self._ = Entity.valid(ent)

    @property
    def api(self):
        return self._.api

#
# Managers
#

class Manager(_data.EntitySubset):

    def __init__(self, x):
        self._ = Engine.valid(x)

    @property
    def api(self):
        return self._

class AuthorManager(Manager):
    pass

class BookManager(Manager):
    pass

class GenreManager(Manager):
    pass

class PublisherManager(Manager):
    pass

#
# Engine
#

class Engine:

    def __init__(self, x):
        if isinstance(x, _model.Dataset):
            self._ds = x
        else: Error.invalid("dataset")
        self._authors = None
        self._books = None
        self._genres = None
        self._publishers = None

    @property
    def ds(self):
        return self._ds

    @property
    def authors(self) -> AuthorManager:
        if self._authors: return self._authors
        Error.missing(f"Authors")

    @property
    def books(self) -> BookManager:
        if self._books: return self._books
        Error.missing(f"Books")

    @property
    def genres(self) -> GenreManager:
        if self._genres: return self._genres
        Error.missing(f"Genres")

    @property
    def publishers(self) -> PublisherManager:
        if self._publishers: return self._publishers
        Error.missing(f"Publishers")

    def print(self):
        self.ds.print()

    @staticmethod
    def valid(x, nullable=False, dettached=True):
        if nullable and (x is None):
            return None
        if isinstance(x, Engine):
            return x
        Error.invalid("engine", x)