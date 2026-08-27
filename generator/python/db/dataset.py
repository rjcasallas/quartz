from db.common import DatabaseGenerator
from quartz.gen.base import Target
from enum import IntFlag
from quartz.log import Log


class DatasetFlags(IntFlag):
    Refs    = 1
    Model   = 2
    Sqlite  = 4
    API     = 8
    Extra   = 16

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
        tables = meta.tables.values()
        entities = sorted(meta.entities + meta.aggregates)
        for t in tables:
            t._module = module
        # Model
        if (0 == flags) or (flags & DatasetFlags.Refs):
            targets.append(Target("python/ds/model/base.hbs", "model/_base.py"))
        if (0 == flags) or (flags & DatasetFlags.Model):
            targets.append(Target("python/ds/model/dataset.hbs", "model/_dataset.py"))
            for t in entities:
                targets.append(Target("python/ds/model/table.hbs", f"model/{t.name}.py", t))
        # SQLite
        if (flags & DatasetFlags.Extra):
            targets.append(Target("python/ds/sqlite/dataset.hbs", "sqlite/_dataset.py"))
        if (0 == flags) or (flags & DatasetFlags.Sqlite):
            for t in entities:
                targets.append(Target("python/ds/sqlite/table.hbs", f"sqlite/{t.name}.py", t))
        # API
        if (0 == flags) or (flags & DatasetFlags.API):
            targets.append(Target("python/ds/api.hbs", "api.py"))
            targets.append(Target("python/ds/data/base.hbs", "data/_base.py"))
            for t in meta.entities:
                targets.append(Target("python/ds/data/table.hbs", f"data/{t.name}.py", t))

        # Generate
        super().generate(targets, output_dir, meta)
