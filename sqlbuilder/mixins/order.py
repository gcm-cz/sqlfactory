"""ORDER BY mixin for query generator"""

from __future__ import annotations
from enum import Enum
from typing import Any, Generic, TypeVar, Collection, Literal

from ..entities import Column, ColumnArg
from ..statement import Statement, StatementWithArgs


class Direction(str, Enum):
    """Ordering direction as enum"""
    ASC = "ASC"
    DESC = "DESC"


OrderColumn = ColumnArg | Statement


class Order(list[tuple[OrderColumn, Direction | Literal['ASC', 'DESC']]], StatementWithArgs):
    """ORDER BY statement as list of columns to use for ordering"""
    def __str__(self):
        if not self:
            return ""

        out = []

        for column, direction in self:
            if isinstance(column, str):
                column = Column(column)

            out.append(f"{str(column)} {direction.value if isinstance(direction, Direction) else direction}")

        return f"ORDER BY {', '.join(out)}"

    @property
    def args(self) -> list[Any]:
        out = []
        for column, _ in self:
            if isinstance(column, StatementWithArgs):
                out.extend(column.args)

        return out


T = TypeVar('T')


class WithOrder(Generic[T]):
    """Mixin to provide ORDER BY support for query generator."""
    def __init__(self, *args, order: OrderArg = None, **kwargs):
        """
        :param order: Ordering specification - either instance of Order, or collection of columns and directions.
        """
        super().__init__(*args, **kwargs)
        if order:
            self._order = order if isinstance(order, Order) else Order(order)
        else:
            self._order = None

    def order_by(self, column: OrderColumn, direction: Direction) -> T:
        """
        Add column to be used for ordering. Can be called multiple times, columns will be ordered by order of calls.
        :param column: Column to use for ordering
        :param direction: Ordering direction
        :return:
        """
        if self._order is None:
            self._order = Order()

        self._order.append((column, direction))
        return self

    # pylint: disable=invalid-name
    def ORDER_BY(self, column: OrderColumn, direction: Direction) -> T:
        """Alias for order_by() to be more SQL-like with all capitals."""
        return self.order_by(column, direction)


# Ordering argument for class init (specify directly instance of Order, or collection of columns and directions).
OrderArg = Order | Collection[tuple[OrderColumn, Direction]]
