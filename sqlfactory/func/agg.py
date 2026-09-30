"""Aggregate functions."""

from collections.abc import Collection
from typing import Any, ClassVar, Literal

from sqlfactory.entities import Column, ColumnArg
from sqlfactory.func.base import Function
from sqlfactory.func.window import Frame, OverClause, WindowableFunction, WindowFunction
from sqlfactory.mixins.limit import Limit
from sqlfactory.mixins.order import Order, OrderArg
from sqlfactory.statement import Statement, operand


class AggregateFunction(WindowableFunction):
    """Base class for aggregate functions"""

    def __init__(self, agg: str, column: ColumnArg | Statement, *columns: ColumnArg | Statement):
        super().__init__(agg, *(Column(c) if isinstance(c, str) else c for c in (column, *columns)))


class DistinctAggregateFunction(AggregateFunction):
    """
    Base class for the aggregate functions MariaDB accepts ``DISTINCT`` for - ``<agg>([DISTINCT] <column>, ...)``.

    Only those aggregates derive from it, so passing ``distinct=`` to any other one is a type error rather than
    invalid SQL.
    """

    #: Whether MariaDB accepts ``<agg>(DISTINCT ...) OVER (...)``. It rejects it (error 1235) for ``AVG``, ``COUNT``
    #: and ``SUM``; ``MIN`` and ``MAX`` (where ``DISTINCT`` makes no difference to the result) and ``ST_COLLECT``
    #: allow it.
    _distinct_over: ClassVar[bool] = False

    def __init__(self, agg: str, column: ColumnArg | Statement, *columns: ColumnArg | Statement, distinct: bool = False):
        super().__init__(agg, column, *columns)
        self._distinct = distinct

    def _args_placeholders(self) -> list[str]:
        # DISTINCT is rendered lazily (here, not at construction time) so that it picks up whichever SQL dialect
        # is active when `str()` is finally called - the column argument's own placeholder/quoting must not be
        # frozen early using whatever dialect happened to be active at `__init__()` time.
        placeholders = super()._args_placeholders()
        if self._distinct:
            placeholders[0] = f"DISTINCT {placeholders[0]}"
        return placeholders

    def over(
        self,
        over: OverClause | None = None,
        *,
        partition_by: Collection[ColumnArg | Statement] | None = None,
        order: OrderArg | None = None,
        frame: Frame | None = None,
    ) -> WindowFunction:
        if self._distinct and not self._distinct_over:
            raise ValueError(
                f"{self.function}(DISTINCT ...) cannot be used as a window function -- MariaDB error 1235 "
                "(ER_NOT_SUPPORTED_YET: this version of MariaDB doesn't yet support "
                f"'{self.function}(DISTINCT) aggregate as window function'). Omit `distinct=True`, or aggregate "
                "with GROUP BY instead of OVER (...)."
            )
        return super().over(over, partition_by=partition_by, order=order, frame=frame)


class Avg(DistinctAggregateFunction):
    """
    ``AVG([DISTINCT] <column>)``

    :param distinct: Renders as ``AVG(DISTINCT <column>)``. MariaDB does not allow ``AVG(DISTINCT ...)`` to be
        used as a window function - calling `.over()` on such an instance raises `ValueError`.
    """

    def __init__(self, column: ColumnArg | Statement, *, distinct: bool = False):
        super().__init__("AVG", column, distinct=distinct)


class BitAnd(AggregateFunction):
    """BIT_AND(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("BIT_AND", column)


class BitOr(AggregateFunction):
    """BIT_OR(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("BIT_OR", column)


class BitXor(AggregateFunction):
    """BIT_XOR(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("BIT_XOR", column)


class Count(DistinctAggregateFunction):
    """
    - ``COUNT(<column>)``
    - ``COUNT(DISTINCT <column>)``
    - ``COUNT(DISTINCT <column>, <column>, ...)`` - MariaDB's multiple-expression "COUNT DISTINCT" form.

    ``distinct`` is required whenever more than one expression is given: bare ``COUNT(a, b)`` is not valid SQL,
    only ``COUNT(DISTINCT a, b)`` is - passing more than one column without ``distinct=True`` raises `ValueError`.

    ``COUNT(DISTINCT *)`` is also not valid SQL (MariaDB rejects ``*`` combined with ``DISTINCT`` or with any
    other expression) - passing ``"*"`` together with ``distinct=True`` or extra columns raises `ValueError`.

    :param distinct: MariaDB does not allow ``COUNT(DISTINCT ...)`` to be used as a window function - calling
        `.over()` on such an instance raises `ValueError`.
    """

    def __init__(self, column: ColumnArg | Literal["*"], *columns: ColumnArg | Statement, distinct: bool = False):
        if columns and not distinct:
            raise ValueError("COUNT() with more than one expression requires distinct=True (bare COUNT(a, b) is invalid SQL).")

        if isinstance(column, str) and column == "*" and (distinct or columns):
            raise ValueError(
                "COUNT(DISTINCT *) is not valid SQL -- MariaDB rejects '*' combined with DISTINCT or with any other expression."
            )

        super().__init__("COUNT", column, *columns, distinct=distinct)


class GroupConcat(Function):
    """
    ``GROUP_CONCAT([DISTINCT] expr [, expr ...] [ORDER BY {col_name | expr} [ASC|DESC] [, ...]] [SEPARATOR str]``
    ``[LIMIT [offset,] row_count])``

    Concatenates the non-NULL values from a group into a single string.

    Cannot be used as a window function — MariaDB does not support ``GROUP_CONCAT() OVER (...)``, so this class
    subclasses :class:`~sqlfactory.func.base.Function` directly instead of :class:`AggregateFunction`.

    The ``LIMIT`` clause requires MariaDB 10.3.3+ (`MDEV-11297
    <https://jira.mariadb.org/browse/MDEV-11297>`_ - confirmed in the 10.3.3 changelog).

    The ``separator`` argument accepts either a plain ``str`` or a `Statement` (e.g. `Raw`):

    - A plain ``str`` is rendered as an ordinary bound placeholder (``self.dialect.placeholder``), the same as any
      other value in this library, and its value is added to ``.args``. This works with drivers that interpolate
      parameters client-side — ``pymysql``, ``aiomysql``, ``mysqlclient``, and ``mysql-connector-python``'s
      default cursor — because they build the final SQL text by substituting each placeholder with an escaped,
      quoted literal via Python string formatting *before* sending the query to the server. It does **not** work
      with a genuine server-side prepared statement: MariaDB's own grammar requires a string literal after
      ``SEPARATOR`` and rejects a bound parameter there (verified on MariaDB 11.4: ``PREPARE s FROM 'SELECT
      GROUP_CONCAT(1 SEPARATOR ?)'`` fails with ``ER_PARSE_ERROR`` (1064)).
    - A `Statement` (e.g. ``separator=Raw("', '")``) is rendered as SQL verbatim, exactly like any other
      `Statement` argument elsewhere in this library. Use this as the escape hatch when the separator must reach
      the server as a real literal token rather than a driver-interpolated placeholder. This library does not add
      its own SQL string-literal escaper — if you build the `Raw` content from untrusted input, escape it
      yourself.

    Usage:

    >>> GroupConcat("name", separator=", ")
    >>> "GROUP_CONCAT(`name` SEPARATOR %s)"

    >>> GroupConcat("name", distinct=True, order=[("name", Direction.ASC)], limit=Limit(10))
    >>> "GROUP_CONCAT(DISTINCT `name` ORDER BY `name` ASC LIMIT %s)"
    """

    def __init__(
        self,
        column: ColumnArg | Statement,
        *columns: ColumnArg | Statement,
        distinct: bool = False,
        order: OrderArg | None = None,
        separator: str | Statement | None = None,
        limit: Limit | None = None,
    ) -> None:
        """
        :param column: First (or only) expression to concatenate.
        :param columns: Further expressions, concatenated onto ``column`` for each row (not to be confused with
            ``ORDER BY``, ``columns`` here mirrors ``GROUP_CONCAT(expr, expr, ...)``'s comma-separated expr list).
        :param distinct: Eliminate duplicate values before concatenating (``GROUP_CONCAT(DISTINCT ...)``).
        :param order: Ordering of the values within the group, applied before concatenation. Independent of the
            surrounding query's own ``ORDER BY``. Same `Order`/`OrderArg` type as accepted by `Select`.
        :param separator: Separator placed between concatenated values. When omitted, MariaDB uses its own
            default (a comma). Accepts a plain ``str`` (bound as a placeholder) or a `Statement` (rendered as SQL
            verbatim) — see the class docstring for when each is appropriate.
        :param limit: Restricts the number of concatenated values. Accepts a `Limit` instance. Requires MariaDB
            10.3.3+.
        """
        super().__init__("GROUP_CONCAT")

        self._columns: list[Statement] = [Column(c) if isinstance(c, str) else c for c in (column, *columns)]
        self._distinct = distinct
        self._order: Order | None = order if isinstance(order, Order) else (Order(order) if order else None)
        self._separator = separator
        self._limit = limit

    def __str__(self) -> str:
        expr = ", ".join(operand(c) for c in self._columns)
        if self._distinct:
            expr = f"DISTINCT {expr}"

        clauses = [expr]

        if self._order:
            clauses.append(str(self._order))

        if self._separator is not None:
            sep = str(self._separator) if isinstance(self._separator, Statement) else self.dialect.placeholder
            clauses.append(f"SEPARATOR {sep}")

        if self._limit:
            clauses.append(str(self._limit))

        return f"GROUP_CONCAT({' '.join(clauses)})"

    @property
    def args(self) -> list[Any]:
        out: list[Any] = []

        for column_stmt in self._columns:
            out.extend(column_stmt.args)

        if self._order:
            out.extend(self._order.args)

        if self._separator is not None:
            if isinstance(self._separator, Statement):
                out.extend(self._separator.args)
            else:
                out.append(self._separator)

        if self._limit:
            out.extend(self._limit.args)

        return out


class JsonArrayAgg(Function):
    """
    ``JSON_ARRAYAGG([DISTINCT] expr [ORDER BY {col_name | expr} [ASC|DESC] [, ...]] [LIMIT [offset,] row_count])``

    Aggregates values from a group into a JSON array.

    MariaDB 10.5+. Cannot be used as a window function, so this class subclasses
    :class:`~sqlfactory.func.base.Function` directly instead of :class:`AggregateFunction`.

    Usage:

    >>> JsonArrayAgg("name", distinct=True, order=[("name", Direction.ASC)])
    >>> "JSON_ARRAYAGG(DISTINCT `name` ORDER BY `name` ASC)"
    """

    def __init__(
        self,
        column: ColumnArg | Statement,
        *,
        distinct: bool = False,
        order: OrderArg | None = None,
        limit: Limit | None = None,
    ) -> None:
        """
        :param column: Expression to aggregate into the JSON array.
        :param distinct: Eliminate duplicate values before aggregating (``JSON_ARRAYAGG(DISTINCT ...)``).
        :param order: Ordering of the values within the group, applied before aggregation. Same `Order`/`OrderArg`
            type as accepted by `Select`.
        :param limit: Restricts the number of aggregated values. Accepts a `Limit` instance.
        """
        super().__init__("JSON_ARRAYAGG")

        self._column: Statement = Column(column) if isinstance(column, str) else column
        self._distinct = distinct
        self._order: Order | None = order if isinstance(order, Order) else (Order(order) if order else None)
        self._limit = limit

    def __str__(self) -> str:
        expr = operand(self._column)
        if self._distinct:
            expr = f"DISTINCT {expr}"

        clauses = [expr]

        if self._order:
            clauses.append(str(self._order))

        if self._limit:
            clauses.append(str(self._limit))

        return f"JSON_ARRAYAGG({' '.join(clauses)})"

    @property
    def args(self) -> list[Any]:
        out: list[Any] = list(self._column.args)

        if self._order:
            out.extend(self._order.args)

        if self._limit:
            out.extend(self._limit.args)

        return out


class JsonObjectAgg(Function):
    """
    ``JSON_OBJECTAGG(key, value)``

    Aggregates key/value pairs from a group into a single JSON object.

    MariaDB 10.5+. Does not support ``DISTINCT`` or ``ORDER BY``, and cannot be used as a window function, so this
    class subclasses :class:`~sqlfactory.func.base.Function` directly instead of :class:`AggregateFunction`.
    """

    def __init__(self, key: ColumnArg | Statement, value: ColumnArg | Statement) -> None:
        key_stmt: Statement = Column(key) if isinstance(key, str) else key
        value_stmt: Statement = Column(value) if isinstance(value, str) else value
        super().__init__("JSON_OBJECTAGG", key_stmt, value_stmt)


class Max(DistinctAggregateFunction):
    """MAX([DISTINCT] <column>)"""

    _distinct_over = True

    def __init__(self, column: ColumnArg | Statement, *, distinct: bool = False):
        super().__init__("MAX", column, distinct=distinct)


class Min(DistinctAggregateFunction):
    """MIN([DISTINCT] <column>)"""

    _distinct_over = True

    def __init__(self, column: ColumnArg | Statement, *, distinct: bool = False):
        super().__init__("MIN", column, distinct=distinct)


class Std(AggregateFunction):
    """STD(<column>)"""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("STD", column)


class Stddev(Std):
    """``STDDEV(<column>)`` — synonym for ``STD()`` / ``STDDEV_POP()``."""

    def __init__(self, column: ColumnArg | Statement) -> None:
        super().__init__(column)
        self.function = "STDDEV"


class StddevPop(AggregateFunction):
    """``STDDEV_POP(<column>)`` — population standard deviation (the square root of ``VAR_POP()``). Equivalent to
    ``STD()``. Usable as a window function."""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("STDDEV_POP", column)


class StddevSamp(AggregateFunction):
    """``STDDEV_SAMP(<column>)`` — sample standard deviation (the square root of ``VAR_SAMP()``). Usable as a
    window function."""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("STDDEV_SAMP", column)


class Sum(DistinctAggregateFunction):
    """
    ``SUM([DISTINCT] <column>)``

    :param distinct: Renders as ``SUM(DISTINCT <column>)``. MariaDB does not allow ``SUM(DISTINCT ...)`` to be
        used as a window function - calling `.over()` on such an instance raises `ValueError`.
    """

    def __init__(self, column: ColumnArg | Statement, *, distinct: bool = False):
        super().__init__("SUM", column, distinct=distinct)


class VarPop(AggregateFunction):
    """``VAR_POP(<column>)`` — population variance (rows treated as the whole population). Usable as a window
    function."""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("VAR_POP", column)


class VarSamp(AggregateFunction):
    """``VAR_SAMP(<column>)`` — sample variance (rows treated as a sample of the population). Usable as a window
    function."""

    def __init__(self, column: ColumnArg | Statement):
        super().__init__("VAR_SAMP", column)


class Variance(VarPop):
    """``VARIANCE(<column>)`` — synonym for ``VAR_POP()``."""

    def __init__(self, column: ColumnArg | Statement) -> None:
        super().__init__(column)
        self.function = "VARIANCE"
