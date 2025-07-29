import uuid

from django.db import models, transaction

from . import TestCase


class ExcludedPKModel(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    color = models.CharField(max_length=30)


class UUIDPKModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)


class ExcludingPKTests(TestCase):
    def test_exclude_pks_with_slice(self):
        for i in range(10):
            ExcludedPKModel.objects.create(name=str(i), color=str(i))

        to_exclude = [str(x) for x in list(range(5)) + list(range(15, 20))]

        to_return = ExcludedPKModel.objects.exclude(pk__in=set(to_exclude)).values_list("pk", flat=True)[:2]
        self.assertEqual(2, len(to_return))
        self.assertIsNotNone(to_return[0])

        qs = ExcludedPKModel.objects.filter(pk__in=to_return)

        self.assertEqual(2, len(qs))

    def test_count_on_excluded_pks(self):
        ExcludedPKModel.objects.create(name="Apple", color="Red")
        ExcludedPKModel.objects.create(name="Orange", color="Orange")

        self.assertEqual(
            1, ExcludedPKModel.objects.filter(pk__in=["Apple", "Orange"]).exclude(pk__in=["Apple"]).count()
        )

    def test_count_using_in_filter_with_excluded_pks(self):
        ExcludedPKModel.objects.create(name="Apple", color="Red")
        ExcludedPKModel.objects.create(name="Orange", color="Orange")

        self.assertEqual(
            1, ExcludedPKModel.objects.filter(color__in=["Red", "Orange"]).exclude(pk__in=["Apple"]).count()
        )

    def test_count_using_eq_filter_with_excluded_pk(self):
        ExcludedPKModel.objects.create(name="Apple", color="Red")
        ExcludedPKModel.objects.create(name="Orange", color="Orange")

        self.assertEqual(
            0, ExcludedPKModel.objects.filter(color="Red").exclude(pk="Apple").count()
        )
        self.assertEqual(
            1, ExcludedPKModel.objects.filter(color="Red").exclude(pk="Orange").count()
        )

    def test_exclude_pks_with_filter(self):
        ExcludedPKModel.objects.create(name="Apple", color="Red")
        ExcludedPKModel.objects.create(name="Orange", color="Orange")

        self.assertEqual(
            ['Orange'],
            [e.pk for e in ExcludedPKModel.objects.filter(
                color__in=["Red", "Orange"]
            ).exclude(pk__in=["Apple"])]
        )

    def test_exclude_by_pk_inside_transaction(self):
        ExcludedPKModel.objects.create(name="Apple", color="Red")
        uuid1 = UUIDPKModel.objects.create()

        with transaction.atomic():
            obj = ExcludedPKModel.objects.get(pk="Apple")
            self.assertEqual(ExcludedPKModel.objects.exclude(pk=obj.pk).count(), 0)
            self.assertEqual(len(ExcludedPKModel.objects.exclude(pk=obj.pk)), 0)

            uuid1 = UUIDPKModel.objects.get(pk=uuid1.pk)
            self.assertEqual(UUIDPKModel.objects.exclude(pk=uuid1.pk).count(), 0)
            self.assertEqual(len(UUIDPKModel.objects.exclude(pk=uuid1.pk)), 0)

    def test_filter_gt_or_lt_by_pk(self):
        objs = {}
        for name in ["a", "b", "c", "d", "e"]:
            obj = ExcludedPKModel.objects.create(name=name, color="Cobalt sky")
            objs[name] = obj

        qs = ExcludedPKModel.objects.filter(pk__gt="a", pk__lt="e")
        expected = [objs["b"], objs["c"], objs["d"]]
        self.assertEqual(list(qs), expected)

        # Try with the ordering being explicit
        qs = qs.order_by("pk")
        self.assertEqual(list(qs), expected)

        # Try with an offset
        qs = qs.all()[2:]
