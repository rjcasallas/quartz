from ds.model._dataset import *
import quartz.gen.sqlite as _sqlite
from quartz.error import Error


class GenreManager(Dataset.Genres, _sqlite.Table):

    def __init__(self, ds, db):
        Dataset.Genres.__init__(self, ds)
        _sqlite.Table.__init__(self, "genre", db)

    def add(self, x: Genre):
        return self._add(x)

    def remove(self, x):
        return self._remove(x)

    def has(self, x) -> bool:
        return self.contains(x)

    def clear(self):
        self.deleteAll()

    def update(self, x: Genre):
        Genre.valid(x)
        _sqlite.Table.update(self, [ x.name, x.id ])
        return x

    def ref(self, x = None) -> GenreRef:
        return self.selectRef(x)

    def one(self, x = None) -> Genre:
        return self.selectOne(x)

    def refs(self, x = None) -> list[GenreRef]:
        return self.selectRefs(x)

    def all(self, x = None) -> list[Genre]:
        return self.selectAll(x)

    def _reference(self, x):
        return GenreRef(id=x[0])

    def _instance(self, x):
        return Genre(id=x[0], name=x[1])

    def _add(self, x):
        # genre
        if isinstance(x, Genre):
            if x.id is None:
                x.id = self.insert([ x.name ], auto=True)
            else:
                self.insert([ x.id, x.name ])
            return x
        # "genre_book" book.id → genre.id
        if isinstance(x, BookGenreRef):
            return self.db.exec("@book_genre/replace", [ x.book_id, x.genre_id ])
        # "child_genre" genre.id → genre.id (self-referencing)
        if isinstance(x, SubgenreRef):
            return self.db.exec("@subgenre/replace", [ x.parent_id, x.child_id ])
        return Error.invalid("genre", x)

    def _remove(self, x):
        # genre
        if isinstance(x, GenreRef):
            return self.db.exec("@genre/delete_pk", [ int(x) ])
        if isinstance(x, str):
            return self.db.exec("@genre/delete_name", [ x ])
        # "genre_book" book.id → genre.id
        if isinstance(x, BookGenreRef):
            return self.db.exec("@book_genre/delete_pk", [ x.book_id, x.genre_id ])
        # "child_genre" genre.id → genre.id (self-referencing)
        if isinstance(x, SubgenreRef):
            return self.db.exec("@subgenre/delete_pk", [ x.parent_id, x.child_id ])

        return self.delete(x)

    def _ref(self, x = None) -> GenreRef:
        # "genre_book" book.id → genre.id 
        if isinstance(x, BookRef):
            return self.db.one("@genre/select_ref_by_book", [ int(x) ])
        # "child_genre" genre.id → genre.id (self-referencing)
        if isinstance(x, ChildGenreRef):
            return self.db.one("@genre/select_ref_by_child", [ int(x) ])
        # "parent_genre" genre.id → genre.id (self-referencing)
        if isinstance(x, ParentGenreRef):
            return self.db.one("@genre/select_ref_by_parent", [ int(x) ])
        # pk
        if isinstance(x, int) or isinstance(x, GenreRef):
            return self.db.one("@genre/select_ref_by_pk", [ int(x) ])
        # name
        if isinstance(x, str):
            return self.db.one("@genre/select_ref_by_name", [ x ])
        return super()._ref(x)

    def _one(self, x = None) -> Genre:
        # "genre_book" book.id → genre.id 
        if isinstance(x, BookRef):
            return self.db.one("@genre/select_all_by_book", [ int(x) ])
        # "child_genre" genre.id → genre.id (self-referencing)
        if isinstance(x, ChildGenreRef):
            return self.db.one("@genre/select_all_by_child", [ int(x) ])
        # "parent_genre" genre.id → genre.id (self-referencing)
        if isinstance(x, ParentGenreRef):
            return self.db.one("@genre/select_all_by_parent", [ int(x) ])
        # pk
        if isinstance(x, int) or isinstance(x, GenreRef):
            return self.db.one("@genre/select_all_by_pk", [ int(x) ])
        # name
        if isinstance(x, str):
            return self.db.one("@genre/select_all_by_name", [ x ])
        return super()._one(x)

    def _refs(self, x = None) -> list[GenreRef]:
        # "genre_book" book.id → genre.id 
        if isinstance(x, BookRef):
            return self.db.all("@genre/select_ref_by_book", [ int(x) ])
        # "child_genre" genre.id → genre.id (self-referencing)
        if isinstance(x, ChildGenreRef):
            return self.db.all("@genre/select_ref_by_child", [ int(x) ])
        # "parent_genre" genre.id → genre.id (self-referencing)
        if isinstance(x, ParentGenreRef):
            return self.db.all("@genre/select_ref_by_parent", [ int(x) ])
        return super()._refs(x)

    def _all(self, x = None) -> list[Genre]:
        # "genre_book" book.id → genre.id 
        if isinstance(x, BookRef):
            return self.db.all("@genre/select_all_by_book", [ int(x) ])
        # "child_genre" genre.id → genre.id (self-referencing)
        if isinstance(x, ChildGenreRef):
            return self.db.all("@genre/select_all_by_child", [ int(x) ])
        # "parent_genre" genre.id → genre.id (self-referencing)
        if isinstance(x, ParentGenreRef):
            return self.db.all("@genre/select_all_by_parent", [ int(x) ])
        return super()._all(x)