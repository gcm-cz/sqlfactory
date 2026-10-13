"""IS [NOT] NULL predicate."""

from __future__ import annotations

from typing import Any, NoReturn

from sqlfactory.condition.base import ConditionBase, StatementOrColumn
from sqlfactory.entities import Column
from sqlfactory.statement import Statement, operand


class IsNull(ConditionBase):
    """
    ``<expr> IS NULL`` - tests whether a column (or other expression) is NULL. Negate with ``negative=True`` or the dedicated
    `IsNotNull` class.

    Prefer this over ``Eq(column, None)``: `Eq` / `Ne` with ``None`` render ``IS %s`` / ``IS NOT %s`` and bind ``None`` as an
    argument, which only becomes ``IS NULL`` when the driver substitutes placeholders on the client side. `IsNull` always
    renders a literal ``IS NULL`` with no argument, and states the intent explicitly.

    Usage:

    >>> from sqlfactory import IsNull
    >>> IsNull("t.deleted_at")
    >>> "`t`.`deleted_at` IS NULL"
    """

    def __init__(self, expr: StatementOrColumn, *, negative: bool = False) -> None:
        """
        :param expr: Column (or other Statement) to test. A bare string is treated as a column name - wrap it in
            ``Value(...)`` to test a literal instead.
        :param negative: Whether to perform negative comparison (``IS NOT NULL``).
        """
        super().__init__()

        if not isinstance(expr, Statement):
            expr = Column(expr)

        self._expr = expr
        self._negative = negative

    def __str__(self) -> str:
        return f"{operand(self._expr)} IS {'NOT ' if self._negative else ''}NULL"

    @property
    def args(self) -> list[Any]:
        return list(self._expr.args)

    def __bool__(self) -> bool:
        return True

    def __invert__(self) -> IsNull:
        """
        Allows using the `~` operator to negate the IS NULL condition, converting it to an IS NOT NULL condition.
        Note: Cannot use ~ operator on IsNotNull conditions.
        """
        if self._negative:
            return IsNull(self._expr)

        return IsNotNull(self._expr)


class IsNotNull(IsNull):
    """
    ``<expr> IS NOT NULL`` - dedicated class for ``IS NOT NULL``, equivalent to using `IsNull` with ``negative=True``.
    Prefer it over ``Ne(column, None)`` for the same reasons as `IsNull`.

    Usage:

    >>> from sqlfactory import IsNotNull
    >>> IsNotNull("t.deleted_at")
    >>> "`t`.`deleted_at` IS NOT NULL"
    """

    def __init__(self, expr: StatementOrColumn) -> None:
        """
        :param expr: Column (or other Statement) to test. A bare string is treated as a column name - wrap it in
            ``Value(...)`` to test a literal instead.
        """
        super().__init__(expr, negative=True)

    def __invert__(self) -> NoReturn:
        """
        The `~` operator is not supported on IsNotNull conditions (same as on the other dedicated `Not*` conditions),
        use `IsNull` directly.
        """
        raise TypeError("Cannot use ~ operator on IsNotNull conditions")
