import ds.model._dataset as _model
import quartz.gen.data as _base
from quartz.error import Error
from quartz.log import Log
from abc import ABC, abstractmethod

#
# Entities
#

class Entity(ABC):

    def __init__(self, x=None):
        self.data = x

    @property
    def data(self):
        if self._ is None: Error.fail("Detached")
        return self._
    @data.setter
    def data(self, x):
        if isinstance(x, Engine) or (x is None):
            self._ = x
        else: Error.invalid("engine")


class Author(_model.Author, Entity):

    @staticmethod
    def valid(x, nullable=False, dettached=True):
        if nullable and (x is None):
            return None
        if isinstance(x, Author):
            if dettached or x.id:
                return x
        Error.invalid("author", x)


class Book(_model.Book, Entity):

    @staticmethod
    def valid(x, nullable=False, dettached=True):
        if nullable and (x is None):
            return None
        if isinstance(x, Book):
            if dettached or x.id:
                return x
        Error.invalid("book", x)


class Genre(_model.Genre, Entity):

    @staticmethod
    def valid(x, nullable=False, dettached=True):
        if nullable and (x is None):
            return None
        if isinstance(x, Genre):
            if dettached or x.id:
                return x
        Error.invalid("genre", x)


class Publisher(_model.Publisher, Entity):

    @staticmethod
    def valid(x, nullable=False, dettached=True):
        if nullable and (x is None):
            return None
        if isinstance(x, Publisher):
            if dettached or x.id:
                return x
        Error.invalid("publisher", x)

#
# Managers
#

class Manager(_base.EntityManager):

    def __init__(self, x):
        if isinstance(x, Engine):
            self._ = x
        else: Error.invalid("engine")

    @property
    def data(self):
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
