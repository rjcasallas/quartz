from db.common import DatabaseGenerator
from quartz.gen.base import Target


class QueriesGenerator(DatabaseGenerator):

    def __init__(self, schema_path: str):
        super().__init__(schema_path)

    def generate(self, output_dir: str):
        # Targets
        targets = []
        for table in self._meta.tables.values():
            targets.append(Target("sql/queries.hbs", f"queries/{table._name}.yaml", table))
        # Generate
        super().generate(targets, output_dir, self._meta)
