from quartz.file import Paths
from quartz.gen.base import TargetGenerator, Helpers
from quartz.db.meta import Table, Column, Link
from quartz.db.sqlite import Database
import os

#
# Helpers
#

class DatabaseHelpers(Helpers):

    def _core(self, x):
        if isinstance(x, Table):
            name = self._pascal(x)
            return name
            # return f"{name}X" # Debug only
        return f"CORE?({type(x)}|{x})"

    def _ref(self, x):
        if isinstance(x, Table):
            name = self._pascal(x)
            # if Table.Type.Aggregate == x.type:
            return f"{name}Ref"
        if isinstance(x, Column):
            if x.into:
                name = self._pascal(x.into.table)
                return f"{name}Ref"
            else:
                return self._ref(x.table)
        if isinstance(x, Link):
            if x.is_recursive:
                return self._pascal(x.name) + "Ref"
            else:
                return self._pascal(x.target.table.name) + "Ref"
        return f"REF?({type(x)}|{x})"

    def ref_from(self, link):
        if not isinstance(link, Link):
            return "L({})".format(type(link))
        if link.is_recursive:
            n = self._pascal(link.name)
            return f"{n}Ref"
        else:
            t = self._pascal(link.source.table)
            return f"{t}Ref"

    def ref_into(self, link):
        if not isinstance(link, Link):
            return "L({})".format(type(link))
        if link.is_recursive:
            n = self._pascal(link.name)
            return f"{n}Ref"
        else:
            t = self._pascal(link.target.table)
            return f"{t}Ref"

    def _query(self, this, action, x, y = None):
        if not isinstance(action, str):
            return "A({})".format(type(action))
        # source/destination
        if isinstance(x, Table) and isinstance(y, Table):
            src = x.name
            dst = y.name.removeprefix(f"{src}_")
        elif isinstance(x, Link):
            src = x.source.table.name
            dst = x.target.table.name
        # action
        if 'add' == action:
            return f"{src}/insert_{dst}"
        elif 'del' == action:
            return f"{src}/delete_{dst}"
        elif 'get' == action:
            return f"{src}/select_{dst}"
            # return f"{from_c._table._name}.{from_c._name}->{into_c._table._name}.{into_c._name}"
        return 'query?'

    def __core(self, this, text = None):
        return self._core(text or this.context)

    def __ref(self, this, text = None):
        return self._ref(text or this.context)

    def __ref_from(self, this, link = None):
        return self.ref_from(link or this.context)

    def __ref_into(self, this, link = None):
        return self.ref_into(link or this.context)

    def compile(self):
        return super().compile() | {
            "-core": self.__core,
            "-ref": self.__ref,
            "-ref_from": self.__ref_from,
            "-ref_into": self.__ref_into,
            "-query": self._query,
        }

#
# Generator
#

class DatabaseGenerator(TargetGenerator):

    def __init__(self, schema_path: str, helpers: DatabaseHelpers = None):
        super().__init__(Paths.quartz("generator/templates"), helpers or DatabaseHelpers())
        temp_db = Paths.normalize("temp/generate.db")
        os.makedirs(os.path.dirname(temp_db), exist_ok=True)
        db = Database(schema_path, temp_db)
        db.open(reset=True)
        self._meta = db.meta()

    def print(self):
        self._meta.print()