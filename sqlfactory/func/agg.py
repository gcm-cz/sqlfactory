"""Aggregate functions."""

from typing import Literal

from ..entities import Column, ColumnArg
from ..statement import Raw, Statement
from .base import Function


# pylint: disable=too-few-public-methods
class AggregateFunction(Function):
    """Base class for aggregate functions"""

    def __init__(self, agg: str, column: ColumnArg | Statement):
        super().__init__(agg, Column(column) if isinstance(column, str) else column)


# pylint: disable=too-few-public-methods
class Avg(AggregateFunction):
    """AVG(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("AVG", column)


# pylint: disable=too-few-public-methods
class BitAnd(AggregateFunction):
    """BIT_AND(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("BIT_AND", column)


# pylint: disable=too-few-public-methods
class BitOr(AggregateFunction):
    """BIT_OR(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("BIT_OR", column)


# pylint: disable=too-few-public-methods
class BitXor(AggregateFunction):
    """BIT_XOR(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("BIT_XOR", column)


# pylint: disable=too-few-public-methods
class Count(Function):
    """
    - COUNT(<column>)
    - COUNT(DISTINCT <column>)
    """

    def __init__(self, column: ColumnArg | Literal["*"], *, distinct: bool = False):
        if isinstance(column, str) and column == "*":
            column_stmt: Statement = Raw("*")
        elif isinstance(column, str):
            column_stmt = Column(column)
        else:
            column_stmt = column

        if distinct:
            super().__init__(
                "COUNT", Raw(f"DISTINCT {column_stmt!s}", *column_stmt.args if isinstance(column_stmt, Statement) else [])
            )
        else:
            super().__init__("COUNT", column_stmt)


# pylint: disable=too-few-public-methods
class Max(AggregateFunction):
    """MAX(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("MAX", column)


# pylint: disable=too-few-public-methods
class Min(AggregateFunction):
    """MIN(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("MIN", column)


# pylint: disable=too-few-public-methods
class Std(AggregateFunction):
    """STD(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("STD", column)


# pylint: disable=too-few-public-methods
class Sum(AggregateFunction):
    """SUM(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("SUM", column)
