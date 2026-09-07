from ds.base import *
from ds.model.book_author import *
from ds.model._dataset import Dataset
from quartz.data.table import Table


class BookAuthorData(Dataset.BookAuthors):

    def __init__(self, db):
        self._table = BookAuthorTable("book_author", db)

    def add(self, x, debug:bool=False):
        self._table.insert(x, debug)
        return x

    def remove(self, x, debug:bool=False):
        return self._table.delete(x, debug)

    def push(self, x, field:Fields=None, debug:bool=False):
        if isinstance(x, BookAuthor) and isinstance(field, Fields):
            match field:
                case Fields.Rank:
                    x = Table.Info("book_author", [ ("book_id", x.book_id), ("author_id", x.author_id), ("rank", x.rank) ], 2)
                case _:
                    x = None
        return self._table.update(x, debug) if (x is not None) else None

    def pull(self, x:BookAuthor, field:Fields=None, debug:bool=False):
        match field:
            case None:
                row = self._table.one(Table.Info("book_author", [ ("book_id", x.book_id), ("author_id", x.author_id), ("rank", None) ], 2), debug=debug)
                if (isinstance(row, tuple) or isinstance(row, list)) and (len(row) > 0):
                    x.rank = row[0]
            case Fields.Rank:
                row = self._table.one(Table.Info("book_author", [ ("book_id", x.book_id), ("author_id", x.author_id), ("rank", None) ], 2), debug=debug)
                if (isinstance(row, tuple) or isinstance(row, list)) and (len(row) > 0):
                    x.rank = row[0]
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

    def _reference(self, x):
        return BookAuthorRef(book_id=x[0], author_id=x[1])

    def _create(self, x):
        return BookAuthor(book_id=x[0], author_id=x[1], rank=x[2])


class BookAuthorTable(Table):

    def _insert(self, x):
        # book_author
        if isinstance(x, BookAuthor):
            return Table.Info("book_author", [ x.book_id, x.author_id, x.rank ], 2, tag=("replace"))

    def _update(self, x):
        # book_author
        if isinstance(x, BookAuthor):
            return Table.Info("book_author", [ x.book_id, x.author_id, x.rank ], 2, tag="update")

    def _delete(self, x):
        # pk
        if isinstance(x, BookAuthorRef):
            return Table.Info("book_author", [x.book_id, x.author_id ], tag="pk")

    def _select(self, x=None) -> tuple:
        # pk
        if isinstance(x, BookAuthorRef):
            return Table.Info("book_author", [ x.book_id, x.author_id ], tag="pk")
        # all
        if x is None:
            return Table.Info("book_author", tag="all")

