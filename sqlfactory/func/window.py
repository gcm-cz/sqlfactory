"""Window functions (https://mariadb.com/kb/en/window-functions/)"""

from __future__ import annotations

from collections.abc import Collection
from enum import Enum
from typing import Any, ClassVar

from sqlfactory.entities import Column, ColumnArg, Expression
from sqlfactory.func.base import Function
from sqlfactory.mixins.order import Direction, Order, OrderArg, OrderColumn
from sqlfactory.statement import Statement, operand


class FrameType(str, Enum):
    """
    Window frame type: ROWS, RANGE, or GROUPS.

    ``GROUPS`` is not implemented by MariaDB (any version) or MySQL 8 -- both reject it with a syntax error
    (verified: MariaDB 11.4 raises ``ERROR 1064``, MySQL 8 raises ``ERROR 1235``). It is kept here because it is
    real, released SQL that other dialects this library supports do accept (verified on PostgreSQL 17 and
    SQLite); do not use it if you target MariaDB or MySQL.
    """

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
            cols = [str(Column(col)) if isinstance(col, str) else operand(col) for col in self._partition_by]
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
    """
    ``LAG(expr[, offset[, default]])`` — value from a preceding row in the partition.

    MariaDB documents only ``LAG(expr[, offset])`` (https://mariadb.com/kb/en/lag/) and rejects the
    three-argument form with a syntax error (verified on MariaDB 11.4: ``ERROR 1064``). MySQL 8, PostgreSQL and
    SQLite all accept ``LAG(expr, offset, default)`` (verified). ``default`` is kept here because it is real,
    released behaviour for those targets; this library's ``MySQLDialect`` (`sqlfactory.dialect`) represents both
    MySQL and MariaDB, so rendering cannot switch on dialect automatically -- passing ``default`` produces SQL
    that a MariaDB server will reject.
    """

    def __init__(self, column: ColumnArg | Statement, offset: int | None = None, default: Any = None) -> None:
        col: Statement = Column(column) if isinstance(column, str) else column
        if offset is not None and default is not None:
            super().__init__("LAG", col, offset, default)
        elif offset is not None:
            super().__init__("LAG", col, offset)
        else:
            super().__init__("LAG", col)


class Lead(WindowableFunction):
    """
    ``LEAD(expr[, offset[, default]])`` — value from a following row in the partition.

    MariaDB documents only ``LEAD(expr[, offset])`` (https://mariadb.com/kb/en/lead/) and rejects the
    three-argument form with a syntax error (verified on MariaDB 11.4: ``ERROR 1064``). MySQL 8, PostgreSQL and
    SQLite all accept ``LEAD(expr, offset, default)`` (verified). ``default`` is kept here because it is real,
    released behaviour for those targets; this library's ``MySQLDialect`` (`sqlfactory.dialect`) represents both
    MySQL and MariaDB, so rendering cannot switch on dialect automatically -- passing ``default`` produces SQL
    that a MariaDB server will reject.
    """

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
    """
    ``LAST_VALUE(expr)`` — last value in the window frame.

    MariaDB also has a multi-argument, non-window ``LAST_VALUE(expr, expr, ...)`` (it evaluates all of them and
    returns the last -- a side-effect trick for reading ``@var := expr`` assignments) documented as an
    information function (https://mariadb.com/kb/en/last_value/), not a window function. That form is out of
    scope here.
    """

    def __init__(self, column: ColumnArg | Statement) -> None:
        col: Statement = Column(column) if isinstance(column, str) else column
        super().__init__("LAST_VALUE", col)


class NthValue(WindowableFunction):
    """
    ``NTH_VALUE(expr, n)`` — nth value in the window frame.

    MariaDB's own BNF (https://mariadb.com/kb/en/nth_value/) writes ``NTH_VALUE(expr[, num_row])`` as if ``n``
    were optional, but ``NTH_VALUE(expr)`` alone is a syntax error (verified on MariaDB 11.4: ``ERROR 1064``) --
    ``n`` is required, as this class already declares.
    """

    def __init__(self, column: ColumnArg | Statement, n: int) -> None:
        col: Statement = Column(column) if isinstance(column, str) else column
        super().__init__("NTH_VALUE", col, n)


class Median(Expression):
    """
    ``MEDIAN(expr) OVER ([PARTITION BY partition_expression])`` — median (50th percentile) of ``expr`` within
    each partition.

    MariaDB 10.3.3+ (https://mariadb.com/kb/en/median/). A specific case of `PercentileCont`, equivalent to
    ``PercentileCont(0.5)`` ordered by ``expr`` itself.

    Unlike the other window functions in this module, its ``OVER (...)`` takes only ``PARTITION BY`` -- MariaDB
    rejects an ``ORDER BY`` there with a syntax error (verified on MariaDB 11.4: ``ERROR 1064``), because the
    ordering is already implied by ``expr``. So this class takes ``partition_by`` directly instead of an
    `OverClause`/`WindowableFunction.over()` call, which would let ``order``/``frame`` be passed for no valid SQL.

    Not implemented by MySQL 8 or PostgreSQL (verified).
    """

    def __init__(
        self,
        column: ColumnArg | Statement,
        *,
        partition_by: Collection[ColumnArg | Statement] | None = None,
    ) -> None:
        super().__init__()
        self._column: Statement = Column(column) if isinstance(column, str) else column
        self._over = OverClause(partition_by=partition_by)

    def __str__(self) -> str:
        return f"MEDIAN({operand(self._column)}) {self._over!s}"

    @property
    def args(self) -> list[Any]:
        return [*self._column.args, *self._over.args]


class PercentileFunction(Expression):
    """
    Base class for MariaDB's ``WITHIN GROUP`` window functions -- `PercentileCont` and `PercentileDisc`.

    ``<FUNCTION>(fraction) WITHIN GROUP (ORDER BY expr) OVER ([PARTITION BY partition_expression])``. Unlike
    every other function in this module, ``OVER`` is not attached with `WindowableFunction.over()`: MariaDB's
    grammar interposes ``WITHIN GROUP (...)`` between the function call and ``OVER``, so there is no position for
    a fluent `.over()` call to render into. ``OVER`` is mandatory (verified: omitting it is a syntax error on
    MariaDB 11.4) and, like `Median`, takes only ``PARTITION BY`` -- the ordering lives in ``WITHIN GROUP``
    instead (verified: an ``ORDER BY`` inside this ``OVER (...)`` is also a syntax error).

    ``fraction`` is rendered as an ordinary bound placeholder, like any other value in this library. This works
    with drivers that interpolate parameters client-side (pymysql, aiomysql, ...), but MariaDB's own server-side
    prepared statements reject a bound parameter here (verified on MariaDB 11.4: ``PREPARE ... FROM 'SELECT
    PERCENTILE_CONT(?) ...'`` fails with error 4104, "only accepts arguments that can be converted to numerical
    types") -- the same limitation `~sqlfactory.func.agg.GroupConcat`'s ``separator`` documents.

    PostgreSQL implements ``percentile_cont``/``percentile_disc`` as ordered-set *aggregates*: ``WITHIN GROUP``
    is used with plain ``GROUP BY``, and attaching ``OVER (...)`` to them is rejected (verified on PostgreSQL 17:
    "OVER is not supported for ordered-set aggregate"). These classes target MariaDB's window-function form and
    do not render valid SQL for that PostgreSQL usage.

    ``WITHIN GROUP (ORDER BY ...)`` takes exactly **one** sort key, unlike a regular ``ORDER BY`` -- MariaDB
    rejects a second one with a syntax error (verified on MariaDB 11.4: ``ERROR 1064`` for ``WITHIN GROUP
    (ORDER BY a, b)``), and PostgreSQL rejects it too (verified on PostgreSQL 17: it looks for an overload of
    the aggregate taking two ordering columns and finds none). So ``order`` takes a single ``(column,
    Direction)`` tuple, not the `OrderArg` collection accepted by a real ``ORDER BY`` elsewhere in this library
    -- passing more than one key is a ``mypy`` error, not just a runtime one. A runtime check still guards
    against a shape that slips past an untyped caller (e.g. the old, now-invalid ``[(column, Direction), ...]``
    list this used to accept).
    """

    #: SQL function name, set by each subclass.
    _function: ClassVar[str]

    def __init__(
        self,
        fraction: float,
        *,
        order: tuple[OrderColumn, Direction],
        partition_by: Collection[ColumnArg | Statement] | None = None,
    ) -> None:
        super().__init__()

        if not (isinstance(order, tuple) and len(order) == 2 and isinstance(order[1], Direction)):
            raise ValueError(
                f"{self._function}'s WITHIN GROUP (ORDER BY ...) takes exactly one sort key -- MariaDB and "
                "PostgreSQL both reject more than one. Pass a single (column, Direction) tuple, not a list of "
                f"them. Got: {order!r}."
            )

        self._fraction = fraction
        self._order: Order = Order([order])
        self._over = OverClause(partition_by=partition_by)

    def __str__(self) -> str:
        return f"{self._function}({self.dialect.placeholder}) WITHIN GROUP ({self._order!s}) {self._over!s}"

    @property
    def args(self) -> list[Any]:
        return [self._fraction, *self._order.args, *self._over.args]


class PercentileCont(PercentileFunction):
    """
    ``PERCENTILE_CONT(fraction) WITHIN GROUP (ORDER BY expr) OVER ([PARTITION BY partition_expression])``

    Continuous percentile: interpolates between adjacent rows when ``fraction`` falls between them. MariaDB
    10.3.3+ (https://mariadb.com/kb/en/percentile_cont/). See `PercentileFunction` for the shared ``WITHIN
    GROUP``/``OVER`` rendering and its dialect notes.

    Usage:

    >>> PercentileCont(0.5, order=("star_rating", Direction.ASC), partition_by=["name"])
    >>> "PERCENTILE_CONT(%s) WITHIN GROUP (ORDER BY `star_rating` ASC) OVER (PARTITION BY `name`)"
    """

    _function = "PERCENTILE_CONT"


class PercentileDisc(PercentileFunction):
    """
    ``PERCENTILE_DISC(fraction) WITHIN GROUP (ORDER BY expr) OVER ([PARTITION BY partition_expression])``

    Discrete percentile: returns the first value whose ``CUME_DIST()`` is at least ``fraction`` -- always an
    actual value from the data, unlike `PercentileCont`. MariaDB 10.3.3+
    (https://mariadb.com/kb/en/percentile_disc/). See `PercentileFunction` for the shared ``WITHIN
    GROUP``/``OVER`` rendering and its dialect notes.

    Usage:

    >>> PercentileDisc(0.5, order=("star_rating", Direction.ASC), partition_by=["name"])
    >>> "PERCENTILE_DISC(%s) WITHIN GROUP (ORDER BY `star_rating` ASC) OVER (PARTITION BY `name`)"
    """

    _function = "PERCENTILE_DISC"
