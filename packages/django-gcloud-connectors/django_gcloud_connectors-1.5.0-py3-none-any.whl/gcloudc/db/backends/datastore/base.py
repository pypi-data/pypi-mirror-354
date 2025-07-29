# Standard library
from typing import Optional, Union, Iterable
import logging
import os
import secrets

# Third Party
from django.core.exceptions import ImproperlyConfigured
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.base.client import BaseDatabaseClient
from django.db.backends.base.creation import BaseDatabaseCreation
from django.db.backends.base.features import BaseDatabaseFeatures
from django.db.backends.base.introspection import (
    TableInfo,
)
from ..common.base.schema import NoSQLDatabaseSchemaEditor
from ..common.base.introspection import NoSQLDatabaseIntrospection

from django.db.backends.base.validation import BaseDatabaseValidation
from google.api_core.exceptions import MethodNotImplemented
from google.cloud import (
    datastore,
    environment_vars,
)
from google.cloud.datastore.query import PropertyFilter
import requests

# gcloudc
from gcloudc.db.backends.common.base import dbapi as Database
from gcloudc.db.backends.common.base.connection import Connection as NoSQLConnection, NoSQLDatabaseOperations, Wrapper
from gcloudc.db.backends.common.base.entity import Entity, Key
from gcloudc.db.backends.common.base.query import Query as NoSQLQuery

logger = logging.getLogger(__name__)


class Connection(NoSQLConnection):
    def _create_client(self, project, database=None, namespace=None):
        host_environ_set = bool(os.environ.get(environment_vars.GCD_HOST))
        client_kwargs = dict(
            namespace=namespace,
            project=project,
        )
        if database:
            client_kwargs["database"] = database

        if database and host_environ_set:
            logger.warning(
                "A database connection is targeting a different Cloud Datastore "
                " using the DATABASE_ID setting (`%s`)."
                " The legacy datastor emulator DOES NOT support this."
                " Entities will be written to the default database",
                database,
            )

        return datastore.Client(
            **client_kwargs,
            # avoid a bug in the google client - it tries to authenticate even when the emulator is enabled
            # see https://github.com/googleapis/google-cloud-python/issues/5738
            _http=requests.Session if host_environ_set else None,
        )

    def _close_client(self):
        try:
            if self._client:
                self._client.close()
        except TypeError:
            # FIXME: Calling close causes an error inside
            # the datastore connector.. .I'm not sure why. Might only
            # happen locally when using requests.Session
            pass

    def _begin(self):
        assert (not self._txn)
        self._txn = self._client.transaction()

        # We need to use __enter__ instead of begin so that current_transaction
        # is appropriately set - otherwise queries are non-transactional!
        self._txn.__enter__()

    def _commit(self):
        assert (self._txn)
        self._txn.__exit__(None, None, None)

    def _rollback(self):
        assert (self._txn)

        # We have to simulate an exception being passed to __exit__
        # otherwise the transaction won't be popped from the stack
        class ExceptionPlaceHolder(Exception):
            pass

        self._txn.__exit__(ExceptionPlaceHolder(), None, None)

    def _exists(self, key):
        key = self.wrapper.to_native_key(key)
        return self._client.get(key) is not None

    def _delete(self, key_or_keys: Union[Key, Iterable[Key]]):
        is_list = hasattr(key_or_keys, "__iter__")
        if not is_list:
            key_or_keys = [key_or_keys]

        self._client.delete_multi([
            self.wrapper.to_native_key(x)
            for x in key_or_keys
        ])

    def _flush(self, tables, namespace=None, database=None):
        for table in tables:
            # The local datastore emulator explodes if you try to delete more than 500
            # things in a single batch. So we just iterate in batches of 500.
            limit = 500

            query = self._client.query(kind=table, namespace=namespace)
            query.keys_only()
            results = [
                x.key for x in query.fetch(limit=limit)
                # FIXME: This shouldn't be necessary, emulator bug??
                if x.key.database == self._client.database
            ]

            assert (not self._txn)

            while results:
                batch = self._client.batch()
                with batch:
                    for result in results:
                        batch.delete(result)

                results = [x.key for x in query.fetch(limit=limit)]

    def _get(self, key_or_keys) -> Union[Entity, Iterable[Entity]]:
        """
            Should return a list of one or more entities
            from the provided keys
        """
        if isinstance(key_or_keys, Key):
            result = self._client.get(self.wrapper.to_native_key(key_or_keys))
            return self.wrapper.from_native_entity(result)
        else:
            results = self._client.get_multi([
                self.wrapper.to_native_key(x) for x in key_or_keys
            ])

            return [
                self.wrapper.from_native_entity(x)
                for x in results if x is not None
            ]

    def _put(self, key, entity_or_entities) -> Optional[Union[Entity, Iterable[Entity]]]:
        is_list = hasattr(entity_or_entities, "__iter__")

        if not is_list:
            entity_or_entities = [entity_or_entities]

        native_entities = [
            self.wrapper.to_native_entity(x)
            for x in entity_or_entities
        ]

        if self._txn:
            for entity in native_entities:
                self._txn.put(entity)
        else:
            self._client.put_multi(native_entities)

        if is_list:
            return entity_or_entities
        else:
            return entity_or_entities[0]

    def new_key(self, table, id_or_name, parent: Optional[Key] = None, namespace=None) -> Key:
        if parent and parent.is_partial():
            raise ValueError("Can't set an incomplete ancestor")

        path = [table]

        if parent:
            path = list(parent.path) + [parent.id_or_name] + path
            namespace = parent.namespace

        if id_or_name is not None:
            path.append(id_or_name)

        return self.wrapper.from_native_key(
            self._client.key(*path, namespace=namespace)
        )


class Query(NoSQLQuery):
    def __init__(self, connection, table_or_path, namespace=None, *args, **kwargs):
        super().__init__(connection, table_or_path, namespace=namespace, *args, **kwargs)
        assert (not isinstance(table_or_path, str))

        if len(table_or_path) == 1:
            kind = table_or_path[0]
            ancestor = None
        elif len(table_or_path) % 2 == 0:
            kind = None
            ancestor = self.wrapper.to_native_key(
                Key(table_or_path[:-1], table_or_path[-1], namespace=namespace)
            )
        else:
            # Not sure how to best deal with this. In this case we have a path
            # but it is a partial path (missing the ID part) and so we can't
            # construct an ancestor
            logger.warn("Got partial path for query")
            kind = table_or_path[0]
            ancestor = None

        connection.ensure_connection()
        self._query = connection.connection._client.query(
            kind=kind, ancestor=ancestor, namespace=self.namespace
        )

    def _add_filter(self, column, operator, value):
        if isinstance(value, Key):
            value = self.wrapper.to_native_key(value)

        if operator == "array_contains":
            operator = "="

        if operator == "array_contains_all":
            for v in value:
                self._query.add_filter(filter=PropertyFilter(column, "=", v))
        else:
            self._query.add_filter(filter=PropertyFilter(column, operator, value))

    def distinct_on(self, fields):
        self._query.distinct_on = fields

    def _order_by(self, orderings):
        self._query.order = orderings

    def fetch(self, offset, limit):
        if self.only_return_keys:
            self._query.keys_only()
        elif self.only_return_fields:
            self._query.projection = self.only_return_fields

        for result in self._query.fetch(offset=offset, limit=limit):
            yield self.wrapper.from_native_entity(result)

    def count(self, limit: Optional[int]) -> int:
        if self.wrapper._count_mode == "native":
            count_query = self.connection._client.aggregation_query(self._query).count()
            try:
                return int(next(count_query.fetch())[0].value)
            except MethodNotImplemented as e:
                raise ImproperlyConfigured(
                    '"native" count mode is not supported with emulated datastore, '
                    'use "emulated" mode for local development'
                ) from e
        self.only_return_keys = True
        return len([x for x in self.fetch(offset=None, limit=limit)])


class DatabaseOperations(NoSQLDatabaseOperations):
    compiler_module = "gcloudc.db.backends.datastore.compiler"


class DatabaseClient(BaseDatabaseClient):
    pass


class DatabaseCreation(BaseDatabaseCreation):
    data_types = {
        "AutoField": "long",
        "RelatedAutoField": "long",
        "ForeignKey": "long",
        "OneToOneField": "key",
        "ManyToManyField": "key",
        "BigIntegerField": "long",
        "BigAutoField": "long",
        "BooleanField": "bool",
        "CharField": "string",
        "CommaSeparatedIntegerField": "string",
        "DateField": "date",
        "DateTimeField": "datetime",
        "DecimalField": "decimal",
        "DurationField": "long",
        "EmailField": "string",
        "FileField": "string",
        "FilePathField": "string",
        "FloatField": "float",
        "ImageField": "string",
        "IntegerField": "integer",
        "IPAddressField": "string",
        "NullBooleanField": "bool",
        "PositiveIntegerField": "integer",
        "PositiveSmallIntegerField": "integer",
        "SlugField": "string",
        "SmallIntegerField": "integer",
        "TimeField": "time",
        "URLField": "string",
        "TextField": "text",
        "BinaryField": "bytes",
    }

    def __init__(self, *args, **kwargs):
        self.testbed = None
        super(DatabaseCreation, self).__init__(*args, **kwargs)

    def sql_create_model(self, model, *args, **kwargs):
        return [], {}

    def sql_for_pending_references(self, model, *args, **kwargs):
        return []

    def sql_indexes_for_model(self, model, *args, **kwargs):
        return []

    def _create_test_db(self, verbosity, autoclobber, *args):
        pass

    def _destroy_test_db(self, name, verbosity):
        pass


class DatabaseIntrospection(NoSQLDatabaseIntrospection):
    def get_table_list(self, cursor):
        assert (not cursor.connection._txn)
        query = cursor.connection._client.query(kind="__kind__")
        query.keys_only()
        kinds = [entity.key.id_or_name for entity in query.fetch()]
        return [TableInfo(x, "t") for x in kinds]

    def get_sequences(self, cursor, table_name, table_fields=()):
        # __key__ is the only column that can auto-populate
        return [{'table': table_name, 'column': '__key__'}]


class DatabaseSchemaEditor(NoSQLDatabaseSchemaEditor):
    pass


class DatabaseFeatures(BaseDatabaseFeatures):
    empty_fetchmany_value = []
    supports_transactions = True
    can_return_id_from_insert = True
    supports_select_related = False
    uses_savepoints = False
    allows_auto_pk_0 = False
    has_native_duration_field = False


class DatabaseWrapper(Wrapper, BaseDatabaseWrapper):
    data_types = DatabaseCreation.data_types  # These moved in 1.8
    supports_range_queries_on_array = True

    operators = {
        "exact": "= %s",
        "iexact": "iexact %s",
        "contains": "contains %s",
        "icontains": "icontains %s",
        "regex": "regex %s",
        "iregex": "iregex %s",
        "gt": "> %s",
        "gte": ">= %s",
        "lt": "< %s",
        "lte": "<= %s",
        "startswith": "startswith %s",
        "endswith": "endswith %s",
        "istartswith": "istartswith %s",
        "iendswith": "iendswith %s",
        "isnull": "isnull %s",
    }

    Database = Database

    # These attributes are only used by Django >= 1.11
    client_class = DatabaseClient
    features_class = DatabaseFeatures
    introspection_class = DatabaseIntrospection
    features_class = DatabaseFeatures
    ops_class = DatabaseOperations
    creation_class = DatabaseCreation
    validation_class = BaseDatabaseValidation

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)

        self.gcloud_project = self.settings_dict["PROJECT"]
        self.namespace = self.settings_dict.get("NAMESPACE") or None
        self.database = self.settings_dict.get("DATABASE_ID") or None
        self.autocommit = True

    def _create_connection(self, params):
        conn = Connection(self, params)
        return conn

    def get_query_class(self):
        return Query

    def key_property_name(self):
        """
            Return the name of the "Key" field, e.g. __key__ or __name__
        """
        return "__key__"

    def schema_editor(self, *args, **kwargs):
        return DatabaseSchemaEditor(self, *args, **kwargs)

    def reserve_id(self, kind, id_or_name, namespace):
        if not isinstance(id_or_name, int):
            # Nothing to do if the ID is a string, no-need to reserve that
            return

        gclient = self.connection._client
        gclient.reserve_ids_sequential(gclient.key(kind, id_or_name, namespace=namespace), 1)

    def generate_id(self, type):
        assert (type is int)
        """
            The Datastore API won't generate keys automatically until a
            transaction commits, that's too late!

            This returns a random 53 bit ID to remain inside the MAX_SAFE_INTEGER
            range in Javascript (ideally this would be 63 bit)
        """
        return secrets.randbits(53)

    def to_native_key(self, key: Key):
        return self.connection._client.key(
            *key.path,
            key.id_or_name,
            namespace=key.namespace or None
        )

    def from_native_key(self, key):
        path = key.flat_path[:]

        # key.flat_path includes the id_or_name as part of the path
        # we don't need that
        if len(path) % 2 == 0:
            path = path[:-1]

        return Key(path, key.id_or_name, namespace=key.namespace)

    def from_native_entity(self, entity_or_key) -> Entity:
        """
            Takes a native entity returned from a query, and turns it into an
            Entity object. If the argument is a key this should be an "empty" entity
            with just the key set.
        """
        if entity_or_key is None:
            return None

        if isinstance(entity_or_key, datastore.Key):
            return Entity(self.from_native_key(entity_or_key))
        else:
            ent = Entity(
                self.from_native_key(entity_or_key.key),
                exclude_from_indexes=entity_or_key.exclude_from_indexes,
            )

            for key in entity_or_key:
                ent[key] = entity_or_key[key]

            return ent

    def to_native_entity(self, entity: Entity):
        """
            When given an Entity object, this should return the same
            thing as a native type.
        """

        result = datastore.Entity(
            self.to_native_key(entity.key()),
            exclude_from_indexes=list(entity._properties_to_exclude_from_index)
        )

        for key in entity.keys():
            result[key] = entity[key]

        return result

    def polymodel_property_name(self):
        return "class"
