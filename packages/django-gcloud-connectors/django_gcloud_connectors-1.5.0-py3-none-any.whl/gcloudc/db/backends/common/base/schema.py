import json
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from .entity import Entity


class NoSQLSchemaMetadata:
    """
        This keeps a record of the constraints that Django migrations
        have attempted to apply. This is just to allow migrations to
        "work" without actually doing anything.
    """

    CONSTRAINT_TABLE = "schema_metadata"

    def __init__(self, wrapper):
        self.wrapper = wrapper

        wrapper.ensure_connection()
        self.key = wrapper.connection.new_key(self.CONSTRAINT_TABLE, 1)
        self.entity = wrapper.connection._get(self.key)
        if self.entity is None:
            self.entity = Entity(
                key=self.key,
                properties={
                    "constraints": json.dumps({}),
                }
            )

    def _save_entity(self):
        self.wrapper.connection._put(self.key, self.entity)

    def add_constraint(self, model, constraint):
        constraints = json.loads(self.entity["constraints"])
        constraints.setdefault(model._meta.db_table, []).append({
            "name": constraint.name,
            "index": False,
            "columns": [
                model._meta.get_field(f).column for f in getattr(constraint, "fields", [])
            ]
        })

        self.entity["constraints"] = json.dumps(constraints)
        self._save_entity()

    def remove_constraint(self, model, constraint):
        constraints = json.loads(self.entity["constraints"])
        constraints[model._meta.db_table] = [
            c for c in constraints[model._meta.db_table] if c["name"] != constraint.name
        ]
        self.entity["constraints"] = json.dumps(constraints)
        self._save_entity()

    def add_index(self, model, index):
        constraints = json.loads(self.entity["constraints"])
        constraints.setdefault(model._meta.db_table, []).append({
            "name": index.name,
            "index": True,
            "columns": [
                model._meta.get_field(f).column for f in index.fields
            ]
        })

        self.entity["constraints"] = json.dumps(constraints)
        self._save_entity()

    def remove_index(self, model, index):
        constraints = json.loads(self.entity["constraints"])
        constraints[model._meta.db_table] = [
            c for c in constraints[model._meta.db_table]
            if c["name"] != index.name and c["index"]
        ]

        self.entity["constraints"] = json.dumps(constraints)
        self._save_entity()

    def rename_index(self, model, old_index, new_index):
        self.entity.remove(old_index.name)
        self.entity.append(new_index.name)
        self._save_entity()


class NoSQLDatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    def __init__(self, connection, *args, **kwargs):
        super().__init__(connection, *args, **kwargs)

        self.metadata = NoSQLSchemaMetadata(connection)

    def column_sql(self, model, field, include_default=False):
        return "", {}

    def create_model(self, model):
        """ Don't do anything when creating tables """
        pass

    def alter_unique_together(self, *args, **kwargs):
        pass

    def alter_field(self, from_model, from_field, to_field):
        pass

    def remove_field(self, from_model, field):
        pass

    def add_field(self, model, field):
        query = self.connection.get_query_class()(
            self.connection,
            [model._meta.db_table],
            namespace=self.connection.namespace,
        )

        # Copy the entities to the new table
        for result in query.fetch(offset=0, limit=None):
            result[field.column] = field.get_default()
            self.connection.connection.put(result)

    def alter_index_together(self, model, old_index_together, new_index_together):
        pass

    def delete_model(self, model):
        pass

    def add_index(self, model, index):
        self.metadata.add_index(model, index)

    def remove_index(self, model, index):
        self.metadata.remove_index(model, index)

    def rename_index(self, model, old_index, new_index):
        self.metadata.rename_index(model, old_index, new_index)

    def add_constraint(self, model, constraint):
        self.metadata.add_constraint(model, constraint)

    def remove_constraint(self, model, constraint):
        self.metadata.remove_constraint(model, constraint)

    def alter_db_table(self, model, old_db_table, new_db_table):
        """
            THIS WILL NOT SCALE! It's largely to satisfy migrations locally
            during development.
        """

        if old_db_table == new_db_table or (
            self.connection.features.ignores_table_name_case
            and old_db_table.lower() == new_db_table.lower()
        ):
            return

        query = self.connection.get_query_class()(
            self.connection,
            [old_db_table],
            namespace=self.connection.namespace,
        )

        # Copy the entities to the new table
        for result in query.fetch(offset=0, limit=None):
            result.key = self.connection.new_key(new_db_table, result.key.id)
            self.connection.connection.put(result.key, result)

        # Delete the old table
        self.connection.connection.flush([old_db_table])
