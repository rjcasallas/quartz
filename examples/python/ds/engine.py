import ds.api._core as _core
from ds.api.author import *
from ds.api.book import *
from ds.api.genre import *
from ds.api.publisher import *
import quartz.db.sqlite as _sqlite

#
# Engine
#

class Engine(_core.Engine):

    def __init__(self, schema_path:str, file_path:str, reset:bool=False):
        db = _sqlite.Database(schema_path, file_path)
        db.open(reset)
        # Entities
        self._authors = AuthorManager(db, self)
        self._books = BookManager(db, self)
        self._genres = GenreManager(db, self)
        self._publishers = PublisherManager(db, self)

