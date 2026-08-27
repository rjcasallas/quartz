from ds.model._dataset import *
import quartz.gen.sqlite as _sqlite
from quartz.error import Error


class AuthorManager(Dataset.Authors, _sqlite.Table):

    def __init__(self, ds, db):
        Dataset.Authors.__init__(self, ds)
        _sqlite.Table.__init__(self, "author", db)

    def add(self, x: Author):
        return self._add(x)

    def remove(self, x):
        return self._remove(x)

    def has(self, x) -> bool:
        return self.contains(x)

    def clear(self):
        self.deleteAll()

    def update(self, x: Author):
        Author.valid(x)
        _sqlite.Table.update(self, [ x.name, x.id ])
        return x

    def ref(self, x = None) -> AuthorRef:
        return self.selectRef(x)

    def one(self, x = None) -> Author:
        return self.selectOne(x)

    def refs(self, x = None) -> list[AuthorRef]:
        return self.selectRefs(x)

    def all(self, x = None) -> list[Author]:
        return self.selectAll(x)

    def _reference(self, x):
        return AuthorRef(id=x[0])

    def _instance(self, x):
        return Author(id=x[0], name=x[1])

    def _add(self, x):
        # author
        if isinstance(x, Author):
            if x.id is None:
                x.id = self.insert([ x.name ], auto=True)
            else:
                self.insert([ x.id, x.name ])
            return x
        # "author_book" book.id → author.id
        if isinstance(x, BookAuthorRef):
            return self.db.exec("@book_author/replace", [ x.book_id, x.author_id, x.rank ])
        return Error.invalid("author", x)

    def _remove(self, x):
        # author
        if isinstance(x, AuthorRef):
            return self.db.exec("@author/delete_pk", [ int(x) ])
        if isinstance(x, str):
            return self.db.exec("@author/delete_name", [ x ])
        # "author_book" book.id → author.id
        if isinstance(x, BookAuthorRef):
            return self.db.exec("@book_author/delete_pk", [ x.book_id, x.author_id, x.rank ])

        return self.delete(x)

    def _ref(self, x = None) -> AuthorRef:
        # "author_book" book.id → author.id 
        if isinstance(x, BookRef):
            return self.db.one("@author/select_ref_by_book", [ int(x) ])
        # pk
        if isinstance(x, int) or isinstance(x, AuthorRef):
            return self.db.one("@author/select_ref_by_pk", [ int(x) ])
        # name
        if isinstance(x, str):
            return self.db.one("@author/select_ref_by_name", [ x ])
        return super()._ref(x)

    def _one(self, x = None) -> Author:
        # "author_book" book.id → author.id 
        if isinstance(x, BookRef):
            return self.db.one("@author/select_all_by_book", [ int(x) ])
        # pk
        if isinstance(x, int) or isinstance(x, AuthorRef):
            return self.db.one("@author/select_all_by_pk", [ int(x) ])
        # name
        if isinstance(x, str):
            return self.db.one("@author/select_all_by_name", [ x ])
        return super()._one(x)

    def _refs(self, x = None) -> list[AuthorRef]:
        # "author_book" book.id → author.id 
        if isinstance(x, BookRef):
            return self.db.all("@author/select_ref_by_book", [ int(x) ])
        return super()._refs(x)

    def _all(self, x = None) -> list[Author]:
        # "author_book" book.id → author.id 
        if isinstance(x, BookRef):
            return self.db.all("@author/select_all_by_book", [ int(x) ])
        return super()._all(x)