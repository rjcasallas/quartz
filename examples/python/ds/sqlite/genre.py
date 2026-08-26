from ds.model._data import *
from quartz.gen.data import Reference
from quartz.gen.sqlite import Manager
from quartz.error import Error


class GenreSqliteManager(Dataset.Genres, Manager):

    def __init__(self, ds, db):
        Dataset.Genres.__init__(self, ds)
        Manager.__init__(self, 'genre', db)


    def add(self, x:Genre):
        g = Genre.valid(x)
        if x.id is None:
            x.id = self.db.exec('@genre/insert', [ x.name ])
        else:
            self.db.exec('@genre/insert_id', [ x.id, x.name ])
        return g


    def update(self, x):
        g = Genre.valid(x)
        self.db.exec('@genre/update', [ x.name, x.id ])
        return g


    def remove(self, x):
        if isinstance(x, int) or isinstance(x, GenreRef):
            return self.db.exec('@genre/delete_id', [ int(x) ])
        if isinstance(x, str):
            return self.db.exec('@genre/delete_name', [ x ])
        Error.missing(f"remove 'genre': {type(x)}")


    def link(self, x, y):
        if not (isinstance(x, int) or isinstance(x, GenreRef)):
            Error.invalid("genre link base", x)
        if not isinstance(x, Reference):
            Error.invalid("genre link target", x)
        return self._link(int(x), y)

    def unlink(self, x, y):
        if not (isinstance(x, int) or isinstance(x, GenreRef)):
            Error.invalid("genre link base", x)
        if not isinstance(x, Reference):
            Error.invalid("genre link target", x)
        return self._unlink(int(x), y)


    def _reference(self, x):
        return GenreRef(x[0])


    def _instance(self, x):
        return Genre(id=x[0], name=x[1])


    def _link(self, base_id, x):
        # "genre_book" genre.id → book.id
        if isinstance(x, BookRef):
            return self.db.exec('@genre/insert_book', [ base_id, int(x) ])
        # "genre_parent" genre.id → genre.id
        if isinstance(x, GenreRef):
            return self.db.exec('@genre/insert_genre', [ base_id, int(x) ])
        # "genre_child" genre.id → genre.id
        if isinstance(x, GenreRef):
            return self.db.exec('@genre/insert_genre', [ base_id, int(x) ])
        Error.invalid("genre link target", x)


    def _unlink(self, base_id, x):
        # "genre_book" genre.id → book.id
        if isinstance(x, BookRef):
            return self.db.exec('@genre/delete_book', [ base_id, int(x) ])
        # "genre_parent" genre.id → genre.id
        if isinstance(x, GenreRef):
            return self.db.exec('@genre/delete_genre', [ base_id, int(x) ])
        # "genre_child" genre.id → genre.id
        if isinstance(x, GenreRef):
            return self.db.exec('@genre/delete_genre', [ base_id, int(x) ])
        Error.invalid("genre link target", x)


    def _ref(self, x = None) -> int:
        if x is None:
            sql = self.db.sql('@genre/select_ref', 'LIMIT 1')
            return self.db.one(sql)
        if isinstance(x, int) or isinstance(x, GenreRef):
            return self.db.one('@genre/select_ref_by_pk', [ int(x) ])
        if isinstance(x, str):
            return self.db.one('@genre/select_ref_by_name', [ x ])
        Error.missing(f"select 'genre' ref: {type(x)}")


    def _refs(self, x = None) -> list[int]:
        if x is None:
            return self.db.all('@genre/select_ref')
        Error.missing(f"select 'genre' refs: {type(x)}")


    def _one(self, x = None) -> Genre:
        if x is None:
            sql = self.db.sql('@genre/select_all', 'LIMIT 1')
            return self.db.one(sql)
        if isinstance(x, int) or isinstance(x, GenreRef):
            return self.db.one('@genre/select_all_by_pk', [ int(x) ])
        if isinstance(x, str):
            return self.db.one('@genre/select_all_by_name', [ x ])
        Error.missing(f"select 'genre' get: {type(x)}")


    def _all(self, x = None) -> list[Genre]:
        if x is None:
            return self.db.all('@genre/select_all')
        Error.missing(f"select 'genre' all: {type(x)}")