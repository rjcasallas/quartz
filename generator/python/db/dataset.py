from db.database import DatabaseGenerator, DatabaseHelpers
from db.common import Target
from quartz.data.meta import Table
from quartz.log import Log
from enum import IntFlag
from abc import ABC, abstractmethod


class DatasetFlags(IntFlag):
    Base    = 1
    Data    = 2
    API     = 4

#
# Helpers
#

class PythonHelpers(DatabaseHelpers):

    def __subset(self, this, table=None):
        p = self._plural(table or this.context)
        return f"self._ds.{p}"

    def compile(self):
        return super().compile() | {
            "-subset": self.__subset,
        }


class PhpHelpers(DatabaseHelpers):

    def _model(self, x):
        if isinstance(x, Table):
            name = self._pascal(x)
            return f"model\\{name}"
        return f"Model?({type(x)}|{x})"

#
# Generators
#

class DatasetGenerator(DatabaseGenerator):

    def generate(self, table, flags, out_dir):
        meta = self._configureMetadata(self.meta)
        targets = self._buildTargets(table, flags, meta)
        super().generate(targets, out_dir, meta)

    def _buildTargets(self, table, flags, meta):
        # Metadata
        targets = []
        # Model
        if (0 == flags) or (flags & DatasetFlags.Base):
            self._addModelBase(targets, meta)
            if table and (table in meta):
                self._addModeTable(targets, meta[table])
            else:
                for t in meta.subsets:
                    if t.nonkeys:
                        self._addModeTable(targets, t)
        # Dataset
        if (0 == flags) or (flags & DatasetFlags.Data):
            self._addDataBase(targets, meta)
            if table and (table in meta):
                self._addDataTable(targets, meta[table])
            else:
                for t in meta.subsets:
                    self._addDataTable(targets, t)
        # API
        if (0 == flags) or (flags & DatasetFlags.API):
            self._addApiBase(targets, meta)
            if table and (table in meta):
                t = meta[table]
                if t.is_api:
                    self._addApiTable(targets, t)
            else:
                for t in meta.apis:
                    self._addApiTable(targets, t)
        return targets
    
    @abstractmethod
    def _configureMetadata(self, meta):
        return meta

    @abstractmethod
    def _addModelBase(self, targets, meta):
        pass

    @abstractmethod
    def _addModeTable(self, targets, table):
        pass
    
    @abstractmethod
    def _addDataBase(self, targets, meta):
        pass

    @abstractmethod
    def _addDataTable(self, targets, table):
        pass
    
    @abstractmethod
    def _addApiBase(self, targets, meta):
        pass

    @abstractmethod
    def _addApiTable(self, targets, table):
        pass


class PythonDatasetGenerator(DatasetGenerator):

    def __init__(self, schema_path:str, mod:str):
        super().__init__(schema_path, PythonHelpers())
        self._module = mod

    def _configureMetadata(self, meta):
        meta._module = self._module
        for t in meta.tables:
            t._module = self._module
        return meta

    def _addModelBase(self, targets, meta):
        targets.append(Target("python/ds/model/base.hbs", "base.py", meta))
        targets.append(Target("python/ds/model/dataset.hbs", "model/_dataset.py", meta))

    def _addModeTable(self, targets, table):
        targets.append(Target("python/ds/model/table.hbs", f"model/{table.name}.py", table))
    
    def _addDataBase(self, targets, meta):
        targets.append(Target("python/ds/data/dataset.hbs", "dataset.py", meta))

    def _addDataTable(self, targets, table):
        targets.append(Target("python/ds/data/table.hbs", f"data/{table.name}.py", table))
    
    def _addApiBase(self, targets, meta):
        targets.append(Target("python/ds/api/engine.hbs", "engine.py", meta))
        targets.append(Target("python/ds/api/core.hbs", "api/_core.py", meta))

    def _addApiTable(self, targets, table):
        targets.append(Target("python/ds/api/table.hbs", f"api/{table.name}.py", table))



class PhpDatasetGenerator(DatasetGenerator):

    def __init__(self, schema_path:str, ns:str):
        super().__init__(schema_path, PhpHelpers())
        self._namespace = ns

    def _configureMetadata(self, meta):
        meta._namespace = self._namespace
        for t in meta.tables:
            t._namespace = self._namespace
        return meta

    def _addModelBase(self, targets, meta):
        targets.append(Target("php/ds/model/base.hbs", "base.php", meta))
        # targets.append(Target("php/ds/model/dataset.hbs", "model/_dataset.php", meta))

    def _addModeTable(self, targets, table):
        targets.append(Target("php/ds/model/table.hbs", f"model/{table.name}.php", table))

    def _addDataBase(self, targets, meta):
        targets.append(Target("php/ds/data/dataset.hbs", "dataset.php", meta))

    def _addDataTable(self, targets, table):
        targets.append(Target("php/ds/data/table.hbs", f"data/{table.name}.php", table))

    def _addApiBase(self, targets, meta):
        targets.append(Target("php/ds/api/engine.hbs", "engine.php", meta))
        # targets.append(Target("php/ds/api/core.hbs", "api/_core.php", meta))

    def _addApiTable(self, targets, table):
        targets.append(Target("php/ds/api/table.hbs", f"api/{table.name}.php", table))

