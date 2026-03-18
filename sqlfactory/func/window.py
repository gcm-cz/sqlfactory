"""Window functions (https://mariadb.com/kb/en/window-functions/)"""

from __future__ import annotations

from collections.abc import Collection
from enum import Enum
from typing import Any, ClassVar

from sqlfactory.entities import Column, ColumnArg, Expression
from sqlfactory.func.base import Function
from sqlfactory.mixins.order import Order, OrderArg
from sqlfactory.statement import Statement


class FrameType(str, Enum):
    """Window frame type: ROWS, RANGE, or GROUPS."""

    ROWS = "ROWS"
    RANGE = "RANGE"
    GROUPS = "GROUPS"


class FrameBound(Statement):
    """
    Window frame boundary specification.

    Predefined constants:

    - ``FrameBound.UNBOUNDED_PRECEDING`` — ``UNBOUNDED PRECEDING``
    - ``FrameBound.CURRENT_ROW`` — ``CURRENT ROW``
    - ``FrameBound.UNBOUNDED_FOLLOWING`` — ``UNBOUNDED FOLLOWING``

    Factory methods for numeric offsets (value is passed as a query parameter):

    - ``FrameBound.preceding(n)`` — ``%s PRECEDING`` with ``args = [n]``
    - ``FrameBound.following(n)`` — ``%s FOLLOWING`` with ``args = [n]``
    """

    UNBOUNDED_PRECEDING: ClassVar["FrameBound"]
    CURRENT_ROW: ClassVar["FrameBound"]
    UNBOUNDED_FOLLOWING: ClassVar["FrameBound"]

    def __init__(self, bound: str, value: int | None = None) -> None:
        super().__init__()
        self._bound = bound
        self._value = value

    def __str__(self) -> str:
        if self._value is not None:
            return f"{self.dialect.placeholder} {self._bound}"
        return self._bound

    @property
    def args(self) -> list[Any]:
        if self._value is not None:
            return [self._value]
        return []

    @classmethod
    def preceding(cls, n: int) -> "FrameBound":
        """``%s PRECEDING`` — ``n`` is substituted as a query parameter."""
        return cls("PRECEDING", n)

    @classmethod
    def following(cls, n: int) -> "FrameBound":
        """``%s FOLLOWING`` — ``n`` is substituted as a query parameter."""
        return cls("FOLLOWING", n)


FrameBound.UNBOUNDED_PRECEDING = FrameBound("UNBOUNDED PRECEDING")
FrameBound.CURRENT_ROW = FrameBound("CURRENT ROW")
FrameBound.UNBOUNDED_FOLLOWING = FrameBound("UNBOUNDED FOLLOWING")


class Frame(Statement):
    """
    Window frame specification.

    Usage:

    >>> Frame(FrameType.ROWS, FrameBound.UNBOUNDED_PRECEDING, FrameBound.CURRENT_ROW)
    >>> "ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW"

    >>> Frame(FrameType.ROWS, FrameBound.UNBOUNDED_PRECEDING)
    >>> "ROWS UNBOUNDED PRECEDING"
    """

    def __init__(
        self,
        frame_type: FrameType,
        start: FrameBound,
        end: FrameBound | None = None,
    ) -> None:
        super().__init__()
        self.frame_type = frame_type
        self.start = start
        self.end = end

    def __str__(self) -> str:
        if self.end is not None:
            return f"{self.frame_type.value} BETWEEN {self.start!s} AND {self.end!s}"
        return f"{self.frame_type.value} {self.start!s}"

    @property
    def args(self) -> list[Any]:
        out = [*self.start.args]
        if self.end is not None:
            out.extend(self.end.args)
        return out


class OverClause(Statement):
    """
    ``OVER`` clause for window functions.

    Usage:

    >>> OverClause(partition_by=["category"], order=[("price", Direction.DESC)])
    >>> "OVER (PARTITION BY `category` ORDER BY `price` DESC)"

    >>> OverClause()
    >>> "OVER ()"
    """

    def __init__(
        self,
        partition_by: Collection[ColumnArg | Statement] | None = None,
        order: OrderArg | None = None,
        frame: Frame | None = None,
    ) -> None:
        super().__init__()
        self._partition_by: list[ColumnArg | Statement] = list(partition_by) if partition_by else []
        self._order: Order | None = order if isinstance(order, Order) else (Order(order) if order else None)
        self._frame = frame

    def __str__(self) -> str:
        parts: list[str] = []

        if self._partition_by:
            cols = [str(Column(col)) if isinstance(col, str) else str(col) for col in self._partition_by]
            parts.append(f"PARTITION BY {', '.join(cols)}")

        if self._order:
            parts.append(str(self._order))

        if self._frame:
            parts.append(str(self._frame))

        return f"OVER ({' '.join(parts)})"

    @property
    def args(self) -> list[Any]:
        out: list[Any] = []
        for col in self._partition_by:
            if isinstance(col, Statement):
                out.extend(col.args)
        if self._order:
            out.extend(self._order.args)
        if self._frame:
            out.extend(self._frame.args)
        return out


class WindowFunction(Expression):
    """
    A function combined with an ``OVER`` clause, representing a complete window function call.

    Produced by calling ``.over()`` on any :class:`WindowableFunction` instance.

    Usage:

    >>> from sqlfactory.func.agg import Sum
    >>> Sum("price").over(partition_by=["category"])
    >>> "SUM(`price`) OVER (PARTITION BY `category`)"
    """

    def __init__(self, function: Function, over: OverClause) -> None:
        super().__init__()
        self._function = function
        self._over = over

    def __str__(self) -> str:
        return f"{self._function!s} {self._over!s}"

    @property
    def args(self) -> list[Any]:
        return [*self._function.args, *self._over.args]


class WindowableFunction(Function):
    """
    Base class for functions that can be used as window functions via an ``OVER`` clause.

    Subclass this instead of :class:`~sqlfactory.func.base.Function` for any function
    that MariaDB allows to be used with ``OVER (...)``.
    """

    def over(
        self,
        over: OverClause | None = None,
        *,
        partition_by: Collection[ColumnArg | Statement] | None = None,
        order: OrderArg | None = None,
        frame: Frame | None = None,
    ) -> WindowFunction:
        """
        Attach an ``OVER`` clause to this function, producing a :class:`WindowFunction`.

        Accepts either a pre-built :class:`OverClause` as the first positional argument,
        or keyword arguments to construct one inline:

        >>> Sum("price").over(partition_by=["category"], order=[("date", Direction.ASC)])
        >>> "SUM(`price`) OVER (PARTITION BY `category` ORDER BY `date` ASC)"

        :param over: A pre-built :class:`OverClause` instance. Mutually exclusive with keyword args.
        :param partition_by: Columns to partition by.
        :param order: Ordering specification — same ``OrderArg`` type accepted by ``Select``.
        :param frame: Frame specification.
        """
        if over is not None:
            return WindowFunction(self, over)
        return WindowFunction(self, OverClause(partition_by=partition_by, order=order, frame=frame))


# ---------------------------------------------------------------------------
# Pure window functions
# ---------------------------------------------------------------------------


class RowNumber(WindowableFunction):
    """``ROW_NUMBER()`` — sequential row number within the window partition."""

    def __init__(self) -> None:
        super().__init__("ROW_NUMBER")


class Rank(WindowableFunction):
    """``RANK()`` — rank of the current row with gaps."""

    def __init__(self) -> None:
        super().__init__("RANK")


class DenseRank(WindowableFunction):
    """``DENSE_RANK()`` — rank of the current row without gaps."""

    def __init__(self) -> None:
        super().__init__("DENSE_RANK")


class PercentRank(WindowableFunction):
    """``PERCENT_RANK()`` — relative rank of the current row: ``(rank - 1) / (rows - 1)``."""

    def __init__(self) -> None:
        super().__init__("PERCENT_RANK")


class CumeDist(WindowableFunction):
    """``CUME_DIST()`` — cumulative distribution of the current row within the partition."""

    def __init__(self) -> None:
        super().__init__("CUME_DIST")


class Ntile(WindowableFunction):
    """``NTILE(n)`` — distributes rows of the partition into ``n`` groups."""

    def __init__(self, n: int) -> None:
        super().__init__("NTILE", n)


class Lag(WindowableFunction):
    """``LAG(expr[, offset[, default]])`` — value from a preceding row in the partition."""

    def __init__(self, column: ColumnArg | Statement, offset: int | None = None, default: Any = None) -> None:
        col: Statement = Column(column) if isinstance(column, str) else column
        if offset is not None and default is not None:
            super().__init__("LAG", col, offset, default)
        elif offset is not None:
            super().__init__("LAG", col, offset)
        else:
            super().__init__("LAG", col)


class Lead(WindowableFunction):
    """``LEAD(expr[, offset[, default]])`` — value from a following row in the partition."""

    def __init__(self, column: ColumnArg | Statement, offset: int | None = None, default: Any = None) -> None:
        col: Statement = Column(column) if isinstance(column, str) else column
        if offset is not None and default is not None:
            super().__init__("LEAD", col, offset, default)
        elif offset is not None:
            super().__init__("LEAD", col, offset)
        else:
            super().__init__("LEAD", col)


class FirstValue(WindowableFunction):
    """``FIRST_VALUE(expr)`` — first value in the window frame."""

    def __init__(self, column: ColumnArg | Statement) -> None:
        col: Statement = Column(column) if isinstance(column, str) else column
        super().__init__("FIRST_VALUE", col)


class LastValue(WindowableFunction):
    """``LAST_VALUE(expr)`` — last value in the window frame."""

    def __init__(self, column: ColumnArg | Statement) -> None:
        col: Statement = Column(column) if isinstance(column, str) else column
        super().__init__("LAST_VALUE", col)


class NthValue(WindowableFunction):
    """``NTH_VALUE(expr, n)`` — nth value in the window frame."""

    def __init__(self, column: ColumnArg | Statement, n: int) -> None:
        col: Statement = Column(column) if isinstance(column, str) else column
        super().__init__("NTH_VALUE", col, n)
