import ds.dataset as _ds
import ds.api._core as _core
from ds.api.author import *
from ds.api.book import *
from ds.api.genre import *
from ds.api.publisher import *


#
# Engine
#

class Engine(_core.Engine):

    def __init__(self, schema_path:str, file_path:str):
        # Dataset
        self._ds = _ds.Dataset(schema_path, file_path)
        # Entities
        self._authors = AuthorManager(self, self._ds)
        self._books = BookManager(self, self._ds)
        self._genres = GenreManager(self, self._ds)
        self._publishers = PublisherManager(self, self._ds)

    def open(self, reset: bool = False):
        self._ds.open(reset)

    def isOpen(self):
        return self._ds.isOpen()

    def close(self):
        self._ds.close()