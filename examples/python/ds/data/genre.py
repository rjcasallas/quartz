from ds.base import *
from ds.model.genre import *
from ds.model._dataset import Dataset
from quartz.data.table import Table


class GenreData(Dataset.Genres):

    def __init__(self, db):
        self._table = GenreTable("genre", db)

    def add(self, x, debug:bool=False):
        if isinstance(x, Genre) and (x.id is None):
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
        if isinstance(x, Genre) and isinstance(field, Fields):
            match field:
                case Fields.Name:
                    x = Table.Info("genre", [ ("id", x.id), ("name", x.name) ], 1)
                case _:
                    x = None
        return self._table.update(x, debug) if (x is not None) else None

    def pull(self, x:Genre, field:Fields=None, debug:bool=False):
        match field:
            case None:
                row = self._table.one(Table.Info("genre", [ ("id", x.id), ("name", None) ], 1), debug=debug)
                if (isinstance(row, tuple) or isinstance(row, list)) and (len(row) > 0):
                    x.name = row[0]
            case Fields.Name:
                row = self._table.one(Table.Info("genre", [ ("id", x.id), ("name", None) ], 1), debug=debug)
                if (isinstance(row, tuple) or isinstance(row, list)) and (len(row) > 0):
                    x.name = row[0]
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
        # "genre_book" book.id → genre.id
        if isinstance(x, BookGenreRef):
            if x.book_id and x.genre_id:
                return self._table.update(x, debug)
            elif allow_delete:
                return self._table.delete(x, debug)
            else:
                Error.invalid(f'"book_genre" replace', x)
        # "child_genre" genre.id → genre.id (recursive)
        if isinstance(x, SubgenreRef):
            if x.parent_id and x.child_id:
                return self._table.update(x, debug)
            elif allow_delete:
                return self._table.delete(x, debug)
            else:
                Error.invalid(f'"subgenre" replace', x)
        return False

    def _reference(self, x):
        return GenreRef(id=x[0])

    def _create(self, x):
        return Genre(id=x[0], name=x[1])


class GenreTable(Table):

    def _insert(self, x):
        # genre
        if isinstance(x, Genre):
            return Table.Info("genre", [ x.id, x.name ], 1, tag=("insert" if (x.id is None) else "insert_id"))

    def _update(self, x):
        # genre
        if isinstance(x, Genre):
            return Table.Info("genre", [ x.id, x.name ], 1, tag="update")
        # "genre_book" book.id → genre.id
        if isinstance(x, BookGenreRef):
            return Table.Info("book_genre", [ x.book_id, x.genre_id ], tag="replace")
        # "child_genre" genre.id → genre.id (recursive)
        if isinstance(x, SubgenreRef):
            return Table.Info("subgenre", [ x.parent_id, x.child_id ], tag="replace")

    def _delete(self, x):
        # "genre_book" book.id → genre.id
        if isinstance(x, BookGenreRef):
            return Table.Info("book_genre", [ ("book_id", x.book_id), ("genre_id", x.genre_id) ])
        # "child_genre" genre.id → genre.id (recursive)
        if isinstance(x, SubgenreRef):
            return Table.Info("subgenre", [ ("parent_id", x.parent_id), ("child_id", x.child_id) ])
        # pk
        if isinstance(x, int) or isinstance(x, GenreRef):
            return Table.Info("genre", [ int(x) ], tag="pk")
        # name
        if isinstance(x, str):
            return Table.Info("genre", [ x ], tag="name")

    def _select(self, x=None) -> tuple:
        # "genre_book" book.id → genre.id
        if isinstance(x, BookRef):
            return Table.Info("genre", [ int(x) ], tag="book")
        # "child_genre" genre.id → genre.id (recursive)
        if isinstance(x, ChildGenreRef):
            return Table.Info("genre", [ int(x) ], tag="child")
        # "parent_genre" genre.id → genre.id (recursive)
        if isinstance(x, ParentGenreRef):
            return Table.Info("genre", [ int(x) ], tag="parent")
        # pk
        if isinstance(x, int) or isinstance(x, GenreRef):
            return Table.Info("genre", [ int(x) ], tag="pk")
        # name (lookup)
        if isinstance(x, str):
            return Table.Info("genre", [ x ], tag="name")
        # all
        if x is None:
            return Table.Info("genre", tag="all")

