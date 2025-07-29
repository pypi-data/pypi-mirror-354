import copy
import logging
from datetime import datetime

from django.db import (
    DatabaseError,
    IntegrityError,
    OperationalError,
)
from django.db.models.expressions import Star
from django.utils.encoding import (
    force_str,
)

from gcloudc.db.backends.common.base.entity import Entity
from gcloudc.db.backends.common import helpers
from django.db.transaction import atomic
from gcloudc.db.backends.common.base.dbapi import NotSupportedError

from .formatting import generate_sql_representation
from gcloudc.db.backends.common.constraints import (
    _unique_combinations,
    CONSTRAINT_VIOLATION_MSG,
)

from gcloudc.db.backends.common.helpers import (
    MockInstance,
    django_instance_to_entities,
    perform_null_checks,
    ensure_datetime,
    get_document_key,
    has_concrete_parents,
    get_model_from_db_table,
)

# We can retry transactions only if the command is not
# being executed within an existing transaction. This controls
# how many times we try in that case.
_TRANSACTION_TRIES = 5

logger = logging.getLogger(__name__)

OPERATORS_MAP = {
    "exact": "=",
    "gt": ">",
    "gte": ">=",
    "lt": "<",
    "lte": "<=",
    # The following operators are supported with special code below.
    "isnull": None,
    "in": None,
    "range": None,
}

EXTRA_SELECT_FUNCTIONS = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "/": lambda x, y: x / y,
    "*": lambda x, y: x * y,
    "<": lambda x, y: x < y,
    ">": lambda x, y: x > y,
    "=": lambda x, y: x == y,
}

REVERSE_OP_MAP = {"=": "exact", ">": "gt", ">=": "gte", "<": "lt", "<=": "lte"}


def field_conv_year_only(value):
    value = ensure_datetime(value)
    return datetime(value.year, 1, 1, 0, 0)


def field_conv_month_only(value):
    value = ensure_datetime(value)
    return datetime(value.year, value.month, 1, 0, 0)


def field_conv_day_only(value):
    value = ensure_datetime(value)
    return datetime(value.year, value.month, value.day, 0, 0)


def coerce_unicode(value):
    if isinstance(value, bytes):
        try:
            value = value.decode("utf-8")
        except UnicodeDecodeError:
            # This must be a Django databaseerror, because the exception happens too
            # early before Django's exception wrapping can take effect (e.g. it happens on SQL
            # construction, not on execution.
            raise DatabaseError("Bytestring is not encoded in utf-8")

    # The SDK raises BadValueError for unicode sub-classes like SafeText.
    return str(value)


def log_once(logging_call, text, args):
    """
        Only logs one instance of the combination of text and arguments to the passed
        logging function
    """
    identifier = "%s:%s" % (text, args)
    if identifier in log_once.logged:
        return
    logging_call(text % args)
    log_once.logged.add(identifier)


log_once.logged = set()


def convert_django_ordering_to_gae(ordering):
    return ordering


def limit_results_generator(results, limit):
    for result in results:
        yield result
        limit -= 1
        if not limit:
            raise StopIteration


class BaseCommand(object):
    def __init__(self, compiler):
        self.compiler = compiler


class SelectCommand(BaseCommand):
    def __init__(self, compiler, wrapper, query, keys_only=False):
        super().__init__(compiler)

        from gcloudc.db.backends.common.base.connection import Wrapper

        assert isinstance(wrapper, Wrapper)

        self.wrapper = wrapper
        self.connection = wrapper.connection
        self.namespace = wrapper.namespace
        self.results = iter([])
        self.model = query.model
        self.query = wrapper.transform_django_query(
            query, keys_only
        )

        self.original_query = query

        # Django's ORM doesn't seem to have a straightforward way to find out
        # the columns returned from a query and the order they should be returned..
        # This is my best guess at what the logic is (based on the logic in ModelIterable)
        # Interestingly, ModelIterable never deals with klass_info being None, so I'm not
        # entirely sure why this happens for us (only in the case a query returns annotations only
        # e.g. dates())
        select, klass_info, annotation_col_map = compiler.get_select()
        if klass_info:
            select_fields = klass_info["select_fields"]
            model_fields_start, model_fields_end = select_fields[0], select_fields[-1] + 1

            self.init_list = [
                f[0].target.column for f in select[model_fields_start:model_fields_end]
            ]
        else:
            self.init_list = []

        for attr_name, col_pos in annotation_col_map.items():
            # In Django 5.2+ for reason that I don't fully understand,
            # the compiler returns "pk" and, in some cases, duplicates
            # of the columns here - which we need to remove
            if attr_name != "pk" and attr_name not in self.init_list:
                self.init_list.insert(col_pos, attr_name)

    def _determine_query_kind(self):
        """ Basically returns SELECT or COUNT """
        query = self.original_query

        if query.annotations:
            if "__count" in query.annotations:
                field = query.annotations["__count"].source_expressions[0]
                if isinstance(field, Star) or field.value == "*":
                    return "COUNT"

        return "SELECT"

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.query == other.query

    def __ne__(self, other):
        return not self.__eq__(other)

    def execute(self):
        high_mark = self.original_query.high_mark
        low_mark = self.original_query.low_mark
        limit = None if high_mark is None else (high_mark - (low_mark or 0))
        offset = low_mark or 0

        query_type = self._determine_query_kind()

        if query_type == "COUNT":
            self.results = iter([self.query.count(limit=limit)])
            return 1
        elif query_type == "AVERAGE":
            raise ValueError("AVERAGE not yet supported")

        assert (query_type == "SELECT")

        results_returned = 0
        results = []

        for entity in self.query.fetch(limit=limit, offset=offset):
            if entity:
                results.append(entity)
                results_returned += 1

        self.results = iter(results)
        return results_returned

    def __repr__(self):
        return force_str(generate_sql_representation(self))

    def __mod__(self, params):
        return repr(self)

    def lower(self):
        """
            This exists solely for django-debug-toolbar compatibility.
        """
        return str(self).lower()


class FlushCommand(BaseCommand):
    """
        sql_flush returns the SQL statements to flush the database,
        which are then executed by cursor.execute()

        We instead return a list of FlushCommands which are called by
        our cursor.execute
    """

    def __init__(self, compiler, table, connection):
        super().__init__(compiler)

        self.connection = connection
        self.table = table
        self.namespace = connection.namespace

    def execute(self):
        self.connection.ensure_connection()
        self.connection.connection.flush(
            [self.table],
            namespace=self.namespace,
            database=self.connection.settings_dict.get("DATABASE_ID"),
        )


def perform_unique_checks(namespace, model, rpc, primary, test_fn):
    def _test_combination(combination):
        # We can't `break` two levels at once, hence the nested function
        query = rpc.query(kind=primary.kind, namespace=namespace)

        for field in combination:
            col_name = model._meta.get_field(field).column
            value = primary.get(col_name)
            if isinstance(value, list):
                if not value:
                    # For lists, empty values are treated as effectively NULL
                    return
                for item in value:
                    query.add_filter(col_name, '=', item)
            elif value is None:
                return
            else:
                query.add_filter(col_name, '=', value)

        # only perform the query if there are filters on it
        if len(query.filters):
            res = list(query.fetch(1))
            if test_fn(res):
                raise IntegrityError(
                    CONSTRAINT_VIOLATION_MSG.format(model._meta.db_table, ", ".join(combination))
                )

    combinations = _unique_combinations(model, ignore_pk=True)
    for combination in combinations:
        _test_combination(combination)


class BulkInsertError(IntegrityError, NotSupportedError):
    pass


class BulkDeleteError(IntegrityError, NotSupportedError):
    pass


class InsertCommand(BaseCommand):
    def __init__(self, compiler, connection, model, objs, fields, raw):
        super().__init__(compiler)

        self.has_pk = any(x.primary_key for x in fields)
        self.model = model
        self.objs = objs
        self.connection = connection
        self.namespace = connection.namespace
        self.raw = raw
        self.fields = fields
        self.entities = []
        self.included_keys = []

        for obj in self.objs:
            if self.has_pk:
                # We must convert the PK value here, even though this normally happens in
                # django_instance_to_entities otherwise
                # custom PK fields don't work properly
                value = self.model._meta.pk.get_db_prep_save(self.model._meta.pk.pre_save(obj, True), self.connection)
                self.included_keys.append(get_document_key(self.connection, self.model, value) if value else None)

                if value == 0:
                    raise IntegrityError("The datastore doesn't support 0 as a key value")

                if not self.model._meta.pk.blank and self.included_keys[-1] is None:
                    raise IntegrityError("You must specify a primary key value for {} instances".format(self.model))
            else:
                # We zip() self.entities and self.included_keys in execute(), so they should be the same length
                self.included_keys.append(None)

            # We don't use the values returned, but this does make sure we're
            # doing the same validation as Django. See issue #493 for an
            # example of how not doing this can mess things up
            for field in fields:
                field.get_db_prep_save(
                    getattr(obj, field.attname) if raw else field.pre_save(obj, True), connection=connection
                )

            # We don't check null fields on polymodels here, we do that on insert
            check_null = not has_concrete_parents(self.model)

            primary, descendents = django_instance_to_entities(
                self.connection, self.fields, self.raw, obj, check_null=check_null,
            )

            # Append the entity, and any descendents to the list to insert
            self.entities.append((primary, descendents))

    def execute(self):
        """
        Returns the keys of all entities succesfully put into the database.

        Under the hood this handles a few implementation specific details,
        such as checking that any unique constraints defined on the entity
        model are respected.
        """
        check_existence = self.has_pk and not has_concrete_parents(self.model)

        def perform_insert(entities):
            results = []
            for primary, descendents in entities:
                if primary.key().is_partial():
                    db_type = self.model._meta.pk.db_type(self.connection)
                    primary.key().complete_key(
                        self.connection.generate_id(
                            int if db_type in ('key', 'int', 'long') else str
                        )
                    )

                self.connection.pre_entity_insert(
                    self.model, primary, {}
                )

                self.connection.connection.put(primary)

                self.connection.post_entity_insert(
                    self.model, primary, {}
                )

                new_key = primary.key()

                for descendent in descendents or []:
                    ancestor_key = self.connection.connection.new_key(
                        descendent.key().path[0],
                        descendent.key().id_or_name,
                        parent=new_key,
                    )
                    descendent.set_key(ancestor_key)
                    self.connection.connection.put(descendent)

                results.append(new_key)
            return results

        @atomic(using=self.connection.alias)
        def insert_chunk(keys, entities):
            for i, key in enumerate(keys):
                # sense check the key isn't already taken
                if check_existence and key is not None:
                    if self.connection.connection.exists(key):
                        raise IntegrityError("Tried to INSERT with existing key")

                    if key.id_or_name is not None:
                        # quick validation of the ID value
                        if not self.connection.is_id_valid(key.id_or_name):
                            raise NotSupportedError(
                                "Key value ({}) is not valid.".format(key.id_or_name)
                            )

                        # Reserve any explicit id
                        # FIXME: This only uses part of the path and won't work
                        # for nested collisions
                        assert (len(key.path) == 1)
                        self.connection.reserve_id(
                            key.path[0], key.id_or_name, self.namespace
                        )
                elif has_concrete_parents(self.model) and key is not None:
                    # If we have concrete parents, we need to fetch any existing data
                    # and update it as if this was an update. We then need to do a null
                    # check (which we couldn't do earlier as we didn't have the data to do so)
                    # the class property should've been populated by this point
                    existing = self.connection.connection.get(key)
                    primary_idx = 0
                    descendents_idx = 1
                    if existing:
                        existing.update(entities[i][primary_idx])
                        entities[i] = (existing, entities[i][descendents_idx])
                    perform_null_checks(entities[i][primary_idx], self.fields)

            results = perform_insert(entities)
            return results

        tries = 1 if self.connection.in_atomic_block else _TRANSACTION_TRIES
        for i in range(tries):
            try:
                return insert_chunk(self.included_keys, self.entities)
            except OperationalError:
                if i == tries - 1:
                    raise
                continue

    def lower(self):
        """
            This exists solely for django-debug-toolbar compatibility.
        """
        return str(self).lower()

    def __str__(self):
        return generate_sql_representation(self)


class DeleteCommand(BaseCommand):
    """
    Delete an entity / multiple entities.

    Limits imposed by the Firestore in Datastore mode (such as 500 write operations
    per batch) and the backend internal implementation details are handled under the hood.
    """

    def __init__(self, compiler, connection, query):
        super().__init__(compiler)

        self.connection = connection
        self.model = query.model
        self.namespace = connection.namespace

        self.select = SelectCommand(compiler, connection, query, keys_only=True)
        self.query = self.select.query  # we only need this for the generate_sql_formatter caller...

        if query.model:
            table = helpers.get_top_concrete_parent(query.model)._meta.db_table
        else:
            table = query.tables[0]
            assert (table)

        self.table_to_delete = table  # used in wipe_polymodel_from_entity

    def execute(self):
        """
            Ideally we'd just be able to tell appengine to delete all the entities
            which match the query, that would be nice wouldn't it?

            Except we can't. Firstly delete() only accepts keys so we first have to
            execute a keys_only query to find the entities that match the query, then send
            those keys to delete().

            And then there are polymodels (model inheritence) which means we might not even be
            deleting the entity after all, only deleting some of the fields from it.

            What we do then is do a keys_only query, then iterate the entities in batches of
            500, each entity in the batch has its polymodel fields wiped out
            (if necessary) and then we do either a put() or delete() all inside a transaction.

            Oh, and we wipe out memcache in an independent transaction.

            Things to improve:

            - Check the entity matches the query still (there's a fixme there)
        """
        from gcloudc.db.backends.common.indexing import indexers_for_model

        @atomic(using=self.connection.alias)
        def delete_batch(key_slice):
            """
                Batch fetch entities, wiping out any polymodel fields if
                necessary, before deleting the entities by key.

                Any memcache references are also removed.
            """
            entities_to_delete = []
            entities_to_update = []
            updated_keys = []

            # get() expects Key objects, not just dicts with id keys
            keys_in_slice = [
                self.connection.connection.new_key(
                    self.model._meta.db_table,
                    key_id,
                    namespace=self.connection.namespace
                )
                for key_id in key_slice
            ]
            entities = self.connection.connection.get(keys_in_slice)
            for entity in entities:

                # make sure the entity still exists
                if entity is None:
                    continue

                polymodel_class_property = self.connection.polymodel_property_name()
                # handle polymodels
                _wipe_polymodel_from_entity(
                    polymodel_class_property, entity, self.table_to_delete
                )

                if not entity.get(polymodel_class_property):
                    entities_to_delete.append(entity)
                else:
                    entities_to_update.append(entity)
                updated_keys.append(entity)

            # we don't need an explicit batch here, as we are inside a transaction
            # which already applies this behaviour of non blocking RPCs until
            # the transaction is commited

            client = self.connection.connection

            for entity in entities:
                self.connection.pre_entity_delete(self.model, entity, {})

            for entity in entities_to_delete:
                client.delete(entity.key())

            for entity in entities_to_update:
                client.put(entity)

            for entity in entities:
                self.connection.post_entity_delete(self.model, entity, {})

            # Clean up any special indexes that need to be removed
            for indexer in indexers_for_model(self.model):
                for entity in entities_to_delete:
                    indexer.cleanup(client, entity.key())

            return len(updated_keys)

        # grab the result of the keys only query (see __init__)
        self.select.execute()
        key_ids = [x.key().id_or_name for x in self.select.results]

        # for now we can only process 500 entities
        # otherwise we need to handle rollback of independent transactions
        # and race conditions between items being deleted and restored...
        max_batch_size = self.connection.TRANSACTION_ENTITY_LIMIT

        if len(key_ids) > max_batch_size:
            raise BulkDeleteError(
                "Bulk deletes for {} can only delete {} instances per batch".format(self.model, max_batch_size)
            )

        tries = 1 if self.connection.in_atomic_block else _TRANSACTION_TRIES
        for i in range(tries):
            try:
                return delete_batch(key_ids)
            except OperationalError:
                if i == tries - 1:
                    raise
                continue

    def lower(self):
        """
            This exists solely for django-debug-toolbar compatibility.
        """
        return str(self).lower()

    def __str__(self):
        return generate_sql_representation(self)


def _wipe_polymodel_from_entity(polymodel_class_field, entity, db_table):
    """
        Wipes out the fields associated with the specified polymodel table.
    """
    polymodel_value = entity.get(polymodel_class_field, [])
    if polymodel_value and db_table in polymodel_value:
        # Remove any local fields from this model from the entity
        model = get_model_from_db_table(db_table)
        for field in model._meta.local_fields:
            col = field.column
            if col in entity:
                del entity[col]

        # Then remove this model from the polymodel heirarchy
        polymodel_value.remove(db_table)
        if polymodel_value:
            entity[polymodel_class_field] = polymodel_value


class UpdateCommand(BaseCommand):
    def __init__(self, compiler, connection, query):
        super().__init__(compiler)

        self.model = query.model
        self.select = SelectCommand(compiler, connection, query, keys_only=False)
        self.query = self.select.query
        self.values = query.values
        self.connection = connection
        self.namespace = connection.namespace
        self.results = []

    def __str__(self):
        return generate_sql_representation(self)

    def lower(self):
        """
            This exists solely for django-debug-toolbar compatibility.
        """
        return str(self).lower()

    def _update_entity(self, result):
        def update_txt():
            if result is None:
                # Return false to indicate update failure
                return False

            original = copy.deepcopy(result)

            instance_kwargs = {field.attname: value for field, param, value in self.values}

            # Note: If you replace MockInstance with self.model, you'll find that some delete
            # tests fail in the test app. This is because any unspecified fields would then call
            # get_default (even though we aren't going to use them) which may run a query which
            # fails inside this transaction. Given as we are just using MockInstance so that we can
            # call django_instance_to_entities it on it with the subset of fields we pass in,
            # what we have is fine.
            meta = self.model._meta
            instance = MockInstance(_original=MockInstance(_meta=meta, **result), _meta=meta, **instance_kwargs)

            # Convert the instance to an entity
            primary, descendents = django_instance_to_entities(
                self.connection,
                [x[0] for x in self.values],  # Pass in the fields that were updated
                True,
                instance,
                model=self.model,
            )
            # Update the entity we read above with the new values
            result.update(primary)

            # Remove fields which have been marked to be unindexed
            for col in getattr(primary, "_properties_to_remove", []):
                if col in result:
                    del result[col]

            # Make sure that any polymodel classes which were in the original entity are kept,
            # as django_instance_to_entities may have wiped them as well as added them.
            polymodel_classes = list(
                set(
                    original.get(self.connection.polymodel_property_name(), []) +
                    result.get(self.connection.polymodel_property_name(), [])
                )
            )
            if polymodel_classes:
                result[self.connection.polymodel_property_name()] = polymodel_classes

            def perform_insert():
                """
                    Inserts result, and any descendents with their ancestor
                    value set
                """

                self.connection.pre_entity_update(self.model, result, {})
                self.connection.connection.put(result)
                self.connection.post_entity_update(self.model, result, {})

                inserted_key = result.key()
                self.results.append((result, None))

                if descendents:
                    for descendent in descendents:
                        final_descendent = Entity(
                            self.connection.connection.new_key(
                                descendent.key().path[0],
                                descendent.key().id_or_name,
                                parent=inserted_key,
                                namespace=inserted_key.namespace
                            )
                        )
                        final_descendent.update(descendent)
                        self.connection.connection.put(final_descendent)

            # this will be async as we're inside a transaction block
            perform_insert()

            # Return true to indicate update success
            return True

        return update_txt()

    def execute(self):
        @atomic(using=self.connection.alias)
        def perform_update():
            self.select.execute()
            results = list(self.select.results)

            i = 0
            for result in results:
                if self._update_entity(result):
                    i += 1

            return i

        # TODO: potential optimisation - consider running transactions
        # around single entity update rather than the whole batch.
        # This could potentially open a can of worms but would have the
        # benefit of locking fewer rows.
        tries = 1 if self.connection.in_atomic_block else _TRANSACTION_TRIES
        for i in range(tries):
            try:
                return perform_update()
            except OperationalError:
                if i == tries - 1:
                    raise
                continue
