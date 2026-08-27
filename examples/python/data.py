import ds.api as _api
import ds.sqlite._dataset as _basic
import quartz.db.sqlite as _sqlite
from quartz.app import BasicApp, BasicCommand, Types
from quartz.error import Error
from quartz.log import Log
from abc import ABC, abstractmethod


class Example(ABC):

    class Entity:
        def __init__(self, id):
            self.id = id

        def __repr__(self):
            return "∅" if self.id is None else f"⌗{self.id}"

        def __str__(self):
            return self.__repr__()

        def __int__(self):
            return self.id

        def print(self, level=0):
            Log.list(str(self), level)

    class Named(Entity):
        def __init__(self, name, id=None):
            super().__init__(id)
            self.name = name

    class Publisher(Named):
        def __init__(self, name, parent=None, id=None):
            super().__init__(name, id)
            self.parent = parent

        def __str__(self):
            sid = super().__str__()
            pid =  "∅" if self.parent is None else repr(self.parent)
            return f'publisher{sid}({pid}, "{self.name}")'

    class Author(Named):
        def __str__(self):
            sid = super().__str__()
            return f'author{sid}("{self.name}")'

    class Genre(Named):
        def __init__(self, name, parent=None, id=None):
            super().__init__(name, id)
            self.parent = parent
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
            return f'book{sid}({repr(self.publisher)}, "{self.title}")'

        def print(self, level=0):
            super().print(level)
            for bg in self.genres:
                Log.list(str(bg), level+1)
            for ba in self.authors:
                Log.list(str(ba), level+1)

    def __init__(self):
        # Publishers
        self.big = Example.Publisher("Big Editorial")
        self.small = Example.Publisher("Small Books", parent=self.big)
        self.modest = Example.Publisher("Modest Reads", parent=self.big)
        # Genres
        self.fiction = Example.Genre("Fiction")
        self.adventure = Example.Genre("Adventure", parent=self.fiction)
        self.comedy = Example.Genre("Comedy")
        self.fantasy = Example.Genre("Fantasy", parent=self.fiction)
        self.novel = Example.Genre("Novel", parent=self.fiction)
        self.satire = Example.Genre("Satire")
        self.sci_fi = Example.Genre("Sci-fi", parent=self.fiction)
        # Authors
        self.adams = Example.Author("Douglas Adams")
        self.asturias = Example.Author("Miguel Ángel Asturias")
        self.brown = Example.Author("Dan Brown")
        self.dumas = Example.Author("Alexandre Dumas")
        self.cervantes = Example.Author("Miguel de Cervantes Saavedra")
        self.marquez = Example.Author("Gabiel García Márquez")
        self.hebert = Example.Author("Frank Herbert")
        self.homer = Example.Author("Homer")
        self.orwell = Example.Author("George Orwell")
        self.swift = Example.Author("Jonathan Swift")
        # Books
        self.illiad = Example.Book(self.small, "The Iliad", 700, [ self.fantasy ], [ self.homer ])
        self.odyssey = Example.Book(self.small, "The Odyssey", 701, [ self.fantasy ], [ self.homer ])
        self.quixote = Example.Book(self.modest, "Don Quixote", 1605, [ self.adventure, self.satire ], [ self.cervantes ])
        self.gulliver = Example.Book(self.modest, "Gulliver's Travels", 1726, [ self.adventure, self.comedy, self.fantasy, self.satire ], [ self.swift ])
        self.le_comte = Example.Book(self.modest, "Le Comte de Monte-Cristo", 1944, [ self.adventure, self.novel ], [ self.dumas ])
        self.les_trois = Example.Book(self.modest, "Les Trois Mousquetaires", 1894, [ self.adventure, self.novel ], [ self.dumas ])
        self.animal = Example.Book(self.big, "Animal Farm", 1945, [ self.satire ], [ self.orwell ])
        self.ninety = Example.Book(self.big, "1984", 1949, [ self.satire ], [ self.orwell ])
        self.maize = Example.Book(self.big, "Hombres de maíz", 1949, [ self.fantasy ], [ self.asturias ])
        self.dune = Example.Book(self.big, "Dune", 1965, [ self.adventure, self.fantasy, self.sci_fi ], [ self.hebert ])
        self.solitude = Example.Book(self.big, "Cien años de soledad", 1967, [ self.fantasy, self.novel ], [ self.marquez ])
        self.hitchhiker = Example.Book(self.big, "The Hitchhiker's Guide to the Galaxy", 1979, [ self.adventure, self.comedy, self.sci_fi ], [ self.adams ])
        self.restaurant = Example.Book(self.big, "The Restaurant at the End of the Universe", 1980, [ self.adventure, self.comedy, self.sci_fi ], [ self.adams ])
        self.everything = Example.Book(self.big, "Life, the Universe and Everything", 1982, [ self.adventure, self.comedy, self.sci_fi ], [ self.adams ])
        self.thanks = Example.Book(self.big, "So Long, and Thanks for All the Fish", 1984, [ self.adventure, self.comedy, self.sci_fi ], [ self.adams ])
        self.harmless = Example.Book(self.big, "Mostly Harmless", 1892, [ self.adventure, self.comedy, self.sci_fi ], [ self.adams ])
        self.the_code = Example.Book(self.big, "The Da Vinci Code", 2003, [ self.adventure, self.novel ], [ self.brown ])
        self.fakebook = Example.Book(self.big, "Fakebook", 2005, [ self.adventure, self.comedy, self.novel ], [ self.homer, self.brown ])

    def execute(self):
        # Insert
        for p in [ self.big, self.modest, self.small ]:
            self._insertPublisher(p)
        for g in [ self.fiction, self.adventure, self.comedy, self.fantasy, self.novel, self.satire, self.sci_fi ]:
            self._insertGenre(g)
        for a in [ self.adams, self.asturias, self.brown, self.dumas, self.cervantes, self.marquez, self.hebert, self.homer, self.orwell, self.swift ]:
            self._insertAuthor(a)
        for b in [ self.illiad, self.odyssey, self.quixote, self.gulliver, self.le_comte, self.les_trois, self.animal, self.ninety, self.maize, self.solitude,
                  self.hitchhiker, self.restaurant, self.everything, self.thanks, self.harmless, self.the_code, self.fakebook ]:
            self._insertBook(b)
        # Print
        self.print()

    def print(self):
        # self.db.print()
        # Publishers
        entries = self._selectPublishers()
        count = len(entries)
        Log.list(f"Publishers({count})", 1)
        for p in entries:
            p.print(2)
        # Genres
        entries = self._selectGenres()
        count = len(entries)
        Log.list(f"Genres({count})", 1)
        for g in entries:
            g.print(2)
        # Authors
        entries = self._selectAuthors()
        count = len(entries)
        Log.list(f"Authors({count})", 1)
        for a in entries:
            a.print(2)
        # Books
        entries = self._selectBooks()
        count = len(entries)
        Log.list(f"Books({count})", 1)
        for b in entries:
            b.print(2)

    @abstractmethod
    def _insertPublisher(self, p):
        pass

    @abstractmethod
    def _selectPublishers(self):
        pass

    @abstractmethod
    def _selectPublisher(self, x):
        pass

    @abstractmethod
    def _insertGenre(self, g):
        pass

    @abstractmethod
    def _selectGenres(self):
        pass

    @abstractmethod
    def _selectGenre(self, x):
        pass

    @abstractmethod
    def _insertAuthor(self, a):
        pass

    @abstractmethod
    def _selectAuthors(self):
        pass

    @abstractmethod
    def _selectAuthor(self, x):
        pass

    @abstractmethod
    def _insertBook(self, b):
        pass

    @abstractmethod
    def _selectBooks(self):
        pass

    @abstractmethod
    def _selectBook(self, x):
        pass


class RawExample(Example):

    def __init__(self, schema, path, reset):
        super().__init__()
        self.db = _sqlite.Database(schema, path)
        self.db.open(reset)

    def _insertPublisher(self, p):
        p.id = self.db.exec("INSERT INTO publisher(parent_id, name) VALUES(?, ?)", [ p.parent.id if p.parent else None,  p.name ])

    def _selectPublishers(self):
        all = []
        for row in self.db.all(f"SELECT `id` FROM `publisher`"):
            all.append(self._selectPublisher(row[0]))
        return all

    def _selectPublisher(self, x):
        if isinstance(x, int):
            row = self.db.one(f"SELECT * FROM `publisher` WHERE `id`=?", [ int(x) ])
        else: Error.invalid("publisher", x)
        return Example.Publisher(id=row[0], parent=row[1], name=row[2]) if row else None

    def _insertGenre(self, g):
        g.id = self.db.exec(f"INSERT INTO genre(name) VALUES(?)", [ g.name ])
        if g.parent:
            self.db.exec("REPLACE INTO subgenre(parent_id, child_id) VALUES(?, ?)", [ g.parent.id, g.id ])

    def _selectGenres(self):
        all = []
        for row in self.db.all(f"SELECT `id` FROM `genre`"):
            all.append(self._selectGenre(row[0], hierarchy=True))
        return all

    def _selectGenre(self, x, hierarchy=False):
        if isinstance(x, int):
            row = self.db.one(f"SELECT * FROM `genre` WHERE `id`=?", [ int(x) ])
        else: Error.invalid("genre", x)
        genre = Example.Genre(id=row[0], name=row[1]) if row else None
        if hierarchy:
            # Parent
            row = self.db.one(f"SELECT `parent_id` FROM `subgenre` WHERE `child_id`=?", [ int(genre) ])
            genre.parent = self._selectGenre(row[0]) if row else None
            # Children
            for row in self.db.all(f"SELECT `child_id` FROM `subgenre` WHERE `parent_id`=?", [ int(genre) ]):
                genre.children.append(self._selectGenre(row[0]))
        return genre

    def _insertAuthor(self, a):
        a.id = self.db.exec("INSERT INTO author(name) VALUES(?)", [ a.name ])

    def _selectAuthors(self):
        all = []
        for row in self.db.all(f"SELECT `id` FROM `author`"):
            all.append(self._selectAuthor(row[0]))
        return all

    def _selectAuthor(self, x):
        if isinstance(x, int) or isinstance(x, _basic.AuthorRef):
            row = self.db.one(f"SELECT * FROM `author` WHERE `id`=?", [ int(x) ])
        else: Error.invalid("author", x)
        return Example.Author(id=row[0], name=row[1]) if row else None

    def _insertBook(self, b):
        b.id = self.db.exec("INSERT INTO book(publisher_id, title, year) VALUES(?, ?, ?)", [ b.publisher.id, b.title, b.year ])
        for g in b.genres:
            self.db.exec("REPLACE INTO book_genre VALUES(?, ?)", [ b.id, g.id ])
        for i in range(0, len(b.authors)):
            self.db.exec("REPLACE INTO book_author VALUES(?, ?, ?)", [ b.id, b.authors[i].id, i+1 ])

    def _selectBooks(self):
        all = []
        for row in self.db.all(f"SELECT `id` FROM `book`"):
            all.append(self._selectBook(row[0]))
        return all

    def _selectBook(self, x):
        if isinstance(x, int):
            row = self.db.one(f"SELECT * FROM `book` WHERE `id`=?", [ x ])
        else: Error.invalid("book", x)
        book = Example.Book(id=row[0], publisher=row[1], title=row[2], year=row[3])
        for bg in self.db.all(f"SELECT * FROM `book_genre` bg WHERE bg.`book_id`=?", [ book.id ]):
            book.genres.append(self._selectGenre(bg[1]))
        for ba in self.db.all(f"SELECT * FROM `book_author` ba WHERE ba.`book_id`=?", [ book.id ]):
            book.genres.append(self._selectAuthor(ba[1]))
        return book


class DatasetExample(Example):

    def __init__(self, schema, path, reset):
        super().__init__()
        self.ds = _basic.Dataset(schema, path)
        self.ds.open(reset)

    def _insertPublisher(self, p):
        pid = p.parent.id if p.parent else None
        p.id = int(self.ds.publishers.add(_basic.Publisher(pid, p.name)))

    def _selectPublishers(self):
        all = []
        for r in self.ds.publishers.refs():
            all.append(self._selectPublisher(r))
        return all

    def _selectPublisher(self, x):
        if isinstance(x, int) or isinstance(x, _basic.PublisherRef):
            p = self.ds.publishers.one(x)
        else: Error.invalid("publisher", x)
        return Example.Publisher(id=p.id, parent=p.parent_id, name=p.name) if p else None

    def _insertGenre(self, g):
        g.id = int(self.ds.genres.add(_basic.Genre(g.name)))
        if g.parent and g.parent.id:
            self.ds.genres.add(_basic.SubgenreRef(g.parent.id, g.id))

    def _selectGenres(self):
        all = []
        for r in self.ds.genres.refs():
            all.append(self._selectGenre(r, hierarchy=True))
        return all

    def _selectGenre(self, x, hierarchy=False):
        if isinstance(x, int) or isinstance(x, _basic.GenreRef):
            g = self.ds.genres.one(x)
        else: Error.invalid("genre", x)
        genre = Example.Genre(id=g.id, name=g.name) if g else None
        if hierarchy:
            # Parent
            gr = self.ds.genres.ref(_basic.ChildGenreRef(g))
            genre.parent = self._selectGenre(gr) if gr else None
            # Children
            for gr in self.ds.genres.refs(_basic.ParentGenreRef(g)):
                genre.children.append(self._selectGenre(gr))
        return genre

    def _insertAuthor(self, a):
        a.id = int(self.ds.authors.add(_basic.Author(a.name)))

    def _selectAuthors(self):
        all = []
        for r in self.ds.authors.refs():
            all.append(self._selectAuthor(r))
        return all

    def _selectAuthor(self, x):
        if isinstance(x, int) or isinstance(x, _basic.AuthorRef):
            a = self.ds.authors.one(x)
        else: Error.invalid("author", x)
        return Example.Author(id=a.id, name=a.name) if a else None

    def _insertBook(self, b):
        b.id = int(self.ds.books.add(_basic.Book(b.publisher.id, b.title, b.year)))
        for g in b.genres:
            self.ds.genres.add(_basic.BookGenreRef(int(b), int(g)))
        for i in range(0, len(b.authors)):
            self.ds.authors.add(_basic.BookAuthor(int(b), int(b.authors[i]), i+1))

    def _selectBooks(self):
        all = []
        for r in self.ds.books.refs():
            all.append(self._selectBook(r))
        return all

    def _selectBook(self, x):
        if isinstance(x, int) or isinstance(x, _basic.BookRef):
            b = self.ds.books.one(x)
        else: Error.invalid("book", x)
        book = Example.Book(id=b.id, publisher=b.publisher_id, title=b.title, year=b.year) if b else None
        for gr in self.ds.genres.refs(b):
            book.genres.append(self._selectGenre(gr))
        for ar in self.ds.authors.refs(b):
            book.genres.append(self._selectAuthor(ar))
        return book


class ApiExample(Example):

    def __init__(self, schema, path, reset):
        super().__init__()
        self.api = _api.Engine(schema, path, reset)

    def _insertPublisher(self, p):
        # Parent
        pp = self.api.publishers.one(p.parent.id) if p.parent else None
		# Insert
        p.id = int(self.api.publishers.add(_api.Publisher(pp, p.name)))

    def _selectPublishers(self):
        all = []
        for r in self.api.publishers.refs():
            all.append(self._selectPublisher(r))
        return all

    def _selectPublisher(self, x):
        if isinstance(x, int) or isinstance(x, _api.PublisherRef):
            p = self.api.publishers.one(x)
        else: Error.invalid("publisher", x)
        return Example.Publisher(id=p.id, parent=p.parent_id, name=p.name) if p else None

    def _insertGenre(self, g):
        g.id = int(self.api.genres.add(_api.Genre(g.name)))
        if g.parent and g.parent.id:
            self.api.genres.add(_api.SubgenreRef(g.parent.id, g.id))

    def _selectGenres(self):
        all = []
        for r in self.api.genres.refs():
            all.append(self._selectGenre(r, hierarchy=True))
        return all

    def _selectGenre(self, x, hierarchy=False):
        if isinstance(x, int) or isinstance(x, _api.GenreRef):
            g = self.api.genres.one(x)
        else: Error.invalid("genre", x)
        genre = Example.Genre(id=g.id, name=g.name) if g else None
        if hierarchy:
            # Parent
            gr = self.api.genres.ref(_api.ChildGenreRef(g))
            genre.parent = self._selectGenre(gr) if gr else None
            # Children
            for gr in self.api.genres.refs(_api.ParentGenreRef(g)):
                genre.children.append(self._selectGenre(gr))
        return genre

    def _insertAuthor(self, a):
        a.id = int(self.api.authors.add(_api.Author(a.name)))

    def _selectAuthors(self):
        all = []
        for r in self.api.authors.refs():
            all.append(self._selectAuthor(r))
        return all

    def _selectAuthor(self, x):
        if isinstance(x, int) or isinstance(x, _api.AuthorRef):
            a = self.api.authors.one(x)
        else: Error.invalid("author", x)
        return Example.Author(id=a.id, name=a.name) if a else None

    def _insertBook(self, b):
        b.id = int(self.api.books.add(_api.Book(b.publisher.id, b.title, b.year)))
        for g in b.genres:
            self.api.genres.add(_api.BookGenreRef(int(b), int(g)))
        for i in range(0, len(b.authors)):
            self.api.authors.add(_api.BookAuthor(int(b), int(b.authors[i]), i+1))

    def _selectBooks(self):
        all = []
        for r in self.api.books.refs():
            all.append(self._selectBook(r))
        return all

    def _selectBook(self, x):
        if isinstance(x, int) or isinstance(x, _api.BookRef):
            b = self.api.books.one(x)
        else: Error.invalid("book", x)
        book = Example.Book(id=b.id, publisher=b.publisher_id, title=b.title, year=b.year) if b else None
        for gr in self.api.genres.refs(b):
            book.genres.append(self._selectGenre(gr))
        for ar in self.api.authors.refs(b):
            book.genres.append(self._selectAuthor(ar))
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
        Log.list("\nRAW")
        e = RawExample(schema, path, reset)
        e.execute()
        # Basic
        Log.list("\nBASIC")
        e = DatasetExample(schema, path, reset)
        e.execute()
        # API
        Log.list("\nAPI")
        e = ApiExample(schema, path, reset)
        e.execute()


if __name__ == "__main__":
    app = DatasetApp()
    app.run()
