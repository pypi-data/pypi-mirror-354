# Standard library
import uuid

# Third party
from django.db import models

# gcloudc
from . import TestCase


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)


class PointsAtUUIDModel(models.Model):
    uuid = models.ForeignKey(UUIDModel, on_delete=models.DO_NOTHING)


class SubqueriesTestCase(TestCase):
    """ Tests for cases where we handle one queryset being filtered by another.
        We can't support this in the way that SQL does, but in some cases we can evaluate the first
        queryset automatically in order to filter the second.
    """

    def test_sub_query_with_values_list(self):
        uuid1 = UUIDModel.objects.create()
        points_at_1 = PointsAtUUIDModel.objects.create(uuid=uuid1)
        queryset = PointsAtUUIDModel.objects.filter(
            uuid_id__in=UUIDModel.objects.values_list("id", flat=True)
        )
        self.assertEqual(list(queryset), [points_at_1])
