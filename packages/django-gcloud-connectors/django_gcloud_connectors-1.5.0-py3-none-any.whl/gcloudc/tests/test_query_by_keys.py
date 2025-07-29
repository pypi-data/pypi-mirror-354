import google

from gcloudc.db.backends.common.base.entity import Entity

from . import TestCase, firestore_only
from .models import NullableFieldModel, StringPkModel, TestUser, TestFruit
from django.db import connection as default_connection


class QueryByKeysTest(TestCase):
    """
        Tests for the Get optimisation when keys are
        included in all branches of a query.
    """

    databases = "__all__"

    def test_missing_results_are_skipped(self):
        NullableFieldModel.objects.create(pk=1)
        NullableFieldModel.objects.create(pk=5)

        results = NullableFieldModel.objects.filter(
            pk__in=[1, 2, 3, 4, 5]
        ).order_by("nullable").values_list("pk", flat=True)

        self.assertCountEqual(results, [1, 5])

    def test_none_namespace(self):
        NullableFieldModel.objects.using("nonamespace").create(pk=1)
        NullableFieldModel.objects.using("nonamespace").create(pk=5)

        results = NullableFieldModel.objects.using(
            "nonamespace").filter(
                pk__in=[1, 2, 3, 4, 5]
        ).order_by("nullable").values_list("pk", flat=True)

        self.assertCountEqual(results, [1, 5])

    def test_large_number_of_keys(self):
        keys = []

        for i in range(1001):
            keys.append(NullableFieldModel.objects.create(pk=i + 1).pk)

        try:
            results = list(NullableFieldModel.objects.filter(pk__in=keys))
        except google.api_core.exceptions.InvalidArgument:
            self.fail("Didn't correctly deal with a large number of keys")

        self.assertEqual(len(results), 1001)
        self.assertCountEqual([x.pk for x in results], keys)

    def test_pk_in(self):
        for i in range(3):
            NullableFieldModel.objects.create(pk=i + 1)
            StringPkModel.objects.create(pk=str(i + 1))

        qs = NullableFieldModel.objects.filter(pk__in=[1, 3])
        self.assertEqual(qs.count(), 2)

        qs = StringPkModel.objects.filter(pk__in=["1", "3"])
        self.assertEqual(qs.count(), 2)

    def test_pk_in_with_ordering(self):
        """ Testing filtering on pk__in with ordering by a different field. """
        int_pk_objs = []
        string_pk_objs = []
        for i in range(3):
            int_pk_objs.append(NullableFieldModel.objects.create(pk=i + 1, nullable=3 - i))
            string_pk_objs.append(StringPkModel.objects.create(pk=str(i + 1), other=f"{3 - i}"))

        qs = NullableFieldModel.objects.filter(pk__in=[1, 3]).order_by("nullable")
        self.assertEqual(list(qs), [int_pk_objs[2], int_pk_objs[0]])

        qs = StringPkModel.objects.filter(pk__in=["1", "3"]).order_by("other")
        self.assertEqual(list(qs), [string_pk_objs[2], string_pk_objs[0]])

    def test_multiple_pk_filters(self):
        for i in range(10):
            NullableFieldModel.objects.create(pk=i + 1)

        qs = NullableFieldModel.objects.all()
        self.assertEqual(qs.count(), 10)

        qs = qs.filter(pk__lt=10)
        self.assertEqual(qs.count(), 9)

        qs = qs.filter(pk__gte=2)
        self.assertEqual(qs.count(), 8)

        qs = qs.filter(pk__gte=3)
        self.assertEqual(qs.count(), 7)

        qs = qs.filter(pk__in=["4", "6"])
        self.assertEqual(qs.count(), 2)

    def test_multiple_str_pk_filters(self):
        for i in range(9):
            StringPkModel.objects.create(pk=str(i + 1))

        qs = StringPkModel.objects.all()
        self.assertEqual(qs.count(), 9)

        qs = qs.filter(pk__lt=str(9))
        self.assertEqual(qs.count(), 8)

        qs = qs.filter(pk__gte=str(2))
        self.assertEqual(qs.count(), 7)

        qs = qs.filter(pk__gte=str(3))
        self.assertEqual(qs.count(), 6)

        qs = qs.filter(pk__in=["4", "6"])
        self.assertEqual(qs.count(), 2)

    def test_update(self):
        """
            This tests that we can run an update which results in a QueryByKeys
            where the query is filtered by another field
        """

        ent = TestUser.objects.create(
            username="cheese", first_name="cheese", second_name="sandwich"
        )

        affected = TestUser.objects.filter(pk=ent.pk, username="cheese").update(username="ham")

        self.assertEqual(affected, 1)
        ent.refresh_from_db()

        self.assertEqual(ent.username, "ham")

    @firestore_only
    def test_update_with_missing_field(self):
        """
            This tests that we can run an update which results in a QueryByKeys
            where the query is filtered by another field, but the other field is missing
            on the specified entity! This caused an exception at one point.
        """
        connection = default_connection.connection
        default_connection.ensure_connection()
        entity = Entity(
            default_connection.connection.new_key(TestUser._meta.db_table, 1),
            properties={"first_name": "cheese", "second_name": "sandwich"},
        )

        connection.put(entity)

        affected = TestUser.objects.filter(pk=1, username="cheese").update(username="ham")

        self.assertEqual(affected, 0)

    def test_filter_by_key_with_ordering(self):
        """ Test that filtering by PK while also having an ordering on another field.
            The ordering may be superfluous, but it is sometimes applied when the model has a
            default ordering.
        """
        string_pk_objs = []
        int_pk_objs = []
        for i in range(2):
            string_pk_objs.append(StringPkModel.objects.create(pk=str(i + 1)))
            int_pk_objs.append(NullableFieldModel.objects.create(pk=i + 1))

        qs1 = StringPkModel.objects.filter(pk="1").order_by("other")
        qs2 = NullableFieldModel.objects.filter(pk=1).order_by("nullable")
        self.assertEqual(list(qs1), string_pk_objs[:1])
        self.assertEqual(list(qs2), int_pk_objs[:1])

        qs1 = StringPkModel.objects.filter(pk="1").order_by("other").values_list("pk", flat=True)
        qs2 = NullableFieldModel.objects.filter(pk=1).order_by("nullable").values_list("pk", flat=True)
        self.assertEqual(list(qs1), ["1"])
        self.assertEqual(list(qs2), [1])

        self.assertEqual(StringPkModel.objects.filter(pk="1").order_by("other").delete()[0], 1)
        self.assertEqual(NullableFieldModel.objects.filter(pk=1).order_by("nullable").delete()[0], 1)

    def test_additional_filters(self):
        """ Any filters applied in addition to the PK should also be respected. """
        TestFruit.objects.create(name="orange", color="orange")
        TestFruit.objects.create(name="raspberry", color="red")
        self.assertEqual(TestFruit.objects.filter(name="orange", color="orange").count(), 1)
        self.assertEqual(TestFruit.objects.filter(name="orange", color="red").count(), 0)
