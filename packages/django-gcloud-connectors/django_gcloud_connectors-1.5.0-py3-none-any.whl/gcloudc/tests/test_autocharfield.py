from django.db.models import Model
from gcloudc.tests import TestCase, firestore_only
from gcloudc.db.models.fields.firestore import AutoCharField


class AutoCharFieldModel(Model):
    id = AutoCharField(primary_key=True)

    class Meta:
        app_label = "gcloudc"


class AutoCharFieldTests(TestCase):

    @firestore_only
    def test_id_generated(self):
        instance = AutoCharFieldModel.objects.create()
        self.assertTrue(instance.pk)
        self.assertTrue(isinstance(instance.pk, str))
        self.assertEqual(len(instance.pk), 20)
