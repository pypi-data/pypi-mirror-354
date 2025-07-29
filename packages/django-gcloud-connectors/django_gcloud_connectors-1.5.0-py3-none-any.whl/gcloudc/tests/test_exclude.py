from . import TestCase
from .models import TestUser


class ExcludeTestCase(TestCase):

    def test_exclude_by_pk(self):
        user = TestUser.objects.create(username="test", first_name="test", second_name="test")
        self.assertEqual(list(TestUser.objects.exclude(pk=user.pk)), [])
        user2 = TestUser.objects.create(username="test2", first_name="test2", second_name="test2")
        self.assertEqual(list(TestUser.objects.exclude(pk=user.pk)), [user2])

    def test_exclude_by_charfield(self):
        user = TestUser.objects.create(username="test", first_name="test", second_name="test")
        self.assertEqual(list(TestUser.objects.exclude(username=user.username)), [])
        user2 = TestUser.objects.create(username="test2", first_name="test2", second_name="test2")
        self.assertEqual(list(TestUser.objects.exclude(username=user.username)), [user2])
