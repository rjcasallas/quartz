# Main entry point for the application.
import sys
import os
from quartz.app import BasicApp, BasicCommand, Types
from quartz.log import Log
import quartz.db.sqlite as _sqlite
from ds.sqlite._data import *


class DatasetApp(BasicApp):

    def __init__(self):
        super().__init__("Dataset Example", "1.0.0")

    def setup(self) -> None:
        self.args.fixed.add("schema", Types.Int16u, "examples/db/books.sql")
        self.args.dashed.add("path", "p", Types.Path)
        self.args.dashed.add("reset", "r", Types.Boolean, True)

    def execute(self):
        self.print()
        schema = self.args.string("schema")
        path = self.args.string("path")
        reset = self.args.boolean("reset")
        Log.info(f"Schema: {schema}")
        self._basicExample(schema, path, reset)
        self._advancedExample(schema, path, False)

    def _basicExample(self, schema, path, reset):
        db = _sqlite.Database(schema)
        db.open(path, reset)
        gi = db.exec("INSERT INTO genre(name) VALUES(?)", [ "Sci-fi" ])
        ai = db.exec("INSERT INTO author(name) VALUES(?)", [ "Douglas Adams" ])
        pi = db.exec("INSERT INTO publisher(name) VALUES(?)", [ "Little Books" ])
        bi = db.exec("INSERT INTO book(publisher_id, title, year) VALUES(?, ?, ?)", [ pi, "The Hitchhiker's Guide to the Galaxy", 1979 ])
        db.exec("INSERT INTO book_genre VALUES(?, ?)", [ bi, gi ])
        db.exec("INSERT INTO book_author VALUES(?, ?, ?)", [ bi, ai, 1 ])

    def _advancedExample(self, schema, path, reset):
        ds = Dataset(schema)
        ds.open(path, reset)
        fantasy = ds.genres.add(Genre("Fantasy"))
        homer = ds.authors.add(Author("Homer"))
        big = ds.publishers.add(Publisher(None, "Big Editorial"))
        illiad = ds.books.add(Book(big, "The Iliad", 700))
        ds.books.link(illiad, fantasy)
        ds.books.link(illiad, homer)
        ds.print()

if __name__ == "__main__":
    app = DatasetApp()
    app.run()
