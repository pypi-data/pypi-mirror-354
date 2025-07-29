import logging
import string
import secrets

from typing import Optional, Union, Iterable

from gcloudc.db.backends.common.base.entity import Entity
from django.db import NotSupportedError
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.base.client import BaseDatabaseClient
from django.db.backends.base.creation import BaseDatabaseCreation
from django.db.backends.base.features import BaseDatabaseFeatures
from django.db.backends.base.introspection import (
    TableInfo,
)

from ..common.base.introspection import NoSQLDatabaseIntrospection
from ..common.base.schema import NoSQLDatabaseSchemaEditor
from django.db.backends.base.validation import BaseDatabaseValidation
from django.core.exceptions import ImproperlyConfigured
from google.cloud import (
    firestore,
)
from google.cloud.firestore_v1.collection import CollectionReference
from google.cloud.firestore_v1.query import CollectionGroup

from gcloudc.db.backends.common.base.connection import Connection as NoSQLConnection, Wrapper, NoSQLDatabaseOperations
from gcloudc.db.backends.common.base.entity import Key
from gcloudc.db.backends.common.base.query import Query as NoSQLQuery
from gcloudc.db.backends.common.base import dbapi as Database

from gcloudc.db.backends.common.helpers import (
    entity_matches_query,
    log_once
)


logger = logging.getLogger(__name__)

# Maximum string length of a signed 64 bit integer
# plus room for the negative sign
INTEGER_KEY_LENGTH = len(str((2 ** 64)))

INEQUALITY_OPERATORS = frozenset([">", "<", "<=", ">="])


def string_is_integer(s: str, digits_number=INTEGER_KEY_LENGTH):
    return (
        s
        and isinstance(s, str)
        and len(s) == digits_number
        and all([x in string.digits + "-" for x in s])
    )


class Connection(NoSQLConnection):

    def _create_client(self, project, database=None, namespace=None):
        if namespace:
            raise ImproperlyConfigured("Firestore doesn't support namespaces")

        kwargs = {"project": project}
        if database:
            # The default value is "(default)", not None, and could change, so only
            # pass this if we have a value
            kwargs["database"] = database
        return firestore.Client(**kwargs)

    def _close_client(self):
        try:
            if self._client:
                self._client.close()
        except TypeError:
            # FIXME: Calling close causes an error inside
            # the firestore connector.. .I'm not sure why. Might only
            # happen locally when using requests.Session
            pass

    def _begin(self):
        assert (self._txn is None)
        self._txn = self._client.transaction()
        self._txn._clean_up()
        self._txn._begin()

        assert (self._txn is not None)
        assert (self._txn.in_progress)

    def _commit(self):
        assert (self._txn is not None)
        self._txn._commit()

    def _rollback(self):
        assert (self._txn is not None)
        self._txn._rollback()

    def _exists(self, key):
        key = self.wrapper.to_native_key(key)
        existing = key.get(transaction=self._txn)
        return existing.exists

    def _delete(self, key_or_keys: Union[Key, Iterable[Key]]):
        is_list = hasattr(key_or_keys, "__iter__")
        if not is_list:
            key_or_keys = [key_or_keys]

        for key in key_or_keys:
            key = self.wrapper.to_native_key(key)
            if self._txn is not None:
                self._txn.delete(key)
            else:
                key.delete()

    def _flush(self, tables, namespace=None, database=None):
        # The local datastore emulator explodes if you try to delete more than 500
        # things in a single batch. So we just iterate in batches of 500.
        limit = 500

        def delete_collection(coll_ref, batch_size):
            query = coll_ref.order_by("__name__").limit(batch_size)
            docs = [x for x in query.stream()]
            while docs:
                last_pk = None
                for doc in docs:
                    last_pk = doc.id
                    doc.reference.delete()

                query = coll_ref.order_by("__name__").start_after({"__name__": last_pk}).limit(batch_size)
                docs = [x for x in query.stream()]

        for table in tables:
            delete_collection(self._client.collection(table), limit)

    def _get(self, key_or_keys) -> Iterable[Entity]:
        """
            Should return a list of one or more entities
            from the provided keys
        """
        if isinstance(key_or_keys, Key):
            result = self.wrapper.to_native_key(key_or_keys).get(transaction=self._txn)
            return [self.wrapper.from_native_entity(result)] if result.exists else []
        else:
            results = [self.wrapper.to_native_key(x).get(transaction=self._txn) for x in key_or_keys]
            return [self.wrapper.from_native_entity(x) for x in results if x is not None and x.exists]

    def _put(self, key_or_keys, entity_or_entities) -> Optional[Union[Entity, Iterable[Entity]]]:
        is_list = hasattr(key_or_keys, "__iter__")

        if not is_list:
            key_or_keys = [key_or_keys]
            entity_or_entities = [entity_or_entities]

        result = []
        for key, entity in zip(key_or_keys, entity_or_entities):
            native_entity = self.wrapper.to_native_entity(entity)
            native_key = self.wrapper.to_native_key(key)

            if entity._properties_to_exclude_from_index:
                msg = (
                    f"Trying to exclude {','.join(entity._properties_to_exclude_from_index)} "
                    f"from indexing on collection <{entity.key().path}> \n"
                    "Firestore doesn't support excluding fields from indexing programmatically. "
                    "You should instead add an index exemption, see  https://cloud.google.com/firestore/docs/query-data/indexing#:~:text=Single%2Dfield%20index%20exemptions%20allow,go%20to%20the%20Databases%20page.&text=Select%20the%20required%20database%20from%20the%20list%20of%20databases.,-In%20the%20navigation"  # noqa: E501
                )
                log_once(
                    logger,
                    msg,
                    method="warn"
                )

            if self._txn is not None:
                self._txn.set(native_key, native_entity, merge=False)
                result.append(entity)
            else:
                native_key.set(native_entity, merge=False)
                result.append(entity)

        if is_list:
            return result
        else:
            return result[0]

    def new_key(self, table, id_or_name, parent: Optional[Key] = None, namespace=None) -> Key:
        if parent and parent.is_partial():
            raise ValueError("Can't set an incomplete ancestor")

        if namespace:
            raise ValueError("Namespace is not valid on Firestore")

        path = [table]

        if parent:
            path = list(parent.path) + [parent.id_or_name] + path

        return Key(path, id_or_name)


class Query(NoSQLQuery):
    def __init__(self, connection, table_or_path, namespace=None, is_nested_collection=False, *args, **kwargs):
        super().__init__(
            connection, table_or_path,
            namespace=namespace,
            is_nested_collection=is_nested_collection,
            *args,
            **kwargs
        )
        assert (not isinstance(table_or_path, str))

        if len(table_or_path) % 2 == 0:
            path = table_or_path[:-1]
        else:
            path = table_or_path

            if len(table_or_path) != 1:
                # Not sure how to best deal with this. In this case we have a path
                # but it is a partial path (missing the ID part) and so we can't
                # construct an ancestor
                logger.warn("Got partial path for query")

        self._empty_result_set = False
        self._distinct_on = []
        collection = CollectionReference(*path, client=connection.connection._client)

        if (is_nested_collection):
            # In order to be able to query across nested collection, we need to use a CollectionGroupReference
            self._query = CollectionGroup(collection)
        else:
            self._query = collection

    def _add_filter(self, column, operator, value):
        if (
            self._is_array_contains_all_filter_on_iterable(operator, value) and
            len(self._get_array_and_filters()) > 0
        ):
            # Firestore doesn't support 'AND' filter on an array natively.
            # We avoid to add the filter and do the filtering in memory while fetching.
            return

        if isinstance(value, Key):
            value = self.wrapper.to_native_key(value)

        if operator == "=":
            operator = "=="

        # Comparisons with None can only be an equality, so if the operator is something else we need
        # to handle it manually
        if value is None:

            if operator == ">":
                # TL;DR
                # For this we need to rely on `start_with` and `end_before``.
                # To do that we need to make sure the query is ordered by the column we are filtering on.
                # So we need to handle this in the fetch method, once we know the ordering of the query.
                #
                # According to the
                # [documentation](https://cloud.google.com/firestore/docs/concepts/data-types#value_type_ordering)
                # we should be able here to use:
                # operator = ">"
                # value = ''
                # given that None < Bool < NaN < Number < Dates < String < Bytes < Reference < GeoPoint < Array < Map
                #
                # However this doesn't seem to work as expected.
                # From a quick test, it seems firestore tries to be clever and returns only the entities with a value
                # type that matches the one in the fitler. (ie. if the filter is 'foo' '>' datetime.datetime(), it will
                # return only the entities with a property 'foo' that is a datetime.datetime() object and the value
                # is greater than the one provided, and not the ones that habe strings for instance).
                # For that reason we are using "start_after" below instead.
                # To do that we need need to make sure the ordering of the query is on the given column.
                # For this reason this case is handled in the fetch method.
                return
            elif operator == ">=":
                return  # Do nothing, this is everything
            elif operator == "<":
                # Nothing is < None
                self._empty_result_set = True
            elif operator == "<=":
                operator = "=="

        if isinstance(value, (list, set, tuple)) and value:
            if operator == "array_contains_all":
                operator = "array_contains_any"
            else:
                # FIXME: it seems like we actually can?
                # https://cloud.google.com/firestore/docs/query-data/queries#in_not-in_and_array-contains-any
                raise ValueError("Can't support list lookups")

        self._query = self._query.where(filter=firestore.FieldFilter(column, operator, value))

    def distinct_on(self, fields):
        self._distinct_on = fields

    def _order_by(self, orderings):
        for order in orderings:
            if order.startswith("-"):
                self._query = self._query.order_by(
                    order.lstrip("-"),
                    direction=firestore.Query.DESCENDING
                )
            else:
                self._query = self._query.order_by(order)

    def _is_array_contains_all_filter_on_iterable(self, op, value):
        return op == "array_contains_all" and isinstance(value, (list, set, tuple))

    def _get_array_and_filters(self):
        result = []

        for (col, op), value in self._filters.items():
            # FIXME?: What if there are multiple list values? That shouldn't happen
            # but this will ignore that situation.
            if self._is_array_contains_all_filter_on_iterable(op, value):
                result.append((col, op, value[0]))

        return result

    def _has_equality_on_key_and_inequality_or_ordering_without_key(self):
        """
            This is a terrible fudge over this ridiculous Firestore restriction:

            > Equality on key is not allowed if there are other inequality fields and
            > key does not appear in inequalities.

            It also seems to be the case that you cannot have an equality on key if there is also
            an ordering which does not contain the key.

            To avoid this situation, if we have a key equality filter, and we are
            filtering on other fields with an inequality (e.g. <, <=, >, >=) or we are ordering by
            other fields then we do a datastore get instead and filter manually
        """

        if not self.has_filter("__name__", "="):
            return False

        if self._orderings and self._orderings[0].lstrip("-") != "__name__":
            # Returning True here causes us to use `_stream_from_get`, which doesn't apply any
            # ordering, but given that we've got an *equality* on a *single* key, ordering is
            # irrelevant
            return True

        inequality_properties = set()
        for (col, op) in self._filters:
            if op in INEQUALITY_OPERATORS:
                inequality_properties.add(col)

        return inequality_properties and "__name__" not in inequality_properties

    def _get_null_inequality_filters(self):
        """
            Return a list of filters that are inequalities with None
        """
        return [
            (col, op, values)
            for (col, op), values in self._filters.items()
            if None in values and op in INEQUALITY_OPERATORS
        ]

    def _apply_null_inequalities(self):
        """
        Applies ">" inequality on null values to the query.
        The method relies on ordering of the query to be set, so it should ONLY be called after
        the ordering has been set.
        """
        inequalities_on_null = self._get_null_inequality_filters()

        # This should be already picked up by the parsing, but adding it for my own sanity.
        inequality_columns = set(x[0] for x in inequalities_on_null)
        assert len(inequality_columns) <= 1, "We can't have inequalities on more than one column"

        # We're doing this here, because to handle the inequalities on null, we need the orderings
        # that aren't available until the fetch.
        if inequalities_on_null:
            for (column, operator, value) in inequalities_on_null:
                if operator == ">":
                    # We need to make sure the query is ordered by the column we are filtering on to use start_after
                    # and end_before
                    if len(self._orderings) == 0:
                        self._query = self._query.order_by(column)
                        self._query = self._query.start_after({
                            column: None
                        })
                    else:
                        first_order = self._orderings[0]
                        if first_order not in (column, "-" + column):
                            raise NotSupportedError(
                                "Cannot have an inequality filter if the query's first sort column "
                                "is not the same column"
                            )

                        if self._orderings[0].startswith("-"):
                            self._query = self._query.end_before({
                                column: None
                            })
                        else:
                            self._query = self._query.start_after({
                                column: None
                            })
                    return

    def _stream_from_get(self, limit, offset):
        """
            Return results from using get
        """
        if limit == 0 or offset > 0:
            return

        entities = self.connection._get(self.get_filter("__name__", "="))
        for ent in entities:
            if ent and entity_matches_query(ent, self):
                yield ent

    def fetch(self, offset, limit):
        in_memory_pagination = False

        if self._distinct_on and (offset or limit):
            # Distinct can't be used with a query that has an offset or a limit.
            # Since Firestore doesn't support distinct natively
            # so we  do it in memory.
            in_memory_pagination = True
            warn_msg = "Firestore doesn't support distinct when setting an offset or limit. "

        if len(self._get_array_and_filters()) > 1:
            # Firestore also does not support 'AND' filter on an array natively.
            # so we do it in memory.
            in_memory_pagination = True
            warn_msg = "Firestore doesn't support multiple 'AND' filters on an array natively. "

        if in_memory_pagination:
            logger.warn(
                f"{warn_msg}To support these kind of queries we fetch all document and filter in memory.\n"
                "This should be avoided if possible since it can be slow and consume a lot of memory.\n"
                f"This warning was raised while fetching data from Collection <{self.path}>."
            )

            in_memory_pagination = True
            original_offset = offset or 0
            original_limit = limit
            offset = None
            limit = None

        if self._empty_result_set:
            return

        if self.only_return_keys:
            self._query = self._query.select(["__name__"])
        elif self.only_return_fields:
            self._query = self._query.select(self.only_return_fields)

        if offset:
            self._query = self._query.offset(offset)

        if limit is not None:
            self._query = self._query.limit(limit)

        seen = set()

        array_and_filters = self._get_array_and_filters()

        # Workaround for Firestore restriction
        if self._has_equality_on_key_and_inequality_or_ordering_without_key():
            for ent in self._stream_from_get(limit, offset):
                yield ent
            return

        self._apply_null_inequalities()
        index = 0

        for result in self._query.stream(transaction=self.connection._txn):
            if self._distinct_on:
                distinct_fields_values = tuple(result._data.get(x) for x in self._distinct_on)
                if distinct_fields_values in seen:
                    continue
                seen.add(distinct_fields_values)

            matches = True
            for col, _, value in array_and_filters:
                ent_data = result._data.get(col, [])
                if set(ent_data).intersection(set(value)) != set(value):
                    matches = False
                    break

            if matches:
                to_yield = True
                if in_memory_pagination:
                    if isinstance(original_offset, int) and (index < original_offset):
                        to_yield = False
                    if isinstance(original_limit, int) and index > original_offset + original_limit:
                        break

                if to_yield:
                    yield self.wrapper.from_native_entity(result)
                index = index + 1

    def count(self, limit: Optional[int]) -> int:
        if self.wrapper._count_mode == "native":
            return int(self._query.limit(limit).count().get()[0][0].value)
        self.only_return_keys = True
        return len([x for x in self.fetch(offset=None, limit=limit)])


class DatabaseOperations(NoSQLDatabaseOperations):
    compiler_module = "gcloudc.db.backends.firestore.compiler"


class DatabaseClient(BaseDatabaseClient):
    pass


class DatabaseCreation(BaseDatabaseCreation):
    data_types = {
        "AutoField": "long",
        "RelatedAutoField": "long",
        "ForeignKey": "long",
        "OneToOneField": "key",
        "ManyToManyField": "key",
        "AutoCharField": "string",
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
        assert (cursor.connection._txn is None)
        collections = [x for x in cursor.connection._client.collections()]
        return [TableInfo(x.id, "t") for x in collections]

    def get_sequences(self, cursor, table_name, table_fields=()):
        # __key__ is the only column that can auto-populate
        return [{'table': table_name, 'column': cursor.connection.key_property_name()}]


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
    INTEGER_KEY_LENGTH = INTEGER_KEY_LENGTH

    array_not_empty_operator_and_value = ("!=", [])
    array_empty_operator_and_value = ("=", [])
    supports_empty_array = True
    supports_only_null_equality = True

    data_types = DatabaseCreation.data_types  # These moved in 1.8

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
        return "__name__"

    def schema_editor(self, *args, **kwargs):
        return DatabaseSchemaEditor(self, *args, **kwargs)

    def reserve_id(self, kind, id_or_name, namespace):
        # Firestore IDs are strings and don't need to be reserved
        pass

    def generate_id(self, kind):
        """
            The Firestore API won't generate keys automatically until a
            transaction commits, that's too late!

            This string ID generation is based on that found in the Node SDK for Firebase
            the integer generation is just a 63 bit integer (as IDs on the Datastore are
            signed 64 bit numbers so we don't use the sign bit and create negative ones)
        """
        assert (kind in (int, str))

        if kind is int:
            return secrets.randbits(63)
        else:
            # If the key type is a string it should not look like an integer string
            # because of the hack in `from_native_key`.
            is_an_integer_id = True
            while is_an_integer_id:
                auto_id = []
                allowed_chars = string.ascii_letters + string.digits
                for _ in range(20):
                    auto_id.append(secrets.choice(allowed_chars))
                id = "".join(auto_id)
                is_an_integer_id = string_is_integer(id)
        return id

    def to_native_key(self, key: Key):
        assert (not key.namespace)

        path = list(key.path) + [key.id_or_name]

        for i in range(len(path)):
            name = path[i]

            if isinstance(name, int):
                # Firestore works in strings, not integers, and to make ordering work
                # correctly we need to pad our integer with zeros.
                length = len(str(2 ** 64))
                if name >= 0:
                    name = str(name)
                    padding = length - len(name)
                    name = ('0' * padding) + name
                else:
                    name = str(abs(name))
                    padding = length - len(name) - 1
                    name = '-' + ('0' * padding) + name
                path[i] = name

        path, name = path[:-1], path[-1]

        return self.connection._client.document(
            *path,
            name
        )

    def from_native_key(self, key):
        path = key.path.split("/")
        assert (path[-1] == key.id)

        # FIXME: Terrible hack.
        # `generate_id` relates to this, if fixed we should change that
        # as well
        # Firestore doesn't support integer keys, so
        # when we need to store an integer, we convert it
        # to a zero-padded string of length = len(str(2 ** 64))
        # Here we convert to an integer if:
        # - The string is this length
        # - It only includes digits or "-"

        def get_int_or_string(id_or_name):
            if string_is_integer(id_or_name):
                return int(id_or_name)
            return id_or_name

        path = [
            x if index % 2 == 0
            else get_int_or_string(x) for index, x in enumerate(path)
        ]

        return Key(path[:-1], path[-1])

    def from_native_entity(self, entity_or_key) -> Entity:
        """
            Takes a native entity returned from a query, and turns it into an
            Entity object. If the argument is a key this should be an "empty" entity
            with just the key set.
        """
        if entity_or_key is None:
            return None

        if isinstance(entity_or_key, firestore.DocumentReference):
            return Entity(self.from_native_key(entity_or_key))
        else:
            ent = Entity(
                self.from_native_key(entity_or_key.reference),
            )

            data = entity_or_key.to_dict()

            for key in data:
                ent[key] = data[key]

            return ent

    def to_native_entity(self, entity: Entity):
        """
            Firestore is weird, you insert dictionaries, and get
            back DocumentSnapshot. We return a dictionary of properties
            here and handle it appropriately in _put
        """
        return entity._properties

    def polymodel_property_name(self):
        return "_class_"
