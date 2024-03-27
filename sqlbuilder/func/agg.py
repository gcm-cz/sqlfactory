from typing import Literal

from .base import Function
from ..column import Column, ColumnArg


class AggregateFunction(Function):
    """Base class for aggregate functions"""
    def __init__(self, agg: str, column: ColumnArg):
        super().__init__(agg, Column(column) if isinstance(column, str) else column)


class Avg(AggregateFunction):
    """AVG(<column>)"""
    def __init__(self, column: ColumnArg):
        super().__init__("AVG", column)


class BitAnd(AggregateFunction):
    """BIT_AND(<column>)"""
    def __init__(self, column: ColumnArg):
        super().__init__("BIT_AND", column)


class BitOr(AggregateFunction):
    """BIT_OR(<column>)"""
    def __init__(self, column: ColumnArg):
        super().__init__("BIT_OR", column)


class BitXor(AggregateFunction):
    """BIT_XOR(<column>)"""
    def __init__(self, column: ColumnArg):
        super().__init__("BIT_XOR", column)


class Count(Function):
    """COUNT(<column>)"""
    def __init__(self, column: ColumnArg | Literal['*']):
        super().__init__(
            "COUNT",
            column if isinstance(column, Column) or column == '*' else Column(column)
        )


class Max(AggregateFunction):
    """MAX(<column>)"""
    def __init__(self, column: ColumnArg):
        super().__init__("MAX", column)


class Min(AggregateFunction):
    """MIN(<column>)"""
    def __init__(self, column: ColumnArg):
        super().__init__("MIN", column)


class Std(AggregateFunction):
    """STD(<column>)"""
    def __init__(self, column: ColumnArg):
        super().__init__("STD", column)


class Sum(AggregateFunction):
    """SUM(<column>)"""
    def __init__(self, column: ColumnArg):
        super().__init__("SUM", column)
