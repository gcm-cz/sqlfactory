"""IN condition, used for checking whether column value is in given list of values."""

from collections.abc import Collection
from typing import overload, Any

from .base import Condition, StatementOrColumn, And, Or
from .simple import Eq, Ne
from ..entities import Column
from ..statement import Statement, Raw


# pylint: disable=too-few-public-methods   # Everything is handled by super classes.
class In(Condition):
    """
    IN condition:

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
    def __init__(
            self, columns: tuple[StatementOrColumn, ...], values: Collection[tuple[Any, ...]], *,
            negative: bool = False
    ):
        """Provides type definition for statement (`column1`, `column2`) IN ((%s, %s), (%s, %s), (%s, %s))"""

    @overload
    def __init__(self, column: StatementOrColumn, values: Collection[Any], *, negative: bool = False):
        """Provides type definition for statement `column` IN (%s, %s, %s)"""

    def __init__(
            self,
            column: StatementOrColumn | tuple[StatementOrColumn, ...],
            values: Collection[Any | tuple[Any, ...]],
            *,
            negative: bool = False
    ):
        """
        :param column: Column to compare, or tuple of columns for multi-column comparison.
        :param values: Values to compare (list of values, or list of tuples of values).
        :param negative: Whether to perform negative comparison (NOT IN)
        """
        is_multi_column = isinstance(column, tuple)

        if is_multi_column:
            stmt, args = self._build_multi_in(column, values, negative=negative)
        else:
            stmt, args = self._build_simple_in(column, values, negative=negative)

        super().__init__(stmt, *args)

    # pylint: disable=consider-using-f-string
    @staticmethod
    def _build_simple_in(
            column: StatementOrColumn,
            values: Collection[Any],
            *,
            negative: bool = False
    ) -> tuple[str, Collection[Any]]:
        if not isinstance(column, Statement):
            column = Column(column)

        add_none = any(value is None for value in values)
        if add_none:
            values = [value for value in values if value is not None]

        args = []

        if values:
            in_stmt = "{} {} ({})".format(
                str(column),
                "IN" if not negative else "NOT IN",
                ", ".join(["%s" if not isinstance(value, Statement) else str(value) for value in values])
            )

            if isinstance(column, Statement):
                args.extend(column.args)

            for value in values:
                if isinstance(value, Statement):
                    args.extend(value.args)
                elif not isinstance(value, Statement):
                    args.append(value)

            if add_none:
                if isinstance(column, Statement):
                    args.extend(column.args)

                return (
                    f"({in_stmt} {'OR' if not negative else 'AND'} {str(column)} IS {'NOT ' if negative else ''}NULL)",
                    args
                )

            return (
                in_stmt,
                args
            )

        if add_none:
            # This could happen only if there is just a one column, not multi-column statement.
            if isinstance(column, Statement):
                args.extend(column.args)

            return (
                f"{str(column)} IS {'NOT ' if negative else ''}NULL",
                args
            )

        return "FALSE" if not negative else "TRUE", []

    # pylint: disable=consider-using-f-string
    @staticmethod
    def _build_multi_in(
            column: tuple[StatementOrColumn, ...],
            values: Collection[tuple[Any, ...]],
            *,
            negative: bool = False
    ) -> tuple[str, Collection[Any]]:
        column = tuple(Column(col) if not isinstance(col, Statement) else col for col in column)

        none_multi_values = [value_tuple for value_tuple in values if any(value is None for value in value_tuple)]
        values = [value_tuple for value_tuple in values if all(value is not None for value in value_tuple)]

        args = []

        for stmt in column:
            if isinstance(stmt, Statement):
                args.extend(stmt.args)

        for value_tuple in values:
            for value in value_tuple:
                if not isinstance(value, Statement):
                    args.append(value)
                elif isinstance(value, Statement):
                    args.extend(value.args)

        multi_in_stmt = "({}) {} ({})".format(
            ", ".join(map(str, column)),
            "IN" if not negative else "NOT IN",
            ", ".join(["(" + ", ".join([
                "%s" if not isinstance(value, Statement) else str(value)
                for value in value_tuple
            ]) + ")" for value_tuple in values])
        )

        if not values and not none_multi_values:
            return "FALSE" if not negative else "TRUE", []

        if not none_multi_values:
            return (
                multi_in_stmt,
                args,
            )

        or_stmt = (Or if not negative else And)()

        if values:
            or_stmt.append(Raw(multi_in_stmt, *args))

        for value_tuple in none_multi_values:
            or_stmt.append(
                And(
                    *[
                        (Eq if not negative else Ne)(col, value)
                        for col, value in zip(column, value_tuple)
                    ]
                )
            )

        return (
            str(or_stmt),
            or_stmt.args
        )
