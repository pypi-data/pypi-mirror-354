import concurrent.futures
import itertools
import multiprocessing
import threading
import unittest

from django.db import IntegrityError
from django.db import connections
from django.db import transaction
from gcloudc.tests.concurrent_utils import increment_integer_model

from . import TestCase, datastore_only, firestore_only
from .models import (
    IntegerModel,
    Tag,
    TestUser,
)


class TransactionTests(TestCase):
    """
    This test case is extended by TransactionTestsExplicitUsingDefault to run the same set of test explicitly
    setting the connection to the default one, and by TransactionTestsNonDefaultConnection to run the same
    set of tests against a different, non-default, connection.

    Always explicitly pass the `using=self.using` when using transaction.atomic, transaction.non_atomic and
    in_atomic_block so that those can be overriden by the child TestCases.
    """

    def test_on_commit_works(self):
        def increment():
            increment.x += 1

        increment.x = 0

        with transaction.atomic(using=self.using):

            transaction.on_commit(increment, using=self.using)
            self.assertEqual(increment.x, 0)

        self.assertEqual(increment.x, 1)

        try:
            with transaction.atomic(using=self.using):
                transaction.on_commit(increment, using=self.using)
                self.assertEqual(increment.x, 1)
                raise ValueError()
        except ValueError:
            pass

        self.assertEqual(increment.x, 1)  # Still the same

        with transaction.atomic(using=self.using):
            pass  # commit hook should have gone with rollback

        self.assertEqual(increment.x, 1)  # Still the same

    def test_get_or_create(self):
        """
            get_or_create uses Django's atomic decorator under the hood
            this can cause issues if called within a gcloudc atomic block
        """

        with transaction.atomic(using=self.using):
            user, created = TestUser.objects.get_or_create(username="foo")
            self.assertTrue(created)

            user, created = TestUser.objects.get_or_create(username="foo")
            self.assertFalse(created)

    def test_repeated_usage_in_a_loop(self):
        pk = TestUser.objects.create(username="foo").pk
        for i in range(4):
            with transaction.atomic(using=self.using):
                TestUser.objects.get(pk=pk)
                continue

        with transaction.atomic(using=self.using):
            TestUser.objects.get(pk=pk)

    def test_recursive_atomic(self):
        lst = []

        @transaction.atomic
        def txn():
            lst.append(True)
            if len(lst) == 3:
                return
            else:
                txn()

        txn()

    def test_atomic_in_separate_thread(self):
        """ Regression test.  See #668. """
        @transaction.atomic
        def txn():
            return

        def target():
            txn()

        thread = threading.Thread(target=target)
        thread.start()
        thread.join()

    def test_atomic_decorator(self):
        connection = connections[self.using]

        @transaction.atomic(using=self.using)
        def txn():
            TestUser.objects.create(username="foo", field2="bar")
            self.assertTrue(connection.in_atomic_block)
            raise ValueError()

        with self.assertRaises(ValueError):
            txn()

        self.assertEqual(0, TestUser.objects.count())

    def test_atomic_context_manager(self):
        self.assertEqual(0, TestUser.objects.count())
        with self.assertRaises(ValueError):
            with transaction.atomic(using=self.using):
                TestUser.objects.create(username="foo", field2="bar")
                raise ValueError()

        self.assertEqual(0, TestUser.objects.count())

    def test_atomic_create_with_unique_constraints(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic(using=self.using):
                TestUser.objects.create(username="one", first_name="one", second_name="one")
                TestUser.objects.create(username="one", first_name="two", second_name="two")

        self.assertEqual(TestUser.objects.count(), 0)

        with self.assertRaises(IntegrityError):
            with transaction.atomic(using=self.using):
                TestUser.objects.create(username="one", first_name="a", second_name="b")
                TestUser.objects.create(username="two", first_name="a", second_name="b")

        self.assertEqual(TestUser.objects.count(), 0)

    def test_atomic_bulk_create_with_unique_constraints(self):
        """Test that bulk_create on models with unique constraints preserve those
        within transactions"""
        self.assertFalse(TestUser.objects.count())
        with self.assertRaises(IntegrityError):
            with transaction.atomic(using=self.using):
                TestUser.objects.bulk_create([
                    TestUser(username="one", first_name="a", second_name="b"),
                    TestUser(username="one", first_name="a", second_name="b"),
                ])

        self.assertEqual(TestUser.objects.count(), 0)

        TestUser.objects.create(username="one", first_name="one", second_name="one")

        with self.assertRaises(IntegrityError):
            with transaction.atomic(using=self.using):
                TestUser.objects.bulk_create([
                    TestUser(username="two", first_name="a", second_name="b"),
                    TestUser(username="one", first_name="x", second_name="y"),
                ])

        self.assertEqual(TestUser.objects.count(), 1)

    def test_atomic_update_with_unique_constraints(self):
        """Test that unique constraint work as intended when performing an update on
        a model with a unique constraint within an atomic block"""
        one = TestUser.objects.create(username="one", first_name="one", second_name="one")

        with self.assertRaises(IntegrityError):
            with transaction.atomic(using=self.using):
                TestUser.objects.create(username="two", first_name="two", second_name="two")
                one.username = "two"
                one.save()

        self.assertEqual(TestUser.objects.count(), 1)

        with self.assertRaises(IntegrityError):
            with transaction.atomic(using=self.using):
                two = TestUser.objects.create(username="two", first_name="two", second_name="two")
                two.username = "one"
                one.save()

        self.assertEqual(TestUser.objects.count(), 1)

        two = TestUser.objects.create(username="two", first_name="two", second_name="two")

        with self.assertRaises(IntegrityError):
            with transaction.atomic(using=self.using):
                one.username = "three"
                two.username = "three"
                one.save()
                two.save()

        self.assertEqual(TestUser.objects.count(), 2)

    def test_atomic_bulk_update_with_unique_constraints(self):
        """Test that unique constraint work as intended when performing a bulk update on
        a model with a unique constraint within an atomic block"""
        one = TestUser.objects.create(username="one", first_name="one", second_name="one")
        two = TestUser.objects.create(username="two", first_name="two", second_name="two")
        with self.assertRaises(IntegrityError):
            # This should raise, since the two instances clash with each other
            with transaction.atomic(using=self.using):
                TestUser.objects.all().update(username="three")

        one.refresh_from_db()
        two.refresh_from_db()

        self.assertEqual(one.username, "one")
        self.assertEqual(two.username, "two")

        # This currently doesn't work because Django transforms it in a single UPDATE
        # with a case-when. E.g.
        #
        # ````sql
        # UPDATE table_users
        # SET username = (case when pk = '1' then 'three'
        #                     when pk = '2' then 'four'
        #                 end),
        #
        # WHERE pk in ('1', '2')
        # ```
        # Currently, the connector doesn't know how to deal with that and blows.
        # I think at least in principle we could support this - but not entirely
        # sure we should, as it would end up as a sequence of put anyway - It might
        # need rewriting using `batch` or something like that maybe?
        #
        # with transaction.atomic(using=self.using):
        #     # This should not fail, since the two instances have different values
        #     one.username = "three"
        #     two.username = "four"
        #     TestUser.objects.bulk_update([one, two], ['username'])

    def test_cache_non_unique_model(self):
        with transaction.atomic():
            number = IntegerModel.objects.create(integer_field=123)
            self.assertTrue(IntegerModel.objects.filter(pk=number.pk).exists())

    def test_cache_non_unique_model_refresh(self):
        number = IntegerModel.objects.create(integer_field=123)
        with transaction.atomic():
            self.assertTrue(IntegerModel.objects.filter(pk=number.pk).exists())
            number.integer_field = 321
            number.save()
            number.refresh_from_db()
            self.assertEqual(number.integer_field, 321)

    def test_cache_non_unique_model_delete(self):
        number = IntegerModel.objects.create(integer_field=123)
        with transaction.atomic():
            self.assertTrue(IntegerModel.objects.filter(pk=number.pk).exists())
            number.delete()
            self.assertFalse(IntegerModel.objects.filter(pk=number.pk).exists())

    def test_nested_decorator(self):
        # Nested decorator pattern we discovered can cause a connection_stack
        # underflow.

        @transaction.atomic
        def inner_txn():
            pass

        @transaction.atomic
        def outer_txn():
            inner_txn()

        # Calling inner_txn first puts it in a state which means it doesn't
        # then behave properly in a nested transaction.
        inner_txn()
        outer_txn()

    def test_nested_atomic_create_should_roll_back(self):
        """
        Test that a nested atomic operation is rolled back as part of the rollback
        of the outer atomic block.
        """

        self.assertEqual(IntegerModel.objects.count(), 0)
        self.assertEqual(Tag.objects.count(), 0)

        with self.assertRaises(ValueError):
            with transaction.atomic(using=self.using):
                IntegerModel.objects.create(integer_field=1)

                with transaction.atomic(using=self.using):
                    Tag.objects.create(name='something')
                raise ValueError()

        self.assertEqual(Tag.objects.count(), 0)
        self.assertEqual(IntegerModel.objects.count(), 0)

    @unittest.skip("Supposed to fail, leaving as reference")
    def test_unique_constraint_sdk(self):
        """Test that, using the low-level sdk APIs two nested transaction
        fail because of too much contention.

        This test is intended to emulate the equivalent of this in Django land

        ```python
        class TestModel(Model):
            name = CharField(unique=True)

        ...
        with transaction.atomic(using=self.using):
            TestModel.objects.create(name="Jason")

            with transaction.non_atomic(using=self.using):
                TestModel.objects.create(name="Jason")
        ```

        This fails, (and it's ok!) but it may not be obvious why. It's useful to remember
        that because when we have unique constraints, before doing a `put` we perform a `fetch`
        inside a transaction, to ensure there are no constraint violation. This extra
        fetch breaks serialisable isolation, and makes the create (correctly) fail.

        Currently, this test fails in slightly different ways in PESSIMISTIC concurrency
        mode, which is expected. In that mode, the inner transaction can't commit,
        because it cannot acquire the relevant lock.
        This creates a deadlock, which is only broken by a timeout in the APIs.
        """
        from django.db import connection
        from google.cloud import datastore

        local_client = connection.connection.gclient

        with local_client.transaction() as txn:
            query = local_client.query(kind="WithUnique")
            query.add_filter('name', '=', 'Jason')
            query.fetch()
            key = local_client.key("WithUnique", 1)
            original_entity = datastore.Entity(key=key)
            original_entity["name"] = "Jason"
            txn.put(original_entity)

            with local_client.transaction() as txn2:
                query = local_client.query(kind="WithUnique")
                query.add_filter('name', '=', 'Jason')
                query.fetch()
                new_key = local_client.key("WithUnique", 2)
                new_entity = datastore.Entity(key=new_key)
                new_entity["name"] = "Jason"
                txn2.put(new_entity)

    @unittest.skip("Supposed to fail, leaving as reference")
    def test_unique_constraint_multiple_connections_sdk(self):
        """Test that, using the low-level sdk APIs two parallell transaction
        fail because of too much contention.

        This test is intended to emulate the equivalend of this in Django land

        ```python
        class TestModel(Model):
            name = CharField(unique=True)

        ...
        # Two requests,  both with name=Jason
        def create_user(request):
            with transaction.atomic(using=self.using):
                TestModel.objects.create(name=request.GET['name'])
        ```
        Because this test doesn't actually run in parallell, but only using
        separate connections in nested transactions for the two requests,
        both `create` actually fail (e.g. the outer transaction fails and is
        rolled back because the inner transaction fails due to contention)

        Currently, this test fails in slightly different ways in PESSIMISTIC concurrency
        mode, which is expected. In that mode, the inner transaction can't commit,
        because it cannot acquire the relevant lock.
        This creates a deadlock, which is only broken by a timeout in the APIs.
        """
        from django.db import connection
        from google.cloud import datastore

        local_client = connection.connection.gclient

        new_connection = connection.copy()
        new_connection.connect()
        local_client2 = new_connection.connection.gclient

        with local_client.transaction() as txn:
            query = local_client.query(kind="WithUnique")
            query.add_filter('name', '=', 'Jason')
            query.fetch()
            key = local_client.key("WithUnique", 1)
            original_entity = datastore.Entity(key=key)
            original_entity["name"] = "Jason"
            txn.put(original_entity)

            with local_client2.transaction() as txn2:
                query = local_client2.query(kind="WithUnique")
                query.add_filter('name', '=', 'Jason')
                query.fetch()
                new_key = local_client2.key("WithUnique", 2)
                new_entity = datastore.Entity(key=new_key)
                new_entity["name"] = "Jason"
                txn2.put(new_entity)

    @datastore_only
    def test_atomic_context_manager_contention_threads(self):
        """
        Test concurrent writes from different threads do not have contention issues.
        """
        initial_value = 0
        concurrent_writes = 10
        futures = []
        original_integer = IntegerModel.objects.create(integer_field=initial_value)

        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_writes) as executor:
            for _ in range(concurrent_writes):
                futures.append(executor.submit(increment_integer_model, original_integer.pk, self.using, False))
        concurrent.futures.wait(futures)

        futures_exceptions = [future.exception() for future in futures]
        number_successful_writes = len(list(itertools.filterfalse(None, futures_exceptions)))

        original_integer.refresh_from_db()

        self.assertGreater(number_successful_writes, 0, 'It should save at least an object')
        self.assertEqual(original_integer.integer_field, initial_value + number_successful_writes)

    # `test_atomic_context_manager_contention_threads` sporadically fails if run on Firestore.
    #  Specificaly, it fails with:
    # `AssertionError: 0 not greater than 0 : It should save at least an object`
    # caused by all the transactions to fail due to
    # `django.db.utils.OperationalError, Aborted('Transaction lock timeout.')`
    # While the expectation would be that at least one of the transactions would succeed, contention never
    # seem to happen.
    # To make sure that's the case we added the following test, where we tweaked the test to cover only
    # the contention scenario.
    # At the same time we should investigate why we have this "unexpected" behaviour in Firestore and if it cause by
    # a bug in our code.
    # TODO(firestore-contention): look into it in a separate ticket.
    @firestore_only
    def test_atomic_context_manager_contention_threads_firestore(self):
        """
        Test concurrent writes from different threads do not have contention issues.
        """
        initial_value = 0
        concurrent_writes = 10
        futures = []
        original_integer = IntegerModel.objects.create(integer_field=initial_value)

        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_writes) as executor:
            for _ in range(concurrent_writes):
                futures.append(executor.submit(increment_integer_model, original_integer.pk, self.using, False))
        concurrent.futures.wait(futures)

        futures_exceptions = [future.exception() for future in futures]
        number_successful_writes = len(list(itertools.filterfalse(None, futures_exceptions)))

        original_integer.refresh_from_db()

        self.assertEqual(original_integer.integer_field, initial_value + number_successful_writes)

    @datastore_only
    def test_atomic_context_manager_contention_processes(self):
        """
        Test concurrent writes from different processes do not have contention issues.
        """
        initial_value = 0
        concurrent_writes = 10
        futures = []
        original_integer = IntegerModel.objects.create(integer_field=initial_value)

        with concurrent.futures.ProcessPoolExecutor(
            max_workers=concurrent_writes, mp_context=multiprocessing.get_context("spawn")
        ) as executor:
            for _ in range(concurrent_writes):
                futures.append(executor.submit(increment_integer_model, original_integer.pk, self.using, True))
        concurrent.futures.wait(futures)

        futures_exceptions = [future.exception() for future in futures]
        number_successful_writes = len(list(itertools.filterfalse(None, futures_exceptions)))

        original_integer.refresh_from_db()

        self.assertGreater(number_successful_writes, 0, 'It should save at least an object')
        self.assertEqual(original_integer.integer_field, initial_value + number_successful_writes)

    # `test_atomic_context_manager_contention_processes` sporadically fails if run on Firestore.
    #  Specificaly, it fails with:
    # `AssertionError: 0 not greater than 0 : It should save at least an object`
    # caused by all the transactions to fail due to
    # `django.db.utils.OperationalError, Aborted('Transaction lock timeout.')`
    # While the expectation would be that at least one of the transactions would succeed, contention never
    # seem to happen.
    # To make sure that's the case we added the following test, where we tweaked the test to cover only
    # the contention scenario.
    # At the same time we should investigate why we have this "unexpected" behaviour in Firestore and if it cause by
    # a bug in our code.
    # TODO(firestore-contention): look into it in a separate ticket.
    @firestore_only
    def test_atomic_context_manager_contention_processes_firestore(self):
        """
        Test concurrent writes from different processes do not have contention issues.
        """
        initial_value = 0
        concurrent_writes = 10
        futures = []
        original_integer = IntegerModel.objects.create(integer_field=initial_value)

        with concurrent.futures.ProcessPoolExecutor(
            max_workers=concurrent_writes, mp_context=multiprocessing.get_context("spawn")
        ) as executor:
            for _ in range(concurrent_writes):
                futures.append(executor.submit(increment_integer_model, original_integer.pk, self.using, True))
        concurrent.futures.wait(futures)

        futures_exceptions = [future.exception() for future in futures]
        number_successful_writes = len(list(itertools.filterfalse(None, futures_exceptions)))

        original_integer.refresh_from_db()

        self.assertEqual(original_integer.integer_field, initial_value + number_successful_writes)

    def test_query_on_unique_hits_cache(self):
        with transaction.atomic():
            TestUser.objects.create(username="foo")
            self.assertTrue(TestUser.objects.filter(username="foo").exists())

    def test_query_on_unique_hits_cache_nested(self):
        with transaction.atomic():
            TestUser.objects.create(username="foo")

            with transaction.atomic():
                self.assertTrue(TestUser.objects.filter(username="foo").exists())

    def test_doesnt_cache(self):
        TestUser.objects.create(username="foo")
        from django.db import connection
        try:
            with transaction.atomic():
                TestUser.objects.create(username="foo")
        except IntegrityError:
            self.assertFalse(connection.connection._cache)


class TransactionTestsNonDefaultConnection(TransactionTests):
    """
    This Testcase runs all the tests defined in TransactionTests against a non default connection.
    """
    using = 'non_default_connection'
