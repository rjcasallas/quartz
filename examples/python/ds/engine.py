import ds.base._core as _core
from ds.api.author import *
from ds.api.book import *
from ds.api.genre import *
from ds.api.publisher import *
import ds.sqlite._dataset as _sqlite

#
# Engine
#

class Engine(_core.Engine):

    def __init__(self, schema_path:str, file_path:str, reset:bool=False):
        super().__init__(_sqlite.Dataset(schema_path, file_path))
        # Entities
        self._authors = AuthorManager(self)
        self._books = BookManager(self)
        self._genres = GenreManager(self)
        self._publishers = PublisherManager(self)
        # Open
        self.ds.open(reset)
