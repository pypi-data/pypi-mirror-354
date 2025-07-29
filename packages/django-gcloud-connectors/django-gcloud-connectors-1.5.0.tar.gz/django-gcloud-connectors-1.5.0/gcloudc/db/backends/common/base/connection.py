import decimal
import datetime
import uuid

from datetime import timezone as tz
from functools import cached_property

from django.conf import settings
from django.db import IntegrityError
from django.core.exceptions import ImproperlyConfigured
from django.db.backends.base.operations import BaseDatabaseOperations
from django.utils import (
    timezone,
)
from django.utils.encoding import smart_str
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from typing import Optional, List, Tuple, Literal, get_args, Union, Iterable
from .entity import Entity, Key

from gcloudc.db.backends.common.indexing import load_special_indexes
from gcloudc.db.backends.common.helpers import (
    decimal_to_string,
    ensure_datetime,
    make_utc_compatible,
    get_model_from_db_table,
    get_bottom_concrete_model,
)
from gcloudc.db.backends.common.constraints import (
    has_unique_constraints,
    perform_unique_checks,
    check_unique_markers_in_memory,
)

from gcloudc.db.backends.common.commands import (
    DeleteCommand,
    FlushCommand,
    InsertCommand,
    SelectCommand,
    UpdateCommand,
    coerce_unicode,
)


class StagedWriteKind:
    INSERT = 0
    UPDATE = 1
    DELETE = 2


CountMode = Literal["native", "emulated"]


class Connection:
    """ Base connection object for Datastore/Firestore implementations to subclass.
        This holds the Datastore/Firestore client. All roads and RPC calls lead back to this object.
    """

    def __init__(self, wrapper, params):
        self.wrapper = wrapper
        self.creation = wrapper.creation
        self.ops = wrapper.ops
        self.queries = []
        self.settings_dict = params
        self.namespace = wrapper.namespace
        self.database = wrapper.database

        self._client = self._create_client(
            params['PROJECT'],
            database=self.database,
            namespace=self.namespace,
        )

        self._autocommit = True
        self._txn = None
        self._seen_keys = set()
        self._cache = {}

        # On non-rel platforms often inside a transaction,
        # you can't perform any read after performing any write. So... if we're inside
        # transaction we "stage" the write and pretend it succeeded, and then do the actual
        # write on transaction commit. We stage these documents by reference so that we
        # only apply the final write for each key
        self._staged_writes = {}

    def _stage_write(self, entity_or_key, kind):
        if kind == StagedWriteKind.DELETE:
            assert (isinstance(entity_or_key, Key))
            self._staged_writes[entity_or_key] = (kind, None)
        else:
            if kind == StagedWriteKind.UPDATE:
                # There is a potential edge case where in the same transaction
                # you do the following:
                # 1. Create a entity
                # 2. Update the entity
                # Here, if we receive an update for an existing staged INSERT
                # we replace the contents of the INSERT and don't stage an update
                # so at the end of the transaction it looks like there was just
                # one INSERT with the final data
                if (
                        entity_or_key.key() in self._staged_writes
                        and self._staged_writes[entity_or_key.key()][0] == StagedWriteKind.INSERT
                ):
                    self._staged_writes[entity_or_key.key()][1] = entity_or_key
                else:
                    self._staged_writes[entity_or_key.key()] = (kind, entity_or_key)
            else:
                self._staged_writes[entity_or_key.key()] = (kind, entity_or_key)

    def _apply_staged_writes(self):
        if not self._staged_writes:
            return

        assert (self._txn is not None)

        insert_keys, insert_entities = [], []
        delete_keys = []

        for key, (kind, entity) in self._staged_writes.items():
            if kind == StagedWriteKind.DELETE:
                delete_keys.append(key)
            else:
                insert_keys.append(key)
                insert_entities.append(entity)

        self._put(insert_keys, insert_entities)
        self._delete(delete_keys)
        self._staged_writes.clear()

    def _cache_entity(self, entity):
        if self._txn is not None:
            self._cache[entity.key()] = entity

    def _find_entity_in_cache(self, field_values: List[Tuple[str, str]]) -> Optional[Entity]:
        for entity in self._cache.values():
            if all([entity._properties.get(k) == v for k, v in field_values]):
                return entity

    def _entity_from_cache(self, key) -> Optional[Entity]:
        if self._txn is not None:
            return self._cache.get(key)

    def _create_client(self, project, database=None, namespace=None):
        raise NotImplementedError()

    def _close_client(self):
        raise NotImplementedError()

    def _begin(self):
        raise NotImplementedError()

    def _rollback(self):
        raise NotImplementedError()

    def _commit(self):
        raise NotImplementedError()

    def _put(self, key_or_keys, entity_or_entities) -> Optional[Union[Entity, Iterable[Entity]]]:
        raise NotImplementedError()

    def _get(self, key_or_keys) -> Union[Entity, Iterable[Entity]]:
        """
            Should return a list of one or more entities
            from the provided keys
        """
        raise NotImplementedError()

    def _delete(self, key_or_keys: Union[Key, Iterable[Key]]):
        raise NotImplementedError()

    def _exists(self, key) -> bool:
        raise NotImplementedError()

    def new_key(self, table, id_or_name, parent=None, namespace=None) -> Key:
        raise NotImplementedError()

    def begin(self):
        self._seen_keys = set()
        self._cache = {}
        self._staged_writes.clear()
        return self._begin()

    def rollback(self):
        try:
            if self._txn is not None:
                return self._rollback()
        finally:
            self._txn = None
            self._cache = {}
            self._seen_keys = set()
            self._staged_writes.clear()

    def _check_unique_constraints(self, puts, deletes):
        # deletes is always a list of keys
        deleted_keys = set(deletes)

        def unique_check(entity, stored, combination):
            if stored and stored[0]:
                stored = stored[0]

                # If the existing entity is being deleted
                # then ignore it
                if stored.key() in deleted_keys:
                    return False

                if stored.key() == entity.key():
                    # Same key, ignore
                    return False

                # If the stored item is in the cache, but the
                # values differ, then we're OK
                from_cache = self._cache.get(stored.key())
                if from_cache:
                    if any([
                        entity.get(field) != from_cache.get(field)
                        for field in combination
                    ]):
                        return False

                return True
            return False

        poly_model_property = self.wrapper.polymodel_property_name()

        check_unique_markers_in_memory(self.wrapper, puts)

        for entity in puts:
            key = entity.key() if hasattr(entity, "key") else entity

            if entity.get(poly_model_property):
                model = get_bottom_concrete_model(entity[poly_model_property])
            else:
                model = get_model_from_db_table(key.path[-1])

            if model and has_unique_constraints(model):
                perform_unique_checks(
                    self.wrapper,
                    model,
                    entity,
                    test_fn=lambda stored, combination: unique_check(
                        entity, stored, combination
                    )
                )

    def commit(self):
        puts, deletes = [], []
        for key, (kind, entity) in self._staged_writes.items():
            if kind == StagedWriteKind.INSERT:
                puts.append(entity)
            elif kind == StagedWriteKind.UPDATE:
                puts.append(entity)
            else:
                assert (kind == StagedWriteKind.DELETE)
                deletes.append(key)

        self._check_unique_constraints(puts, deletes)

        self.wrapper.pre_commit(puts, deletes)
        self._apply_staged_writes()
        try:
            self._commit()
        finally:
            self._txn = None
            self._cache = {}
            self._seen_keys = set()
            self._staged_writes.clear()

    def savepoint(self, sid):
        raise NotImplementedError()

    def savepoint_commit(self, sid):
        raise NotImplementedError()

    def savepoint_rollback(self, sid):
        raise NotImplementedError()

    def exists(self, key) -> bool:
        return self._exists(key)

    def put(self, entity, allow_existing=True):
        key = entity.key()
        new = not self.exists(key)

        if not new and not allow_existing:
            raise IntegrityError("Tried to INSERT with existing key")

        if self._txn is not None:
            self._stage_write(entity, StagedWriteKind.INSERT if new else StagedWriteKind.UPDATE)
            self._cache_entity(entity)
        else:
            if new:
                updated_entity = self._put(key, entity)
            else:
                updated_entity = self._put(key, entity)

            if not updated_entity:
                return

            key = updated_entity.key()

        self._seen_keys.add(key)

    def get(self, key_or_keys):
        is_list = hasattr(key_or_keys, "__iter__") and not isinstance(key_or_keys, str)
        if not is_list:
            keys = [key_or_keys]
        else:
            keys = key_or_keys

        # Get what we can from the cache - this will be empty
        # if we're not in a transaction
        cached = [self._entity_from_cache(key) for key in keys]

        # Make a list of all the keys that weren't cached
        to_fetch = []
        for key, ent in zip(keys, cached):
            if not ent:
                to_fetch.append(key)

        # Fetch the ones we need
        fetched = self._get(to_fetch)
        fetched = {x.key(): x for x in fetched if x}

        # Build results in the original order the keys
        # were provided
        results = []
        for key, ent in zip(keys, cached):
            result = ent or fetched.get(key)
            if result:
                results.append(result)
                self._seen_keys.add(key)

        if is_list:
            return results
        else:
            return results[0] if results else None

    def delete(self, key: Key):
        if self._txn is not None:
            self._stage_write(key, StagedWriteKind.DELETE)

            # FIXME: Mark the entity as deleted in the cache.
            # This is different to removing from the cache because
            # we want subsequent gets to fail, not hit the database.
        else:
            return self._delete(key)

    def _flush(self, tables, namespace=None):
        raise NotImplementedError()

    def flush(self, tables, namespace=None, database=None):
        return self._flush(tables, namespace, database)

    def close(self):
        self._close_client()

    @property
    def autocommit(self):
        return self._autocommit

    @autocommit.setter
    def autocommit(self, value):
        if value and not self._autocommit:
            self.rollback()
        elif not value and self._autocommit:
            self.begin()
        self._autocommit = value


class Cursor(object):
    """ Dummy cursor class """

    def __init__(self, connection):
        self.connection = connection
        self.start_cursor = None
        self.returned_ids = []
        self.rowcount = -1
        self.last_select_command: Optional[SelectCommand] = None
        self.last_delete_command = None

    def execute(self, sql, *params):
        if isinstance(sql, SelectCommand):
            # Also catches subclasses of SelectCommand (e.g Update)
            self.last_select_command = sql
            self.rowcount = self.last_select_command.execute() or -1
        elif isinstance(sql, FlushCommand):
            sql.execute()
        elif isinstance(sql, UpdateCommand):
            self.rowcount = sql.execute()
        elif isinstance(sql, DeleteCommand):
            self.rowcount = sql.execute()
        elif isinstance(sql, InsertCommand):
            self.connection.queries.append(sql)
            self.returned_ids = sql.execute()
        else:
            raise ValueError(
                "Can't execute traditional SQL: '%s' (although perhaps we could make GQL work)" % sql
            )

    def next(self):
        row = self.fetchone()
        if row is None:
            raise StopIteration
        return row

    def fetchone(self, delete_flag=False):
        try:
            result = next(self.last_select_command.results)

            if isinstance(result, int):
                return (result,)

            row = []

            for col in self.last_select_command.init_list:
                if col == self.last_select_command.model._meta.pk.column:
                    row.append(result.key().id_or_name)
                else:
                    row.append(result.get(col))

            self.returned_ids.append(result.key().id_or_name)
            return row
        except StopIteration:
            return None

    def fetchmany(self, size, delete_flag=False):
        if not self.last_select_command.results:
            return []

        result = []
        for i in range(size):
            entity = self.fetchone(delete_flag)
            if entity is None:
                break

            # Python DB API suggests a list of tuples, and returning
            # a list-of-lists breaks some tests
            result.append(tuple(entity))

        return result

    @property
    def lastrowid(self):
        return self.returned_ids[-1].id_or_name

    def __iter__(self):
        return self

    def close(self):
        pass


class Wrapper:
    """
        A base class for all connections in gcloudc. This defines some additional
        operation methods we expect each backend to implement.
    """

    TRANSACTION_ENTITY_LIMIT = 500

    array_not_empty_operator_and_value = (">", None)
    array_empty_operator_and_value = ("=", None)
    supports_empty_array = False
    supports_only_null_equality = False

    # If this is True, we can get away with storing much less
    # data when doing contains/icontains queries.
    supports_range_queries_on_array = False

    def __init__(self, *args, **kwargs):
        self.connection = None
        super().__init__(*args, **kwargs)

    def _set_autocommit(self, autocommit):
        if not self.connection:
            raise ValueError("No valid connection")

        self.connection.autocommit = autocommit

    def is_usable(self):
        return True

    def get_connection_params(self):
        if not self.settings_dict.get("INDEXES_FILE"):
            raise ImproperlyConfigured("You must specify an INDEXES_FILE in the DATABASES setting")

        return self.settings_dict.copy()

    def _create_connection(self, params):
        raise NotImplementedError()

    def get_new_connection(self, params):
        conn = self._create_connection(params)
        load_special_indexes(conn)  # make sure special indexes are loaded
        return conn

    def init_connection_state(self):
        pass

    def create_cursor(self, name=None):
        self.name = name
        self.ensure_connection()
        return Cursor(self.connection)

    def get_query_class(self):
        raise NotImplementedError()

    def is_id_valid(self, value) -> bool:
        if isinstance(value, int) and value != 0:
            return True
        elif isinstance(value, str) and value and not value.startswith("__"):
            return True

        return False

    def transform_django_query(self, query, force_keys_only):
        """
            This is where the magic happens! We take a Django Query object, manipulate it
            so that it's suitable for a non-relational backend and then return an ORQuery
            that can be executed.
        """

        from gcloudc.db.backends.common.parsers import base
        parser = base.BaseParser(query, self)
        return parser.get_transformed_query(
            self,
            force_keys_only=force_keys_only
        )

    def namespace(self):
        """
            Returns the namespace of this connection if any. This is normally
            specified in DATABASES, but not all backends support it. If it's unsupported
            then return None.
        """
        raise NotImplementedError()

    def database(self):
        """
            Returns the database of this connection if any. This is normally
            specified in DATABASES, but not all backends support it. If it's unsupported
            then return None.
        """
        raise NotImplementedError()

    def generate_id(self, type):
        raise NotImplementedError()

    def reserve_id(self, table, id_or_name, namespace):
        raise NotImplementedError()

    def key_property_name(self):
        """
            Return the name of the "Key" field, e.g. __key__ or __name__
        """
        raise NotImplementedError()

    def polymodel_property_name(self):
        """
            Ideally this would be the same on all backends, but
            Datastore used the (problematic) "class", so for backwards
            compatibility we need to be able to switch based
            on the backend
        """

        raise NotImplementedError()

    def to_native_key(self, key):
        """
            When given a Key object, this should return the native
            type.
        """
        raise NotImplementedError()

    def from_native_key(self, key) -> Key:
        """
            Returns an equivalent Key object to the native key passed
            in.
        """
        raise NotImplementedError()

    def to_native_entity(self, entity: Entity):
        """
            When given an Entity object, this should return the same
            thing as a native type.
        """
        raise NotImplementedError()

    def from_native_entity(self, entity_or_key) -> Entity:
        """
            Takes a native entity returned from a query, and turns it into an
            Entity object. If the argument is a key this should be an "empty" entity
            with just the key set.
        """
        raise NotImplementedError()

    def pre_entity_insert(self, model, entity, constraints):
        pass

    def post_entity_insert(self, model, entity, constraints):
        pass

    def pre_entity_update(self, model, entity, constraints):
        pass

    def post_entity_update(self, model, entity, constraints):
        pass

    def pre_entity_delete(self, model, entity, constraints):
        pass

    def post_entity_delete(self, model, entity, constraints):
        pass

    def pre_commit(self, puts, deletes):
        pass

    def _savepoint(self, sid):
        self.connection.savepoint(sid)

    def _savepoint_rollback(self, sid):
        self.connection.savepoint_rollback(sid)

    def _savepoint_commit(self, sid):
        self.connection.savepoint_commit(sid)

    def get_transaction_entity_limit(self) -> Optional[int]:
        """
            Returns the number of entities that can be read/written
            within a transaction. Return None if there is no limit
        """

        return 500

    @cached_property
    def _count_mode(self) -> CountMode:
        count_mode = self.settings_dict.get("OPTIONS", {}).get("count_mode", "native")
        allowed_modes = get_args(CountMode)
        if count_mode not in allowed_modes:
            raise ImproperlyConfigured(f"Invalid count_mode {count_mode}, allowed values: {', '.join(allowed_modes)}")
        return count_mode


MAXINT = 9223372036854775808
_BULK_BATCH_SIZE_SETTING = "BULK_BATCH_SIZE"


class NoSQLDatabaseOperations(BaseDatabaseOperations):
    compiler_module = "gcloudc.db.backends.datastore.compiler"

    # Datastore will store all integers as 64bit long values
    integer_field_ranges = {
        "SmallIntegerField": (-MAXINT, MAXINT - 1),
        "IntegerField": (-MAXINT, MAXINT - 1),
        "BigIntegerField": (-MAXINT, MAXINT - 1),
        "PositiveSmallIntegerField": (0, MAXINT - 1),
        "PositiveBigIntegerField": (0, MAXINT - 1),
        "PositiveIntegerField": (0, MAXINT - 1),
        "SmallAutoField": (-MAXINT, MAXINT - 1),
        "AutoField": (-MAXINT, MAXINT - 1),
        "BigAutoField": (-MAXINT, MAXINT - 1),
    }

    def bulk_batch_size(self, field, objs):
        # This value is used in cascade deletions, and also on bulk insertions
        # This is the limit of the number of entities that can be manipulated in
        # a single transaction

        settings_dict = self.connection.settings_dict
        if _BULK_BATCH_SIZE_SETTING in settings_dict['OPTIONS']:
            return int(settings_dict['OPTIONS'][_BULK_BATCH_SIZE_SETTING])
        return 500

    def quote_name(self, name):
        return name

    def date_trunc_sql(self, lookup_type, sql, params, tzname=None):
        return "", []

    def datetime_trunc_sql(self, lookup_type, sql, params, tzname):
        return "", []

    def datetime_extract_sql(self, lookup_type, sql, params, tzname):
        return "", []

    def date_extract_sql(self, lookup_type, sql, params):
        return "", []

    def get_db_converters(self, expression):
        converters = super().get_db_converters(expression)

        db_type = expression.field.db_type(self.connection)
        internal_type = expression.field.get_internal_type()

        if internal_type == "TextField":
            converters.append(self.convert_textfield_value)
        elif internal_type == "DateTimeField":
            converters.append(self.convert_datetime_value)
        elif internal_type == "DateField":
            converters.append(self.convert_date_value)
        elif internal_type == "TimeField":
            converters.append(self.convert_time_value)
        elif internal_type == "DecimalField":
            converters.append(self.convert_decimal_value)
        elif internal_type == 'UUIDField':
            converters.append(self.convert_uuidfield_value)
        elif db_type == "list":
            converters.append(self.convert_list_value)
        elif db_type == "set":
            converters.append(self.convert_set_value)

        return converters

    def convert_uuidfield_value(self, value, expression, connection):
        if value is not None:
            value = uuid.UUID(value)
        return value

    def convert_textfield_value(self, value, expression, connection):
        if isinstance(value, bytes):
            # Should we log a warning here? It shouldn't have been stored as bytes
            value = value.decode("utf-8")
        return value

    def convert_datetime_value(self, value, expression, connection):
        return self.connection.ops.value_from_db_datetime(value)

    def convert_date_value(self, value, expression, connection):
        return self.connection.ops.value_from_db_date(value)

    def convert_time_value(self, value, expression, connection):
        return self.connection.ops.value_from_db_time(value)

    def convert_decimal_value(self, value, expression, connection):
        return self.connection.ops.value_from_db_decimal(value)

    def convert_list_value(self, value, expression, connection):
        if expression.output_field.db_type(connection) != "list":
            return value

        if not value:
            value = []
        return value

    def convert_set_value(self, value, expression, connection):
        if expression.output_field.db_type(connection) != "set":
            return value

        if not value:
            value = set()
        else:
            value = set(value)
        return value

    def sql_flush(self, style, tables, allow_cascade=False, reset_sequences=False, *args, **kwargs):
        additional_djangaeidx_tables = [
            x
            for x in self.connection.introspection.table_names()
            if [y for y in tables if x.startswith("_djangae_idx_{}".format(y))]
        ]

        return [
            FlushCommand(None, table, self.connection)
            for table in tables + additional_djangaeidx_tables
        ]

    def execute_sql_flush(self, sql_list):
        """Execute a list of SQL statements to flush the database."""
        with self.connection.cursor() as cursor:
            for sql in sql_list:
                cursor.execute(sql)

    def value_for_db(self, value, field):
        if value is None:
            return None

        db_type = field.db_type(self.connection)

        if db_type in ("integer", "long"):
            if isinstance(value, float):
                # round() always returns a float, which has a smaller max value than an int
                # so only round() it if it's already a float
                value = round(value)

            value = int(value)
        elif db_type == "float":
            value = float(value)
        elif db_type == "string" or db_type == "text":
            value = coerce_unicode(value)
        elif db_type == "bytes":
            # Store BlobField, DictField and EmbeddedModelField values as Blobs.
            # We encode to bytes, as that's what the Cloud Datastore API expects
            # we use ASCII to make sure there's no funky unicode data, it should
            # be binary
            if isinstance(value, str):
                value = value.encode("ascii")
        elif db_type == "decimal":
            value = self.adapt_decimalfield_value(value, field.max_digits, field.decimal_places)
        elif db_type in ("list", "set"):
            if hasattr(value, "__len__") and not value:
                if not self.connection.supports_empty_array:
                    value = None  # Convert empty lists to None
                else:
                    value = []
            elif hasattr(value, "__iter__"):
                # Convert sets to lists
                value = list(value)

        return value

    def last_insert_id(self, cursor, db_table, column):
        return cursor.lastrowid

    def last_executed_query(self, cursor, sql, params):
        """
            We shouldn't have to override this, but Django's BaseOperations.last_executed_query
            assumes does u"QUERY = %r" % (sql) which blows up if you have encode unicode characters
            in your SQL. Technically this is a bug in Django for assuming that sql is ASCII but
            it's only our backend that will ever trigger the problem
        """
        return u"QUERY = {}".format(smart_str(sql))

    def fetch_returned_insert_id(self, cursor):
        return cursor.lastrowid

    def adapt_datetimefield_value(self, value):
        value = make_utc_compatible(value)
        return value

    def value_to_db_datetime(self, value):  # Django 1.8 compatibility
        return self.adapt_datetimefield_value(value)

    def adapt_datefield_value(self, value):
        if value is not None:
            value = datetime.datetime.combine(value, datetime.time())
        return value

    def adapt_timefield_value(self, value):
        if value is not None:
            value = make_utc_compatible(value)
            value = datetime.datetime.combine(datetime.datetime.utcfromtimestamp(0), value)
        return value

    def adapt_decimalfield_value(self, value, max_digits, decimal_places):
        if isinstance(value, decimal.Decimal):
            return decimal_to_string(value, max_digits, decimal_places)
        return value

    def value_to_db_decimal(self, value, max_digits, decimal_places):  # Django 1.8 compatibility
        return self.adapt_decimalfield_value(value, max_digits, decimal_places)

    # Unlike value_to_db, these are not overridden or standard Django, it's just nice to have symmetry
    def value_from_db_datetime(self, value):

        # Convert to a regular datetime.datetime
        if isinstance(value, DatetimeWithNanoseconds):
            if not settings.USE_TZ:
                # we always receive a timezone.utc set, even when there is no timezone enabled
                value = value.utcfromtimestamp(value.timestamp())
            else:
                value = datetime.datetime.fromtimestamp(value.timestamp(), tz=value.tzinfo)

        if isinstance(value, int):
            # App Engine Query's don't return datetime fields (unlike Get) I HAVE NO IDEA WHY
            value = ensure_datetime(value)
        if value is not None and settings.USE_TZ and timezone.is_naive(value):
            value = value.replace(tzinfo=tz.utc)
        return value

    def value_from_db_date(self, value):
        if isinstance(value, int):
            # App Engine Query's don't return datetime fields (unlike Get) I HAVE NO IDEA WHY
            value = ensure_datetime(value)

        if value:
            value = value.date()
        return value

    def value_from_db_time(self, value):
        if isinstance(value, (DatetimeWithNanoseconds, int)):
            # App Engine Queries don't return datetime fields (unlike Get) I HAVE NO IDEA WHY
            value = ensure_datetime(value)

        if value is not None and settings.USE_TZ and timezone.is_naive(value):
            value = value.replace(tzinfo=tz.utc)

        if value:
            value = value.time()

        return value

    def value_from_db_decimal(self, value):
        if value:
            value = decimal.Decimal(value)
        return value
