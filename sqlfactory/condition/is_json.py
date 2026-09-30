"""IS JSON predicate, used for checking whether an expression is (or is not) valid JSON."""

from __future__ import annotations

from enum import Enum
from typing import Any, NoReturn

from sqlfactory.condition.base import ConditionBase, StatementOrColumn
from sqlfactory.entities import Column
from sqlfactory.statement import Statement


class JsonValueType(str, Enum):
    """Value-type constraint for the :class:`IsJson` / ``IS JSON`` predicate."""

    VALUE = "VALUE"
    ARRAY = "ARRAY"
    OBJECT = "OBJECT"
    SCALAR = "SCALAR"


class IsJson(ConditionBase):
    """
    ``<expr> IS [NOT] JSON [VALUE|ARRAY|OBJECT|SCALAR] [[WITH|WITHOUT] UNIQUE KEYS]`` — the ``IS JSON`` comparison
    operator, testing whether ``expr`` is (or, negated, is not) valid JSON — optionally constrained to a JSON value
    type, and/or to having (or not having) unique object keys. MariaDB 12.3+ (MDEV-37072).

    Negate with ``negative=True`` or the dedicated :class:`IsNotJson` class.

    Usage:

    >>> from sqlfactory.condition.is_json import IsJson, JsonValueType
    >>> IsJson("doc")
    >>> "`doc` IS JSON"

    >>> IsJson("doc", JsonValueType.OBJECT, unique=True)
    >>> "`doc` IS JSON OBJECT WITH UNIQUE KEYS"
    """

    def __init__(
        self,
        expr: StatementOrColumn,
        value_type: JsonValueType | None = None,
        *,
        unique: bool | None = None,
        negative: bool = False,
    ) -> None:
        """
        :param expr: Column (or other Statement) to test. A bare string is treated as a column name — wrap it in
            ``Value(...)`` to test a literal instead.
        :param value_type: Restrict to this JSON value type (``VALUE``, ``ARRAY``, ``OBJECT`` or ``SCALAR``), if given.
        :param unique: ``True`` for ``WITH UNIQUE KEYS``, ``False`` for ``WITHOUT UNIQUE KEYS``, ``None`` to omit.
        :param negative: Whether to perform negative comparison (``IS NOT JSON``).
        """
        super().__init__()

        if not isinstance(expr, Statement):
            expr = Column(expr)

        self._expr = expr
        self._value_type = value_type
        self._unique = unique
        self._negative = negative

    def __str__(self) -> str:
        parts = [str(self._expr), "IS"]

        if self._negative:
            parts.append("NOT")

        parts.append("JSON")

        if self._value_type is not None:
            parts.append(self._value_type.value)

        if self._unique is not None:
            parts.append("WITH" if self._unique else "WITHOUT")
            parts.append("UNIQUE KEYS")

        return " ".join(parts)

    @property
    def args(self) -> list[Any]:
        return list(self._expr.args)

    def __bool__(self) -> bool:
        return True

    def __invert__(self) -> "IsJson":
        """
        Allows using the `~` operator to negate the IS JSON condition, converting it to an IS NOT JSON condition.
        Note: Cannot use ~ operator on IsNotJson conditions.
        """
        return IsNotJson(self._expr, self._value_type, unique=self._unique)


class IsNotJson(IsJson):
    """
    ``<expr> IS NOT JSON [...]`` — dedicated class for ``IS NOT JSON``, equivalent to using :class:`IsJson` with
    ``negative=True``. MariaDB 12.3+ (MDEV-37072).
    """

    def __init__(self, expr: StatementOrColumn, value_type: JsonValueType | None = None, *, unique: bool | None = None) -> None:
        """
        :param expr: Column (or other Statement) to test. A bare string is treated as a column name — wrap it in
            ``Value(...)`` to test a literal instead.
        :param value_type: Restrict to this JSON value type (``VALUE``, ``ARRAY``, ``OBJECT`` or ``SCALAR``), if given.
        :param unique: ``True`` for ``WITH UNIQUE KEYS``, ``False`` for ``WITHOUT UNIQUE KEYS``, ``None`` to omit.
        """
        super().__init__(expr, value_type, unique=unique, negative=True)

    def __invert__(self) -> NoReturn:
        """
        Allows using the `~` operator to negate the IS NOT JSON condition, converting it to an IS JSON condition.
        Note: Cannot use ~ operator on IsNotJson conditions.
        """
        raise TypeError("Cannot use ~ operator on IsNotJson conditions")
