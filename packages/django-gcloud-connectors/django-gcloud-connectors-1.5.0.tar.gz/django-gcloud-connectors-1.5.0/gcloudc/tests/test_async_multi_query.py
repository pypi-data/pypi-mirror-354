import sleuth
from django.db import NotSupportedError
from django.db import models
from django.db.models import Q
from django.test import override_settings
from django.core.paginator import Paginator

from . import TestCase, firestore_only, datastore_only
from .models import (
    MultiQueryModel,
    NullableFieldModel,
)


class PageModel(models.Model):
    page = models.PositiveIntegerField()


class AsyncMultiQueryTest(TestCase):
    """
        Specific tests for multiquery
    """

    @datastore_only
    def test_paginated_query(self):
        pages = [x for x in range(10)]
        for i in pages:
            for _ in range(10):
                PageModel.objects.create(page=i)

        qs = PageModel.objects.filter(page__in=pages).order_by("page")
        paginator = Paginator(qs, 10)

        for page in pages:
            i = 0

            with sleuth.watch("gcloudc.db.backends.datastore.base.Query.fetch") as fetch:  # noqa
                for object in paginator.page(page + 1):
                    self.assertEqual(object.page, page)
                    i += 1

            self.assertEqual(i, 10)

            # There should be 10 calls (one per "Page") with the correct offset and limit
            self.assertEqual(len([
                x for x in fetch.calls
                if x.kwargs['offset'] == 0 and x.kwargs['limit'] == (page * 10) + 10
            ]), 10)

    def test_hundred_or(self):
        for i in range(100):
            MultiQueryModel.objects.create(field1=i)

        self.assertEqual(len(MultiQueryModel.objects.filter(field1__in=list(range(100)))), 100)

        self.assertEqual(MultiQueryModel.objects.filter(field1__in=list(range(100))).count(), 100)

        qs = MultiQueryModel.objects.filter(field1__in=list(range(100))).values_list("field1", flat=True)

        self.assertItemsEqual(
            qs,
            list(range(100)),
        )

        self.assertItemsEqual(
            MultiQueryModel.objects.filter(field1__in=list(range(100)))
            .order_by("-field1")
            .values_list("field1", flat=True),
            list(range(100))[::-1],
        )

    @override_settings(DJANGAE_MAX_QUERY_BRANCHES=10)
    def test_max_limit_enforced(self):
        for i in range(11):
            MultiQueryModel.objects.create(field1=i)

        self.assertRaises(NotSupportedError, list, MultiQueryModel.objects.filter(field1__in=list(range(11))))

    def test_pk_in_with_slicing(self):
        i1 = MultiQueryModel.objects.create()

        self.assertFalse(MultiQueryModel.objects.filter(pk__in=[i1.pk])[9999:])

        self.assertFalse(MultiQueryModel.objects.filter(pk__in=[i1.pk])[9999:10000])

    @datastore_only
    def test_limit_correctly_applied_per_branch_ds(self):
        MultiQueryModel.objects.create(field2="test")
        MultiQueryModel.objects.create(field2="test2")

        with sleuth.watch("google.cloud.datastore.query.Query.fetch") as run_calls:

            list(MultiQueryModel.objects.filter(field2__in=["test", "test2"])[:1])

            self.assertEqual(1, run_calls.calls[0].kwargs["limit"])
            self.assertEqual(1, run_calls.calls[1].kwargs["limit"])

        with sleuth.watch("google.cloud.datastore.query.Query.fetch") as run_calls:

            list(MultiQueryModel.objects.filter(field2__in=["test", "test2"])[1:2])

            self.assertEqual(0, run_calls.calls[0].kwargs["offset"])
            self.assertEqual(0, run_calls.calls[1].kwargs["offset"])
            self.assertEqual(2, run_calls.calls[0].kwargs["limit"])
            self.assertEqual(2, run_calls.calls[1].kwargs["limit"])

    @firestore_only
    def test_limit_correctly_applied_per_branch_fs(self):
        MultiQueryModel.objects.create(field2="test")
        MultiQueryModel.objects.create(field2="test2")

        with sleuth.watch("google.cloud.firestore_v1.query.Query.limit") as run_calls:

            list(MultiQueryModel.objects.filter(field2__in=["test", "test2"])[:1])

            self.assertEqual(1, run_calls.calls[0].args[1])
            self.assertEqual(1, run_calls.calls[1].args[1])

        with sleuth.watch("google.cloud.firestore_v1.query.Query.limit") as run_calls:

            list(MultiQueryModel.objects.filter(field2__in=["test", "test2"])[1:2])

            self.assertEqual(2, run_calls.calls[0].args[1])
            self.assertEqual(2, run_calls.calls[1].args[1])

    def test_ordered_by_nullable_field(self):
        NullableFieldModel.objects.create(pk=1)
        NullableFieldModel.objects.create(pk=5, nullable=2)

        results = NullableFieldModel.objects.filter(
            Q(nullable=1) | Q(nullable=2) | Q(nullable__isnull=True)
        ).order_by("nullable").values_list("pk", flat=True)

        self.assertCountEqual(results, [1, 5])

    @firestore_only
    def test_correct_number_of_queries(self):
        ids = [str(x) for x in range(50)]

        qs = MultiQueryModel.objects.filter(field2__in=ids).filter(field2__in=ids)

        with sleuth.watch("gcloudc.db.backends.firestore.base.Query.fetch") as fetch_calls:
            list(qs)
            self.assertEqual(fetch_calls.call_count, 50)
