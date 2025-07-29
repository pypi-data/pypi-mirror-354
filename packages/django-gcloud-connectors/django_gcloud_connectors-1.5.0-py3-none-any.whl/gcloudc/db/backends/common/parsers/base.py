import logging
import decimal
from typing import Optional, List
from django.core.exceptions import FieldError, FieldDoesNotExist, EmptyResultSet
from django.db import NotSupportedError
from django.db.models.aggregates import Aggregate
from django.db.models.query import FlatValuesListIterable, QuerySet
from django.db.models.sql.query import Query as DjangoQuery
from gcloudc.db.backends.common.base.query import ORQuery
from gcloudc.db.backends.common.indexing import get_indexer, special_indexes_for_column
from .builder import QueryBuilder, WhereNode
from django.db import DatabaseError
from ..helpers import has_concrete_parents, indexed_columns_on_model, get_top_concrete_parent
from .dnf import normalize_query
from ..constraints import _unique_combinations


# Django >= 1.9
class ValuesListQuerySet(object):
    pass


def _iterable(x):
    # Returns True if x is iterable and not a string type
    return hasattr(x, "__iter__") and not isinstance(x, (str, bytes))


logger = logging.getLogger(__name__)


INVALID_ORDERING_FIELD_MESSAGE = (
    "Ordering on TextField or BinaryField is not supported on the Datastore. "
    "You might consider using a ComputedCharField which stores the first "
    "_MAX_STRING_LENGTH (from google.appengine.api.datastore_types) bytes of the "
    "field and instead order on that."
)


def _get_concrete_fields_with_model(model):
    return [
        (f, f.model if f.model != model else None)
        for f in model._meta.get_fields()
        if f.concrete and (not f.is_relation or f.one_to_one or (f.many_to_one and f.related_model))
    ]


def _walk_django_where(query, trunk_callback, leaf_callback, **kwargs):
    """
        Walks through a Django where tree. If a leaf node is encountered
        the leaf_callback is called, otherwise the trunk_callback is called
    """

    def walk_node(node, **kwargs):
        negated = kwargs["negated"]

        if node.negated:
            negated = not negated

        for child in node.children:
            new_kwargs = kwargs.copy()
            new_kwargs["negated"] = negated
            if not getattr(child, "children", []):
                leaf_callback(child, **new_kwargs)
            else:
                new_parent = trunk_callback(child, **new_kwargs)

                if new_parent:
                    new_kwargs["new_parent"] = new_parent

                walk_node(child, **new_kwargs)

    kwargs.setdefault("negated", False)
    walk_node(query.where, **kwargs)


class BaseParser(object):
    """
        Supports the most recent version of Django. Subclasses can
        override parts of this to support older versions.

        (NOTE: this goes against all my thoughts on good OO but I can't think
        of a cleaner way of doing things at the moment!)
    """

    def __init__(self, django_query, connection=None):
        self.django_query = django_query
        self.connection = connection
        self.model = self.django_query.model

    def deferred_to_columns(self):
        """
        Convert the self.deferred_loading data structure to mapping of table
        names to sets of column names which are to be loaded. Return the
        dictionary.
        """
        columns = {}
        # This is bad, but it's necessary to work around inconsistencies between
        # the Query implementation in django 3.2+ vs 4.1.
        extra_kwargs = {}
        if hasattr(self.django_query, "get_loaded_field_names_cb"):
            extra_kwargs["callback"] = self.django_query.get_loaded_field_names_cb

        # Django <4.2 has deferred_to_data
        if hasattr(self.django_query, "deferred_to_data"):
            self.django_query.deferred_to_data(columns, **extra_kwargs)
        else:
            # Django 4.2 introduced get_select_mask instead
            for field, _ in self.django_query.get_select_mask().items():
                # Django 5 wraps relational fields in an additional object
                if hasattr(field, "field"):
                    field = field.field
                columns.setdefault(field.model, set()).add(field.column)

        return columns

    def _prepare_for_transformation(self):
        from django.db.models.sql.where import NothingNode

        query = self.django_query

        def where_will_always_be_empty(where):
            if isinstance(where, NothingNode):
                return True

            if where.connector == "AND" and any(isinstance(x, NothingNode) for x in where.children):
                return True

            if where.connector == "OR" and len(where.children) == 1 and isinstance(where.children[0], NothingNode):
                return True

            return False

        # It could either be a NothingNode, or a WhereNode(AND NothingNode)
        if where_will_always_be_empty(query.where):
            # Empty where means return nothing!
            raise EmptyResultSet()

    def _extract_projected_columns(self):
        result = []
        query = self.django_query

        if query.select:
            for x in query.select:
                column = x.target.column
                result.append(column)
            return result
        else:
            # If the query uses defer()/only() then we need to process deferred. We have to get all deferred columns
            # for all (concrete) inherited models and then only include columns if they appear in that list
            only_load = self.deferred_to_columns()
            if only_load:
                for field, model in _get_concrete_fields_with_model(query.model):
                    model = model or query.model
                    try:
                        if field.column in only_load[model]:
                            # Add a field that has been explicitly included
                            result.append(field.column)
                    except KeyError:
                        # Model wasn't explicitly listed in the only_load table
                        # Therefore, we need to load all fields from this model
                        result.append(field.column)
                return result
            else:
                return []

    def _apply_ordering_to_query(self, query):
        # Extract the ordering of the query results
        for order_col in self.get_extracted_ordering():
            query.add_order_by(order_col)

    def _set_projected_columns_on_query(self, query):
        # Extract any projected columns (values/values_list/only/defer)
        for projected_col in self._extract_projected_columns():
            query.add_projected_column(projected_col)

    def _apply_extra_selects_to_query(self, query):
        # Add any extra selects
        for col, select in self.django_query.extra_select.items():
            query.add_extra_select(col, select[0])

    def _apply_annotations_to_query(self, query):
        # Process annotations!
        if self.django_query.annotation_select:
            for k, v in self.django_query.annotation_select.items():
                query.add_annotation(k, v)

    def _apply_distinct_columns_to_query(self, query):
        if self.django_query.distinct:
            # This must happen after extracting projected cols
            query.set_distinct(list(self.django_query.distinct_fields))

    def _where_node_trunk_callback(self, node, negated, new_parent, **kwargs):
        new_node = WhereNode(new_parent.using)
        new_node.connector = node.connector
        new_node.negated = node.negated

        new_parent.children.append(new_node)

        return new_node

    def _where_node_leaf_callback(self, node, negated, new_parent, connection, model, compiler):
        new_node = WhereNode(new_parent.using)

        def convert_rhs_op(node):
            db_rhs = getattr(node.rhs, "_db", None)
            if db_rhs is not None and db_rhs != connection.alias:
                raise ValueError(
                    "Subqueries aren't allowed across different databases. Force "
                    "the inner query to be evaluated using `list(inner_query)`."
                )

            value = node.get_rhs_op(connection, node.rhs)
            operator = value.split()[0].lower().strip()
            if operator == "between":
                operator = "range"
            return operator

        if not hasattr(node, "lhs"):
            raise NotSupportedError("Attempted probable subquery, these aren't supported on the Datastore")

        # Don't call on querysets
        if not hasattr(node.rhs, "_as_sql") and not isinstance(node.rhs, DjangoQuery):
            try:
                # Although we do nothing with this. We need to call it as many lookups
                # perform validation etc.
                node.process_rhs(compiler, connection)
            except EmptyResultSet:
                if node.lookup_name == "in":
                    node.rhs = []
                else:
                    raise

        # Leaf
        if hasattr(node.lhs, "target"):
            # from Django 1.9, some node.lhs might not have a target attribute
            # as they might be wrapping date fields
            field = node.lhs.target
            operator = convert_rhs_op(node)
        elif isinstance(node.lhs, Aggregate):
            raise NotSupportedError("Aggregate filters are not supported")
        else:
            field = node.lhs.lhs.target
            operator = convert_rhs_op(node)

            # This deals with things like datefield__month__gt=X which means from this point
            # on, operator will have two parts in that particular case and will probably need to
            # be dealt with by a special indexer
            if node.lookup_name != node.lhs.lookup_name:
                operator = "{}__{}".format(node.lhs.lookup_name, node.lookup_name)

        if get_top_concrete_parent(field.model) != get_top_concrete_parent(model):
            raise NotSupportedError("Cross-join where filters are not supported")

        # Make sure we don't let people try to filter on a text field, otherwise they just won't
        # get any results!

        lookup_supports_text = getattr(node, "lookup_supports_text", False)

        if field.db_type(connection) in ("bytes", "text") and not lookup_supports_text:
            raise NotSupportedError("You can't filter on text or blob fields")

        if operator == "isnull" and field.model._meta.parents.values():
            raise NotSupportedError("isnull lookups on inherited relations aren't supported")

        if negated and operator in ("=", ">", ">=", "<", "<=") and field.db_type(connection) in ("list", "set"):
            raise NotSupportedError("inequality filters on list fields return unexpected results")

        lhs = field.column
        was_iter = None

        if hasattr(node.rhs, "get_compiler"):
            if len(node.rhs.select) == 1:
                # In Django >= 1.11 this is a values list type query, which we explicitly handle
                # because of the common case of pk__in=Something.objects.values_list("pk", flat=True)
                qs = QuerySet(query=node.rhs, using=self.connection.alias)

                # Explicitly tell the code below that this was an iterable. This whole set of
                # if/elif statements might benefit from rethinking!
                was_iter = True
                rhs = list(qs.values_list("pk", flat=True))
            else:
                # This is a subquery
                raise NotSupportedError("Attempted to run a subquery on an non-relational database")
        elif isinstance(node.rhs, ValuesListQuerySet):
            # We explicitly handle ValuesListQuerySet because of the
            # common case of pk__in=Something.objects.values_list("pk", flat=True)
            # this WILL execute another query, but that is to be expected on a
            # non-relational database.

            rhs = [x for x in node.rhs]  # Evaluate the queryset

        elif isinstance(node.rhs, QuerySet):
            # In Django 1.9, ValuesListQuerySet doesn't exist anymore, and instead
            # values_list returns a QuerySet
            if node.rhs._iterable_class == FlatValuesListIterable:
                # if the queryset has FlatValuesListIterable as iterable class
                # then it's a flat list, and we just need to evaluate the
                # queryset converting it into a list
                rhs = [x for x in node.rhs]
            else:
                # otherwise, we try to get the PK from the queryset
                rhs = list(node.rhs.values_list("pk", flat=True))
        else:
            rhs = node.rhs

        if was_iter is None:
            was_iter = _iterable(node.rhs)

        rhs = node.get_db_prep_lookup(rhs, connection)[-1]
        if rhs and not was_iter and _iterable(rhs):
            rhs = rhs[0]

        # This is a special case. Annoyingly Django's decimal field doesn't
        # ever call ops.get_prep_save or lookup or whatever when you are filtering
        # on a query. It *does* do it on a save, so we basically need to do a
        # conversion here, when really it should be handled elsewhere.
        # *Seems to be fixed in Django 4.2+*
        if isinstance(rhs, decimal.Decimal):
            rhs = self.connection.ops.adapt_decimalfield_value(
                rhs,
                field.max_digits,
                field.decimal_places,
            )

        new_node.set_leaf(
            lhs,
            operator,
            rhs,
            is_pk_field=field == model._meta.pk,
            negated=negated,
            lookup_name=node.lookup_name,
            namespace=connection.namespace,
            target_field=field,
        )

        # For some reason, this test:
        # test_update_with_related_manager (get_or_create.tests.UpdateOrCreateTests)
        # ends up with duplicate nodes in the where tree. I don't know why. But this
        # weirdly causes the Datastore query to return nothing.
        # so here we don't add duplicate nodes, I can't think of a case where that would
        # change the query if it's under the same parent.
        if new_node in new_parent.children:
            return

        new_parent.children.append(new_node)

    def _generate_where_node(self, query):
        output = WhereNode(query.connection.alias)
        output.connector = self.django_query.where.connector
        _walk_django_where(
            self.django_query,
            self._where_node_trunk_callback,
            self._where_node_leaf_callback,
            new_parent=output,
            connection=self.connection,
            negated=self.django_query.where.negated,
            model=self.model,
            compiler=self.django_query.get_compiler(self.connection.alias),
        )

        return output

    def _remove_overlapping_exact_and_in(self, where):
        """ Given a WhereNode, find any IN filter which is combined with an "exact" filter where the
            value of the "exact" filter exists in the value of the "IN" filter, and remove that "IN"
            filter. This is because in that scenario the "IN" has no effect other than to confuse
            our DNF code. Django doesn't remove this for us.
        """
        equality_nodes_by_column = {}
        for node in where.children:
            if node.children and not node.column:
                # The node is a combinator, rather than a filter itself; traverse down the tree
                self._remove_overlapping_exact_and_in(node)
            elif (
                where.connector == "AND"
                and node.lookup_name in ("exact", "in")
                and not node.negated
            ):
                equality_nodes_by_column.setdefault(node.column, [])
                equality_nodes_by_column[node.column].append(node)
        for column, nodes in equality_nodes_by_column.items():
            if len(nodes) > 1:
                # exact_nodes = [node for node in nodes if node.lookup_name == "exact"]
                # If there's an "exact" lookup, then any other lookups are redunant. So we pick
                # an exact node at random to keep, and discard any other "exact" or "in" lookups.
                exact_values = {
                    node.value for node in nodes
                    if node.lookup_name == "exact" and not node.negated
                }
                if exact_values:
                    for node in nodes:
                        if (
                            node.lookup_name == "in"
                            and not node.negated
                            and set(node.value).intersection(exact_values)
                        ):
                            # The node is an "in" filter which overlaps with (one of) the exact
                            # filter(s), and therefore has no useful effect
                            where.children.remove(node)

    def _remove_impossible_branches(self, query):
        """
            If we mark a child node as never returning results we either need to
            remove those nodes, or remove the branches of the tree they are on depending
            on the connector of the parent node.
        """
        if not query._where:
            return

        def walk(node, negated):
            if node.negated:
                negated = not negated

            for child in node.children[:]:
                walk(child, negated)

                if child.will_never_return_results:
                    if node.connector == "AND":
                        if child.negated:
                            node.children.remove(child)
                        else:
                            node.will_never_return_results = True
                    else:
                        # OR
                        if not child.negated:
                            node.children.remove(child)
                            if not node.children:
                                node.will_never_return_results = True
                        else:
                            node.children[:] = []

        walk(query._where, False)

        if query._where.will_never_return_results:
            # We removed all the children of the root where node, so no results
            raise EmptyResultSet()

    def _remove_erroneous_isnull(self, query):
        # This is a little weird, but bear with me...
        # If you run a query like this:  filter(thing=1).exclude(field1="test") where field1 is
        # null-able you'll end up with a negated branch in the where tree which is:

        #           AND (negated)
        #          /            \
        #   field1="test"   field1__isnull=False

        # This is because on SQL, field1 != "test" won't give back rows where field1 is null, so
        # django has to include the negated isnull=False as well in order to get back the null rows
        # as well.  On App Engine though None is just a value, not the lack of a value, so it's
        # enough to just have the first branch in the negated node and in fact, if you try to use
        # the above tree, it will result in looking for:
        #  field1 < "test" and field1 > "test" and field1__isnull=True
        # which returns the wrong result (it'll return when field1 == None only)

        def walk(node, negated):
            if node.negated:
                negated = not negated

            if not node.is_leaf:
                equality_fields = set()
                negated_isnull_fields = set()
                isnull_lookup = {}

                for child in node.children[:]:
                    if negated:
                        if child.lookup_name != "isnull":
                            equality_fields.add(child.column)
                            if child.column in negated_isnull_fields:
                                node.children.remove(isnull_lookup[child.column])
                        else:
                            negated_isnull_fields.add(child.column)
                            if child.column in equality_fields:
                                node.children.remove(child)
                            else:
                                isnull_lookup[child.column] = child

                    walk(child, negated)

        if query.where:
            walk(query._where, False)

    def _remove_negated_empty_in(self, query):
        """
            An empty exclude(id__in=[]) is pointless, but can cause trouble
            during denormalization. We remove such nodes here.
        """
        if not query._where:
            return

        def walk(node, negated):
            if node.negated:
                negated = node.negated

            for child in node.children[:]:
                if negated and child.operator == "IN" and not child.value:
                    node.children.remove(child)

                walk(child, negated)

            node.children = [x for x in node.children if x.children or x.column]

        had_where = bool(query._where.children)
        walk(query._where, False)

        # Reset the where if that was the only filter
        if had_where and not bool(query._where.children):
            query._where = None

    def _add_inheritence_filter(self, query):
        """
            We support inheritence with polymodels. Whenever we set
            the 'where' on this query, we manipulate the tree so that
            the lookups are ANDed with a filter on 'class = db_table'
            and on inserts, we add the 'class' column if the model is part
            of an inheritance tree.

            We only do any of this if the model has concrete parents and isn't
            a proxy model
        """
        if has_concrete_parents(self.model) and not self.model._meta.proxy:
            if query.polymodel_filter_added:
                return

            new_filter = WhereNode(query.connection.alias)
            new_filter.column = query.connection.polymodel_property_name()
            new_filter.operator = "array_contains"
            new_filter.value = self.model._meta.db_table

            # We add this bare AND just to stay consistent with what Django does
            new_and = WhereNode(query.connection.alias)
            new_and.connector = "AND"
            new_and.children = [new_filter]

            new_root = WhereNode(query.connection.alias)
            new_root.connector = "AND"
            new_root.children = [new_and]
            if query._where:
                # Add the original where if there was one
                new_root.children.append(query._where)
            query._where = new_root

            query.polymodel_filter_added = True

    def _populate_excluded_pks(self, query):
        if not query._where:
            return

        query.excluded_pks = set()

        def walk(node, negated):
            if node.connector == "OR":
                # We can only process AND nodes, if we hit an OR we can't
                # use the excluded PK optimization
                return

            if node.negated:
                negated = not negated

            for child in node.children[:]:
                # As more than one inequality filter is not allowed on the datastore
                # this leaf + count check is probably pointless, but at least if you
                # do try to exclude two things it will blow up in the right place and not
                # return incorrect results
                if child.is_leaf and len(node.children) == 1:
                    if negated and child.operator == "=" and child.column == query.connection.key_property_name():
                        query.excluded_pks.add(child.value)
                        node.children.remove(child)
                    elif negated and child.operator == "IN" and child.column == query.connection.key_property_name():
                        [query.excluded_pks.add(x) for x in child.value]
                        node.children.remove(child)
                else:
                    walk(child, negated)

            node.children = [x for x in node.children if x.children or x.column]

        walk(query._where, False)

        if not query._where.children:
            query._where = None

    def _disable_projection_if_fields_used_in_equality_filter(self, query):
        if not query._where or not query.columns:
            return

        equality_columns = set()

        def walk(node):
            if not node.is_leaf:
                for child in node.children:
                    walk(child)
            elif node.operator == "=" or node.operator == "IN":
                equality_columns.add(node.column)

        walk(query._where)

        if equality_columns and equality_columns.intersection(query.columns):
            query.projection_possible = False

    def _check_only_single_inequality_filter(self, query):
        inequality_fields = set()

        def walk(node, negated):
            if node.negated:
                negated = not negated

            for child in node.children[:]:
                if (negated and child.operator == "=") or child.operator in (">", "<", ">=", "<="):
                    inequality_fields.add(child.column)
                walk(child, negated)

            if len(inequality_fields) > 1:
                raise NotSupportedError(
                    "You can only have one inequality filter per query on the rpc. "
                    "Filters were: %s" % " ".join(inequality_fields)
                )

        if query.where:
            walk(query._where, False)

    def _apply_keys_only_flag(self, qry, keys_only):
        # We enable keys only queries if they have been forced, or, if
        # someone did only("pk") or someone did values_list("pk") this is a little
        # inconsistent with other fields which aren't projected if just values(_list) is used
        pk_field = self.django_query.model._meta.pk
        qry.keys_only = (
            keys_only
            or (
                self.django_query.deferred_loading[1] is False
                and len(self.django_query.deferred_loading[0]) == 1
                and self.django_query.model._meta.pk.column in self.django_query.deferred_loading[0]
            )
            or (len(self.django_query.select) == 1 and self.django_query.select[0].field == pk_field)
        )

        # MultiQuery doesn't support keys_only
        if self.django_query.where and len(self.django_query.where.children) > 1:
            qry.keys_only = False

    def _sense_check(self, ret):
        # Local so we don't have a circular import
        from django.conf import settings

        if ret.distinct and not ret.columns:
            raise NotSupportedError("Tried to perform distinct query when projection wasn't possible")

        def _exclude_pk(columns) -> Optional[List[str]]:
            if columns is None:
                return None

            opts = ret.model._meta
            copts = ret.concrete_model._meta

            return [x for x in columns if x not in (opts.pk.column, copts.pk.column)]

        projection = _exclude_pk(ret.columns) or None

        model_indexed_fields = indexed_columns_on_model(ret.model)

        perform_index_checking = (
            model_indexed_fields and f"{ret.model._meta.app_label}.{ret.model.__name__}"
            not in getattr(settings, "GCLOUDC_EXCLUDE_FROM_INDEX_CHECKS", [])
        )

        if not perform_index_checking:
            return

        if projection:
            missing_index_fields = set(projection) - model_indexed_fields
            if missing_index_fields:
                raise DatabaseError(
                    f"Projection query missing an index: Ensure field `{missing_index_fields}` "
                    f"is indexed by defining the field in the meta of `{ret.model}`."
                )

        for and_branch in ret.where.children if ret.where else []:
            # This deals with the oddity that the root of the tree may well be a leaf
            filters = [and_branch] if and_branch.is_leaf else and_branch.children

            for filter_node in filters:
                if (
                    filter_node.column != self.connection.key_property_name()
                    and filter_node.column != self.connection.polymodel_property_name()
                    and filter_node.column not in model_indexed_fields
                ):
                    raise DatabaseError(
                        f"Query missing an index: Ensure field `{filter_node.column}` "
                        f"is indexed by defining the field in the Meta.indexes of `{ret.model}`."
                    )

    def _generate_builder(self, force_keys_only):
        self._prepare_for_transformation()

        ret = QueryBuilder(self.model, self.connection)

        # Add the root concrete table as the source table
        root_table = get_top_concrete_parent(self.model)._meta.db_table
        ret.add_source_table(root_table)
        self._apply_ordering_to_query(ret)
        self._set_projected_columns_on_query(ret)
        self._apply_extra_selects_to_query(ret)
        self._apply_distinct_columns_to_query(ret)
        self._apply_annotations_to_query(ret)

        # Extract any query offsets and limits
        ret.low_mark = self.django_query.low_mark
        ret.high_mark = self.django_query.high_mark

        output = self._generate_where_node(ret)
        self._remove_overlapping_exact_and_in(output)

        # If there no child nodes, just wipe out the where
        if not output.children:
            output = None

        ret.where = output

        self._remove_impossible_branches(ret)
        self._remove_erroneous_isnull(ret)
        self._remove_negated_empty_in(ret)
        self._add_inheritence_filter(ret)
        self._populate_excluded_pks(ret)
        self._disable_projection_if_fields_used_in_equality_filter(ret)
        self._check_only_single_inequality_filter(ret)

        ret = normalize_query(ret)

        self._apply_list_field_operators(ret)
        self._squash_contains(ret)
        self._apply_keys_only_flag(ret, force_keys_only)
        self._sense_check(ret)

        return ret

    def _apply_list_field_operators(self, query):
        """
            If a backend supplies:

             - array_contains_operator: str

            This will be used instead of "=" when querying list fields.

            If a backend supplies:

             - array_empty_operator_and_value: Tuple[str, str]

            This will be used in place of array > None
        """

        def array_fields_from_model():
            for field in self.model._meta.fields:
                if field.db_type(self.connection) in ('list', 'set'):
                    yield field.column

                for name in special_indexes_for_column(self.model, field.column):
                    # These indexers use array fields under the hood
                    if name in (
                        'endswith',
                        'startswith',
                        'iendswith',
                        'istartswith',
                        'item__startswith',
                        'item__endswith',
                        'item__iendswith',
                        'item__istartswith'
                    ):

                        indexer = get_indexer(field, name)
                        yield indexer.indexed_column_name(field.column, None, None)

        def is_array_field(column):
            return column in array_fields_from_model()

        def walk(node, negated):
            if node.negated:
                negated = not negated

            for child in node.children[:]:
                if is_array_field(child.column):
                    if negated:
                        iterable_value = isinstance(child.value, (list, set, tuple))
                        if child.operator == "=":
                            if iterable_value and not child.value:
                                # Unless the list is Falsey, in which case we use the empty operator
                                # and value
                                child.operator, child.value = self.connection.array_not_empty_operator_and_value
                            else:
                                raise NotSupportedError(
                                    "Can't support negated '=' filter on an array field"
                                )
                        elif not iterable_value and child.operator == "<":
                            child.operator = ">="
                        elif not iterable_value and child.operator == "<=":
                            child.operator = ">"
                        elif not iterable_value and child.operator == ">=":
                            child.operator = "<"
                        elif not iterable_value and child.operator == ">":
                            child.operator = "<="
                        else:
                            raise NotSupportedError(
                                f"Can't support negated '{child.operator}' filter on an array field"
                            )
                    else:
                        if child.operator == "=":
                            iterable_value = isinstance(child.value, (list, set, tuple))
                            # If we specify a list, we want to return things that match
                            # all items
                            if iterable_value and child.value:
                                child.operator = "array_contains_all"
                            elif iterable_value and not child.value:
                                # Unless the list is Falsey, in which case we use the empty operator
                                # and value
                                child.operator, child.value = self.connection.array_empty_operator_and_value
                            else:
                                child.operator = "array_contains"
                        elif (child.operator, child.value) != self.connection.array_not_empty_operator_and_value:
                            raise NotSupportedError(
                                f"Can't support '{child.operator}' filter on an array field"
                            )

                walk(child, negated)

        if query.where:
            walk(query._where, False)

    def _squash_contains(self, query):
        """Normalise (contains X) AND (contains Y)  to (contains_all X Y)"""
        def walk(node, negated):
            if node.negated:
                negated = not negated

            # At this stage, the query is normalised, so we have a disjunction of either
            # conjunctions or leaf nodes. We only care about squashing for conjunctions
            if node.connector == "AND":
                contains_lookups = {}
                new_children = []
                for child in node.children[:]:
                    if child.operator in ("array_contains", "array_contains_all"):
                        contains_lookups.setdefault(child.column, []).append(child)
                    else:
                        new_children.append(child)

                for _, nodes in contains_lookups.items():
                    if len(nodes) > 1:

                        new_values = []
                        for n in nodes:
                            if isinstance(n.value, list):
                                new_values.extend(n.value)
                            else:
                                new_values.append(n.value)

                        # remove duplicates
                        nodes[0].value = list(set(new_values))
                        if len(nodes[0].value) > 1:
                            nodes[0].operator = "array_contains_all"
                        else:
                            nodes[0].value = nodes[0].value[0]

                        new_children.append(nodes[0])
                    else:
                        new_children.append(nodes[0])

                node.children[:] = new_children

            for child in node.children[:]:
                walk(child, negated)

        if query.where:
            walk(query._where, False)

    def get_transformed_query(self, connection, force_keys_only=False) -> ORQuery:
        builder: QueryBuilder = self._generate_builder(force_keys_only=force_keys_only)

        all_fields_selected = builder.columns is None or (len(builder.columns) == len(self.model._meta.fields))

        if builder.projection_possible and not all_fields_selected:
            only_return_fields = [x for x in builder.columns or [] if x != self.model._meta.pk.column] or None
        else:
            only_return_fields = None

        unique_combos = _unique_combinations(self.model, ignore_pk=True)

        field_columns = [x.column for x in self.model._meta.fields]

        query = ORQuery(
            connection,
            builder.tables[0],
            unique_combos,
            only_return_keys=builder.keys_only,
            only_return_fields=only_return_fields,
            select=builder.columns or field_columns,
            distinct_fields=only_return_fields if builder.distinct else None,
            annotations=builder.extra_selects,
        )

        if builder.where and builder.where.children:
            for branch in (builder.where.children if builder.where else []):
                sub_query = query.push_query(connection)

                # This deals with the oddity that the root of the tree may well be a leaf
                filters = [branch] if branch.is_leaf else branch.children

                for filter_node in filters:
                    sub_query.add_filter(filter_node.column, filter_node.operator, filter_node.value)
        else:
            # No where tree? Add a single unfiltered query
            sub_query = query.push_query(connection)

        # We only order by fields which are actual fields in the database (e.g. not annotations)
        ordering = [
            x for x in builder.order_by
            if x.lstrip("-") in field_columns + [self.connection.key_property_name()]
        ]

        memory_ordering = None
        if len(ordering) != len(builder.order_by):
            # 1+ of the ordering fields was not a real column, so we pass this as the in memory
            # ordering
            memory_ordering = builder.order_by

        query.order_by(ordering, memory_ordering=memory_ordering)
        query.set_excluded_keys(builder.excluded_pks)
        return query

    def get_extracted_ordering(self):
        from gcloudc.db.backends.common.commands import log_once
        from django.db.models.expressions import OrderBy, F
        from .expressions import Scatter

        query = self.django_query

        # Add any orderings
        if not query.default_ordering:
            result = list(query.order_by)
        else:
            result = list(query.order_by or query.get_meta().ordering or [])

        if query.extra_order_by:
            result = list(query.extra_order_by)

            # we need some extra logic to handle dot seperated ordering
            new_result = []
            cross_table_ordering = set()
            for ordering in result:
                if "." in ordering:
                    dot_based_ordering = ordering.split(".")
                    if dot_based_ordering[0] == query.model._meta.db_table:
                        ordering = dot_based_ordering[1]
                    elif dot_based_ordering[0].lstrip("-") == query.model._meta.db_table:
                        ordering = "-{}".format(dot_based_ordering[1])
                    else:
                        cross_table_ordering.add(ordering)
                        continue  # we don't want to add this ordering value
                new_result.append(ordering)

            if len(cross_table_ordering):
                log_once(
                    logger.warning,
                    "The following orderings were ignored as cross-table orderings"
                    " are not supported on the Datastore: %s",
                    cross_table_ordering,
                )

            result = new_result

        final = []

        opts = query.model._meta

        # Apparently expression ordering is absolute and so shouldn't be flipped
        # if the standard_ordering is False. This keeps track of which columns
        # were expressions and so don't need flipping
        expressions = set()

        for col in result:
            if isinstance(col, OrderBy):
                descending = col.descending
                col = col.expression.name
                if descending:
                    col = "-" + col
                expressions.add(col)
            elif isinstance(col, F):
                col = col.name
            elif isinstance(col, Scatter):
                final.append("__scatter__")
                continue

            if isinstance(col, int):
                # If you do a Dates query, the ordering is set to [1] or [-1]... which is weird
                # I think it's to select the column number but then there is only 1 column so
                # unless the ordinal is one-based I have no idea. So basically if it's an integer
                # subtract 1 from the absolute value and look up in the select for the column (guessing)
                idx = abs(col) - 1
                try:
                    field_name = query.select[idx].col.col[-1]
                    field = query.model._meta.get_field(field_name)
                    final.append("-" + field.column if col < 0 else field.column)
                except IndexError:
                    raise NotSupportedError("Unsupported order_by %s" % col)
            elif col.lstrip("-") == "pk":
                pk_col = self.connection.key_property_name()
                final.append("-" + pk_col if col.startswith("-") else pk_col)
            elif col == "?":
                raise NotSupportedError("Random ordering is not supported on the Datastore")
            elif col.lstrip("-").startswith("__") and col.endswith("__"):
                # Allow stuff like __scatter__
                final.append(col)
            elif "__" in col:
                continue
            else:
                try:
                    column = col.lstrip("-")
                    field = opts.get_field(column)

                    if field.get_internal_type() in (u"TextField", u"BinaryField"):
                        raise NotSupportedError(INVALID_ORDERING_FIELD_MESSAGE)

                    # If someone orders by 'fk' rather than 'fk_id' this complains as that should take
                    # into account the related model ordering. Note the difference between field.name == column
                    # and field.attname (X_id)
                    if field.related_model and field.name == column and field.related_model._meta.ordering:
                        raise NotSupportedError("Related ordering is not supported.")

                    column = self.connection.key_property_name() if field.primary_key else field.column
                    final.append("-" + column if col.startswith("-") else column)
                except FieldDoesNotExist:
                    column = col.lstrip("-")
                    if column in query.extra_select:
                        # If the column is in the extra select we transform to the original
                        # column
                        try:
                            field = opts.get_field(query.extra_select[col][0])
                            column = self.connection.key_property_name() if field.primary_key else field.column
                            final.append("-" + column if col.startswith("-") else column)
                            continue
                        except FieldDoesNotExist:
                            # Just pass through to the exception below
                            pass
                    elif column in query.annotations:
                        try:
                            # If the annotation has a target field then use the db column for that, otherwise
                            # just use the provided target column provided to the annotation
                            if hasattr(query.annotations[column], "lhs"):
                                field = query.annotations[column].lhs.field
                                column = self.connection.key_property_name() if field.primary_key else field.column

                            final.append("-" + column if col.startswith("-") else column)
                            continue
                        except FieldDoesNotExist:
                            pass

                    available = opts.get_fields()
                    raise FieldError(
                        "Cannot resolve keyword %r into field. " "Choices are: %s" % (
                            col, ", ".join([getattr(x, "attname", "unknown") for x in available])
                        )
                    )
            try:
                # It doesn't make sense to order_by a field after ordering by its primary key
                # given it's unique and further ordering wouldn't make a difference.
                column = col.lstrip("-")
                field = opts.get_field(column)
                if field.primary_key:
                    break
            except FieldDoesNotExist:
                pass

        # Reverse if not using standard ordering
        def swap(col):
            if col.startswith("-"):
                return col.lstrip("-")
            else:
                return "-{}".format(col)

        if not query.standard_ordering:
            final = [x if x in expressions else swap(x) for x in final]

        if len(final) != len(result):
            diff = set(result) - set(final)
            log_once(
                logger.warning,
                "The following orderings were ignored as cross-table and random orderings"
                " are not supported on the Datastore: %s",
                diff,
            )

        # Remove duplicates in the ordering
        # This is to handle the following case:
        # `MyModel.object.order_by('name', 'name')`
        final = list(dict.fromkeys(final))

        return final
