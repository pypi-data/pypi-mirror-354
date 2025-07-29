"""
The Datastore does not provide database level constraints around uniqueness
(unlike relational a SQL database, where you can ensure uniqueness for a certain
column, or a combination of columns).

To mimic the ability to define these constraints using the Django API,
we have implemented an approach where, thanks to Cloud Firestore strong
consistency we check unique constraints transactionally before any write

This allows us to efficiently check for existing constraints before doing a put().
"""

from hashlib import md5

from django.db import NotSupportedError
from django.db.utils import IntegrityError
from .helpers import (
    get_top_concrete_parent,
    get_bottom_concrete_model,
    get_concrete_parents,
)


UNIQUE_MARKER_KIND = "uniquemarker"
CONSTRAINT_VIOLATION_MSG = "Unique constraint violation for kind {} on fields: {}"


def _format_value_for_identifier(value):
    # AppEngine max key length is 500 chars, so if the value is a string we hexdigest it to reduce the length
    # otherwise we str() it as it's probably an int or bool or something.
    return md5(value.encode("utf-8")).hexdigest() if isinstance(value, str) else str(value)


def has_unique_constraints(model_or_instance):
    """
    Returns a boolean to indicate if the given model has any type of unique
    constraint defined (e.g. unique on a single field, or meta.unique_together).

    To support concrete model inheritance we state that uniqueness checks
    should only be performed on the class that the defines the unique constraint.

    Note - you can see a much more verbose implementation of this in
    django.db.models.base.Model._get_unique_checks() - but we implement our
    own logic to exit early when the first constraint is found.
    """
    meta_options = model_or_instance._meta
    # we may get an instance here, so ensure we have a reference to the
    # model class
    model_class = meta_options.model
    unique_together = meta_options.unique_together
    unique_fields = any(
        field.unique and field.model == model_class
        for field in meta_options.fields
    )

    return any([unique_fields, unique_together])


def check_unique_markers_in_memory(wrapper, entities):
    """
    Compare the entities using their in memory properties, to see if any
    unique constraints are violated.

    This would always need to be used in conjunction with RPC checks against
    persisted markers to ensure data integrity.
    """

    polymodel_field = wrapper.polymodel_property_name()

    all_unique_marker_key_values = set([])
    for entity in entities:
        tables = [entity.key().path[-1]] + entity.get(polymodel_field, [])
        model = get_bottom_concrete_model(tables)
        if not model:
            # Not all entities have a model
            continue

        unique_marker_key_values = unique_identifiers_from_entity(model, entity, ignore_pk=True)
        for named_key in unique_marker_key_values:
            if named_key not in all_unique_marker_key_values:
                all_unique_marker_key_values.add(named_key)
            else:
                table_name = named_key.split("|")[0]
                unique_fields = named_key.split("|")[1:]
                raise IntegrityError(CONSTRAINT_VIOLATION_MSG.format(table_name, unique_fields))


def _unique_combinations(model, ignore_pk=False, include_bases=True):
    """
    Returns an iterable of iterables to represent all the unique constraints
    defined on the model. For example given the following model definition:

        class ExampleModel(models.Model):
            username = models.CharField(unique=True)
            email = models.EmailField(primary_key=True)
            first_name = models.CharField()
            second_name = models.CharField()

        class Meta:
            unique_together = ('first_name', 'second_name')

    This method would return

    [
        ['username'], # from field level unique=True
        ['email'], # implicit unique constraint from primary_key=True
        ['first_name', 'second_name'] # from model meta unique_together
    ]

    Fields with unique constraint defined in a concrete parent model are ingored
    since they're checked when that model is saved
    """

    unique_constraints = []
    if include_bases:
        for child_or_parent in get_concrete_parents(model):
            unique_constraints.extend(
                [list(x) for x in child_or_parent._meta.unique_together]
            )
    else:
        # first grab all the unique together constraints
        unique_constraints = [
            list(together_constraint)
            for together_constraint in model._meta.unique_together
        ]

    # then the column level constraints - special casing PK if required
    for field in model._meta.fields:
        if field.primary_key and ignore_pk:
            continue

        if (not include_bases) and field.model != model:
            continue

        if field.unique:
            unique_constraints.append([field.name])

    # the caller should sort each inner iterable really - but we do this here
    # for now - motive being that interpolated keys from these values are consistent
    return [sorted(constraint) for constraint in unique_constraints]


def unique_identifiers_from_entity(model, entity, ignore_pk=True, ignore_null_values=True):
    """
    This method returns a list of all unique marker key identifier values for
    the given entity by combining the field and entity values. For example:

    [
        # example of a single field unique constraint
        djange_<model_db_table>|<field_name>:<entity_value>
        # example of unique together
        djange_<model_db_table>|<field_name>:<entity_value>|<field_name>:<entity_value>
        ...
    ]

    These are then used before we put() anything into the database, to check
    that there are no existing markers satisfying those unique constraints.
    """

    assert (entity is not None)

    field_data = entity._data if hasattr(entity, "_data") else entity

    # get all combintatons of unique combinations defined on the model class
    unique_combinations = _unique_combinations(model, ignore_pk)

    meta = model._meta

    identifiers = []
    for combination in unique_combinations:
        combo_identifiers = [[]]

        include_combination = True

        for field_name in combination:
            field = meta.get_field(field_name)

            if field.primary_key:
                value = entity.key().id_or_name
            else:
                value = field_data.get(field.column)  # Get the value from the entity

            # If ignore_null_values is True, then we don't include combinations where the value is None
            # or if the field is a multivalue field where None means no value (you can't store None in a list)
            if (value is None and ignore_null_values) or (not value and isinstance(value, (list, set))):
                include_combination = False
                break

            if not isinstance(value, (list, set)):
                value = [value]

            new_combo_identifers = []

            for existing in combo_identifiers:
                for v in value:
                    identifier = "{}:{}".format(field.column, _format_value_for_identifier(v))
                    new_combo_identifers.append(existing + [identifier])

            combo_identifiers = new_combo_identifers

        if include_combination:
            # create the final value - eg <app_db_table>|<field_name>:<field_val>
            for identifier_pairs in combo_identifiers:
                constraint_prefix = get_top_concrete_parent(model)._meta.db_table
                constraint_suffix = "|".join(identifier_pairs)
                constraint_value = "{prefix}|{suffix}".format(prefix=constraint_prefix, suffix=constraint_suffix)
                identifiers.append(constraint_value)

    return identifiers


def perform_unique_checks(connection, model, primary, test_fn):
    """
        fetch_fn: Given a combination (and the default_fetch_fn), returns the result that's passed to test_fn
        test_fn: Takes a query result and returns true if it will cause a constraint issue
    """
    def fetch(combination, **kwargs):
        query = connection.get_query_class()(
            connection,
            [primary.key().path[-1]],
            namespace=connection.namespace,
        )

        filtered = False
        for field in combination:
            field = model._meta.get_field(field)
            col_name = field.column
            value = primary.get(col_name)
            if value is None:
                return
            if field.db_type(connection) in ('list', 'set'):
                if len(value) == 0:
                    return
                if isinstance(value, (list, set, tuple)) and value:
                    query.add_filter(col_name, 'array_contains_all', value)
                else:
                    query.add_filter(col_name, 'array_contains', value)
                filtered = True
            elif value is None:
                return
            else:
                query.add_filter(col_name, '=', value)
                filtered = True

        # only perform the query if there are filters on it
        if filtered:
            try:
                return list(query.fetch(offset=0, limit=1))
            except NotSupportedError:
                # This query with `limit=1` isn't supported in Firestore,
                # retry removing the limit.
                return list(query.fetch(offset=0, limit=None))

    combinations = _unique_combinations(model, ignore_pk=True)
    for combination in combinations:
        res = fetch(combination)
        if res and test_fn(res, combination):
            raise IntegrityError(
                CONSTRAINT_VIOLATION_MSG.format(model._meta.db_table, ", ".join(combination))
            )
