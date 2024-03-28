"""Simple binary comparison conditions."""

from typing import Any

from .base import Condition, StatementOrColumn
from ..statement import Statement, StatementWithArgs


# pylint: disable=too-few-public-methods  # As everything is handled in base classes.
class SimpleCondition(Condition):
    # pylint: disable=duplicate-code  # It does not make sense to generalize two-row statement used on two places.
    """
    Simple condition comparing one column with given value, using specified operator.
    """
    def __init__(self, column: StatementOrColumn, operator: str, value: Statement | Any):
        """
        :param column: Column to compare (string or instance of Column) or Statement to use on left side of comparison.
        :param operator: Operator to use for comparison.
        :param value: Value to compare column value to (or statement to use on right side of comparison).
        """
        if not isinstance(column, Statement):
            # pylint: disable=import-outside-toplevel,cyclic-import
            from ..entities import Column
            column = Column(column)

        args = []

        if isinstance(column, StatementWithArgs):
            args.extend(column.args)

        if isinstance(value, StatementWithArgs):
            args.extend(value.args)

        elif not isinstance(value, Statement):
            args.append(value)

        if isinstance(value, Statement):
            super().__init__(
                f"{str(column)} {operator} {str(value)}",
                *args
            )
        else:
            super().__init__(
                f"{str(column)} {operator} %s",
                *args
            )


# pylint: disable=too-few-public-methods  # As everything is handled in base classes.
class Equals(SimpleCondition):
    """
    - `column` = <value>
    - `column` IS NULL
    - <statement> = <value>
    - <statement> IS NULL
    """
    def __init__(self, column: StatementOrColumn, value: Any | None | Statement):
        """
        :param column: Column to compare (string or instance of Column) or Statement to use on left side of comparison.
        :param value: Value to compare column value to (or statement to use on right side of comparison).
        """
        if value is None:
            super().__init__(column, "IS", value)
        else:
            super().__init__(column, "=", value)


# pylint: disable=too-few-public-methods  # As everything is handled in base classes.
class NotEquals(SimpleCondition):
    """
    - `column` != <value>
    - <statement> != <value>
    - `column` IS NOT NULL
    - <statement> IS NOT NULL
    """
    def __init__(self, column: StatementOrColumn, value: Any | None | Statement):
        """
        :param column: Column to compare (string or instance of Column) or Statement to use on left side of comparison.
        :param value: Value to compare column value to (or statement to use on right side of comparison).
        """
        if value is None:
            super().__init__(column, "IS NOT", value)
        else:
            super().__init__(column, "!=", value)


# pylint: disable=too-few-public-methods  # As everything is handled in base classes.
class GreaterThanOrEquals(SimpleCondition):
    """
    - `column` >= <value>
    - <statement> >= <value>
    """
    def __init__(self, column: StatementOrColumn, value: Any | Statement):
        """
        :param column: Column to compare (string or instance of Column) or Statement to use on left side of comparison.
        :param value: Value to compare column value to (or statement to use on right side of comparison).
        """
        super().__init__(column, ">=", value)


# pylint: disable=too-few-public-methods  # As everything is handled in base classes.
class GreaterThan(SimpleCondition):
    """
    - `column` > <value>
    - <statement> > <value>
    """
    def __init__(self, column: StatementOrColumn, value: Any | Statement):
        """
        :param column: Column to compare (string or instance of Column) or Statement to use on left side of comparison.
        :param value: Value to compare column value to (or statement to use on right side of comparison).
        """
        super().__init__(column, ">", value)


# pylint: disable=too-few-public-methods  # As everything is handled in base classes.
class LessThanOrEquals(SimpleCondition):
    """
    - `column` <= <value>
    - <statement> <= <value>
    """
    def __init__(self, column: StatementOrColumn, value: Any | Statement):
        """
        :param column: Column to compare (string or instance of Column) or Statement to use on left side of comparison.
        :param value: Value to compare column value to (or statement to use on right side of comparison).
        """
        super().__init__(column, "<=", value)


# pylint: disable=too-few-public-methods  # As everything is handled in base classes.
class LessThan(SimpleCondition):
    """
    - `column` < <value>
    - <statement> < <value>
    """
    def __init__(self, column: StatementOrColumn, value: Any | Statement):
        """
        :param column: Column to compare (string or instance of Column) or Statement to use on left side of comparison.
        :param value: Value to compare column value to (or statement to use on right side of comparison).
        """
        super().__init__(column, "<", value)


# Convenient aliases for shorter code.
Eq = Equals
Ge = GreaterThanOrEquals
Gt = GreaterThan
Le = LessThanOrEquals
Lt = LessThan
Ne = NotEquals
