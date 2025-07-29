

def increment_integer_model(integer_pk, using='default', init_django=False):
    if init_django:
        import django
        from gcloudc.tests.router import Router
        django.setup()
        Router.activate_connection(connection_alias=using)

    from django.db import connections, transaction, IntegrityError
    from .models import (
        IntegerModel,
    )

    connection = connections['default']
    connection.ensure_connection()

    try:
        with transaction.atomic(using=using):
            the_integer = IntegerModel.objects.get(pk=integer_pk)
            the_integer.integer_field = the_integer.integer_field + 1
            the_integer.save()
    except IntegrityError:
        raise Exception("TransactionFailedError")
    except Exception as e:
        raise Exception(f"{e.__class__}: {e.args}")
