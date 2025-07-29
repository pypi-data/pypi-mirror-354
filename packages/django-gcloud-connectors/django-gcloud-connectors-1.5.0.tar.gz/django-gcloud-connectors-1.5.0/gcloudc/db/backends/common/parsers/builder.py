import logging
import re
import datetime
from itertools import chain
from typing import List
from django.db import (
    NotSupportedError,
    connections,
)
from django.db.models import AutoField
from django.db.models.lookups import Lookup
from gcloudc.db.backends.common.base.connection import Connection
from gcloudc.db.backends.common.base.entity import Key
from gcloudc.db.backends.common.indexing import (
    add_special_index,
    get_indexer,
)

from ..helpers import (
    get_field_from_column,
    get_top_concrete_parent,
    ensure_datetime,
)

logger = logging.getLogger(__name__)


VALID_QUERY_KINDS = ("SELECT", "UPDATE", "INSERT", "DELETE", "COUNT", "AVERAGE")
VALID_ANNOTATIONS = {"MIN": min, "MAX": max, "SUM": sum, "COUNT": len, "AVG": lambda x: (sum(x) / len(x))}
VALID_CONNECTORS = ("AND", "OR")
VALID_OPERATORS = ("=", "<", ">", "<=", ">=", "IN")


def convert_operator(operator):
    if operator == "exact":
        return "="
    elif operator == "gt":
        return ">"
    elif operator == "lt":
        return "<"
    elif operator == "gte":
        return ">="
    elif operator == "lte":
        return "<="

    return operator.upper()


class WhereNode:
    def __init__(self, using):
        self.using = using

        self.column = None
        self.operator = None
        self.value = None
        self.output_field = None
        self.will_never_return_results = False
        self.lookup_name = None
        self.is_iterable_field = False

        self.children = []
        self.connector = "AND"
        self.negated = False

    @property
    def is_leaf(self):
        return bool(self.column and self.operator)

    def set_connector(self, connector):
        self.connector = connector

    def append_child(self, node):
        self.children.append(node)

    def set_leaf(self, column, operator, value, is_pk_field, negated, lookup_name, namespace, target_field=None):
        # We need access to the Datastore client to access the Key factory
        wrapper = connections[self.using]
        wrapper.ensure_connection()

        assert column
        assert operator
        assert isinstance(is_pk_field, bool)
        assert isinstance(negated, bool)

        if operator == "iexact" and isinstance(target_field, AutoField):
            # When new instance is created, automatic primary key 'id'
            # does not generate '_idx_iexact_id'.
            # As the primary key 'id' (AutoField) is integer and is always case insensitive,
            # we can deal with 'id_iexact=' query by using 'exact' rather than 'iexact'.
            operator = "exact"
            value = int(value)

        if is_pk_field:
            # If this is a primary key, we need to make sure that the value
            # we pass to the query is a datastore Key. We have to deal with IN queries here
            # because they aren't flattened until the DNF stage
            model = get_top_concrete_parent(target_field.model)
            table = model._meta.db_table

            if isinstance(value, (list, tuple)):
                value = [
                    wrapper.connection.new_key(table, x, namespace=namespace)
                    for x in value if x
                ]
            else:
                # Django 1.11 has operators as symbols, earlier versions use "exact" etc.
                if (operator == "isnull" and value is True) or (
                    operator in ("exact", "lt", "lte", "<", "<=", "=") and not value
                ):
                    # id=None will never return anything and
                    # Empty strings and 0 are forbidden as keys
                    self.will_never_return_results = True
                    value = Key([""], 0)  # Impossible key
                elif operator in ("gt", "gte", ">", ">=") and not value:
                    # If the value is 0 or "", then we need to manipulate the value and operator here to
                    # get the right result (given that both are invalid keys) so for both we return
                    # >= 1 or >= "\0" for strings
                    if isinstance(value, int):
                        value = 1
                    else:
                        value = "\0"

                    value = wrapper.connection.new_key(table, value, namespace=namespace)
                    operator = "gte"
                else:
                    value = wrapper.connection.new_key(table, value, namespace=namespace)
            column = wrapper.key_property_name()

        # Do any special index conversions necessary to perform this lookup
        special_indexer = get_indexer(target_field, operator)

        if special_indexer:
            if is_pk_field:
                column = model._meta.pk.column
                value = str(value.id_or_name)

            add_special_index(
                connections[self.using],
                target_field.model, column, special_indexer, operator, value
            )

            index_type = special_indexer.prepare_index_type(operator, value)
            value = special_indexer.prep_value_for_query(
                value, model=target_field.model,
                column=column, connection=connections[self.using]
            )
            column = special_indexer.indexed_column_name(column, value, index_type, connection=wrapper)
            operator = special_indexer.prep_query_operator(operator)

        self.column = column
        self.operator = convert_operator(operator)
        self.value = value
        self.lookup_name = lookup_name
        self.is_iterable_field = target_field.db_type(wrapper) in ['list', 'set']

    def __iter__(self):
        for child in chain(*map(iter, self.children)):
            yield child
        yield self

    def __repr__(self):
        if self.is_leaf:
            return "[%s %s %s]" % (self.column, self.operator, self.value)
        else:
            return "(%s:%s%s)" % (
                self.connector,
                "!" if self.negated else "",
                ",".join([f"{x!r}" for x in self.children]),
            )

    def __eq__(self, rhs):
        if self.is_leaf != rhs.is_leaf:
            return False

        if self.is_leaf:
            assert (isinstance(self.column, str))
            assert (isinstance(rhs.column, str))
            return self.column == rhs.column and self.value == rhs.value and self.operator == rhs.operator
        else:
            return self.connector == rhs.connector and self.children == rhs.children

    def __hash__(self):
        if self.is_leaf:
            value = frozenset(self.value) if isinstance(self.value, (set, list, tuple)) else self.value
            return hash((self.column, value, self.operator))
        else:
            return hash((self.connector,) + tuple([hash(x) for x in self.children]))


class QueryBuilder(object):
    def __init__(self, model, connection):
        self.connection: Connection = connection
        self.model = model
        self.concrete_model = get_top_concrete_parent(model)

        self.projection_possible = True
        self.tables = []

        self.columns = None  # None means all fields

        self.distinct = False
        self.order_by: List[str] = []
        self.row_data = []  # For insert/updates
        self._where = None
        self.low_mark = self.high_mark = None

        self.polymodel_filter_added = False

        # A list of PKs that should be excluded from the resultset
        self.excluded_pks = set()
        self.keys_only = False

        self.extra_selects = []
        self.annotations = []
        self.per_entity_annotations = []

    @property
    def is_normalized(self):
        """
            Returns True if this query has a normalized where tree
        """
        if not self.where:
            return True

        # Only a leaf node, return True
        if not self.where.is_leaf:
            return True

        # If we have children, and they are all leaf nodes then this is a normalized
        # query
        return self.where.connector == "OR" and self.where.children and all(x.is_leaf for x in self.where.children)

    def add_extra_select(self, column, lookup):
        if lookup.lower().startswith("select "):
            raise ValueError("SQL statements aren't supported with extra(select=)")

        # Boolean expression test
        bool_expr = r"(?P<lhs>[a-zA-Z0-9_]+)\s?(?P<op>[=|>|<]{1,2})\s?(?P<rhs>[\w+|']+)"

        # Operator expression test
        op_expr = r"(?P<lhs>[a-zA-Z0-9_]+)\s?(?P<op>[+|-|/|*])\s?(?P<rhs>[\w+|']+)"

        OP_LOOKUP = {
            "=": lambda e, x, y: e[x] == y,
            "is": lambda e, x, y: e[x] == y,
            "<": lambda e, x, y: e[x] < y,
            ">": lambda e, x, y: e[x] > y,
            ">=": lambda e, x, y: e[x] >= y,
            "<=": lambda e, x, y: e[x] <= y,
            "+": lambda e, x, y: e[x] + y,
            "-": lambda e, x, y: e[x] - y,
            "/": lambda e, x, y: e[x] / y,
            "*": lambda e, x, y: e[x] * y,
        }

        for regex in (bool_expr, op_expr):
            match = re.match(regex, lookup)
            if match:
                lhs = match.group("lhs")
                rhs = match.group("rhs")
                op = match.group("op").lower()

                if rhs.lower() == "null":
                    rhs = None
                elif rhs.lower() == "false":
                    rhs = False
                elif rhs.lower() == "true":
                    rhs = True
                elif rhs.startswith("'") and rhs.endswith("'"):
                    rhs = rhs.strip("'")

                if op in OP_LOOKUP:
                    self.extra_selects.append((column, OP_LOOKUP[op], (lhs, rhs)))
                else:
                    raise ValueError("Unsupported operator")
                return

        # Assume literal
        self.extra_selects.append((column, lambda e, x: x, [lookup]))

    def add_source_table(self, table):
        if table in self.tables:
            return

        self.tables.append(table)

    def set_distinct(self, distinct_fields):
        self.distinct = True
        if distinct_fields:
            for field in distinct_fields:
                self.add_projected_column(field)
        elif not self.columns:
            for field in self.model._meta.fields:
                self.add_projected_column(field.column)

    def add_order_by(self, column):
        self.order_by.append(column)

    def add_annotation(self, column, annotation):
        # The Trunc annotation class doesn't exist in Django 1.8, hence we compare by
        # strings, rather than importing the class to compare it
        name = annotation.__class__.__name__
        if name == "Count":
            return  # Handled elsewhere

        if name == "Value":
            # This may break if we, in the future, decide we want to support Values in
            # F expression. AFAICT, Value is only used (outside of F expressions) as a
            # trick when performing "exists" queries, so it should be safe to ignore.
            return

        if name not in ("Trunc", "Col", "Date", "DateTime", "Case"):
            raise NotSupportedError("Unsupported annotation %s" % name)

        def process_date(value, lookup_type):
            value = ensure_datetime(value)
            ret = datetime.datetime.utcfromtimestamp(0)

            POSSIBLE_LOOKUPS = ("year", "month", "day", "hour", "minute", "second")
            ret = ret.replace(
                value.year,
                value.month if lookup_type in POSSIBLE_LOOKUPS[1:] else ret.month,
                value.day if lookup_type in POSSIBLE_LOOKUPS[2:] else ret.day,
                value.hour if lookup_type in POSSIBLE_LOOKUPS[3:] else ret.hour,
                value.minute if lookup_type in POSSIBLE_LOOKUPS[4:] else ret.minute,
                value.second if lookup_type in POSSIBLE_LOOKUPS[5:] else ret.second,
            )

            return ret

        # Abuse the extra_select functionality
        if name == "Col":
            self.extra_selects.append((column, lambda e, x: x, [column]))
        elif name == "Case":
            def entity_matches_where_tree(entity, node):
                comparisons = {
                    "exact": lambda n: entity[n.lhs.field.column] == n.rhs,
                }

                # negated = node.negated
                for child in node.children:
                    # If the child is a lookup, then we check that it matches the entity
                    if isinstance(child, Lookup):
                        if child.lookup_name not in comparisons:
                            raise NotImplementedError("Unimplemented lookup: %s" % child.lookup_name)

                        if not comparisons[child.lookup_name](child):
                            return False
                        else:
                            continue
                    else:
                        raise NotImplementedError("Only lookups are supported in Case annotations")
                else:
                    return True

            def process_case(e, *args):
                for case in annotation.cases:
                    if entity_matches_where_tree(e, case.condition):
                        return (
                            annotation.output_field.to_python(case.result.value)
                            if annotation.output_field
                            else case.result.value
                        )

                return (
                    annotation.output_field.to_python(annotation.default.value)
                    if annotation.output_field
                    else annotation.default.value
                )

            self.extra_selects.append((column, process_case, []))

        elif name in ("Trunc", "Date", "DateTime"):
            # Trunc stores the source column and the lookup type differently to Date
            # which is why we have the getattr craziness here
            lookup_column = (
                annotation.lhs.output_field.column if name == "Trunc" else getattr(annotation, "lookup", column)
            )

            lookup_type = getattr(annotation, "lookup_type", getattr(annotation, "kind", None))
            assert lookup_type

            self.extra_selects.append((column, lambda e, x: process_date(e[x], lookup_type), [lookup_column]))
            # Override the projection so that we only get this column
            self.columns = set([lookup_column])

    def add_projected_column(self, column):
        field = get_field_from_column(self.model, column)

        if field is None:
            raise NotSupportedError(
                "{} is not a valid column for the queried model. Did you try to join?".format(column)
            )

        if field.db_type(self.connection) in ("bytes", "text", "list", "set"):
            logger.warn("Disabling projection query as %s is an unprojectable type", column)
            self.projection_possible = False
            return

        if self.columns and column in self.columns:
            return

        if not self.columns:
            self.columns = [column]
        else:
            self.columns.append(column)

    @property
    def where(self):
        return self._where

    @where.setter
    def where(self, where):
        assert where is None or isinstance(where, WhereNode)

        self._where = where


INVALID_ORDERING_FIELD_MESSAGE = (
    "Ordering on TextField or BinaryField is not supported on the rpc. "
    "You might consider using a ComputedCharField which stores the first "
    "_MAX_STRING_LENGTH (from google.appengine.api.datastore_types) bytes of the "
    "field and instead order on that."
)


def _serialize_sql_value(value):
    if isinstance(value, int):
        return value
    else:
        return str("NULL" if value is None else value)
