import ds.data._base as _base
from ds.data.author import *
from ds.data.book import *
from ds.data.genre import *
from ds.data.publisher import *
import ds.sqlite._dataset as _sqlite

#
# Engine
#

class Engine(_base.Engine):

    def __init__(self, schema_path:str, file_path:str, reset:bool = False):
        super().__init__(_sqlite.Dataset(schema_path, file_path))
        # Entities
        self._authors = AuthorManager(self)
        self._books = BookManager(self)
        self._genres = GenreManager(self)
        self._publishers = PublisherManager(self)
        # Open
        self.ds.open(reset)
