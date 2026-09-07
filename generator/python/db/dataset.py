from db.common import DatabaseGenerator
from quartz.gen.base import Target
from enum import IntFlag
from quartz.log import Log


class DatasetFlags(IntFlag):
    Core    = 1
    Sqlite  = 2
    Base    = 4
    API     = 8

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
        for t in meta.tables:
            t._module = module
        # Model
        if (0 == flags) or (flags & DatasetFlags.Core):
            targets.append(Target("python/ds/model/reference.hbs", "model/_reference.py"))
            targets.append(Target("python/ds/model/dataset.hbs", "model/_dataset.py"))
            for t in meta.entities:
                targets.append(Target("python/ds/model/table.hbs", f"model/{t.name}.py", t))
        # SQLite
        if (0 == flags) or (flags & DatasetFlags.Sqlite):
            targets.append(Target("python/ds/sqlite/dataset.hbs", "sqlite/_dataset.py"))
            for t in meta.entities:
                targets.append(Target("python/ds/sqlite/table.hbs", f"sqlite/{t.name}.py", t))
        # API
        if (0 == flags) or (flags & DatasetFlags.Base):
            targets.append(Target("python/ds/engine.hbs", "engine.py"))
            targets.append(Target("python/ds/base/core.hbs", "base/_core.py"))
            for t in meta.entities:
                targets.append(Target("python/ds/base/table.hbs", f"base/{t.name}.py", t))
        if (flags & DatasetFlags.API):
            for t in meta.entities:
                targets.append(Target("python/ds/api/table.hbs", f"api/{t.name}.py", t))

        # Generate
        super().generate(targets, output_dir, meta)
        # self.print()
