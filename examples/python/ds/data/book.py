from ds.base import *
from ds.model.book import *
from ds.model._dataset import Dataset
from quartz.data.table import Table


class BookData(Dataset.Books):

    def __init__(self, db):
        self._table = BookTable("book", db)

    def add(self, x, debug:bool=False):
        if isinstance(x, Book) and (x.id is None):
            x.id = self._table.insert(x, debug)
            return x
        elif self._replace(x, debug):
            return x
        self._table.insert(x, debug)
        return x

    def remove(self, x, debug:bool=False):
        return self._table.delete(x, debug)

    def push(self, x, field:Fields=None, debug:bool=False):
        if self._replace(x, True, debug):
            return x
        if isinstance(x, Book) and isinstance(field, Fields):
            match field:
                case Fields.Publisher:
                    x = Table.Info("book", [ ("id", x.id), ("publisher_id", x.publisher_id) ], 1)
                case Fields.Title:
                    x = Table.Info("book", [ ("id", x.id), ("title", x.title) ], 1)
                case Fields.Year:
                    x = Table.Info("book", [ ("id", x.id), ("year", x.year) ], 1)
                case _:
                    x = None
        return self._table.update(x, debug) if (x is not None) else None

    def pull(self, x:Book, field:Fields=None, debug:bool=False):
        match field:
            case None:
                row = self._table.one(Table.Info("book", [ ("id", x.id), ("publisher_id", None), ("title", None), ("year", None) ], 1), debug=debug)
                if (isinstance(row, tuple) or isinstance(row, list)) and (len(row) > 0):
                    x.publisher_id = row[0]
                    x.title = row[1]
                    x.year = row[2]
            case Fields.Publisher:
                row = self._table.one(Table.Info("book", [ ("id", x.id), ("publisher_id", None) ], 1), debug=debug)
                if (isinstance(row, tuple) or isinstance(row, list)) and (len(row) > 0):
                    x.publisher_id = row[0]
            case Fields.Title:
                row = self._table.one(Table.Info("book", [ ("id", x.id), ("title", None) ], 1), debug=debug)
                if (isinstance(row, tuple) or isinstance(row, list)) and (len(row) > 0):
                    x.title = row[0]
            case Fields.Year:
                row = self._table.one(Table.Info("book", [ ("id", x.id), ("year", None) ], 1), debug=debug)
                if (isinstance(row, tuple) or isinstance(row, list)) and (len(row) > 0):
                    x.year = row[0]
        return x

    def has(self, x, debug:bool=False) -> bool:
        return self.ref(x, debug) is not None

    def clear(self, debug:bool=False):
        self._table.deleteAll(debug)

    def refb(self, x=None, order:list[str]=None, limit:str=None, debug:bool=False):
        return self.begin(x, 'pk', order, limit, debug)

    def refn(self, cursor) -> Reference:
        return self.next(cursor, self._reference)

    def ref(self, x=None, order:list[str]=None, limit:str=None, debug:bool=False):
        return self.one(x, self._reference, 'pk', order, limit, debug)

    def refs(self, x=None, order:list[str]=None, limit:str=None, debug:bool=False):
        return self.all(x, self._reference, 'pk', order, limit, debug)

    def begin(self, x=None, columns:str='full', order:list[str]=None, limit:str=None, debug:bool=False):
        return self._table.begin(x, columns, order, limit, debug)

    def next(self, cursor, builder=None):
        fn = self._create if (builder is None) else builder
        return self._table.next(cursor, fn)

    def one(self, x=None, builder=None, columns:str='full', order:list[str]=None, limit:str=None, debug:bool=False):
        fn = self._create if (builder is None) else builder
        return self._table.one(x, fn, columns, order, limit, debug)

    def all(self, x=None, builder=None, columns:str='full', order:list[str]=None, limit:str=None, debug:bool=False):
        fn = self._create if (builder is None) else builder
        return self._table.select(x, fn, columns, order, limit, debug)

    def _replace(self, x, allow_delete=False, debug:bool=False) -> bool:
        # "book_genre" genre.id → book.id
        if isinstance(x, BookGenreRef):
            if x.book_id and x.genre_id:
                return self._table.update(x, debug)
            elif allow_delete:
                return self._table.delete(x, debug)
            else:
                Error.invalid(f'"book_genre" replace', x)
        return False

    def _reference(self, x):
        return BookRef(id=x[0])

    def _create(self, x):
        return Book(id=x[0], publisher_id=x[1], title=x[2], year=x[3])


class BookTable(Table):

    def _insert(self, x):
        # book
        if isinstance(x, Book):
            return Table.Info("book", [ x.id, x.publisher_id, x.title, x.year ], 1, tag=("insert" if (x.id is None) else "insert_id"))

    def _update(self, x):
        # book
        if isinstance(x, Book):
            return Table.Info("book", [ x.id, x.publisher_id, x.title, x.year ], 1, tag="update")
        # "book_genre" genre.id → book.id
        if isinstance(x, BookGenreRef):
            return Table.Info("book_genre", [ x.book_id, x.genre_id ], tag="replace")

    def _delete(self, x):
        # "book_genre" genre.id → book.id
        if isinstance(x, BookGenreRef):
            return Table.Info("book_genre", [ ("book_id", x.book_id), ("genre_id", x.genre_id) ])
        # pk
        if isinstance(x, int) or isinstance(x, BookRef):
            return Table.Info("book", [ int(x) ], tag="pk")
        # title
        if isinstance(x, str):
            return Table.Info("book", [ x ], tag="title")

    def _select(self, x=None) -> tuple:
        # "book_author" author.id → book.id
        if isinstance(x, AuthorRef):
            return Table.Info("book", [ int(x) ], tag="author")
        # "book_genre" genre.id → book.id
        if isinstance(x, GenreRef):
            return Table.Info("book", [ int(x) ], tag="genre")
        # pk
        if isinstance(x, int) or isinstance(x, BookRef):
            return Table.Info("book", [ int(x) ], tag="pk")
        # title (lookup)
        if isinstance(x, str):
            return Table.Info("book", [ x ], tag="title")
        # publisher (foreign)
        if isinstance(x, PublisherRef):
            return Table.Info("book", [ int(x) ], tag="publisher")
        # all
        if x is None:
            return Table.Info("book", tag="all")
        # year (custom)
        if isinstance(x, YearRef):
            return Table.Info("book", [ x.start, x.end ], tag="year")
