from django.db import models

from . import TestCase


class AlphabeticalFields(models.Model):
    """ A model with two fields which have an obvious alphabetical order. """
    a_field = models.CharField(max_length=100)
    b_field = models.CharField(max_length=100)


class ObscureQueriesTestCase(TestCase):
    """ Tests for bizarre edge cases! """

    def test_combine_exact_and_in_filter_with_another_exact(self):
        """ This tests a particular bug which existed in which the existence of both an `__in` and
            an exact/equal filter on the same field would cause a filter on another field to be
            ignored, but only if the field with the two filters had a name which was alphabetically
            lower than that of the other field.
        """
        thing1 = AlphabeticalFields.objects.create(a_field="1", b_field="cake")
        AlphabeticalFields.objects.create(a_field="1", b_field="notcake")
        AlphabeticalFields.objects.create(a_field="2", b_field="notcake")
        queryset = AlphabeticalFields.objects.filter(
            a_field__in=["1", "2"],
            a_field="1",
            b_field="cake",
        )
        self.assertEqual(list(queryset), [thing1])
