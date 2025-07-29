from datetime import datetime
from decimal import Decimal
from functools import lru_cache
from logging import Logger
from typing import (
    Set,
    Tuple,
)

from django.apps import apps
from django.conf import settings
from django.db import IntegrityError, models
from django.db.backends.utils import format_number
from django.utils import timezone
from gcloudc.db.backends.common.base.entity import Entity
from datetime import timezone as tz
from gcloudc.utils import memoized

try:
    from django.db.models.expressions import BaseExpression
except ImportError:
    from django.db.models.expressions import ExpressionNode as BaseExpression


def make_utc_compatible(value):
    if value is None:
        return None

    if timezone.is_aware(value):
        if settings.USE_TZ:
            try:
                value = value.astimezone(tz.utc)
            except (OverflowError, ValueError):
                # Value is datetime.min or max, and is out of range for conversion.
                # Instead, just replace the timezone.
                value = value.replace(tzinfo=tz.utc)
        else:
            raise ValueError("Djangae backend does not support timezone-aware datetimes when USE_TZ is False.")
    return value


@memoized
def get_model_from_db_table(db_table):
    # We use include_swapped=True because tests might need access to gauth User models which are
    # swapped if the user has a different custom user model

    kwargs = {"include_auto_created": True, "include_swapped": True}

    for model in apps.get_models(**kwargs):
        if model._meta.db_table == db_table:
            return model


def decimal_to_string(value, max_digits=16, decimal_places=0):
    """
    Converts decimal to a unicode string for storage / lookup by nonrel
    databases that don't support decimals natively.

    This is an extension to `django.db.backends.utils.format_number`
    that preserves order -- if one decimal is less than another, their
    string representations should compare the same (as strings).

    TODO: Can't this be done using string.format()?
          Not in Python 2.5, str.format is backported to 2.6 only.
    """

    # Handle sign separately.
    if value.is_signed():
        sign = u"-"
        value = abs(value)
    else:
        sign = u""

    # Let Django quantize and cast to a string.
    value = format_number(value, max_digits, decimal_places)

    # Pad with zeroes to a constant width.
    n = value.find(".")
    if n < 0:
        n = len(value)
    if n < max_digits - decimal_places:
        value = u"0" * (max_digits - decimal_places - n) + value
    return sign + value


def normalise_field_value(value):
    """ Converts a field value to a common type/format to make comparable to another. """
    if isinstance(value, datetime):
        return make_utc_compatible(value)
    elif isinstance(value, Decimal):
        return decimal_to_string(value)
    return value


def get_datastore_kind(model):
    return get_top_concrete_parent(model)._meta.db_table


def get_prepared_db_value(connection, instance, field, raw=False):
    value = getattr(instance, field.attname) if raw else field.pre_save(instance, instance._state.adding)

    if isinstance(value, BaseExpression):
        from gcloudc.db.backends.common.parsers.expressions import (
            evaluate_expression,
        )

        # We can't actually support F expressions on the datastore, but we can simulate
        # them, evaluating the expression in place.
        # TODO: For saves and updates we should raise a Warning. When evaluated in a filter
        # we should raise an Error
        value = evaluate_expression(value, instance, connection)

    if hasattr(value, "prepare_database_save"):
        value = value.prepare_database_save(field)
    else:
        value = field.get_db_prep_save(value, connection=connection)

    value = connection.ops.value_for_db(value, field)

    return value


def get_concrete_parents(model, ignore_leaf=False):
    ret = [x for x in model.mro() if hasattr(x, "_meta") and not x._meta.abstract and not x._meta.proxy]
    if ignore_leaf:
        ret = [x for x in ret if x != model]
    return ret


@memoized
def get_top_concrete_parent(model):
    return get_concrete_parents(model)[-1]


def get_bottom_concrete_model(tables):
    """
        Given a list of db_tables from a heirarchy of concrete models
        this works out which one is the "bottom" model
    """

    lowest = None
    highest_parent_count = 0

    for table in tables:
        model = get_model_from_db_table(table)
        if model:
            parents = get_concrete_parents(model)
            if len(parents) >= highest_parent_count:
                lowest = model
                highest_parent_count = len(parents)

    return lowest


def get_concrete_fields(model, ignore_leaf=False):
    """
        Returns all the concrete fields for the model, including those
        from parent models
    """
    concrete_classes = get_concrete_parents(model, ignore_leaf)
    fields = []
    for klass in concrete_classes:
        fields.extend(klass._meta.fields)

    return fields


@memoized
def get_concrete_db_tables(model):
    return [x._meta.db_table for x in get_concrete_parents(model)]


@memoized
def has_concrete_parents(model):
    return get_concrete_parents(model) != [model]


@memoized
def get_field_from_column(model, column):
    for field in model._meta.fields:
        if field.column == column:
            return field
    return None


def indexed_columns_on_model(model) -> Set[str]:
    """
    Return a set of the properties indexed in the datastore based on the
    model.meta.indexes definition.

    Note this currently assumes supports for single indexes only (not composite).
    """

    # Now this is a little unusual. We could use field.db_index to determine if db_index is
    # set. But what we actually need is *explicit* db_index=True. ForeignKeys implicitly get
    # db_index==True and we don't want the act of adding an FK to trigger these checks, so
    # we call deconstruct() and check the kwargs to that instead.

    fields_with_db_index = {
        field.column
        for field in model._meta.fields
        if "db_index" in field.deconstruct()[-1]
    }

    # If we have fields with a db_index or model._meta.indexes, then we can and should include
    # ForeignKey fields as well, we just don't want to use those to indicate the presence of indexes
    if fields_with_db_index or model._meta.indexes:
        fields_with_db_index = {field.column for field in model._meta.fields if field.db_index}

    return fields_with_db_index.union({
        model._meta.get_field(field.fields[0]).column for field in model._meta.indexes
    })


def model_fields_to_exclude_from_indexes(connection, model) -> Tuple[str]:
    """
    Returns a tuple of the model fields to exclude from the database index.
    """
    # exclude text and bytes fields from indexes by default
    excluded_indexes = set(
        field.column
        for field in model._meta.fields
        if field.db_type(connection) in ("text", "bytes")
    )

    # check if any indexes are defined on the model._meta - this is considering
    # opting into the explicit indexing and exclusion of indexes
    indexed_columns = indexed_columns_on_model(model)
    if indexed_columns:
        # exclude from indexes any field not passed to the index_fields function
        fields_to_exclude_from_indexes = set(
            field.name
            for field in model._meta.fields
            if field.column not in indexed_columns
            and not field.primary_key
            and field.db_type(connection) not in ("text", "bytes")
        )
        excluded_indexes.update(fields_to_exclude_from_indexes)

    return tuple(excluded_indexes)


class NotProvided:
    pass


def perform_null_checks(instance, fields, value_override=NotProvided):
    for field in fields:
        value = value_override if value_override != NotProvided else (
            getattr(instance, field.attname)
            if isinstance(instance, (models.Model, MockInstance))
            else instance.get(field.attname, None)
        )

        if not field.null and (not field.null and not field.primary_key) and value is None:
            raise IntegrityError("You can't set %s (a non-nullable field) to None!" % field.name)


def django_instance_to_entities(connection, fields, raw, instance, check_null=True, model=None):
    """
        Converts a Django Model instance to an App Engine `Entity`

        Arguments:
            connection: Djangae appengine connection object
            fields: A list of fields to populate in the Entity
            raw: raw flag to pass to get_prepared_db_value
            instance: The Django model instance to convert
            check_null: Whether or not we should enforce NULL during conversion
            (throws an error if None is set on a non-nullable field)
            model: Model class to use instead of the instance one

        Returns:
            entity, [entity, entity, ...]

       Where the first result in the tuple is the primary entity, and the
       remaining entities are optionally descendents of the primary entity. This
       is useful for special indexes (e.g. contains)
    """

    from gcloudc.db.backends.common.indexing import (
        IgnoreForIndexing,
        get_indexer,
        special_indexes_for_column,
    )

    model = model or type(instance)
    inheritance_root = get_top_concrete_parent(model)

    db_table = get_datastore_kind(inheritance_root)

    def value_from_instance(_instance, _field):
        value = get_prepared_db_value(connection, _instance, _field, raw)

        # If value is None, but there is a default, and the field is not nullable then we should populate it
        # Otherwise thing get hairy when you add new fields to models
        if value is None and _field.has_default() and not _field.null:
            # We need to pass the default through get_db_prep_save to properly do the conversion
            # this is how
            value = _field.get_db_prep_save(_field.get_default(), connection)

        if check_null:
            perform_null_checks(_instance, [_field], value_override=value)

        is_primary_key = False
        if _field.primary_key and _field.model == inheritance_root:
            is_primary_key = True

        return value, is_primary_key

    field_values = {}
    primary_key = None

    descendents = []
    fields_to_unindex = set()

    for field in fields:
        value, is_primary_key = value_from_instance(instance, field)
        if is_primary_key:
            primary_key = value
        else:
            field_values[field.column] = value

        # Add special indexed fields
        for index in special_indexes_for_column(model, field.column):
            indexer = get_indexer(field, index)

            unindex = False
            try:
                values = indexer.prep_value_for_database(
                    value, index, model=model, column=field.column, connection=connection
                )
            except IgnoreForIndexing as e:
                # We mark this value as being wiped out for indexing
                unindex = True
                values = e.processed_value

            if not hasattr(values, "__iter__") or isinstance(values, (bytes, str)):
                values = [values]

            # If the indexer returns additional entities (instead of indexing a special column)
            # then just store those entities
            if indexer.PREP_VALUE_RETURNS_ENTITIES:
                descendents.extend(values)
            else:
                for i, v in enumerate(values):
                    column = indexer.indexed_column_name(field.column, v, index, connection=connection)

                    if unindex:
                        fields_to_unindex.add(column)
                        continue

                    # If the column already exists in the values, then we convert it to a
                    # list and append the new value
                    if column in field_values:
                        if not isinstance(field_values[column], list):
                            field_values[column] = [field_values[column], v]
                        else:
                            field_values[column].append(v)
                    else:
                        # Otherwise we just set the column to the value
                        field_values[column] = v

    key = connection.connection.new_key(
        db_table, primary_key,
        namespace=connection.namespace
    )

    assert (key)

    exclude_from_indexes = model_fields_to_exclude_from_indexes(connection, model)

    entity = Entity(key, field_values, exclude_from_indexes=exclude_from_indexes)

    for field in fields_to_unindex or []:
        entity.add_property_to_unindex(field)

    classes = get_concrete_db_tables(model)
    if len(classes) > 1:
        entity[connection.polymodel_property_name()] = list(set(classes))

    return entity, descendents


def get_document_key(connection, model, pk):
    """ Return a datastore.Key for the given model and primary key.
    """
    kind = get_top_concrete_parent(model)._meta.db_table
    return connection.connection.new_key(kind, pk, namespace=connection.namespace)


class MockInstance(object):
    """
        This creates a mock instance for use when passing a datastore entity
        into get_prepared_db_value. This is used when performing updates to prevent a complete
        conversion to a Django instance before writing back the entity
    """

    def __init__(self, **kwargs):
        is_adding = kwargs.pop("_is_adding", False)
        self._original = kwargs.pop("_original", None)
        self._meta = kwargs.pop("_meta", None)

        class State:
            adding = is_adding

        self.fields = {}
        for field_name, value in kwargs.items():
            self.fields[field_name] = value

        self._state = State()

    def __getattr__(self, attr):
        if attr in self.fields:
            return self.fields[attr]
        raise AttributeError(attr)


# Null-friendly comparison functions


def lt(x, y):
    if x is None and y is None:
        return False
    if x is None and y is not None:
        return True
    elif x is not None and y is None:
        return False
    else:
        return x < y


def gt(x, y):
    if x is None and y is None:
        return False
    if x is None and y is not None:
        return False
    elif x is not None and y is None:
        return True
    else:
        return x > y


def gte(x, y):
    return not lt(x, y)


def lte(x, y):
    return not gt(x, y)


def eq(x, y):
    return x == y


def array_contains(e, q):
    return q in e if e is not None else q is None


def array_contains_all(e, q):
    return e and set(e).intersection(set(q)) == set(q)


def entity_matches_query(entity, query):
    """
        Return True if the entity would potentially be returned by the datastore
        query
    """

    OPERATORS = {
        '=': eq,
        "<": lt,
        ">": gt,
        "<=": lte,
        ">=": gte,
        "array_contains": array_contains,
        "array_contains_all": array_contains_all
    }

    if list(entity.key().path) != list(query.path):
        # If the entity key doesn't match the query key then it can't match.
        return False

    for (prop, op), query_values in query._filters.items():
        if prop == query.wrapper.key_property_name():
            ent_value = entity.key()
        else:
            ent_value = entity.get(prop)

        compare = OPERATORS[op]  # We want this to throw if there's some op we don't know about

        matches = False
        for value in query_values:  # [22, 23]
            # If any of the values don't match then this query doesn't match
            if not compare(ent_value, value):
                matches = False
                break
        else:
            # One of the ent_attrs matches the query_attrs
            matches = True

        if not matches:
            # One of the AND values didn't match
            break
    else:
        # If we got through the loop without breaking, then the entity matches
        return True

    return False


def ensure_datetime(value):
    """
        Painfully, sometimes the Datastore returns dates as datetime objects, and sometimes
        it returns them as unix timestamps in microseconds!!
    """
    if isinstance(value, int):
        return datetime.utcfromtimestamp(value / 1e6)
    return value


def count_query(query):
    """
        The Google Cloud Datastore API doesn't expose a way to count a query
        the traditional method of doing a keys-only query is apparently actually
        slower than this method
    """

    # Largest 32 bit number, fairly arbitrary but I've seen Java Cloud Datastore
    # code that uses Integer.MAX_VALUE which is this value
    MAX_INT = 2147483647

    # Setting a limit of zero and an offset of max int will make
    # the server (rather than the client) skip the entities and then
    # return the number of skipped entities, fo realz yo!
    iterator = query.fetch(limit=0, offset=MAX_INT)
    [x for x in iterator]  # Force evaluation of the iterator

    count = iterator._skipped_results
    while iterator._more_results:
        # If we have more results then use cursor offsetting and repeat
        iterator = query.fetch(limit=0, offset=MAX_INT, start_cursor=iterator.next_page_token)
        [x for x in iterator]  # Force evaluation of the iterator

        count += iterator._skipped_results

    return count


@lru_cache(None)
def log_once(logger: Logger, msg: str, method='info'):
    getattr(logger, method)(msg)
