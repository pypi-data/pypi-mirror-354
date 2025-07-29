import datetime
import pickle
import sleuth
import django
from django import forms
from django.core.exceptions import ValidationError
from django.db import (
    DatabaseError,
    connection,
    models,
)
from django.test import override_settings

from gcloudc.db.backends.common.base.entity import Entity

from gcloudc.db.models.fields.boolean import TrueOrNoneField
from gcloudc.db.models.fields.charfields import (
    CharField,
    CharOrNoneField,
)
from gcloudc.db.models.fields.computed import (
    ComputedBooleanField,
    ComputedCharField,
    ComputedIntegerField,
    ComputedPositiveIntegerField,
    ComputedTextField,
)
from gcloudc.db.models.fields.iterable import (
    ListField,
    SetField,
)
from gcloudc.db.models.fields.json import JSONField
from gcloudc.db.models.fields.related import (
    GenericRelationField,
    RelatedListField,
    RelatedSetField,
)

from . import TestCase, firestore_only, datastore_only
from .models import (
    BasicTestModel,
    BinaryFieldModel,
    EmptyIndexesModel,
    IndexAllFieldsModel,
    IndexPrimaryKeyModel,
    IndexSelectedFieldsModel,
    ISOther,
    ISStringReferenceModel,
    ModelWithCharField,
    NonIndexedModel,
    NullableFieldModel,
    PFAuthor,
    PFAwards,
    PFPost,
)


class BasicTest(TestCase):
    def test_basic_connector_usage(self):
        # Create
        instance = BasicTestModel.objects.create(field1="Hello World!", field2=1998)

        # Count
        self.assertEqual(1, BasicTestModel.objects.count())

        # Get
        self.assertEqual(instance, BasicTestModel.objects.get())

        # Update
        instance.field1 = "Hello Mars!"
        instance.save()

        # Query
        instance2 = BasicTestModel.objects.filter(field1="Hello Mars!")[0]

        self.assertEqual(instance, instance2)
        self.assertEqual(instance.field1, instance2.field1)

        # Query by PK
        instance2 = BasicTestModel.objects.filter(pk=instance.pk)[0]

        self.assertEqual(instance, instance2)
        self.assertEqual(instance.field1, instance2.field1)

        # Non-existent PK
        instance3 = BasicTestModel.objects.filter(pk=999).first()
        self.assertIsNone(instance3)

        # Unique field
        instance2 = BasicTestModel.objects.filter(field2=1998)[0]

        self.assertEqual(instance, instance2)
        self.assertEqual(instance.field1, instance2.field1)


class CharFieldModelTests(TestCase):
    def test_char_field_with_max_length_set(self):
        test_bytestrings = [(u"01234567891", 11), (u"ążźsęćńół", 17)]

        for test_text, byte_len in test_bytestrings:
            test_instance = ModelWithCharField(char_field_with_max=test_text)
            self.assertRaisesMessage(
                ValidationError,
                "Ensure this value has at most 10 bytes (it has %d)." % byte_len,
                test_instance.full_clean,
            )

    def test_char_field_with_not_max_length_set(self):
        longest_valid_value = u"0123456789" * 150
        too_long_value = longest_valid_value + u"more"

        test_instance = ModelWithCharField(char_field_without_max=longest_valid_value)
        test_instance.full_clean()  # max not reached so it's all good

        test_instance.char_field_without_max = too_long_value
        self.assertRaisesMessage(
            ValidationError, u"Ensure this value has at most 1500 bytes (it has 1504).", test_instance.full_clean
        )

    def test_additional_validators_work(self):
        test_instance = ModelWithCharField(char_field_as_email="bananas")
        self.assertRaisesMessage(ValidationError, "failed", test_instance.full_clean)

    def test_too_long_max_value_set(self):
        try:

            class TestModel(models.Model):
                test_char_field = CharField(max_length=1501)

        except AssertionError as e:
            self.assertEqual(str(e), "CharFields max_length must not be greater than 1500 bytes.")


class ModelWithCharOrNoneField(models.Model):
    char_or_none_field = CharOrNoneField(max_length=100)


class CharOrNoneFieldTests(TestCase):
    def test_char_or_none_field(self):
        # Ensure that empty strings are coerced to None on save
        obj = ModelWithCharOrNoneField.objects.create(char_or_none_field="")
        obj.refresh_from_db()
        self.assertIsNone(obj.char_or_none_field)


class StringReferenceRelatedSetFieldModelTests(TestCase):
    def test_can_update_related_field_from_form(self):
        related = ISOther.objects.create()
        thing = ISStringReferenceModel.objects.create(related_things={related})
        before_set = thing.related_things
        thing.related_list.field.save_form_data(thing, set())
        thing.save()
        self.assertNotEqual(before_set.all(), thing.related_things.all())

    def test_saving_forms(self):
        class TestForm(forms.ModelForm):
            class Meta:
                model = ISStringReferenceModel
                fields = ("related_things",)

        related = ISOther.objects.create()
        post_data = {"related_things": [str(related.pk)]}

        form = TestForm(post_data)
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertEqual({related.pk}, instance.related_things_ids)


class RelatedFieldPrefetchTests(TestCase):
    def test_prefetch_related(self):
        award = PFAwards.objects.create(name="award")
        author = PFAuthor.objects.create(awards={award})
        PFPost.objects.create(authors={author})

        posts = list(PFPost.objects.all().prefetch_related("authors__awards"))

        with self.assertNumQueries(0):
            list(posts[0].authors.all()[0].awards.all())


class PickleTests(TestCase):
    def test_all_fields_are_pickleable(self):
        """ In order to work with Djangae's migrations, all fields must be pickeable. """
        fields = [
            CharField(),
            CharOrNoneField(),
            ComputedBooleanField("method_name"),
            ComputedCharField("method_name"),
            ComputedIntegerField("method_name"),
            ComputedPositiveIntegerField("method_name"),
            ComputedTextField("method_name"),
            GenericRelationField(),
            JSONField(default=list),
            ListField(CharField(), default=["badger"]),
            SetField(CharField(), default=set(["badger"])),
        ]

        fields.extend(
            [RelatedListField(ModelWithCharField), RelatedSetField(ModelWithCharField)]
        )

        for field in fields:
            try:
                pickle.dumps(field)
            except (pickle.PicklingError, TypeError) as e:
                self.fail("Could not pickle %r: %s" % (field, e))


class BinaryFieldModelTests(TestCase):
    binary_value = b"\xff"

    def test_insert(self):

        obj = BinaryFieldModel.objects.create(binary=self.binary_value)
        obj.save()

        readout = BinaryFieldModel.objects.get(pk=obj.pk)

        assert readout.binary == self.binary_value

    def test_none(self):

        obj = BinaryFieldModel.objects.create()
        obj.save()

        readout = BinaryFieldModel.objects.get(pk=obj.pk)

        assert readout.binary is None

    def test_update(self):

        obj = BinaryFieldModel.objects.create()
        obj.save()

        toupdate = BinaryFieldModel.objects.get(pk=obj.pk)
        toupdate.binary = self.binary_value
        toupdate.save()

        readout = BinaryFieldModel.objects.get(pk=obj.pk)

        assert readout.binary == self.binary_value


class CharFieldModel(models.Model):
    char_field = models.CharField(max_length=500)


class CharFieldModelTest(TestCase):
    def test_query(self):
        instance = CharFieldModel(char_field="foo")
        instance.save()

        readout = CharFieldModel.objects.get(char_field="foo")
        self.assertEqual(readout, instance)

    def test_query_unicode(self):
        name = u"Jacqu\xe9s"

        instance = CharFieldModel(char_field=name)
        instance.save()

        readout = CharFieldModel.objects.get(char_field=name)
        self.assertEqual(readout, instance)

    @override_settings(DEBUG=True)
    def test_query_unicode_debug(self):
        """ Test that unicode query can be performed in DEBUG mode,
            which will use CursorDebugWrapper and call last_executed_query.
        """
        name = u"Jacqu\xe9s"

        instance = CharFieldModel(char_field=name)
        instance.save()

        readout = CharFieldModel.objects.get(char_field=name)
        self.assertEqual(readout, instance)


class DecimalFieldModel(models.Model):
    decimal_field = models.DecimalField(decimal_places=4, max_digits=7)


class DecimalFieldModelTest(TestCase):
    def test_query(self):
        instance = DecimalFieldModel(decimal_field=3.14)
        instance.save()

        query = DecimalFieldModel.objects.filter(decimal_field=3.14)

        readout = query.get()
        self.assertEqual(readout, instance)

        self.assertEqual(query.count(), 1)


class DurationFieldModelWithDefault(models.Model):
    duration = models.DurationField(default=datetime.timedelta(1, 0))


class DurationFieldModelTests(TestCase):
    def test_creates_with_default(self):
        instance = DurationFieldModelWithDefault()

        self.assertEqual(instance.duration, datetime.timedelta(1, 0))

        instance.save()

        readout = DurationFieldModelWithDefault.objects.get(pk=instance.pk)
        self.assertEqual(readout.duration, datetime.timedelta(1, 0))

    def test_none_saves_as_default(self):
        instance = DurationFieldModelWithDefault()
        # this could happen if we were reading an existing instance out of the database that didn't have this field
        instance.duration = None
        instance.save()

        readout = DurationFieldModelWithDefault.objects.get(pk=instance.pk)
        self.assertEqual(readout.duration, datetime.timedelta(1, 0))


class ModelWithNonNullableFieldAndDefaultValue(models.Model):
    some_field = models.IntegerField(null=False, default=1086)


class NonIndexedModelFieldsTests(TestCase):

    @datastore_only
    def test_long_textfield(self):
        """
        Assert long text fields are implicitly excluded from the datastore index.

        This is datastore_only because Firestore indexes all fields.

        There are "single-field index exemptions" but it's not clear how to use those.
        Possible FIXME?
        """
        long_text = "A" * 1501
        instance = NonIndexedModel()
        instance.content = long_text
        instance.save()

        # grab the entity from the datastore directly
        key = connection.connection.new_key(instance._meta.db_table, instance.pk, namespace=connection.namespace)
        entity = connection.connection.get(key)
        self.assertIn('content', entity._properties_to_exclude_from_index)

    @datastore_only
    def test_big_binaryfield(self):
        """
        Assert binary fields are implicitly excluded from the datastore index.
        """
        long_binary = ("A" * 1501).encode('utf-8')
        instance = NonIndexedModel()
        instance.binary = long_binary
        instance.save()

        # grab the entity from the datastore directly
        client = connection.connection._client
        key = client.key(instance._meta.db_table, instance.pk, namespace=connection.namespace)
        entity = client.get(key)

        self.assertIn('binary', entity.exclude_from_indexes)

    @firestore_only
    def test_it_warns_it_is_not_supported_on_firestore(self):
        """
        Assert that we raise a warning when trying to exclude fields from the index
        in firestore.
        """
        with sleuth.watch("gcloudc.db.backends.firestore.base.logger.warn") as mock_warn:
            instance = NonIndexedModel()
            instance.save()
            self.assertTrue(mock_warn.called)
            self.assertIn("Firestore doesn't support excluding fields from indexing", mock_warn.calls[0].args[0])


class IndexFieldsModelTests(TestCase):
    """
    Tests to assert behaviour when configuring database indexes.
    """

    @datastore_only
    def test_index_selected_fields(self):
        instance = IndexSelectedFieldsModel()
        instance.save()

        # grab the entity from the datastore directly
        client = connection.connection._client
        key = client.key(instance._meta.db_table, instance.pk, namespace=connection.namespace)
        entity = client.get(key)

        self.assertNotIn('field1', entity.exclude_from_indexes)
        self.assertIn('field2', entity.exclude_from_indexes)
        # `field3` is a text field and so should not be indexed
        self.assertIn('field3', entity.exclude_from_indexes)

    @datastore_only
    def test_index_all_fields_including_text_or_binary_field(self):
        instance = IndexAllFieldsModel()
        instance.save()

        # grab the entity from the datastore directly
        client = connection.connection._client
        key = client.key(instance._meta.db_table, instance.pk, namespace=connection.namespace)
        entity = client.get(key)

        self.assertNotIn('field1', entity.exclude_from_indexes)
        self.assertNotIn('field2', entity.exclude_from_indexes)
        # Even though we selected `field3` and `field4` to be indexed in
        # the meta, the fields should not be indexed as they are text & binary fields
        self.assertIn('field3', entity.exclude_from_indexes)
        self.assertIn('field4', entity.exclude_from_indexes)

    @datastore_only
    def test_primary_key_field_not_indexed(self):
        instance = IndexPrimaryKeyModel(field1="foo")
        instance.save()

        # grab the entity from the datastore directly
        client = connection.connection._client
        key = client.key(instance._meta.db_table, instance.pk, namespace=connection.namespace)
        entity = client.get(key)

        # Even though we only selected `field2` to be indexed in
        # the meta, `field1` should still be indexed as it is a primary key
        self.assertNotIn('field1', entity.exclude_from_indexes)
        self.assertNotIn('field2', entity.exclude_from_indexes)

    @datastore_only
    def test_all_fields_indexed_by_default_if_no_indexes_in_meta(self):
        instance = BasicTestModel(field1="foo", field2=1)
        instance.save()

        # grab the entity from the datastore directly
        client = connection.connection._client
        key = client.key(instance._meta.db_table, instance.pk, namespace=connection.namespace)
        entity = client.get(key)

        self.assertNotIn('field1', entity.exclude_from_indexes)
        self.assertNotIn('field2', entity.exclude_from_indexes)

    @datastore_only
    def test_single_property_query(self):
        IndexSelectedFieldsModel.objects.create(field1=1, field2="foo")
        # where `field1` is indexed
        self.assertTrue(IndexSelectedFieldsModel.objects.filter(field1=1).exists())

        # where `field2` is not indexed and so should raise an exception
        self.assertRaises(DatabaseError, list, IndexSelectedFieldsModel.objects.filter(field2="foo"))

    @datastore_only
    def test_composite_index_query(self):
        IndexAllFieldsModel.objects.create(field1=1, field2="foo")
        # where `field1` and `field2` are indexed
        self.assertTrue(IndexAllFieldsModel.objects.filter(field1=1, field2="foo").exists())

        IndexSelectedFieldsModel.objects.create(field1=1, field2="foo")
        # where `field2` is not indexed and so should raise an exception
        # as a property cannot be excluded from composite indexes
        self.assertRaises(DatabaseError, list, IndexSelectedFieldsModel.objects.filter(field1=1, field2="foo"))

    @datastore_only
    def test_projection_query(self):
        IndexSelectedFieldsModel.objects.create(
            field1=1, field2="foo", field3="hello world"
        )
        # where `field1` is indexed
        self.assertEqual(
            IndexSelectedFieldsModel.objects.values_list("field1", flat=True)[0], 1
        )
        # where `field2` is not indexed and so should raise an exception
        self.assertRaises(
            DatabaseError,
            list,
            IndexSelectedFieldsModel.objects.values_list("field1", "field2"),
        )

    @datastore_only
    @override_settings(GCLOUDC_EXCLUDE_FROM_INDEX_CHECKS=["tests.IndexSelectedFieldsModel"])
    def test_projection_query_when_disabled(self):
        IndexSelectedFieldsModel.objects.create(
            field1=1, field2="foo", field3="hello world"
        )
        # where `field1` is indexed
        self.assertEqual(
            IndexSelectedFieldsModel.objects.values_list("field1", flat=True)[0], 1
        )

        # Should work now that we've disabled checking the model
        list(IndexSelectedFieldsModel.objects.values_list("field1", "field2"))

    @datastore_only
    def test_empty_indexes(self):
        instance = EmptyIndexesModel.objects.create(field1=1, field2="foo")

        # grab the entity from the datastore directly
        client = connection.connection._client
        key = client.key(instance._meta.db_table, instance.pk, namespace=connection.namespace)
        entity = client.get(key)

        # despite passing an empty list to indexes we have a limitation where
        # that doesn't really work as you might expect due to the internals
        # of django we can't get around - so we fall back to indexing all fields
        self.assertNotIn('field1', entity.exclude_from_indexes)
        self.assertNotIn('field2', entity.exclude_from_indexes)


# ModelWithNonNullableFieldAndDefaultValueTests verifies that we maintain same
# behavior as Django with respect to a model field that is non-nullable with default value.
class ModelWithNonNullableFieldAndDefaultValueTests(TestCase):
    def _create_instance(self):
        instance = ModelWithNonNullableFieldAndDefaultValue.objects.create(some_field=1)
        client = connection.connection

        instance_default_values = {x.attname: x.default for x in ModelWithNonNullableFieldAndDefaultValue._meta.fields
                                   if x.default != django.db.models.fields.NOT_PROVIDED}

        k = connection.connection.new_key(
            ModelWithNonNullableFieldAndDefaultValue._meta.db_table,
            instance.pk,
            namespace=connection.namespace
        )

        del instance_default_values["some_field"]

        entity = Entity(k, properties=instance_default_values)

        client.put(entity)

        instance.refresh_from_db()
        return instance

    def test_none_in_db_reads_as_none_in_model(self):
        instance = self._create_instance()
        self.assertIsNone(instance.some_field)

    def test_none_in_model_saved_as_default(self):
        instance = self._create_instance()
        instance.refresh_from_db()
        instance.save()
        instance.refresh_from_db()

        self.assertEqual(instance.some_field, 1086)

    @datastore_only
    def test_key_is_deleted_from_entity(self):
        instance = ModelWithNonNullableFieldAndDefaultValue.objects.create(some_field=1)
        client = connection.connection

        instance_default_values = {x.attname: x.default for x in ModelWithNonNullableFieldAndDefaultValue._meta.fields
                                   if x.default != django.db.models.fields.NOT_PROVIDED}

        k = connection.connection.new_key(
            ModelWithNonNullableFieldAndDefaultValue._meta.db_table,
            instance.pk,
            namespace=connection.namespace
        )

        del instance_default_values["some_field"]

        entity = Entity(k, properties=instance_default_values)

        client.put(entity)

        instance.refresh_from_db()


class NullableFieldModelTests(TestCase):

    def test_query_in_list_of_null_not_supported_in_django_32(self):
        """Before Django 3.2, this unit test's query used to return [1],
        but since the following change is no longer supported:
        https://code.djangoproject.com/ticket/31667"""

        NullableFieldModel.objects.create(pk=1)
        NullableFieldModel.objects.create(pk=5, nullable=2)

        results = NullableFieldModel.objects.filter(nullable__in=[None])

        self.assertEqual(
            [r.pk for r in results],
            [] if django.VERSION >= (3, 2) else [1]
        )

    def test_query_isnull(self):
        NullableFieldModel.objects.create(pk=1)
        NullableFieldModel.objects.create(pk=5, nullable=2)

        results = NullableFieldModel.objects.filter(nullable__isnull=True)
        self.assertEqual([r.pk for r in results], [1])

    def test_query_in_list_of_null_and_non_null(self):
        NullableFieldModel.objects.create(pk=1)
        NullableFieldModel.objects.create(pk=5, nullable=2)
        NullableFieldModel.objects.create(pk=6, nullable=3)

        results = NullableFieldModel.objects.filter(nullable__in=[None, 3])
        self.assertEqual({r.pk for r in results}, {1, 6})


class TrueOrNoneModel(models.Model):
    name = models.CharField(max_length=100)
    true_or_null = TrueOrNoneField()

    class Meta:
        unique_together = [("name", "true_or_null")]


class TrueOrNoneFieldTestCase(TestCase):
    """ Tests for using the TrueOrNoneField. """

    def test_converts_false_to_none(self):
        obj = TrueOrNoneModel.objects.create(name="Gordon", true_or_null=False)
        obj.refresh_from_db()
        self.assertIsNone(obj.true_or_null)

    def test_unique_together(self):
        """ Any objects where true_or_null is None should be ignored by the unique_together check.
        """
        TrueOrNoneModel.objects.create(name="Gordon", true_or_null=True)
        TrueOrNoneModel.objects.create(name="Gordon", true_or_null=None)


class TestNegativePrimaryKeys(TestCase):

    def test_inserting_negative_primary_key(self):
        instance = BasicTestModel.objects.create(pk=-1, field1="Hello World!", field2=1998)
        instance.save()

        readout = BasicTestModel.objects.get(pk=-1)

        self.assertEqual(readout.pk, -1)

        readout.field1 = "Hello Mars!"
        readout.save()
        readout.refresh_from_db()

        self.assertEqual(readout.field1, "Hello Mars!")

    def test_querying_negative_numbers(self):
        BasicTestModel.objects.create(pk=-100, field1="Hello World!", field2=1998)
        BasicTestModel.objects.create(pk=-200, field1="Hello World!", field2=1999)

        self.assertEqual(BasicTestModel.objects.filter(pk=-100).count(), 1)
        self.assertEqual(BasicTestModel.objects.filter(pk=-200).count(), 1)
        self.assertEqual(BasicTestModel.objects.exclude(pk=-200).count(), 1)


class DateFieldModel(models.Model):
    dt = models.DateTimeField()


class DateFieldModelTestCase(TestCase):

    def test_min_datetime(self):
        DateFieldModel.objects.create(id=1, dt=datetime.datetime.min)
        self.assertEqual(DateFieldModel.objects.filter(dt=datetime.datetime.min).count(), 1)

    def test_max_datetime(self):
        DateFieldModel.objects.create(id=1, dt=datetime.datetime.max)
        self.assertEqual(DateFieldModel.objects.filter(dt=datetime.datetime.max).count(), 1)


class AbstractParentDbColumnModel(models.Model):
    class Meta(object):
        abstract = True
    parent_field = models.CharField(max_length=100)
    parent_static_field = models.CharField(max_length=100, db_column='legacy_parent_static_field')
    parent_dynamic_field = models.CharField(max_length=100)


AbstractParentDbColumnModel._meta.get_field('parent_dynamic_field').db_column = 'legacy_parent_dynamic_field'


class DbColumnModel(AbstractParentDbColumnModel):
    child_field = models.CharField(max_length=100)
    child_static_field = models.CharField(max_length=100, db_column='legacy_child_static_field')
    child_dynamic_field = models.CharField(max_length=100)


DbColumnModel._meta.get_field('child_dynamic_field').db_column = 'legacy_child_dynamic_field'
# When setting db_column after model class definition, set_attributes_from_name needs to be called.
DbColumnModel._meta.get_field('child_dynamic_field').set_attributes_from_name(None)


class DbColumnModelTestCase(TestCase):

    def test_save_and_read(self):
        django_entity = DbColumnModel.objects.create(
            parent_field='parent_field_value',
            parent_static_field='parent_static_field_value',
            parent_dynamic_field='parent_dynamic_field_value',
            child_field='child_field_value',
            child_static_field='child_static_field_value',
            child_dynamic_field='child_dynamic_field_value',
        )

        saved_django_entity = DbColumnModel.objects.filter(id=django_entity.id).first()
        self.assertEqual(saved_django_entity.parent_field, 'parent_field_value')
        self.assertEqual(saved_django_entity.parent_static_field, 'parent_static_field_value')
        self.assertEqual(saved_django_entity.parent_dynamic_field, 'parent_dynamic_field_value')
        self.assertEqual(saved_django_entity.child_field, 'child_field_value')
        self.assertEqual(saved_django_entity.child_static_field, 'child_static_field_value')
        self.assertEqual(saved_django_entity.child_dynamic_field, 'child_dynamic_field_value')

        # grab the entity from the datastore directly
        key = connection.connection.new_key(DbColumnModel._meta.db_table, django_entity.pk,
                                            namespace=connection.namespace)
        ds_entity = connection.connection.get(key)
        self.assertEqual(ds_entity['parent_field'], 'parent_field_value')
        self.assertEqual(ds_entity['legacy_parent_static_field'], 'parent_static_field_value')
        self.assertEqual(ds_entity['legacy_parent_dynamic_field'], 'parent_dynamic_field_value')
        self.assertEqual(ds_entity['child_field'], 'child_field_value')
        self.assertEqual(ds_entity['legacy_child_static_field'], 'child_static_field_value')
        self.assertEqual(ds_entity['legacy_child_dynamic_field'], 'child_dynamic_field_value')
