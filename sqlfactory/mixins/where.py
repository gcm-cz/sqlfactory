"""WHERE mixin for query generator."""

from typing import Generic, TypeVar

from ..condition.base import ConditionBase

T = TypeVar("T")


class WithWhere(Generic[T]):
    """Mixin to provide WHERE support for query generator."""
    def __init__(self, *args, where: ConditionBase = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._where = where

    def where(self, condition: ConditionBase) -> T:
        """Set WHERE condition for query."""
        if self._where is not None:
            raise AttributeError("Where has already been specified.")

        self._where = condition
        return self

    # pylint: disable=invalid-name
    def WHERE(self, condition: ConditionBase) -> T:
        """Alias for where() to be more SQL-like with all capitals."""
        return self.where(condition)
