# Main entry point for the application.
from quartz.log import Log
from quartz.app import BasicCommand, Types
from db.queries import QueriesGenerator
from db.dataset import DatabaseGenerator, PythonDatasetGenerator, DatasetFlags


class DatabaseCommand(BasicCommand):

    def setup(self) -> None:
        self.args.dashed.add("schema", "s", Types.Path, "examples/db/books.sql")
        self.args.dashed.add("file", "f", Types.Path, "temp/generate.sqlite")
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


class PythonDatasetCommand(DatabaseCommand):

    def __init__(self):
        super().__init__("Python Dataset")

    def setup(self) -> None:
        super().setup()
        self.args.dashed.add("module", "m", Types.Path, "ds")
        self.args.dashed.add("core", "c", Types.Flag)
        self.args.dashed.add("sqlite", "q", Types.Flag)
        self.args.dashed.add("base", "b", Types.Flag)
        self.args.dashed.add("api", "a", Types.Flag)

    def execute(self):
        super().execute()
        schema = self.args.string("schema")
        mod = self.args.string("module")
        out = self.args.string("out") or "examples/python/ds"
        flags = DatasetFlags(0)
        if self.args.boolean("core"):  flags |= DatasetFlags.Core
        if self.args.boolean("sqlite"): flags |= DatasetFlags.Sqlite
        if self.args.boolean("base"):   flags |= DatasetFlags.Base
        if self.args.boolean("api"):    flags |= DatasetFlags.API

        gen = PythonDatasetGenerator(schema)
        gen.generate(out, mod, flags)


class DatasetCommand(DatabaseCommand):

    def __init__(self):
        super().__init__("Dataset")

    def setup(self) -> None:
        super().setup()
        self.commands.add(["python", "p"], PythonDatasetCommand())

    def execute(self):
        Log.list(f"Schema", 0, '‣')
        schema = self.args.string("schema")
        gen = DatabaseGenerator(schema)
        gen.print()
