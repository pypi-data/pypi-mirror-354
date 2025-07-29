import secrets

# Third Party
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db import IntegrityError
from google.cloud import firestore

# Gcloudc
from gcloudc.db.models.fields.firestore import (
    AutoCharField,
    MapField,
)
from gcloudc.tests import (
    TestCase,
    firestore_only,
)


class ValidationModel(models.Model):
    name = models.CharField(max_length=32, db_column="db_name")
    age = models.IntegerField()

    class Meta:
        abstract = True


class ValidationModel2(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        abstract = True


class ValidationModel1(models.Model):
    nested = MapField(model=ValidationModel2, null=True, blank=True)
    nested_other = MapField(model=ValidationModel2, null=True, blank=True)

    class Meta:
        abstract = True


class MapFieldModel(models.Model):
    id = AutoCharField(primary_key=True)
    map_field = MapField(null=True, blank=True)
    validated_map_field = MapField(model=ValidationModel)

    class Meta:
        app_label = "gcloudc"


class NestedMapFieldModel(models.Model):
    id = AutoCharField(primary_key=True)
    map_field = MapField(model=ValidationModel1, null=True, blank=True)

    class Meta:
        app_label = "gcloudc"


class MapFieldTests(TestCase):

    @firestore_only
    def test_save_and_query(self):
        instance = MapFieldModel.objects.create(
            map_field={
                "value0": "Test value",
                "value1": 100,
            },
            validated_map_field={
                "name": "Luke",
                "age": 22
            }
        )

        self.assertEqual(instance.map_field, {"value0": "Test value", "value1": 100})

        self.assertTrue(MapFieldModel.objects.filter(map_field__value0="Test value").exists())
        self.assertFalse(MapFieldModel.objects.filter(map_field__value0="Cheese").exists())

        self.assertTrue(MapFieldModel.objects.filter(validated_map_field__age=22).exists())

    @firestore_only
    def test_validation(self):
        instance = MapFieldModel(
            validated_map_field={
                "name": False,
                "age": "bananas"
            }
        )

        self.assertRaises(ValidationError, instance.clean_fields)
        self.assertRaises(IntegrityError, instance.save)

        values = {
            "name": "Luke",
            "age": 22
        }

        instance.validated_map_field = values.copy()

        try:
            instance.clean_fields()
            instance.save()
        except (IntegrityError):
            self.fail("Failed validation")

        instance.refresh_from_db()
        self.assertEqual(instance.map_field, None)
        self.assertEqual(instance.validated_map_field, values)

    @firestore_only
    def test_fields_outside_model_raises_validation_error(self):
        values = {
            "name": False,
            "age": 22,
            "notinmodel": "something not in model",
        }
        instance = MapFieldModel(
            validated_map_field=values
        )

        self.assertRaises(ValidationError, instance.clean_fields)
        self.assertRaises(IntegrityError, instance.save)

    @firestore_only
    def test_validation_nested_model_field_missing(self):
        values = {
            "nested": {
                "randomfield": "my name",
            }
        }
        instance = NestedMapFieldModel(
            map_field=values
        )
        self.assertRaises(ValidationError, instance.clean_fields)
        self.assertRaises(IntegrityError, instance.save)

    @firestore_only
    def test_validation_nested_model_valid(self):
        values = {
            "nested": {
                "name": "my name",
            }
        }
        instance = NestedMapFieldModel(
            map_field=values
        )
        instance.clean_fields()
        instance.save()
        self.assertEqual(instance.map_field, values)

    @firestore_only
    def test_validation_nested_model_extra_field(self):
        values = {
            "nested": {
                "name": "my name",
                "surname": "my surname",
            }
        }
        instance = NestedMapFieldModel(
            map_field=values
        )
        self.assertRaises(ValidationError, instance.clean_fields)
        self.assertRaises(IntegrityError, instance.save)

    @firestore_only
    def test_dict_or_none(self):
        instance0 = MapFieldModel(map_field="Test")
        self.assertRaises(IntegrityError, instance0.save)

        instance1 = MapFieldModel.objects.create(validated_map_field=dict())
        instance1.refresh_from_db()
        self.assertIsNone(instance1.map_field)

    @firestore_only
    def test_db_column_parameter(self):
        gclient = firestore.Client(
            project=settings.DATABASES["default"]["PROJECT"],
        )
        map_collection = gclient.collection(MapFieldModel._meta.db_table)
        map_collection.add({
            'validated_map_field': {
                'db_name': 'Luke',
                'age': 22
            },
            'map_field': None
        }, str(secrets.randbits(53)))
        instance1 = MapFieldModel.objects.first()
        self.assertEqual(instance1.validated_map_field.get('name'), 'Luke')

    @firestore_only
    def test_blank_is_saved(self):
        instance = NestedMapFieldModel.objects.create()
        self.assertIsNone(instance.map_field)
        instance = NestedMapFieldModel()
        try:
            instance.clean_fields()
            instance.save()
        except (IntegrityError):
            self.fail("Failed validation")
