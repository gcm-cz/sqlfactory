from typing import Any

from .base import Condition, StatementOrColumn
from ..statement import Statement, StatementWithArgs


class SimpleCondition(Condition):
    """
    Simple condition comparing one column with given value, using specified operator.
    """
    def __init__(self, column: StatementOrColumn, operator: str, value: Statement | Any):
        """
        :param column: Column to compare.
        :param operator: Operator to use for comparison.
        :param value: Value to compare column value to.
        """
        if not isinstance(column, Statement):
            from ..column import Column
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


class Equals(SimpleCondition):
    """
    - `column` = <value>
    - `column` IS NULL
    - <statement> = <value>
    - <statement> IS NULL
    """
    def __init__(self, column: StatementOrColumn, value: Any | None | Statement):
        if value is None:
            super().__init__(column, "IS", value)
        else:
            super().__init__(column, "=", value)


class NotEquals(SimpleCondition):
    """
    - `column` != <value>
    - <statement> != <value>
    - `column` IS NOT NULL
    - <statement> IS NOT NULL
    """
    def __init__(self, column: StatementOrColumn, value: Any | None | Statement):
        if value is None:
            super().__init__(column, "IS NOT", value)
        else:
            super().__init__(column, "!=", value)


class GreaterThanOrEquals(SimpleCondition):
    """
    - `column` >= <value>
    - <statement> >= <value>
    """
    def __init__(self, column: StatementOrColumn, value: Any | Statement):
        super().__init__(column, ">=", value)


class GreaterThan(SimpleCondition):
    """
    - `column` > <value>
    - <statement> > <value>
    """
    def __init__(self, column: StatementOrColumn, value: Any | Statement):
        super().__init__(column, ">", value)


class LessThanOrEquals(SimpleCondition):
    """
    - `column` <= <value>
    - <statement> <= <value>
    """
    def __init__(self, column: StatementOrColumn, value: Any | Statement):
        super().__init__(column, "<=", value)


class LessThan(SimpleCondition):
    """
    - `column` < <value>
    - <statement> < <value>
    """
    def __init__(self, column: StatementOrColumn, value: Any | Statement):
        super().__init__(column, "<", value)


# Aliases for simple conditions
Eq = Equals
Ge = GreaterThanOrEquals
Gt = GreaterThan
Le = LessThanOrEquals
Lt = LessThan
Ne = NotEquals
