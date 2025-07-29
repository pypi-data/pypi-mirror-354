""" Fake DB API 2.0 for App engine """

from google.api_core.exceptions import Aborted, GoogleAPICallError


DatabaseError = GoogleAPICallError


class IntegrityError(DatabaseError):
    pass


class NotSupportedError(Exception):
    pass


class CouldBeSupportedError(NotSupportedError):
    pass


class DataError(DatabaseError):
    pass


OperationalError = Aborted


class InternalError(DatabaseError):
    pass


class ProgrammingError(DatabaseError):
    pass


class InterfaceError(DatabaseError):
    pass


class TransactionFailedError(IntegrityError):
    """
        Although not defined by the DB-API, it's nice
        to have a consistent way of detecting transaction failures.
    """
    pass


def Binary(val):
    return val


Error = DatabaseError
Warning = DatabaseError
