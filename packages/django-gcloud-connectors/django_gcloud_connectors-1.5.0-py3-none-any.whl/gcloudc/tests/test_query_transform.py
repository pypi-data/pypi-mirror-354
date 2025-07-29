

from django.db import connection as default_connection
from django.db import (
    connections,
    models,
)
from django.db.models.query import Q
from django.core.exceptions import EmptyResultSet

from gcloudc.db.backends.common.parsers.dnf import normalize_query
from gcloudc.db.backends.common.parsers.builder import (
    QueryBuilder as Query,
    WhereNode,
)
from gcloudc.db.models.fields.iterable import ListField

from . import TestCase, datastore_only, firestore_only
from .models import (
    InheritedModel,
    Relation,
    TestUser,
    TransformTestModel,
)

DEFAULT_NAMESPACE = default_connection.ops.connection.settings_dict.get("NAMESPACE")


class ListFieldModel(models.Model):
    list_field = ListField(models.CharField(max_length=3))

    class Meta:
        app_label = "gcloudc"


def transform_query(connection, query):
    from gcloudc.db.backends.common.parsers import base
    parser = base.BaseParser(query, connection)
    return parser.get_transformed_query(
        connection
    )


def get_builder(connection, query):
    from gcloudc.db.backends.common.parsers import base
    parser = base.BaseParser(query, connection)
    return parser._generate_builder(connection)


def find_children_containing_node(list_of_possible_children, column, op, value):
    for children in list_of_possible_children:
        for node in (children or []):
            if node.column == column and node.operator == op and node.value == value:
                return children


class TransformQueryTest(TestCase):

    def test_polymodel_filter_applied(self):
        query = transform_query(
            connections['default'],
            InheritedModel.objects.filter(field1="One").all().query
        )

        self.assertEqual(
            query.queries[0].get_filter(connections['default'].polymodel_property_name(), "array_contains"),
            [InheritedModel._meta.db_table]
        )

        self.assertEqual(
            query.queries[0].get_filter("field1", "="),
            ["One"]
        )

    def test_basic_query(self):
        query = transform_query(
            connections['default'],
            TransformTestModel.objects.all().query
        )

        self.assertEqual(query.path, [TransformTestModel._meta.db_table])
        self.assertFalse(query.queries[0]._filters)

    def test_and_filter(self):
        query = transform_query(
            connections['default'],
            TransformTestModel.objects.filter(field1="One", field2="Two").all().query
        )
        self.assertEqual(1, len(query.queries))
        self.assertEqual(2, len(query.queries[0]._filters))  # Two child nodes

    @datastore_only
    def test_exclude_filter(self):
        query = transform_query(
            connections['default'],
            TransformTestModel.objects.exclude(field1="One").all().query
        )

        self.assertEqual(query.path, [TransformTestModel._meta.db_table])
        self.assertEqual(2, len(query.queries))  # Three children

    @firestore_only
    def test_exclude_filter_firestore(self):
        query = transform_query(
            connections['default'],
            TransformTestModel.objects.exclude(field1="One").all().query
        )

        self.assertEqual(query.path, [TransformTestModel._meta.db_table])
        self.assertEqual(3, len(query.queries))  # Three children

    def test_ordering(self):
        query = transform_query(
            connections['default'],
            TransformTestModel.objects.filter(field1="One", field2="Two").order_by("field1", "-field2").query
        )

        self.assertEqual(query.path, [TransformTestModel._meta.db_table])
        self.assertEqual(len(query.queries), 1)
        self.assertEqual(2, len(query.queries[0]._filters))
        self.assertEqual(["field1", "-field2"], query.ordering)

    def test_projection(self):
        query = transform_query(
            connections['default'],
            TransformTestModel.objects.only("field1").query
        )

        self.assertItemsEqual(["id", "field1"], query.select)

        query = transform_query(
            connections['default'],
            TransformTestModel.objects.values_list("field1").query
        )

        self.assertEqual(["field1"], query.select)

        query = transform_query(
            connections['default'],
            TransformTestModel.objects.defer("field1", "field4").query
        )

        self.assertItemsEqual(["id", "field2", "field3"], query.select)

    def test_no_results_returns_emptyresultset(self):
        self.assertRaises(
            EmptyResultSet,
            transform_query,
            connections['default'],
            TransformTestModel.objects.none().query
        )

    def test_isnull(self):
        query = transform_query(
            connections['default'],
            TransformTestModel.objects.filter(field3__isnull=True).all()[5:10].query
        )

        self.assertEqual(query.queries[0].get_filter("field3", "="), [None])

    def test_distinct(self):
        query = transform_query(
            connections['default'],
            TransformTestModel.objects.distinct("field2", "field3").query
        )

        self.assertTrue(query.distinct_fields)
        self.assertEqual(query.only_return_fields, ["field2", "field3"])

        query = transform_query(
            connections['default'],
            TransformTestModel.objects.distinct().values("field2", "field3").query
        )

        self.assertTrue(query.distinct_fields)
        self.assertEqual(query.only_return_fields, ["field2", "field3"])

    def test_order_by_pk(self):
        key_property = connections['default'].key_property_name()
        query = transform_query(
            connections['default'],
            TransformTestModel.objects.order_by("pk").query
        )

        self.assertEqual(key_property, query.ordering[0])

        query = transform_query(
            connections['default'],
            TransformTestModel.objects.order_by("-pk").query
        )

        self.assertEqual(f"-{key_property}", query.ordering[0])

    def test_reversed_ordering(self):
        key_property = connections['default'].key_property_name()
        query = transform_query(
            connections['default'],
            TransformTestModel.objects.order_by("pk").reverse().query
        )

        self.assertEqual(f"-{key_property}", query.ordering[0])

    def test_clear_ordering(self):
        query = transform_query(
            connections['default'],
            TransformTestModel.objects.order_by("pk").order_by().query
        )

        self.assertFalse(query.ordering)

    def test_projection_on_textfield_disabled(self):
        query = transform_query(
            connections['default'],
            TransformTestModel.objects.values_list("field4").query
        )

        self.assertFalse(query.only_return_fields)


class QueryNormalizationTests(TestCase):
    """
        The parse_dnf function takes a Django where tree, and converts it
        into a tree of one of the following forms:

        [ (column, operator, value), (column, operator, value) ] <- AND only query
        [ [(column, operator, value)], [(column, operator, value) ]] <- OR query, of multiple ANDs
    """

    def test_and_with_child_or_promoted(self):
        """
            Given the following tree:

                   AND
                  / | ﹨
                 A  B OR
                      / ﹨
                     C   D

             The OR should be promoted, so the resulting tree is

                        OR
                     /     ﹨
                   AND      AND
                  / | ﹨   / | ﹨
                 A  B  C  A  B  D
        """
        from django.db import connection
        query = Query(TestUser, connection)
        query.where = WhereNode('default')
        query.where.children.append(WhereNode('default'))
        query.where.children[-1].column = "A"
        query.where.children[-1].operator = "="
        query.where.children.append(WhereNode('default'))
        query.where.children[-1].column = "B"
        query.where.children[-1].operator = "="
        query.where.children.append(WhereNode('default'))
        query.where.children[-1].connector = "OR"
        query.where.children[-1].children.append(WhereNode('default'))
        query.where.children[-1].children[-1].column = "C"
        query.where.children[-1].children[-1].operator = "="
        query.where.children[-1].children.append(WhereNode('default'))
        query.where.children[-1].children[-1].column = "D"
        query.where.children[-1].children[-1].operator = "="

        query = normalize_query(query)

        self.assertEqual(query.where.connector, "OR")
        self.assertEqual(2, len(query.where.children))
        self.assertFalse(query.where.children[0].is_leaf)
        self.assertFalse(query.where.children[1].is_leaf)
        self.assertEqual(query.where.children[0].connector, "AND")
        self.assertEqual(query.where.children[1].connector, "AND")
        self.assertEqual(3, len(query.where.children[0].children))
        self.assertEqual(3, len(query.where.children[1].children))

    @datastore_only
    def test_and_queries(self):
        qs = TestUser.objects.filter(username="test").all()

        query = transform_query(
            connections['default'],
            qs.query
        )

        self.assertEqual(1, len(query.queries))
        self.assertEqual(1, len(query.queries[0]._filters))
        self.assertEqual(query.queries[0].get_filter("username", "="), ["test"])

        qs = TestUser.objects.filter(username="test", email="test@example.com")

        query = transform_query(
            connections['default'],
            qs.query
        )

        self.assertEqual(1, len(query.queries))
        self.assertEqual(2, len(query.queries[0]._filters))

        self.assertEqual(query.queries[0].get_filter("username", "="), ["test"])
        self.assertEqual(query.queries[0].get_filter("email", "="), ["test@example.com"])

        qs = TestUser.objects.filter(username="test").exclude(email="test@example.com")
        query = transform_query(
            connections['default'],
            qs.query
        )

        if connections['default'].supports_only_null_equality:
            self.assertEqual(3, len(query.queries))
            self.assertEqual(2, len(query.queries[0]._filters))
            self.assertEqual(2, len(query.queries[1]._filters))
            self.assertEqual(2, len(query.queries[2]._filters))
        else:
            self.assertEqual(2, len(query.queries))
            self.assertEqual(2, len(query.queries[0]._filters))
            self.assertEqual(2, len(query.queries[1]._filters))

        self.assertTrue(all([x.has_filter("username", "=") for x in query.queries]))

        gt = [x.has_filter("email", ">") for x in query.queries]
        self.assertTrue(any(gt) and not all(gt))

        lt = [x.has_filter("email", ">") for x in query.queries]
        self.assertTrue(any(lt) and not all(lt))

        instance = Relation(pk=1)
        qs = instance.related_set.filter(headline__startswith='Fir')

        query = transform_query(
            connections['default'],
            qs.query
        )

        self.assertTrue(1, len(query.queries))
        self.assertTrue(2, len(query.queries[0]._filters))
        self.assertEqual(query.queries[0].get_filter("relation_id", "="), [1])
        self.assertEqual(query.queries[0].get_filter("_idx_startswith_headline", "array_contains"), ["Fir"])

    def test_impossible_or_query(self):
        qs = TestUser.objects.filter(
            username="python").filter(
            Q(username__in=["ruby", "jruby"]) | (Q(username="php") & ~Q(username="perl"))
        )

        with self.assertRaises(EmptyResultSet):
            transform_query(
                connections['default'],
                qs.query
            )

    def test_or_queries(self):
        qs = TestUser.objects.filter(
            first_name="python").filter(
            Q(username__in=["ruby", "jruby"]) | (Q(username="php") & ~Q(username="perl"))
        )

        query = transform_query(
            connections['default'],
            qs.query
        )

        key_property = connections['default'].key_property_name()

        # After IN and != explosion, we have...
        # (AND:
        #       (first_name='python',
        #        OR: (username='ruby', username='jruby',
        #             AND: (username='php',
        #                   AND: (username < 'perl', username > 'perl')
        #                  )
        #            )
        #        )
        # )

        # Working backwards,
        # AND: (username < 'perl', username > 'perl') can't be simplified
        #
        # AND: (username='php', AND: (username < 'perl', username > 'perl'))
        # can become
        # (OR: (AND: username = 'php', username < 'perl'), (AND: username='php', username > 'perl'))
        #
        # OR: (username='ruby', username='jruby',(OR: (AND: username = 'php', username < 'perl'),
        # (AND: username='php', username > 'perl')) can't be simplified
        #
        # (AND: (first_name='python', OR: (username='ruby', username='jruby',
        # (OR: (AND: username = 'php', username < 'perl'), (AND: username='php', username > 'perl'))
        # becomes...
        # (OR: (AND: first_name='python', username = 'ruby'), (AND: first_name='python', username='jruby'),
        #      (AND: first_name='python', username='php', username < 'perl')
        #      (AND: first_name='python', username='php', username > 'perl')

        self.assertTrue(4, len(query.queries))

        self.assertTrue(all([x.get_filter("first_name", "=") == ["python"] for x in query.queries]))
        self.assertEqual(len([x for x in query.queries if x.get_filter("username", "=") == ["jruby"]]), 1)
        self.assertEqual(len([x for x in query.queries if x.get_filter("username", "=") == ["ruby"]]), 1)
        self.assertEqual(len([x for x in query.queries if x.get_filter("username", ">") == ["perl"]]), 1)
        self.assertEqual(len([x for x in query.queries if x.get_filter("username", "<") == ["perl"]]), 1)
        self.assertEqual(len([x for x in query.queries if x.get_filter("username", "=") == ["php"]]), 2)

        qs = TestUser.objects.filter(username="test") | TestUser.objects.filter(username="cheese")

        query = transform_query(
            connections['default'],
            qs.query
        )

        self.assertEqual(2, len(query.queries))
        self.assertEqual(1, len([x for x in query.queries if x.get_filter("username", "=") == ["test"]]), 1)
        self.assertEqual(1, len([x for x in query.queries if x.get_filter("username", "=") == ["cheese"]]), 1)

        qs = TestUser.objects.using("default").filter(username__in=set()).values_list('email')

        with self.assertRaises(EmptyResultSet):
            query = transform_query(
                connections['default'],
                qs.query
            )

        qs = TestUser.objects.filter(
            username__startswith='Hello'
        ) | TestUser.objects.filter(username__startswith='Goodbye')

        query = transform_query(
            connections['default'],
            qs.query
        )

        self.assertEqual(2, len(query.queries))

        self.assertEqual(
            1, len(
                [x for x in query.queries if x.get_filter("_idx_startswith_username", "array_contains") == ["Hello"]]
            ), 1
        )

        self.assertEqual(
            1, len(
                [x for x in query.queries if x.get_filter("_idx_startswith_username", "array_contains") == ["Goodbye"]]
            ), 1
        )

        qs = TestUser.objects.filter(pk__in=[1, 2, 3])
        query = transform_query(
            connections['default'],
            qs.query
        )

        self.assertEqual(3, len(query.queries))
        self.assertTrue(query.queries[0].has_filter(key_property, "="))
        self.assertTrue(query.queries[1].has_filter(key_property, "="))
        self.assertTrue(query.queries[2].has_filter(key_property, "="))
        self.assertEqual({
                default_connection.connection.new_key(TestUser._meta.db_table, 1),
                default_connection.connection.new_key(TestUser._meta.db_table, 2),
                default_connection.connection.new_key(TestUser._meta.db_table, 3),
            }, {
                query.queries[0].get_filter(key_property, "=")[0],
                query.queries[1].get_filter(key_property, "=")[0],
                query.queries[2].get_filter(key_property, "=")[0],
            }
        )

        qs = TestUser.objects.filter(pk__in=[1, 2, 3]).filter(username="test")
        query = transform_query(
            connections['default'],
            qs.query
        )

        self.assertEqual(3, len(query.queries))
        self.assertTrue(all([x for x in query.queries if x.has_filter(key_property, "=")]))
        self.assertTrue(all([x for x in query.queries if x.has_filter("test", "=")]))

        self.assertEqual({
                default_connection.connection.new_key(TestUser._meta.db_table, 1),
                default_connection.connection.new_key(TestUser._meta.db_table, 2),
                default_connection.connection.new_key(TestUser._meta.db_table, 3),
            }, {
                query.queries[0].get_filter(key_property, "=")[0],
                query.queries[1].get_filter(key_property, "=")[0],
                query.queries[2].get_filter(key_property, "=")[0],
            }
        )

    def test_removal_of_multiple_pk_equalities(self):
        """ Regression test for #1174/#1175.
            Make sure that we don't get an error when a query has multiple different equality
            filters on the PK.
        """
        query = TransformTestModel.objects.filter(pk=1).filter(pk=2).filter(pk=3)
        try:
            list(query)
        except ValueError:
            raise
            self.fail("ValueError raised when filtering on multiple different PK equalities")


class QueryBuilderTests(TestCase):
    """Test for the internals of the query normalization and transformation process"""

    def test_overlap_is_or(self):
        """Test that an overlap with two values is transformed into an
            OR query with two branches like this

                             OR
           array_contains A     array_contains B
        """
        qs = ListFieldModel.objects.filter(list_field__overlap=["a", "b"])
        root = get_builder(
            connections['default'],
            qs.query
        ).where

        self.assertEqual(2, len(root.children))  # Two leaf nodes
        self.assertTrue(root.children[0].is_leaf)
        self.assertTrue(root.children[1].is_leaf)

        self.assertEqual(root.children[0].operator, "array_contains")
        self.assertEqual(root.children[1].operator, "array_contains")
        self.assertItemsEqual([root.children[0].value, root.children[1].value], ["a", "b"])

    def test_multiple_overlap_single_value_squashed(self):
        """Test that subsequent overlaps of single items are squashed into a single contains_all query"""
        qs = ListFieldModel.objects.filter(
                list_field__overlap=["a"]
            ).filter(
                list_field__overlap=["b"]
            )

        root = get_builder(
            connections['default'],
            qs.query
        ).where

        self.assertEqual(1, len(root.children))
        child = root.children[0]
        self.assertEqual(child.connector, "AND")
        self.assertEqual(1, len(child.children))

        leaf = child.children[0]
        self.assertTrue(leaf.is_leaf)
        self.assertEqual(leaf.column, "list_field")
        self.assertEqual(leaf.operator, "array_contains_all")
        self.assertItemsEqual(leaf.value, ["a", "b"])

    def test_multiple_overlap_multiple_values_not_intersecting(self):
        """Overlap [A, B] AND overlap [C, D] should be first turned into
        OR
            AND array_contains A, array_contains C
            AND array_contains A, array_contains D
            AND array_contains B, array_contains C
            AND array_contains B, array_contains D

        and then squashed into:

        OR
            AND array_contains_all [A, C]
            AND array_contains_all [A, D]
            AND array_contains_all [A, B]
            AND array_contains_all [A, C]
        """
        qs = ListFieldModel.objects.filter(
                list_field__overlap=["a", "b"]
            ).filter(
                list_field__overlap=["c", "d"]
            )

        root = get_builder(
            connections['default'],
            qs.query
        ).where

        self.assertEqual(4, len(root.children))

        for child in root.children:
            self.assertEqual(child.connector, "AND")
            self.assertEqual(1, len(child.children))
            self.assertTrue(child.children[0].is_leaf)
            self.assertEqual(child.children[0].operator, "array_contains_all")

    def test_multiple_overlap_multiple_values_intersecting(self):
        """Overlap [A, B] AND overlap [B, C] should be first turned into
        OR
            AND array_contains A, array_contains B
            AND array_contains A, array_contains C
            AND array_contains B, array_contains B
            AND array_contains B, array_contains C

        then squashed into

        OR
            AND array_contains_all [A, B]
            AND array_contains_all [A, C]
            AND array_contains B
            AND array_contains_all [B, C]


        ASIDE: not yet implemented
          |  Idally, we should also optimize the tree so that it is something like
          |
          |  OR
          |      AND array_contains_all [A, C]
          |      AND array_contains B
          |
          |  because `array_contains_all ["A", "B"] OR array_contains ["B"]"`
          |  is equivalent to `array_contains "B"` (an entity with field B would pass both test,
          |  an entity with field A would pass the first test but not the second, so the first test
          |  is superfluous).
        """
        qs = ListFieldModel.objects.filter(
                list_field__overlap=["a", "b"]
            ).filter(
                list_field__overlap=["b", "c"]
            )

        root = get_builder(
            connections['default'],
            qs.query
        ).where

        self.assertEqual(4, len(root.children))

        for child in root.children:
            self.assertEqual(child.connector, "AND")
            self.assertEqual(1, len(child.children))
            self.assertTrue(child.children[0].is_leaf)
            self.assertTrue(child.children[0].operator in ("array_contains_all", "array_contains"))
            if child.children[0].operator == "array_contains_all":
                self.assertEqual(len(child.children[0].value), 2)
            else:
                self.assertEqual(child.children[0].value, "b")
