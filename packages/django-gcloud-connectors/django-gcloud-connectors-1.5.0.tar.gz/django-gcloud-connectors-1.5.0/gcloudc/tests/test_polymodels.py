from django.db import models, IntegrityError
from . import TestCase
import os


class PolyModelBase(models.Model):
    x = models.PositiveIntegerField()

    class Meta:
        app_label = "gcloudc"


class PolyModelLeaf(PolyModelBase):
    y = models.PositiveIntegerField()

    class Meta:
        app_label = "gcloudc"


class PolymodelTests(TestCase):
    databases = {"default"}
    fixtures = [os.path.join(os.path.dirname(__file__), "data", "polymodel.default.json")]

    def test_subclass_creation(self):
        self.assertRaises(IntegrityError, PolyModelLeaf.objects.create, y=1)

        instance = PolyModelLeaf.objects.create(x=1, y=1)
        self.assertTrue(instance)
