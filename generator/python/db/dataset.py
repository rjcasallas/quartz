from db.common import DatabaseGenerator
from quartz.gen.base import Target
from enum import IntFlag


class DatasetFlags(IntFlag):
    Refs    = 1
    Model   = 2
    Sqlite  = 3
    Dataset = 4

#
# Generators
#

class PythonDatasetGenerator(DatabaseGenerator):

    def generate(self, output_dir: str, module: str = "db", flags:DatasetFlags = 0):
        # Metadata
        meta = self._meta
        meta._module = module
        # Targets
        targets = []
        tables = sorted(meta.entities + meta.aggregates)
        # Model
        if (0 == flags) or (flags & DatasetFlags.Refs):
            targets.append(Target("python/ds/model/reference.hbs", "model/_reference.py"))
        if (0 == flags) or (flags & DatasetFlags.Model):
            targets.append(Target("python/ds/model/data.hbs", "model/_data.py"))
            for table in tables:
                table._module = module
                targets.append(Target("python/ds/model/table.hbs", f"model/{table.name}.py", table))
        # SQLite
        if (0 == flags) or (flags & DatasetFlags.Dataset):
            targets.append(Target("python/ds/sqlite/data.hbs", "sqlite/_data.py"))
        if (0 == flags) or (flags & DatasetFlags.Sqlite):
            for table in tables:
                table._module = module
                targets.append(Target("python/ds/sqlite/table.hbs", f"sqlite/{table.name}.py", table))

        # Generate
        super().generate(targets, output_dir, meta)
