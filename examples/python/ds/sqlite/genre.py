from ds.core import *
from ds.model._dataset import Dataset
from quartz.gen.sqlite import Table


class GenreManager(Dataset.Genres):

    def __init__(self, ds, db):
        super().__init__(ds)
        self._table = Table("genre", db, GenreFilter())

    def add(self, x, debug=False):
        if isinstance(x, Genre) and (x.id is None):
            x.id = self._table.insert(x, debug)
        else:
            self._table.insert(x, debug)
        return x

    def set(self, x, debug=False):
        # "genre_book" book.id → genre.id
        if isinstance(x, BookGenreRef):
            if (x.book_id is None) or (x.genre_id is None):
                return self._table.delete(x, debug)
        # "child_genre" genre.id → genre.id (recursive)
        if isinstance(x, SubgenreRef):
            if (x.parent_id is None) or (x.child_id is None):
                return self._table.delete(x, debug)
        # Fields
        if isinstance(x, tuple) and isinstance(x[0], Genre) and isinstance(x[1], Fields):
            o, f = x
            if f == Fields.Name:
                x = Table.Update("genre", [ "name", "id" ], [ o.name, o.id ], 1)
        return self._table.update(x, debug)

    def get(self, x:Genre, field:Fields=None, debug=False):
        if field is None:
            row = self._table.select(Table.Select("genre", [ "name", "id" ], [ x.id ], 1), one=True, debug=debug)
            x.name = row[0]
        elif field == Fields.Name:
            x.name = self._table.select(Table.Select("genre", [ "name", "id" ], [ x.id ], 1), one=True, debug=debug)[0]
    def remove(self, x, debug=False):
        return self._table.delete(x, debug)

    def has(self, x, debug=False) -> bool:
        return self._table.contains(x, debug)

    def clear(self, debug=False):
        self._table.deleteAll(debug)

    def find(self, x=None, tag:str="all", builder=None, one=False, order=None, debug=False) -> list[object]:
        return self._table.select(x, tag, builder, one, order, debug)

    def ref(self, x=None, order=None, debug=False) -> GenreRef:
        return self._table.select(x, "ref", self._reference, True, order, debug)

    def refs(self, x=None, order=None, debug=False) -> list[GenreRef]:
        return self._table.select(x, "ref", self._reference, False, order, debug)

    def one(self, x=None, order=None, debug=False) -> Genre:
        return self._table.select(x, "all", self._create, True, order, debug)

    def all(self, x=None, order=None, debug=False) -> list[Genre]:
        return self._table.select(x, "all", self._create, False, order, debug)

    def _reference(self, x):
        return GenreRef(id=x[0])

    def _create(self, x):
        return Genre(id=x[0], name=x[1])


class GenreFilter(Table.Filter):

    def insert(self, x):
        # genre
        if isinstance(x, Genre):
            return Table.Insert("genre", False, [ x.id, x.name ])
        # "genre_book" book.id → genre.id
        if isinstance(x, BookGenreRef):
            return Table.Insert("book_genre", True, [ x.book_id, x.genre_id ])
        # "child_genre" genre.id → genre.id (recursive)
        if isinstance(x, SubgenreRef):
            return Table.Insert("subgenre", True, [ x.parent_id, x.child_id ])

    def update(self, x):
        # genre
        if isinstance(x, Genre):
            return Table.Update("genre", False, [ x.name, x.id ])
        # "genre_book" book.id → genre.id
        if isinstance(x, BookGenreRef):
            return Table.Update("book_genre", True, [x.book_id, x.genre_id ])
        # "child_genre" genre.id → genre.id (recursive)
        if isinstance(x, SubgenreRef):
            return Table.Update("subgenre", True, [x.parent_id, x.child_id ])

    def delete(self, x):
        # "genre_book" book.id → genre.id
        if isinstance(x, BookGenreRef):
            return Table.Delete("book_genre", [ "book_id", "genre_id" ], [ x.book_id, x.genre_id ])
        # "child_genre" genre.id → genre.id (recursive)
        if isinstance(x, SubgenreRef):
            return Table.Delete("subgenre", True, [x.parent_id, x.child_id ])
        # pk
        if isinstance(x, int) or isinstance(x, GenreRef):
            return Table.Delete("genre", "pk", [ int(x) ])
        # name
        if isinstance(x, str):
            return Table.Delete("genre", "name", [ x ])

    def select(self, x=None) -> tuple:
        # "genre_book" book.id → genre.id 
        if isinstance(x, BookRef):
            return Table.Select("genre", "book", [ int(x) ])
        # "child_genre" genre.id → genre.id (recursive)
        if isinstance(x, ChildGenreRef):
            return Table.Select("genre", "child", [ int(x) ])
        # "parent_genre" genre.id → genre.id (recursive)
        if isinstance(x, ParentGenreRef):
            return Table.Select("genre", "parent", [ int(x) ])
        # pk
        if isinstance(x, int) or isinstance(x, GenreRef):
            return Table.Select("genre", "pk", [ int(x) ])
        # name (lookup)
        if isinstance(x, str):
            return Table.Select("genre", "name", [ x ])
        # all
        if x is None:
            return Table.Select("genre")

