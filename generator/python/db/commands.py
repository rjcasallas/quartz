# Main entry point for the application.
from quartz.log import Log
from quartz.app import BasicCommand, Types
from db.queries import QueriesGenerator


class DatabaseCommand(BasicCommand):

    def setup(self) -> None:
        self.args.dashed.add("schema", "s", Types.Path, "examples/db/books.sql")
        self.args.dashed.add("database", "d", Types.Path, "temp/generate.sqlite")
        self.args.dashed.add("templates", "t", Types.Path, "generator/templates")
        self.args.dashed.add("out", "o", Types.Path)


class QueriesCommand(DatabaseCommand):

    def __init__(self):
        super().__init__("Queries")

    def setup(self) -> None:
        super().setup()
        self.args.dashed.add("out", "o", Types.Path, "examples/db")

    def execute(self):
        Log.list(f"Database", 0, '‣')
        self.print()
        schema = self.args.string("schema")
        out = self.args.string("out")
        gen = QueriesGenerator(schema)
        gen.print()
        gen.generate(out)

