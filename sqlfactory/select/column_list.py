"""Column list for usage in SELECT statement."""

from __future__ import annotations

from typing import Any, Iterable, Self

from sqlfactory.entities import Column, ColumnArg
from sqlfactory.statement import Statement


class ColumnList(Statement, list[Statement]):  # type: ignore[misc]
    """
    Unique(ish) set of columns to be used in SELECT statement.
    """

    def __init__(self, iterable: Iterable[Statement | ColumnArg] | None = None) -> None:
        if iterable:
            super().__init__([Column(i) if not isinstance(i, Statement) else i for i in iterable])
        else:
            super().__init__()

    def __contains__(self, other: Statement) -> bool:  # type: ignore[override]
        """This needs custom implementation over default list.__contains__ because we need to compare Expression
        objects, which would generate Eq() instances instead of doing comparison."""
        if not isinstance(other, Statement):
            raise AttributeError("ColumnList can only contain Statement objects.")

        for item in self:
            if str(item) == str(other) and item.args == other.args:
                return True

        return False

    def add(self, element: Statement | str) -> Self:
        """Add new columns to the set."""
        return self.append(element)

    def append(self, element: Statement | str) -> Self:  # type: ignore[override]
        """Add new columns to the set."""
        if not isinstance(element, Statement):
            element = Column(element)

        if element not in self:
            super().append(element)

        return self

    def update(self, iterable: Iterable[Statement | str]) -> Self:
        """Add multiple new columns to the set."""
        for item in iterable:
            self.add(item)

        return self

    def __str__(self) -> str:
        return ", ".join(map(str, self))

    def __repr__(self) -> str:
        return "[" + ", ".join(map(repr, self)) + "]"

    @property
    def args(self) -> list[Any]:
        """Argument values of the column list statement."""
        out = []

        for item in self:
            if isinstance(item, Statement):
                out.extend(item.args)

        return out
