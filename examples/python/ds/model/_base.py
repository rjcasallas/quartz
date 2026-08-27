from quartz.gen.data import Reference
from quartz.error import Error
from quartz.util import Parse
from quartz.log import Log

#
# Entities
#

class AuthorRef(Reference):

    @staticmethod
    def valid(x, nullable = False):
        if nullable and x is None:
            return None
        if isinstance(x, int) or isinstance(x, AuthorRef):
            return int(x)
        Error.invalid("author reference", x)

class BookRef(Reference):

    @staticmethod
    def valid(x, nullable = False):
        if nullable and x is None:
            return None
        if isinstance(x, int) or isinstance(x, BookRef):
            return int(x)
        Error.invalid("book reference", x)

class GenreRef(Reference):

    @staticmethod
    def valid(x, nullable = False):
        if nullable and x is None:
            return None
        if isinstance(x, int) or isinstance(x, GenreRef):
            return int(x)
        Error.invalid("genre reference", x)

class PublisherRef(Reference):

    @staticmethod
    def valid(x, nullable = False):
        if nullable and x is None:
            return None
        if isinstance(x, int) or isinstance(x, PublisherRef):
            return int(x)
        Error.invalid("publisher reference", x)

#
# Junctions
#

class BookAuthorRef:

    def __init__(self, book_id, author_id):
        self.book_id = book_id
        self.author_id = author_id

    def __repr__(self):
        book_id = Parse.string(self._book_id)
        author_id = Parse.string(self._author_id)
        return "book_author⌗{}⌗{}".format(book_id, author_id)

    @property
    def book_id(self):
        return self._book_id
    @book_id.setter
    def book_id(self, x):
        self._book_id = BookRef.valid(x, True)

    @property
    def author_id(self):
        return self._author_id
    @author_id.setter
    def author_id(self, x):
        self._author_id = AuthorRef.valid(x, True)

    def copy(self, x):
        if isinstance(x, BookAuthorRef):
            self.book_id = x.book_id
            self.author_id = x.author_id
        return self

    @staticmethod
    def valid(x, nullable = False):
        if nullable and (x is None):
            return None
        if isinstance(x, BookAuthorRef):
            return x
        Error.invalid("book_author reference", x)

class BookGenreRef:

    def __init__(self, book_id, genre_id):
        self.book_id = book_id
        self.genre_id = genre_id

    def __repr__(self):
        book_id = Parse.string(self._book_id)
        genre_id = Parse.string(self._genre_id)
        return "book_genre⌗{}⌗{}".format(book_id, genre_id)

    @property
    def book_id(self):
        return self._book_id
    @book_id.setter
    def book_id(self, x):
        self._book_id = BookRef.valid(x, True)

    @property
    def genre_id(self):
        return self._genre_id
    @genre_id.setter
    def genre_id(self, x):
        self._genre_id = GenreRef.valid(x, True)

    def copy(self, x):
        if isinstance(x, BookGenreRef):
            self.book_id = x.book_id
            self.genre_id = x.genre_id
        return self

    @staticmethod
    def valid(x, nullable = False):
        if nullable and (x is None):
            return None
        if isinstance(x, BookGenreRef):
            return x
        Error.invalid("book_genre reference", x)

class SubgenreRef:

    def __init__(self, parent_id, child_id):
        self.parent_id = parent_id
        self.child_id = child_id

    def __repr__(self):
        parent_id = Parse.string(self._parent_id)
        child_id = Parse.string(self._child_id)
        return "subgenre⌗{}⌗{}".format(parent_id, child_id)

    @property
    def parent_id(self):
        return self._parent_id
    @parent_id.setter
    def parent_id(self, x):
        self._parent_id = GenreRef.valid(x, True)

    @property
    def child_id(self):
        return self._child_id
    @child_id.setter
    def child_id(self, x):
        self._child_id = GenreRef.valid(x, True)

    def copy(self, x):
        if isinstance(x, SubgenreRef):
            self.parent_id = x.parent_id
            self.child_id = x.child_id
        return self

    @staticmethod
    def valid(x, nullable = False):
        if nullable and (x is None):
            return None
        if isinstance(x, SubgenreRef):
            return x
        Error.invalid("subgenre reference", x)

#
# Self-referencing
#

# "child_genre" genre.id → genre.id
class ChildGenreRef(GenreRef):
    pass

# "parent_genre" genre.id → genre.id
class ParentGenreRef(GenreRef):
    pass

# "parent_publisher" publisher.parent_id → publisher.id
class ParentPublisherRef(PublisherRef):
    pass


