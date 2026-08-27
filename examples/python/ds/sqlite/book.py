from ds.model._dataset import *
import quartz.gen.sqlite as _sqlite
from quartz.error import Error


class BookManager(Dataset.Books, _sqlite.Table):

    def __init__(self, ds, db):
        Dataset.Books.__init__(self, ds)
        _sqlite.Table.__init__(self, "book", db)

    def add(self, x: Book):
        return self._add(x)

    def remove(self, x):
        return self._remove(x)

    def has(self, x) -> bool:
        return self.contains(x)

    def clear(self):
        self.deleteAll()

    def update(self, x: Book):
        Book.valid(x)
        _sqlite.Table.update(self, [ x.publisher_id, x.title, x.year, x.id ])
        return x

    def ref(self, x = None) -> BookRef:
        return self.selectRef(x)

    def one(self, x = None) -> Book:
        return self.selectOne(x)

    def refs(self, x = None) -> list[BookRef]:
        return self.selectRefs(x)

    def all(self, x = None) -> list[Book]:
        return self.selectAll(x)

    def _reference(self, x):
        return BookRef(id=x[0])

    def _instance(self, x):
        return Book(id=x[0], publisher_id=x[1], title=x[2], year=x[3])

    def _add(self, x):
        # book
        if isinstance(x, Book):
            if x.id is None:
                x.id = self.insert([ x.publisher_id, x.title, x.year ], auto=True)
            else:
                self.insert([ x.id, x.publisher_id, x.title, x.year ])
            return x
        # "book_author" author.id → book.id
        if isinstance(x, BookAuthorRef):
            return self.db.exec("@book_author/replace", [ x.book_id, x.author_id, x.rank ])
        # "book_genre" genre.id → book.id
        if isinstance(x, BookGenreRef):
            return self.db.exec("@book_genre/replace", [ x.book_id, x.genre_id ])
        return Error.invalid("book", x)

    def _remove(self, x):
        # book
        if isinstance(x, BookRef):
            return self.db.exec("@book/delete_pk", [ int(x) ])
        if isinstance(x, str):
            return self.db.exec("@book/delete_title", [ x ])
        # "book_author" author.id → book.id
        if isinstance(x, BookAuthorRef):
            return self.db.exec("@book_author/delete_pk", [ x.book_id, x.author_id, x.rank ])
        # "book_genre" genre.id → book.id
        if isinstance(x, BookGenreRef):
            return self.db.exec("@book_genre/delete_pk", [ x.book_id, x.genre_id ])

        return self.delete(x)

    def _ref(self, x = None) -> BookRef:
        # "book_author" author.id → book.id 
        if isinstance(x, AuthorRef):
            return self.db.one("@book/select_ref_by_author", [ int(x) ])
        # "book_genre" genre.id → book.id 
        if isinstance(x, GenreRef):
            return self.db.one("@book/select_ref_by_genre", [ int(x) ])
        # pk
        if isinstance(x, int) or isinstance(x, BookRef):
            return self.db.one("@book/select_ref_by_pk", [ int(x) ])
        # title
        if isinstance(x, str):
            return self.db.one("@book/select_ref_by_title", [ x ])
        return super()._ref(x)

    def _one(self, x = None) -> Book:
        # "book_author" author.id → book.id 
        if isinstance(x, AuthorRef):
            return self.db.one("@book/select_all_by_author", [ int(x) ])
        # "book_genre" genre.id → book.id 
        if isinstance(x, GenreRef):
            return self.db.one("@book/select_all_by_genre", [ int(x) ])
        # pk
        if isinstance(x, int) or isinstance(x, BookRef):
            return self.db.one("@book/select_all_by_pk", [ int(x) ])
        # title
        if isinstance(x, str):
            return self.db.one("@book/select_all_by_title", [ x ])
        return super()._one(x)

    def _refs(self, x = None) -> list[BookRef]:
        # "book_author" author.id → book.id 
        if isinstance(x, AuthorRef):
            return self.db.all("@book/select_ref_by_author", [ int(x) ])
        # "book_genre" genre.id → book.id 
        if isinstance(x, GenreRef):
            return self.db.all("@book/select_ref_by_genre", [ int(x) ])
        return super()._refs(x)

    def _all(self, x = None) -> list[Book]:
        # "book_author" author.id → book.id 
        if isinstance(x, AuthorRef):
            return self.db.all("@book/select_all_by_author", [ int(x) ])
        # "book_genre" genre.id → book.id 
        if isinstance(x, GenreRef):
            return self.db.all("@book/select_all_by_genre", [ int(x) ])
        return super()._all(x)