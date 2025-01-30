"""WHERE mixin for query generator."""

from __future__ import annotations

from typing import Any, Generic, Self, TypeVar

from ..condition.base import ConditionBase

T = TypeVar("T")


class WithWhere(Generic[T]):
    """
    Mixin to provide `WHERE` support for query generator.

    Example:

    >>> Select(where=And(Equals("id", 1), Equals("status", "active")))

    >>> Update(where=And(Equals("id", 1), Equals("status", "active")))

    >>> Delete(where=And(Equals("id", 1), Equals("status", "active")))

    """

    def __init__(self, *args: Any, where: ConditionBase | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._where = where

    def where(self, condition: ConditionBase) -> Self:
        """
        Set `WHERE` condition for query. This cannot be chained, as the library does not take assumption of how to chain
        individual where conditions. Use one of `sqlfactory.And` or `sqlfactory.Or` compound classes to chain multiple conditions.

        Example:

        >>> sel = Select().where(And(Equals("id", 1), Equals("status", "active")))

        :param condition: Condition to be used in WHERE clause.
        """
        if self._where is not None:
            raise AttributeError("Where has already been specified.")

        self._where = condition
        return self

    # pylint: disable=invalid-name
    def WHERE(self, condition: ConditionBase) -> Self:
        """Alias for `WithWhere.where()` to be more SQL-like with all capitals."""
        return self.where(condition)
