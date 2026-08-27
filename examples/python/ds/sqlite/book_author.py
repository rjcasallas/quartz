from ds.model._dataset import *
import quartz.gen.sqlite as _sqlite
from quartz.error import Error


class BookAuthorManager(Dataset.BookAuthors, _sqlite.Table):

    def __init__(self, ds, db):
        Dataset.BookAuthors.__init__(self, ds)
        _sqlite.Table.__init__(self, "book_author", db)

    def add(self, x: BookAuthor):
        return self._add(x)

    def remove(self, x):
        return self._remove(x)

    def has(self, x) -> bool:
        return self.contains(x)

    def clear(self):
        self.deleteAll()

    def update(self, x: BookAuthor):
        BookAuthor.valid(x)
        _sqlite.Table.update(self, [ x.rank, x.book_id, x.author_id ])
        return x

    def ref(self, x = None) -> BookAuthorRef:
        return self.selectRef(x)

    def one(self, x = None) -> BookAuthor:
        return self.selectOne(x)

    def refs(self, x = None) -> list[BookAuthorRef]:
        return self.selectRefs(x)

    def all(self, x = None) -> list[BookAuthor]:
        return self.selectAll(x)

    def _reference(self, x):
        return BookAuthorRef(book_id=x[0], author_id=x[1])

    def _instance(self, x):
        return BookAuthor(book_id=x[0], author_id=x[1], rank=x[2])

    def _add(self, x):
        # book_author
        if isinstance(x, BookAuthor):
            self.replace([ x.book_id, x.author_id, x.rank ])
            return x
        return Error.invalid("book_author", x)

    def _remove(self, x):
        # book_author
        if isinstance(x, BookAuthorRef):
            return self.db.exec("@book_author/delete_pk", [ x.book_id, x.author_id ])

        return self.delete(x)

    def _ref(self, x = None) -> BookAuthorRef:
        # pk
        if isinstance(x, BookAuthorRef):
            return self.db.one("@book_author/select_ref_by_pk", x.book_id, x.author_id)
        return super()._ref(x)

    def _one(self, x = None) -> BookAuthor:
        # pk
        if isinstance(x, BookAuthor):
            return self.db.one("@book_author/select_all_by_pk", x.book_id, x.author_id)
        return super()._one(x)

    def _refs(self, x = None) -> list[BookAuthorRef]:
        return super()._refs(x)

    def _all(self, x = None) -> list[BookAuthor]:
        return super()._all(x)