from db.common import Target
from db.database import DatabaseGenerator


class QueriesGenerator(DatabaseGenerator):

    def __init__(self, schema_path: str):
        super().__init__(schema_path)

    def generate(self, output_dir: str):
        # Targets
        targets = []
        for table in self._meta.tables:
            targets.append(Target("sql/select_pk-all.hbs", f"sql/{table._name}/select_pk-all.sql", table))
            targets.append(Target("sql/select_pk-pk.hbs",  f"sql/{table._name}/select_pk-pk.sql", table))
            if table.auto:
                targets.append(Target("sql/insert_id.hbs",     f"sql/{table._name}/insert_id.sql", table))
            targets.append(Target("sql/replace.hbs",       f"sql/{table._name}/replace.sql", table))
            targets.append(Target("sql/delete-all.hbs",    f"sql/{table._name}/delete-all.sql", table))
            targets.append(Target("sql/delete-pk.hbs",     f"sql/{table._name}/delete-pk.sql", table))
            for c in table.indexed:
                targets.append(Target("sql/select_pk-index.hbs", f"sql/{table._name}/select_pk-{c.short}.sql", c))
                targets.append(Target("sql/delete-index.hbs",    f"sql/{table._name}/delete-{c.short}.sql", c))
            if table.nonkeys:
                targets.append(Target("sql/select_full-all.hbs", f"sql/{table._name}/select_full-all.sql", table))
                targets.append(Target("sql/select_full-pk.hbs",  f"sql/{table._name}/select_full-pk.sql", table))
                targets.append(Target("sql/insert.hbs",        f"sql/{table._name}/insert.sql", table))
                targets.append(Target("sql/update.hbs",          f"sql/{table._name}/update.sql", table))
                for c in table.indexed:
                    targets.append(Target("sql/select_full-index.hbs", f"sql/{table._name}/select_full-{c.short}.sql", c))
        # Generate
        super().generate(targets, output_dir, self._meta)
