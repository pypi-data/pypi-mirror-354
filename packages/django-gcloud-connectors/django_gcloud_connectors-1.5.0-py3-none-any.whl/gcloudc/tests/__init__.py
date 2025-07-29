import atexit
import cProfile
import functools
import io
import pstats

from django.test import TransactionTestCase as DjangoTestCase
from django.db import connection
from pstats import SortKey
from gcloudc.tests.router import Router


PROFILER = None


class TestCase(DjangoTestCase):
    databases = '__all__'
    using = 'default'

    def setUp(self):
        global PROFILER
        if not PROFILER:
            PROFILER = cProfile.Profile()
            PROFILER.enable()

            def print_stats():
                global PROFILER # noqa
                if PROFILER:
                    PROFILER.disable()
                    s = io.StringIO()
                    sortby = SortKey.CUMULATIVE
                    ps = pstats.Stats(PROFILER, stream=s).sort_stats(sortby)
                    ps.print_stats()
                    with open("profile.txt", "w") as f:
                        f.write(s.getvalue())

            atexit.register(print_stats)

        connection.ensure_connection()
        Router.activate_connection(self.using)
        super().setUp()

    # This was mistakenly renamed to assertCountsEqual
    # in Python 3, so this avoids any complications arising
    # when they rectify that! https://bugs.python.org/issue27060
    def assertItemsEqual(self, lhs, rhs):
        if set(lhs) != set(rhs):
            raise AssertionError("Items were not the same in both lists")


def test_firestore():
    return "firestore" in connection.ops.__module__


def test_datastore():
    return "datastore" in connection.ops.__module__


def skip_firestore(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if test_firestore():
            return

        return func(*args, **kwargs)
    return wrapper


def skip_datastore(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if test_datastore():
            return

        return func(*args, **kwargs)
    return wrapper


datastore_only = skip_firestore
firestore_only = skip_datastore
