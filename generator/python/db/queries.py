from db.common import DatabaseGenerator
from quartz.gen.base import Target


class QueriesGenerator(DatabaseGenerator):

    def __init__(self, schema_path: str):
        super().__init__(schema_path)

    def generate(self, output_dir: str):
        # Targets
        targets = []
        for table in self._meta.tables:
            targets.append(Target("sql/select_all-pk.hbs", f"sql/{table._name}/select_all-pk.sql", table))
            targets.append(Target("sql/select_pk-pk.hbs",  f"sql/{table._name}/select_pk-pk.sql", table))
            if table.auto:
                targets.append(Target("sql/insert_id.hbs",     f"sql/{table._name}/insert_id.sql", table))
            targets.append(Target("sql/replace.hbs",       f"sql/{table._name}/replace.sql", table))
            targets.append(Target("sql/delete_all.hbs",    f"sql/{table._name}/delete_all.sql", table))
            targets.append(Target("sql/delete_pk.hbs",     f"sql/{table._name}/delete_pk.sql", table))
            for c in table.indexed:
                targets.append(Target("sql/select_index-pk.hbs", f"sql/{table._name}/select_{c.short}-pk.sql", c))
                targets.append(Target("sql/delete_index.hbs",    f"sql/{table._name}/delete_{c.short}.sql", c))
            if table.nonkeys:
                targets.append(Target("sql/select_all-full.hbs", f"sql/{table._name}/select_all-full.sql", table))
                targets.append(Target("sql/select_pk-full.hbs",  f"sql/{table._name}/select_pk-full.sql", table))
                targets.append(Target("sql/insert.hbs",        f"sql/{table._name}/insert.sql", table))
                targets.append(Target("sql/update.hbs",          f"sql/{table._name}/update.sql", table))
                for c in table.indexed:
                    targets.append(Target("sql/select_index-full.hbs", f"sql/{table._name}/select_{c.short}-full.sql", c))
        # Generate
        super().generate(targets, output_dir, self._meta)
