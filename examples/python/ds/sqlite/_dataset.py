import ds.model._dataset as _base
from ds.sqlite.author import *
from ds.sqlite.book import *
from ds.sqlite.genre import *
from ds.sqlite.publisher import *
import quartz.db.sqlite as _sqlite

#
# Dataset
#

class Dataset(_base.Dataset):

    def __init__(self, schema_path, file_path:str):
        super().__init__()
        self._db = _sqlite.Database(schema_path, file_path)
        self._authors = AuthorSubset(self._db)
        self._books = BookSubset(self._db)
        self._genres = GenreSubset(self._db)
        self._publishers = PublisherSubset(self._db)

    @property
    def path(self):
        return self._db.path

    def open(self, reset: bool = False):
        self._db.open(reset)

    def isOpen(self):
        return self._db.isOpen()
