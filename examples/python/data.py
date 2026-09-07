import ds.engine as _api
import ds.sqlite._dataset as _ds
import quartz.db.sqlite as _sqlite
from quartz.app import BasicApp, Types
from quartz.error import Error
from quartz.log import Log
from abc import ABC, abstractmethod
from ds.model._reference import *

class Example(ABC):

    class Entity(Reference):

        def __repr__(self):
            return "∅" if self.id is None else f"⌗{self.id}"

        def __str__(self):
            return self.__repr__()

        def __int__(self):
            return self.id or 0

        def __eq__(self, other):
            return isinstance(other, type(self)) and (self.id == other.id)

        def print(self, level=0):
            Log.list(str(self), level)

    class Named(Entity):
        def __init__(self, name, id=None):
            super().__init__(id)
            self.name = name

        def __eq__(self, other):
            return super().__eq__(other) and (self.name == other.name)

    class Child(Named):
        def __init__(self, name, parent=None, id=None):
            super().__init__(name, id)
            self.parent = parent

        def __eq__(self, other):
            if self.parent is None:
                return super().__eq__(other) and (other.parent is None)
            else:
                return super().__eq__(other) and other.parent and (other.parent.id == self.parent.id)

    class Publisher(Child):

        def __str__(self):
            sid = super().__str__()
            pid =  "∅" if self.parent is None else repr(self.parent)
            return f'publisher{sid}({pid}, "{self.name}")'

    class Author(Named):
        def __init__(self, name, rank=None, id=None):
            super().__init__(name, id)
            self.rank = rank

        def __str__(self):
            sid = super().__str__()
            rank = "" if (self.rank is None) else f", {self.rank}"
            return f'author{sid}("{self.name}"{rank})'

    class Genre(Child):
        def __init__(self, name, parent=None, id=None):
            super().__init__(name, parent, id)
            self.children = []

        def __str__(self):
            sid = super().__str__()
            pid =  "∅" if self.parent is None else repr(self.parent)
            return f'genre{sid}({pid}, "{self.name}")'

        def print(self, level=0):
            super().print(level)
            for g in self.children:
                Log.list(str(g), level+1)

    class Book(Entity):
        def __init__(self, publisher, title, year, genres=None, authors=None, id=None):
            super().__init__(id)
            self.publisher = publisher
            self.title = title
            self.year = year
            self.genres = genres or []
            self.authors = authors or []

        def __str__(self):
            sid = super().__str__()
            return f'book{sid}({repr(self.publisher)}, "{self.title}", {self.year})'

        def __eq__(self, other):
            if not super().__eq__(other): return False
            publisher = ((self.publisher is None) and (other.publisher is None)) or (self.publisher.id == other.publisher.id)
            return  publisher and (self.title == other.title) and (self.year == other.year)

        @property
        def publisher(self):
            return self._publisher

        @publisher.setter
        def publisher(self, value):
            if (value is not None) and not isinstance(value, Example.Publisher): Error.invalid("publisher", value)
            self._publisher = value

        def copy(self, other):
            if isinstance(other, Example.Book):
                self.id = other.id
                self.publisher = other.publisher
                self.title = other.title
                self.year = other.year
            else:
                Error.invalid("book", other)

        def print(self, level=0):
            super().print(level)
            for bg in self.genres:
                Log.list(str(bg), level+1)
            for ba in self.authors:
                Log.list(str(ba), level+1)

    def __init__(self, title):
        self.title = title
        # Publishers
        self.big = Example.Publisher("Big Editorial")
        self.small = Example.Publisher("Small Books", parent=self.big)
        self.modest = Example.Publisher("Modest Reads", parent=self.big)
        self.tiny = Example.Publisher("Tiny House", parent=self.small)
        self.micro = Example.Publisher("Micro Ink", parent=self.modest)
        # Genres
        self.fiction = Example.Genre("Fiction")
        self.non_fiction = Example.Genre("Non-fiction")
        self.adventure = Example.Genre("Adventure", parent=self.fiction)
        self.comedy = Example.Genre("Comedy")
        self.horror = Example.Genre("Horror")
        self.fantasy = Example.Genre("Fantasy", parent=self.fiction)
        self.novel = Example.Genre("Novel", parent=self.fiction)
        self.satire = Example.Genre("Satire")
        self.sci_fi = Example.Genre("Sci-fi", parent=self.fiction)
        # Authors
        self.adams = Example.Author("Douglas Adams")
        self.asturias = Example.Author("Miguel Ángel Asturias")
        self.cervantes = Example.Author("Miguel de Cervantes Saavedra")
        self.dumas = Example.Author("Alexandre Davy de la Pailleterie")
        self.hebert = Example.Author("Frank Herbert")
        self.homer = Example.Author("Homer")
        self.kernighan = Example.Author("Brian Kernighan")
        self.orwell = Example.Author("Eric Arthur Blair")
        self.ritchie = Example.Author("Dennis Ritchie")
        self.rowling = Example.Author("Joanne Rowling")
        self.swift = Example.Author("Jonathan Swift")
        self.woolf = Example.Author("Adeline Virginia Stephen")
        # Books
        self.illiad = Example.Book(self.small, "The Iliad", 700, [ self.fantasy ], [ self.homer ])
        self.quixote = Example.Book(self.modest, "Don Quixote", 1605, [ self.adventure, self.satire ], [ self.cervantes ])
        self.gulliver = Example.Book(self.modest, "Gulliver's Travels", 1726, [ self.adventure, self.comedy, self.fantasy, self.satire ], [ self.swift ])
        self.potter = Example.Book(self.big, "Harry Potter and the Philosopher's Stone", 1997, [ self.adventure, self.fantasy ], [ self.rowling ])
        self.les_trois = Example.Book(self.modest, "Les Trois Mousquetaires", 1894, [ self.adventure, self.novel ], [ self.dumas ])
        self.animal = Example.Book(self.big, "Animal Farm", 1945, [ self.satire ], [ self.orwell ])
        self.ninety = Example.Book(self.big, "1984", 1949, [ self.satire ], [ self.orwell ])
        self.maize = Example.Book(self.small, "Hombres de maíz", 1949, [ self.fantasy ], [ self.asturias ])
        self.dune = Example.Book(self.big, "Dune", 1965, [ self.adventure, self.fantasy, self.sci_fi ], [ self.hebert ])
        self.the_guide = Example.Book(self.big, "The Hitchhiker's Guide to the Galaxy", 1979, [ self.adventure, self.comedy, self.sci_fi ], [ self.adams ])
        self.c_lang = Example.Book(self.small, "The C Programming Language", 1978, [ self.non_fiction ], [ self.kernighan, self.ritchie ])
        self.lighthouse = Example.Book(self.big, "To the Lighthouse", 1927, [ self.novel ], [ self.woolf ])

    def check(self, tag, cond):
        if not cond:
            Error.fail(f"FAILED: {tag}")

    def execute(self):
        self.insert()
        self.update()
        self.select()
        self.delete()

    def insert(self):
        for p in [ self.big, self.modest, self.small, self.tiny, self.micro ]:
            self._insertPublisher(p)
        for g in [ self.fiction, self.non_fiction, self.adventure, self.comedy, self.fantasy, self.novel, self.satire, self.sci_fi ]:
            self._insertGenre(g)
        for a in [ self.adams, self.asturias, self.cervantes, self.dumas, self.hebert, self.homer, self.kernighan, self.orwell, self.ritchie, self.rowling, self.swift, self.woolf ]:
            self._insertAuthor(a)
        for b in [ self.illiad, self.quixote, self.gulliver, self.potter, self.les_trois, self.animal,
                  self.ninety, self.maize, self.dune, self.the_guide, self.c_lang, self.lighthouse ]:
            self._insertBook(b)
        # self.print(f"{self.title} (insert)")
        self.print(f"{self.title} (insert)")

    def update(self):
        # Publisher
        small = self._selectPublisher("Small Books")
        small.name = "Prentice Hall"
        small.parent = self.modest
        self._updatePublisher(small, parent_only=True)
        pub = self._selectPublisher(small, hierarchy=True)
        self.check("update publisher0", (pub and pub.parent is not None))
        self.check("update publisher1", self.small.name == pub.name)   # name unchanged
        self.check("update publisher2", self.modest.id == pub.parent.id) # publisher changed
        self._updatePublisher(small)
        pub = self._selectPublisher(small, hierarchy=True)
        self.check("update publisher3", small == pub)

        # Genres
        novel = self._selectGenre("Novel")
        novel.name = "Romance"
        novel.parent = None
        self._updateGenre(novel)
        self.comedy.name = "Funny"
        self.comedy.parent = self.satire
        self._updateGenre(self.comedy)
        # Author
        self.orwell = self._selectAuthor("Eric Arthur Blair")
        self.orwell.name = "George Orwell"
        self._updateAuthor(self.orwell)
        self.rowling.name = "J. K. Rowling"
        self._updateAuthor(self.rowling)
        self.dumas.name = "Alexandre Dumas"
        self._updateAuthor(self.dumas)
        self.woolf.name = "Virginia Woolf"
        self._updateAuthor(self.woolf)
        # Books
        c_lang = self._selectBook("The C Programming Language")
        c_lang.title = "The C Programming Language, Second Edition"
        c_lang.publisher = self.modest
        self._updateBook(c_lang)
        self._renameBook(self.potter, "Harry Potter and the Sorcerer's Stone")
        self.print(f"{self.title} (update)")

        dune = Example.Book(publisher=None, title="X", year=0, id=self.dune.id)
        self._syncBook(dune, True)
        self.check("sync book title", dune.title == self.dune.title)
        self.check("sync book title2", dune.year == 0)
        self._syncBook(dune)
        self.check("sync book", dune == self.dune)

    def select(self, level=0):
        Log.list(f"\n{self.title} (select)", level)
        # Publishers
        Log.list(f"Publishers", level+1)
        big = self._selectPublisher(self.big.id, True)
        Log.list(f"{big} == {self.big}", level+2, "★")
        self.check("select publisher by id", big == self.big)
        modest = self._selectPublisher("Modest Reads", True)
        Log.list(f"{modest} == {self.modest}", level+2, "★")
        self.check("select publisher by name", modest == self.modest)
        Log.list(f"{self.small}", level+2)
        for b in self._selectBooks(self.small):
            Log.list(f"{b}", level+3)
        # Genres
        Log.list(f"Genres", level+1)
        fiction = self._selectGenre(self.fiction.id, True)
        Log.list(f"{fiction} == {self.fiction}", level+2, "★")
        self.check("select genre by id", fiction == self.fiction)
        comedy = self._selectGenre("Funny", True)
        Log.list(f"{comedy} == {self.comedy}", level+2, "★")
        self.check("select genre by name", comedy == self.comedy)

        # Author
        Log.list(f"Author", level+1)
        # By id
        adams = self._selectAuthor(self.adams.id)
        Log.list(f"{adams} == {self.adams}", level+2, "★")
        self.check("select author by id", adams == self.adams)
        # By name
        woolf = self._selectAuthor("Virginia Woolf")
        Log.list(f"{woolf} == {self.woolf}", level+2, "★")
        self.check("select author by name", woolf == self.woolf)
        # By book
        Log.list(f"{self.c_lang}", level+2)
        for a in self._selectAuthors(self.c_lang, order_by="rank"):
            Log.list(f"{a}", level+3)

        # Books
        Log.list(f"Books", level+1)
        # By id
        quixote = self._selectBook(self.quixote.id)
        Log.list(f"{quixote} == {self.quixote}", level+2, "★")
        self.check("select book by id", quixote == self.quixote)
        # By title
        dune = self._selectBook("Dune")
        Log.list(f"{dune} == {self.dune}", level+2, "★")
        self.check("select book by name", dune == self.dune)
        # By author
        Log.list(f"{self.orwell}", level+2)
        for b in self._selectBooks(self.orwell):
            Log.list(f"{b}", level+3)
        # By genre
        Log.list(f"{self.sci_fi}", level+2)
        for b in self._selectBooks(self.sci_fi):
            Log.list(f"{b}", level+3)
        # By year
        Log.list(f"[1940, 1980]", level+2, "★")
        books = self._selectBooks(YearRef(1940, 1980))
        for b in books:
            Log.list(f"{b}", level+3)
        # self.check("select book by year", dune == self.dune)

    def delete(self):
        # Publisher
        self._deletePublisher(self.micro)
        self._deletePublisher("Tiny House")
        # Genres
        self._deleteGenre(self.adventure)
        self._deleteGenre("Horror")
        # Author
        self._deleteAuthor(self.homer)
        self._deleteAuthor("Miguel Ángel Asturias")
        # Books
        self._deleteBook(self.gulliver)
        self._deleteBookGenre(self.dune, self.fantasy)
        self._deleteBookAuthor("The C Programming Language, Second Edition", self.kernighan)
        self.print(f"{self.title} (delete)")

    def print(self, title=None, level=0, publishers=False, genres=False, authors=False, books=False):
        if title:
            Log.list(f"\n{title}", level)
        all = not (publishers or genres or authors or books)
        # self.db.print()
        if all or publishers: self._printPublishers(level)
        if all or genres: self._printGenres(level)
        if all or authors: self._printAuthors(level)
        if all or books: self._printBooks(level)

    def _printPublishers(self, level=0):
        entries = self._selectPublishers()
        count = len(entries)
        Log.list(f"Publishers({count})", level+1)
        for p in entries:
            if p: p.print(level+2)

    def _printGenres(self, level=0):
        entries = self._selectGenres()
        count = len(entries)
        Log.list(f"Genres({count})", level+1)
        for g in entries:
            if g: g.print(level+2)

    def _printAuthors(self, level=0):
        entries = self._selectAuthors()
        count = len(entries)
        Log.list(f"Authors({count})", level+1)
        for a in entries:
            if a: a.print(level+2)

    def _printBooks(self, level=0):
        entries = self._selectBooks()
        count = len(entries)
        Log.list(f"Books({count})", level+1)
        for b in entries:
            if b: b.print(level+2)

    # Publishers

    @abstractmethod
    def _insertPublisher(self, p):
        pass

    @abstractmethod
    def _updatePublisher(self, p, parent_only=False):
        pass

    @abstractmethod
    def _deletePublisher(self, p):
        pass

    @abstractmethod
    def _selectPublishers(self):
        pass

    @abstractmethod
    def _selectPublisher(self, p, hierarchy=False):
        pass

    # Genres

    @abstractmethod
    def _insertGenre(self, g):
        pass

    @abstractmethod
    def _updateGenre(self, g):
        pass

    @abstractmethod
    def _deleteGenre(self, g):
        pass

    @abstractmethod
    def _selectGenres(self):
        pass

    @abstractmethod
    def _selectGenre(self, x, hierarchy=False):
        pass

    # Authors

    @abstractmethod
    def _insertAuthor(self, a):
        pass

    @abstractmethod
    def _updateAuthor(self, a):
        pass

    @abstractmethod
    def _deleteAuthor(self, a):
        pass

    @abstractmethod
    def _selectAuthors(self, a=None, order_by=None):
        pass

    @abstractmethod
    def _selectAuthor(self, x):
        pass

    # Books

    @abstractmethod
    def _insertBook(self, b):
        pass

    @abstractmethod
    def _updateBook(self, b):
        pass

    @abstractmethod
    def _renameBook(self, b, name:str):
        pass

    @abstractmethod
    def _syncBook(self, b):
        pass

    @abstractmethod
    def _deleteBook(self, b):
        pass

    @abstractmethod
    def _deleteBookGenre(self, b, g):
        pass

    @abstractmethod
    def _deleteBookAuthor(self, b, a):
        pass

    @abstractmethod
    def _selectBooks(self, b=None, order_by=None):
        pass

    @abstractmethod
    def _selectBook(self, x):
        pass


class RawExample(Example):

    def __init__(self, schema, path, reset):
        super().__init__("RAW")
        self.db = _sqlite.Database(schema, path)
        self.db.open(reset)

    # Publishers

    def _insertPublisher(self, p):
        p.id = self.db.exec("INSERT INTO publisher(parent_id, name) VALUES(?, ?)", [ p.parent.id if p.parent else None,  p.name ])

    def _updatePublisher(self, p, parent_only=False):
        if parent_only:
            self.db.exec("UPDATE `publisher` SET `parent_id`=? WHERE `id`=?", [ p.parent.id, p.id ])
        else:
            self.db.exec("UPDATE `publisher` SET `parent_id`=?, `name`=? WHERE `id`=?", [ p.parent.id if p.parent else None,  p.name, p.id ])

    def _deletePublisher(self, x):
        if isinstance(x, int) or isinstance(x, Example.Publisher):
            self.db.exec("DELETE FROM `publisher` WHERE `id`=?", [ int(x) ])
        elif isinstance(x, str):
            self.db.exec("DELETE FROM `publisher` WHERE `name`=?", [ x ])

    def _selectPublishers(self):
        all = []
        for row in self.db.all(f"SELECT `id` FROM `publisher`"):
            all.append(self._selectPublisher(row[0], True))
        return all

    def _selectPublisher(self, x, hierarchy=False):
        row = None
        if isinstance(x, int) or isinstance(x, Example.Publisher):
            row = self.db.one(f"SELECT * FROM `publisher` WHERE `id`=?", [ int(x) ])
        elif isinstance(x, str):
            row = self.db.one(f"SELECT * FROM `publisher` WHERE `name`=?", [ x ])
        if row is None:
            Error.invalid("publisher", x)
        pp = self._selectPublisher(row[1]) if (hierarchy and row[1]) else None
        return Example.Publisher(id=row[0], parent=pp, name=row[2])

    # Genres

    def _insertGenre(self, g):
        g.id = self.db.exec(f"INSERT INTO genre(name) VALUES(?)", [ g.name ])
        if g.parent:
            self.db.exec("REPLACE INTO subgenre(parent_id, child_id) VALUES(?, ?)", [ g.parent.id, g.id ])

    def _updateGenre(self, g):
        self.db.exec("UPDATE `genre` SET `name`=? WHERE `id`=?", [ g.name, g.id ])
        if g.parent and g.parent.id:
            self.db.exec(f"REPLACE INTO `subgenre`(`parent_id`, `child_id`) VALUES (?, ?)", [ g.parent.id, g.id ])
        else:
            self.db.exec(f"DELETE FROM `subgenre` WHERE `child_id`=?", [ g.id ])

    def _deleteGenre(self, x):
        if isinstance(x, int) or isinstance(x, Example.Genre):
            self.db.exec("DELETE FROM `genre` WHERE `id`=?", [ int(x) ])
        elif isinstance(x, str):
            self.db.exec("DELETE FROM `genre` WHERE `name`=?", [ x ])

    def _selectGenres(self):
        all = []
        for row in self.db.all(f"SELECT `id` FROM `genre`"):
            all.append(self._selectGenre(row[0], hierarchy=True))
        return all

    def _selectGenre(self, x, hierarchy=False):
        row = None
        if isinstance(x, int) or isinstance(x, Example.Genre):
            row = self.db.one(f"SELECT * FROM `genre` WHERE `id`=?", [ int(x) ])
        elif isinstance(x, str):
            row = self.db.one(f"SELECT * FROM `genre` WHERE `name`=?", [ x ])
        if row is None:
            Error.invalid("genre", x)
        genre = Example.Genre(id=row[0], name=row[1]) if row else None
        if hierarchy:
            # Parent
            row = self.db.one(f"SELECT `parent_id` FROM `subgenre` WHERE `child_id`=?", [ int(genre) ])
            genre.parent = self._selectGenre(row[0]) if row else None
            # Children
            for row in self.db.all(f"SELECT `child_id` FROM `subgenre` s INNER JOIN `genre` g ON g.`id` = s.`child_id` WHERE `parent_id`=?", [ int(genre) ]):
                genre.children.append(self._selectGenre(row[0]))
        return genre

    # Authors

    def _insertAuthor(self, a):
        a.id = self.db.exec("INSERT INTO author(name) VALUES(?)", [ a.name ])

    def _updateAuthor(self, a):
        self.db.exec("UPDATE `author` SET `name`=? WHERE `id`=?", [ a.name, a.id ])

    def _deleteAuthor(self, x):
        if isinstance(x, int) or isinstance(x, Example.Author):
            self.db.exec("DELETE FROM `author` WHERE `id`=?", [ int(x) ])
        elif isinstance(x, str):
            self.db.exec("DELETE FROM `author` WHERE `name`=?", [ x ])

    def _selectAuthors(self, x=None, order_by=None):
        all = []
        order = f"ORDER BY {order_by or 'name'}"
        if x is None:
            rows = self.db.all(f"SELECT a.*, NULL FROM `author` a {order}")
        elif isinstance(x, Example.Book):
            rows = self.db.all(f"SELECT a.*, ba.`rank` FROM `author` a INNER JOIN `book_author` ba ON ba.`author_id`=a.`id` WHERE ba.`book_id`=? {order}", [ x.id ])
        else:
            Error.invalid(f"author ref", x)
        for r in rows:
            all.append(Example.Author(id=r[0], name=r[1], rank=r[2]))
        return all

    def _selectAuthor(self, x):
        row = None
        if isinstance(x, int) or isinstance(x, Example.Author):
            row = self.db.one(f"SELECT * FROM `author` WHERE `id`=?", [ int(x) ])
        elif isinstance(x, str):
            row = self.db.one(f"SELECT * FROM `author` WHERE `name`=?", [ x ])
        if row is None:
            Error.invalid("author", x)
        return Example.Author(id=row[0], name=row[1]) if row else None

    # Books

    def _insertBook(self, b:Example.Book):
        b.id = self.db.exec("INSERT INTO book(publisher_id, title, year) VALUES(?, ?, ?)", [ b.publisher.id, b.title, b.year ])
        for g in b.genres:
            self.db.exec("REPLACE INTO book_genre VALUES(?, ?)", [ b.id, g.id ])
        for i in range(0, len(b.authors)):
            self.db.exec("REPLACE INTO book_author VALUES(?, ?, ?)", [ b.id, b.authors[i].id, i+1 ])

    def _updateBook(self, b:Example.Book):
        self.db.exec("UPDATE `book` SET `publisher_id`=?, `title`=?, `year`=? WHERE `id`=?", [ b.publisher.id, b.title, b.year, b.id ])

    def _renameBook(self, b:Example.Book, name:str):
        b.title = name
        self.db.exec("UPDATE `book` SET `title`=? WHERE `id`=?", [ b.title, b.id ])

    def _syncBook(self, b:Example.Book, name_only=False):
        b2 = self._selectBook(b.id)
        if name_only:
            b.title = b2.title
        else:
            b.copy(b2)

    def _deleteBook(self, x):
        if isinstance(x, int) or isinstance(x, Example.Book):
            self.db.exec("DELETE FROM `book` WHERE `id`=?", [ int(x) ])
        elif isinstance(x, str):
            self.db.exec("DELETE FROM `book` WHERE `title`=?", [ x ])

    def _deleteBookGenre(self, b, g):
        b = self._selectBook(b)
        if b:
            self.db.exec("DELETE FROM `book_genre` WHERE `book_id`=? AND `genre_id`=?", [ int(b), int(g) ])

    def _deleteBookAuthor(self, b, a):
        b = self._selectBook(b)
        if b:
            self.db.exec("DELETE FROM `book_author` WHERE `book_id`=? AND `author_id`=?", [ int(b), int(a) ])

    def _selectBooks(self, x=None, order_by=None):
        all = []
        order = f" ORDER BY {order_by or 'year'}"
        if x is None:
            rows = self.db.all(f"SELECT `id` FROM `book`{order}")
        elif isinstance(x, Example.Publisher):
            rows = self.db.all(f"SELECT `id` FROM `book` WHERE `publisher_id`=? {order}", [ x.id ])
        elif isinstance(x, Example.Genre):
            rows = self.db.all(f"SELECT `id` FROM `book` b INNER JOIN `book_genre` bg ON bg.`book_id`=b.`id` WHERE bg.`genre_id`=? {order}", [ x.id ])
        elif isinstance(x, Example.Author):
            rows = self.db.all(f"SELECT `id` FROM `book` b INNER JOIN `book_author` ba ON ba.`book_id`=b.`id` WHERE ba.`author_id`=? {order}", [ x.id ])
        elif isinstance(x, YearRef):
            rows = self.db.all(f"SELECT `id` FROM `book` b WHERE b.`year` >= ? AND b.`year` <= ? {order}", [ x.start, x.end ])
        else:
            Error.invalid(f"book ref", x)
        for r in rows:
            all.append(self._selectBook(r[0]))
        return all

    def _selectBook(self, x):
        # Book
        row = None
        if isinstance(x, int) or isinstance(x, Example.Book):
            row = self.db.one(f"SELECT * FROM `book` WHERE `id`=?", [ int(x) ])
        elif isinstance(x, str):
            row = self.db.one(f"SELECT * FROM `book` WHERE `title`=?", [ x ])
        if row is None:
            Error.invalid("book", x)
        # Publisher
        p = self._selectPublisher(row[1])
        book = Example.Book(id=row[0], publisher=p, title=row[2], year=row[3])
        # Genres
        for bg in self.db.all(f"SELECT * FROM `genre` g INNER JOIN `book_genre` bg ON bg.`genre_id`=g.`id` WHERE bg.`book_id`=?", [ book.id ]):
            book.genres.append(Example.Genre(id=bg[0], name=bg[1]))
        # Authors
        for ba in self.db.all(f"SELECT * FROM `author` a INNER JOIN `book_author` ba ON ba.`author_id`=a.`id` WHERE ba.`book_id`=?", [ book.id ]):
            book.genres.append(Example.Author(id=ba[0], name=ba[1]))
        return book


class DatasetExample(Example):

    def __init__(self, schema, path, reset):
        super().__init__("DATASET")
        self.ds = _ds.Dataset(schema, path)
        self.ds.open(reset)

    # Publishers

    def _insertPublisher(self, p):
        pid = p.parent.id if p.parent else None
        p.id = int(self.ds.publishers.add(_ds.Publisher(pid, p.name)))

    def _updatePublisher(self, p, parent_only=False):
        ppi = p.parent.id if p.parent else None
        pd = _ds.Publisher(id=p.id, parent_id=ppi, name=p.name)
        if parent_only:
            self.ds.publishers.set((pd, Fields.Parent))
        else:
            self.ds.publishers.set(pd)

    def _deletePublisher(self, x):
        if isinstance(x, int) or isinstance(x, Example.Publisher):
            self.ds.publishers.remove(int(x))
        elif isinstance(x, str):
            self.ds.publishers.remove(x)

    def _selectPublishers(self):
        all = []
        for r in self.ds.publishers.refs():
            all.append(self._selectPublisher(r, True))
        return all

    def _selectPublisher(self, x, hierarchy=False):
        y = int(x) if isinstance(x, Example.Publisher) else x
        pd = self.ds.publishers.one(y)
        if pd is None:
            Error.invalid("publisher", x)
        pp = self._selectPublisher(pd.parent_id) if (hierarchy and pd.parent_id) else None
        return Example.Publisher(id=pd.id, parent=pp, name=pd.name)

    # Genres

    def _insertGenre(self, g):
        g.id = int(self.ds.genres.add(_ds.Genre(g.name)))
        if g.parent and g.parent.id:
            self.ds.genres.add(SubgenreRef(g.parent.id, g.id))

    def _updateGenre(self, g):
        self.ds.genres.set(_ds.Genre(id=g.id, name=g.name) )
        self.ds.genres.set(SubgenreRef(g.parent.id if g.parent else None, g.id))

    def _deleteGenre(self, x):
        if isinstance(x, int) or isinstance(x, Example.Genre):
            self.ds.genres.remove(int(x))
        elif isinstance(x, str):
            self.ds.genres.remove(x)

    def _selectGenres(self):
        all = []
        for r in self.ds.genres.refs():
            all.append(self._selectGenre(r, hierarchy=True))
        return all

    def _selectGenre(self, x, hierarchy=False):
        g = self.ds.genres.one(x)
        if g is None:
            Error.invalid("genre", x)
        genre = Example.Genre(id=g.id, name=g.name) if g else None
        if hierarchy:
            # Parent
            gr = self.ds.genres.ref(ChildGenreRef(g))
            genre.parent = self._selectGenre(gr) if gr else None
            # Children
            for gr in self.ds.genres.refs(ParentGenreRef(g)):
                genre.children.append(self._selectGenre(gr))
        return genre

    # Authors

    def _insertAuthor(self, a):
        a.id = int(self.ds.authors.add(_ds.Author(a.name)))

    def _updateAuthor(self, a):
        self.ds.authors.set(_ds.Author(id=a.id, name=a.name))

    def _deleteAuthor(self, x):
        if isinstance(x, int) or isinstance(x, Example.Author):
            self.ds.authors.remove(int(x))
        elif isinstance(x, str):
            self.ds.authors.remove(x)

    def _selectAuthors(self, x=None, order_by=None):
        all = []
        if x is None:
            rows = self.ds.authors.find(tag="full", order=order_by)
        elif isinstance(x, Example.Book):
            rows = self.ds.authors.find(BookRef(x.id), tag="full", order=order_by)
        else:
            Error.invalid(f"author ref", x)
        for r in rows:
            all.append(Example.Author(id=r[0], name=r[1], rank=r[2]))
        return all

    def _selectAuthor(self, x):
        a = self.ds.authors.one(x)
        if a is None:
            Error.invalid("author", x)
        return Example.Author(id=a.id, name=a.name) if a else None

    # Books

    def _insertBook(self, b:Example.Book):
        b.id = int(self.ds.books.add(_ds.Book(b.publisher.id, b.title, b.year)))
        for g in b.genres:
            self.ds.genres.add(BookGenreRef(int(b), int(g)))
        for i in range(0, len(b.authors)):
            self.ds.authors.add(_ds.BookAuthor(int(b), int(b.authors[i]), i+1))

    def _updateBook(self, b:Example.Book):
        self.ds.books.set(_ds.Book(b.publisher.id, b.title, b.year, id=b.id))

    def _renameBook(self, b:Example.Book, name:str):
        b.title = name
        self.ds.books.set((_ds.Book(title=b.title, id=b.id), Fields.Title))

    def _syncBook(self, b:Example.Book, name_only=False):
        pid = int(b.publisher) if b.publisher else None
        bd = _ds.Book(publisher_id=pid, title=b.title, year=b.year, id=b.id)
        if name_only:
            self.ds.books.get(bd, Fields.Title)
        else:
            self.ds.books.get(bd)
        b.publisher = self._selectPublisher(bd.publisher_id) if bd.publisher_id else None
        b.title = bd.title
        b.year = bd.year

    def _deleteBook(self, x):
        if isinstance(x, int) or isinstance(x, Example.Book):
            self.ds.books.remove(int(x))
        elif isinstance(x, str):
            self.ds.books.remove(x)

    def _deleteBookGenre(self, b, g):
        b = self._selectBook(b)
        if b:
            self.ds.books.remove(BookGenreRef(int(b), int(g)))

    def _deleteBookAuthor(self, b, a):
        b = self._selectBook(b)
        if b:
            self.ds.books.remove(BookAuthorRef(int(b), int(a)))

    def _selectBooks(self, x=None, order_by=None):
        all = []
        if x is None:
            rows = self.ds.books.refs(order=order_by)
        elif isinstance(x, Example.Publisher):
            rows = self.ds.books.refs(PublisherRef(x.id), order=order_by, debug=True)
        elif isinstance(x, Example.Genre):
            rows = self.ds.books.refs(GenreRef(x.id), order=order_by)
        elif isinstance(x, Example.Author):
            rows = self.ds.books.refs(AuthorRef(x.id), order=order_by)
        elif isinstance(x, YearRef):
            rows = self.ds.books.refs(x, order=order_by)
        else:
            Error.invalid(f"book ref", x)
        for r in rows:
            all.append(self._selectBook(r))
        return all

    def _selectBook(self, x):
        # Book
        y = x.id if isinstance(x, Example.Book) else x
        b = self.ds.books.one(y)
        if b is None:
            Error.invalid("book", x)
        # Publisher
        p = self._selectPublisher(b.publisher_id)
        book = Example.Book(id=b.id, publisher=p, title=b.title, year=b.year) if b else None
        # Genres
        for gr in self.ds.genres.refs(b):
            book.genres.append(self._selectGenre(gr))
        # Authors
        for ar in self.ds.authors.refs(b):
            book.genres.append(self._selectAuthor(ar))
        return book


class ApiExample(Example):

    def __init__(self, schema, path, reset):
        super().__init__("API")
        self.api = _api.Engine(schema, path, reset)

    # Publishers

    def _insertPublisher(self, p):
        # Parent
        pp = p.parent.id if p.parent else None
		# Insert
        pd = _api.Publisher(pp, p.name).add(self.api)
        p.id = int(pd)

    def _updatePublisher(self, p, parent_only=False):
        pid = p.parent.id if p.parent else None
        pd = _api.Publisher(id=p.id, parent_id=pid, name=p.name).attach(self.api)
        if parent_only:
            pd.parent.set(pid)
        else:
            pd.push()

    def _deletePublisher(self, x):
        if isinstance(x, int) or isinstance(x, Example.Publisher):
            self.api.publishers.remove(int(x))
        elif isinstance(x, str):
            self.api.publishers.remove(x)

    def _selectPublishers(self):
        all = []
        for r in self.api.publishers.refs():
            all.append(self._selectPublisher(r, True))
        return all

    def _selectPublisher(self, x, hierarchy=False):
        y = int(x) if isinstance(x, Example.Publisher) else x
        pd = self.api.publishers.one(y)
        if pd is None:
            Error.invalid("publisher", x)
        pp = pd.parent.get()
        pe = Example.Publisher(id=pp.id, name=pp.name) if pp else None
        return Example.Publisher(id=pd.id, parent=pe, name=pd.name)

    # Genres

    def _insertGenre(self, g):
        g.id = int(self.api.genres.fetch(g.name))
        if g.parent and g.parent.id:
            pd = self.api.genres.one(g.parent.id)
            pd.children.add(g.id)

    def _updateGenre(self, g):
        gd = self.api.genres.set(_api.Genre(id=g.id, name=g.name, api=self.api) )
        gd.parent.set(g.parent.id if g.parent else None)

    def _deleteGenre(self, x):
        if isinstance(x, int) or isinstance(x, Example.Genre):
            self.api.genres.remove(int(x))
        elif isinstance(x, str):
            gr = self.api.genres.fetch(x)
            gr.remove()

    def _selectGenres(self):
        all = []
        for r in self.api.genres.refs():
            all.append(self._selectGenre(r, hierarchy=True))
        return all

    def _selectGenre(self, x, hierarchy=False):
        gd = self.api.genres.one(x)
        if gd is None:
            Error.invalid("genre", x)
        genre = Example.Genre(id=gd.id, name=gd.name) if gd else None
        if hierarchy:
            # Parent
            gp = gd.parent.get()
            genre.parent = Example.Genre(id=gp.id, name=gp.name) if gp else None
            # Children
            for g in gd.children.all():
                genre.children.append(Example.Genre(id=g.id, name=g.name))
        return genre

    # Authors

    def _insertAuthor(self, a):
        a.id = int(self.api.authors.fetch(a.name))

    def _updateAuthor(self, a):
        self.api.authors.set(_ds.Author(id=a.id, name=a.name))

    def _deleteAuthor(self, x):
        if isinstance(x, int) or isinstance(x, Example.Author):
            self.api.authors.remove(int(x))
        elif isinstance(x, str):
            self.api.authors.remove(x)

    def _selectAuthors(self, x=None, order_by=None):
        all = []
        if x is None:
            rows = self.api.authors.all(order=order_by)
        elif isinstance(x, Example.Book):
            rows = self.api.authors.all(BookRef(x.id), order=order_by)
        else:
            Error.invalid(f"author ref", x)
        for a in rows:
            all.append(Example.Author(id=a.id, name=a.name, rank=a.rank))
        return all

    def _selectAuthor(self, x):
        a = self.api.authors.one(x)
        if a is None:
            Error.invalid("author", x)
        return Example.Author(id=a.id, name=a.name) if a else None

    # Books

    def _insertBook(self, b:Example.Book):
        p = self.api.publishers.one(b.publisher.id)
        bd = _api.Book(p, b.title, b.year, api=self.api).add(self.api)
        b.id = int(bd)
        for g in b.genres:
            bd.genres.add(g)
        for i in range(0, len(b.authors)):
            bd.authors.add(b.authors[i], i+1)

    def _updateBook(self, b:Example.Book):
        p = self.api.publishers.one(b.publisher.id)
        _api.Book(p, b.title, b.year, id=b.id).attach(self.api).push()

    def _renameBook(self, b:Example.Book, name:str):
        b.title = name
        _api.Book(title=b.title, id=b.id).attach(self.api).push(Fields.Title)

    def _syncBook(self, b:Example.Book, name_only=False):
        pid = int(b.publisher) if b.publisher else None
        bd = _api.Book(publisher_id=pid, title=b.title, year=b.year, id=b.id).attach(self.api)
        if name_only:
            bd.pull(Fields.Title)
        else:
            bd.pull()
        pd = bd.publisher.get()
        b.publisher = Example.Publisher(id=pd.id, name=pd.name) if pd else None
        b.title = bd.title
        b.year = bd.year

    def _deleteBook(self, x):
        if isinstance(x, int) or isinstance(x, Example.Book):
            _api.Book(id=int(x)).attach(self.api).remove()
        elif isinstance(x, str):
            self.api.books.remove(x)

    def _deleteBookGenre(self, b, g):
        x = b.id if isinstance(b, Example.Book) else b
        bd = self.api.books.one(x)
        if bd:
            bd.genres.remove(g)

    def _deleteBookAuthor(self, b, a):
        x = b.id if isinstance(b, Example.Book) else b
        bd = self.api.books.one(x)
        if bd:
            bd.authors.remove(a)

    def _selectBooks(self, x=None, order_by=None):
        all = []
        if x is None:
            rows = self.api.books.refs(order=order_by)
        elif isinstance(x, Example.Publisher):
            rows = self.api.books.refs(PublisherRef(x.id), order=order_by)
        elif isinstance(x, Example.Genre):
            rows = self.api.books.refs(GenreRef(x.id), order=order_by)
        elif isinstance(x, Example.Author):
            rows = self.api.books.refs(AuthorRef(x.id), order=order_by)
        elif isinstance(x, YearRef):
            rows = self.api.books.refs(x, order=order_by)
        else:
            Error.invalid(f"book ref", x)
        for r in rows:
            all.append(self._selectBook(r))
        return all

    def _selectBook(self, x):
        # Book
        y = x.id if isinstance(x, Example.Book) else x
        bd = self.api.books.one(y)
        if bd is None:
            Error.invalid("book", x)
        # Publisher
        p = self._selectPublisher(bd.publisher_id)
        book = Example.Book(id=bd.id, publisher=p, title=bd.title, year=bd.year)
        # Genres
        for gd in bd.genres.all():
            book.genres.append(Example.Genre(id=gd.id, name=gd.name))
        # Authors
        for ad in bd.authors.all():
            book.authors.append(Example.Author(id=ad.id, name=ad.name))
        return book


class DatasetApp(BasicApp):

    def __init__(self):
        super().__init__("Dataset Example", "1.0.0")

    def setup(self) -> None:
        self.args.fixed.add("schema", Types.Int16u, "examples/db/books.sql")
        self.args.dashed.add("path", "p", Types.Path, "temp/books.db")
        self.args.dashed.add("reset", "r", Types.Boolean, True)

    def execute(self):
        self.print()
        schema = self.args.string("schema")
        path = self.args.string("path")
        reset = self.args.boolean("reset")
        # Raw
        e = RawExample(schema, path, reset)
        e.execute()
        # Core
        e = DatasetExample(schema, path, reset)
        e.execute()
        # API
        e = ApiExample(schema, path, reset)
        e.execute()


if __name__ == "__main__":
    app = DatasetApp()
    app.run()
