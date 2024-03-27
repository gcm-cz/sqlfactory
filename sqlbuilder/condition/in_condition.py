from collections.abc import Collection
from typing import overload, Any

from ..column import Column
from ..statement import StatementWithArgs, Statement
from .base import Condition, StatementOrColumn


class In(Condition):
    """
    - `column` IN (%s, %s, %s)
    - <statement> IN (%s, %s, %s)

    OR

    - (`column1`, `column2`) IN ((%s, %s), (%s, %s), (%s, %s))
    - (<statement>, `column`) IN ((%s, %s), (%s, %s), (%s, %s))
    - (<statement>, <statement>) IN ((%s, %s), (%s, %s), (%s, %s))
    - (`column`, <statement>) IN ((%s, %s), (%s, %s), (%s, %s))

    Also supports comparing to None for single-column conditions (In("column", [1,2,3,None]) will work as expected).
    """

    @overload
    def __init__(self, columns: tuple[StatementOrColumn, ...], values: Collection[tuple[Any, ...]], *, negative: bool = False):
        """Provides type definition for statement (`column1`, `column2`) IN ((%s, %s), (%s, %s), (%s, %s))"""

    @overload
    def __init__(self, column: StatementOrColumn, values: Collection[Any], *, negative: bool = False):
        """Provides type definition for statement `column` IN (%s, %s, %s)"""

    # pylint: disable=consider-using-f-string
    def __init__(self, column: StatementOrColumn | tuple[StatementOrColumn, ...], values: Collection[Any | tuple[Any, ...]], *, negative: bool = False):
        add_none = False

        if None in values:
            add_none = True
            values = list(filter(lambda v: v is not None, values))

        args = []

        if isinstance(column, tuple):
            column = tuple(Column(col) if not isinstance(col, Statement) else col for col in column)
        elif not isinstance(column, Statement):
            column = Column(column)

        if values:
            if isinstance(column, tuple):
                for stmt in column:
                    if isinstance(stmt, StatementWithArgs):
                        args.extend(stmt.args)

                for value_tuple in values:
                    for value in value_tuple:
                        if not isinstance(value, Statement):
                            args.append(value)
                        elif isinstance(value, StatementWithArgs):
                            args.extend(value.args)

                super().__init__(
                    "({}) {} ({})".format(
                        ", ".join(map(str, column)),
                        "IN" if not negative else "NOT IN ",
                        ", ".join(["(" + ", ".join([
                            "%s" if not isinstance(value, Statement) else str(value)
                            for value in value_tuple
                        ]) + ")" for value_tuple in values])
                    ),
                    *args,
                )
            else:
                in_stmt = "{} {} ({})".format(
                    str(column),
                    "IN" if not negative else "NOT IN",
                    ", ".join(["%s" if not isinstance(value, Statement) else str(value) for value in values])
                )

                if isinstance(column, StatementWithArgs):
                    args.extend(column.args)

                for value in values:
                    if isinstance(value, StatementWithArgs):
                        args.extend(value.args)
                    elif not isinstance(value, Statement):
                        args.append(value)

                if add_none:
                    if isinstance(column, StatementWithArgs):
                        args.extend(column.args)

                    super().__init__(
                        f"({in_stmt} {'OR' if not negative else 'AND'} {str(column)} IS {'NOT ' if negative else ''}NULL)",
                        *args
                    )
                else:
                    super().__init__(
                        in_stmt,
                        *args
                    )
        elif add_none:
            # This could happen only if there is just a one column, not multi-column statement.
            if isinstance(column, StatementWithArgs):
                args.extend(column.args)

            super().__init__(
                f"{str(column)} IS {'NOT ' if negative else ''}NULL",
                *args
            )
        else:
            super().__init__("FALSE" if not negative else "TRUE")
