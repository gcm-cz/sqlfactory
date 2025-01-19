"""WHERE mixin for query generator."""

from __future__ import annotations

from typing import Any, Generic, Self, TypeVar

from ..condition.base import ConditionBase

T = TypeVar("T")


class WithWhere(Generic[T]):
    """Mixin to provide WHERE support for query generator."""

    def __init__(self, *args: Any, where: ConditionBase | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._where = where

    def where(self, condition: ConditionBase) -> Self:
        """Set WHERE condition for query."""
        if self._where is not None:
            raise AttributeError("Where has already been specified.")

        self._where = condition
        return self

    # pylint: disable=invalid-name
    def WHERE(self, condition: ConditionBase) -> Self:
        """Alias for where() to be more SQL-like with all capitals."""
        return self.where(condition)
