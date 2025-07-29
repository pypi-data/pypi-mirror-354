from . import TestCase
from .models import BinaryFieldModel


class OffsetLimitTestCase(TestCase):
    """ Tests for limits and offsets on queries. """

    def test_offset_no_ordering(self):
        # This was causing an error with Firestore because it always wants an explicit ordering
        # when using a cursor.
        for _ in range(3):
            BinaryFieldModel.objects.create(binary=True)
        list(BinaryFieldModel.objects.all()[2:])
