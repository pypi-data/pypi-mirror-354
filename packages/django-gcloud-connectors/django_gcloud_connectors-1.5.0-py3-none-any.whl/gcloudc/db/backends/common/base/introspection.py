import json
from django.db.backends.base.introspection import (
    BaseDatabaseIntrospection,
)

from gcloudc.db.backends.common.helpers import get_model_from_db_table


class NoSQLDatabaseIntrospection(BaseDatabaseIntrospection):

    def get_constraints(self, cursor, table_name):
        metadata = self.connection.schema_editor().metadata.entity
        constraints = metadata["constraints"]
        if constraints is None:
            return {}

        constraints = json.loads(constraints)
        result = {}
        for constraint in constraints.get(table_name, []):
            model = get_model_from_db_table(table_name)
            result[constraint["name"]] = {
                "columns": constraint["columns"],
                "index": constraint["index"],
                "primary_key": model._meta.pk.name in constraint["columns"],
            }

        return result
