from __future__ import unicode_literals


SELECT_PATTERN = """
SELECT (%(columns)s) FROM %(table)s
WHERE %(where)s
ORDER BY %(order)s
OFFSET %(offset)s
LIMIT %(limit)s
""".lstrip()

INSERT_PATTERN = """
INSERT INTO %(table)s (%(columns)s)
VALUES %(values)s
""".lstrip()

UPDATE_PATTERN = """
REPLACE INTO %(table)s (%(columns)s)
VALUES %(values)s
WHERE %(where)s
""".lstrip()

DELETE_PATTERN = """
DELETE FROM %(table)s
WHERE %(where)s
""".lstrip()


def _generate_values_expression(instances, columns):
    values = []
    for instance in instances:
        row = []
        for column in columns:
            # FIXME: should this use get_default as a default?
            value = getattr(instance, column, None)

            try:
                text_value = _quote_string(value)
            except UnicodeDecodeError:
                text_value = "'<binary>'"

            row.append(text_value)

        values.append("(" + ", ".join(row) + ")")
    return ", ".join(values)


def _generate_insert_sql(command):
    columns = sorted([x.column for x in command.fields])

    params = {
        "table": command.model._meta.db_table,
        "columns": ", ".join(columns),
        "values": _generate_values_expression(command.objs, columns),
    }

    return (INSERT_PATTERN % params).replace("\n", " ").strip()


def _generate_where_expression(command):
    where = []
    for branch in command.query.queries:
        filters = []
        for key, values in branch.filters.items():
            (column, operator) = key
            if len(values) == 1:
                filters.append(f"{column}{operator}{_quote_string(values[0])}")
            else:
                assert operator == '='
                quoted = map(_quote_string, values)
                filters.append(f"{column} IN ({', '.join(quoted)})")

        branch_sql = (
            "("
            + " AND ".join(filters)
            + ")"
        )

        where.append(branch_sql)

    return " OR ".join(where)


def _quote_string(value):
    needs_quoting = isinstance(value, str)
    # in ANSI SQL as well as GQL, string literals are wrapped in single quotes
    return "'{}'".format(value) if needs_quoting else str(value)


def _generate_select_sql(command):
    has_offset = (command.original_query.low_mark or 0) > 0
    has_limit = command.original_query.high_mark is not None
    has_ordering = bool(command.query.ordering)
    has_where = bool(len(command.query.queries) > 0)

    lines = SELECT_PATTERN.split("\n")

    # Remove limit and offset and where if we don't need them
    if not has_limit:
        del lines[4]

    if not has_offset:
        del lines[3]

    if not has_ordering:
        del lines[2]

    if not has_where:
        del lines[1]

    sql = "\n".join(lines)

    columns = (
        "*"
        if not command.query.only_return_fields and not command.query.only_return_keys
        else ", ".join(sorted(command.query.only_return_fields or command.query.wrapper.key_property_name()))  # noqa Just to make the output predictable
    )

    ordering = [
        ("%s %s" % (x.lstrip("-"), "DESC" if x.startswith("-") else "")).strip() for x in command.query.ordering
    ]

    replacements = {
        "table": command.query.queries[0].path[0],
        "columns": columns,
        "offset": command.original_query.low_mark,
        "limit": (command.original_query.high_mark or 0) - (command.original_query.low_mark or 0),
        "where": _generate_where_expression(command),
        "order": ", ".join(ordering),
    }

    return (sql % replacements).replace("\n", " ").strip()


def _generate_delete_sql(command):
    has_where = bool(len(command.query.queries) > 0)

    replacements = {
        "table": command.query.queries[0].path[0],
        "where": _generate_where_expression(command),
    }

    lines = DELETE_PATTERN.split("\n")
    if not has_where:
        del lines[1]

    sql = "\n".join(lines)

    return (
        (sql % replacements)
        .replace("\n", " ")
        .strip()
    )


def _generate_update_sql(command):
    has_where = bool(len(command.query.queries) > 0)

    lines = UPDATE_PATTERN.split("\n")
    if not has_where:
        del lines[2]

    sql = "\n".join(lines)
    columns = sorted([x[0].column for x in command.values])

    values = {x[0].column: str(x[2]) for x in command.values}

    params = {
        "table": command.query.queries[0].path[0],
        "columns": ", ".join(columns),
        "values": "(" + ", ".join([values[x] for x in columns]) + ")",
        "where": _generate_where_expression(command),
    }

    return (sql % params).replace("\n", " ").strip()


def generate_sql_representation(command):
    from .commands import SelectCommand, DeleteCommand, UpdateCommand, InsertCommand

    if isinstance(command, InsertCommand):
        # Inserts don't have a .query so we have to deal with them
        # separately
        return _generate_insert_sql(command)

    if isinstance(command, SelectCommand):
        return _generate_select_sql(command)
    elif isinstance(command, DeleteCommand):
        return _generate_delete_sql(command)
    elif isinstance(command, UpdateCommand):
        return _generate_update_sql(command)

    raise NotImplementedError("Unrecognized query type")
