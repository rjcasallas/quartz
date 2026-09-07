import ds.model._dataset as _base
from ds.data.author import *
from ds.data.book import *
from ds.data.book_author import *
from ds.data.genre import *
from ds.data.publisher import *
import quartz.data.sqlite as _sqlite
import quartz.data.mysql as _mysql

#
# Dataset
#

class Dataset(_base.Dataset):

    def __init__(self, schema_path, file_path:str):
        super().__init__()
        # Database
        self._db = _sqlite.Database(schema_path, file_path)
        # self._db = _mysql.Database(os.getenv("DB_SCHEMA"), os.getenv("DB_NAME"), os.getenv("DB_USER"), os.getenv("DB_PASS"))
        # Entities
        self._authors = AuthorData(self._db)
        self._books = BookData(self._db)
        self._book_authors = BookAuthorData(self._db)
        self._genres = GenreData(self._db)
        self._publishers = PublisherData(self._db)

    @property
    def path(self):
        return self._db.path

    def open(self, reset: bool = False):
        self._db.open(reset)

    def isOpen(self):
        return self._db.isOpen()

    def close(self):
        self._db.close()

    @staticmethod
    def valid(x, nullable=False):
        if nullable and (x is None):
            return None
        if isinstance(x, Dataset):
            return x
        Error.invalid("dataset", x)
