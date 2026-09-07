from quartz.log import Log
from quartz.app import BasicCommand, Types
from db.queries import QueriesGenerator
from db.dataset import *
from pathlib import Path
import os


class DatabaseCommand(BasicCommand):

    def setup(self) -> None:
        self.args.dashed.add("schema", "s", Types.Path, "examples/db/sqlite.sql")
        self.args.dashed.add("file", "f", Types.Path, "temp/generate.sqlite")
        self.args.dashed.add("templates", "t", Types.Path, "generator/templates")


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
        gen = QueriesGenerator(schema)
        gen.print()
        out = self.args.string("out")
        if out is None:
            schema_dir = Path(os.path.dirname(schema))
            out = str(schema_dir)
        gen.generate(out)


class BaseDatasetCommand(DatabaseCommand):

    def setup(self) -> None:
        super().setup()
        self.args.dashed.add("base", "b", Types.Flag, False)
        self.args.dashed.add("data", "d", Types.Flag, False)
        self.args.dashed.add("api", "a", Types.Flag, False)
        self.args.dashed.add("table", "t", Types.Text, None)

    def execute(self):
        schema = self.args.string("schema")
        flags = DatasetFlags(0)
        table = self.args.string("table")
        if self.args.boolean("base"):   flags |= DatasetFlags.Base
        if self.args.boolean("data"):   flags |= DatasetFlags.Data
        if self.args.boolean("api"):    flags |= DatasetFlags.API
        self._generate(schema, table, flags)

    def _generate(self, schema, table, flags):
        pass


class PythonDatasetCommand(BaseDatasetCommand):

    def __init__(self):
        super().__init__("Python Dataset")

    def setup(self) -> None:
        super().setup()
        self.args.dashed.add("module", "m", Types.Text, "ds")
        self.args.dashed.add("out", "o", Types.Path, "examples/python/ds")


    def _generate(self, schema, table, flags):
        out = self.args.string("out")
        mod = self.args.string("module")
        gen = PythonDatasetGenerator(schema, mod)
        gen.generate(table, flags, out)


class PhpDatasetCommand(BaseDatasetCommand):

    def __init__(self):
        super().__init__("PHP Dataset")

    def setup(self) -> None:
        super().setup()
        self.args.dashed.add("namespace", "n", Types.Text, "ds")
        self.args.dashed.add("out", "o", Types.Path, "examples/php/ds")

    def _generate(self, schema, table, flags):
        out = self.args.string("out")
        ns = self.args.string("namespace")
        gen = PhpDatasetGenerator(schema, ns)
        gen.generate(table, flags, out)


class DatasetCommand(DatabaseCommand):

    def __init__(self):
        super().__init__("Dataset")

    def setup(self) -> None:
        super().setup()
        self.commands.add(["python", "py"], PythonDatasetCommand())
        self.commands.add(["php", "ph"], PhpDatasetCommand())

    def execute(self):
        Log.list(f"Schema", 0, '‣')
        schema = self.args.string("schema")
        gen = DatabaseGenerator(schema)
        gen.print()
