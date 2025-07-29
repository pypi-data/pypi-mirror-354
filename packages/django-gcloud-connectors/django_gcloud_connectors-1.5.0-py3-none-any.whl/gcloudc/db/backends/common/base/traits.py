from gcloudc.db.backends.common.base.connection import Connection
from gcloudc.db.backends.common.base.query import ORQuery, Operator


def all_branches_filter_on_key(query, connection: Connection) -> bool:
    """
        Given a normalized query, returns True if there is an equality
        filter on a key in each branch of the where
    """
    assert isinstance(query, ORQuery)

    for query in query.queries:
        found = False
        for field, op, value in query.get_filters():
            if field == connection.key_property_name() and op == Operator.EQ:
                found = True
                break

        if not found:
            return False

    return True
