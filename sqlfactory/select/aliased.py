"""Column / Statement aliasing support"""

from typing import Any

from sqlfactory.entities import Column, ColumnArg
from sqlfactory.statement import Statement


class Aliased(Statement):
    """Aliased generic statement. Only to be used in SELECT statement, where AS statement is only valid."""

    def __init__(self, statement: Statement | ColumnArg, alias: str | None = None) -> None:
        super().__init__()
        self._statement = statement if isinstance(statement, Statement) else Column(statement)
        self.alias = alias

    def __str__(self) -> str:
        if self.alias is None:
            return str(self._statement)

        return f"{self._statement!s} AS `{self.alias}`"

    @property
    def args(self) -> list[Any]:
        """Argument values of the aliased statement"""
        return self._statement.args

    def __getattr__(self, name: str) -> Any:
        """Proxy to access attributes of inner (non-aliased) statement."""
        return getattr(self._statement, name)


class SelectColumn(Aliased):
    """Aliased column"""

    def __init__(self, column: ColumnArg, alias: str | None = None, distinct: bool = False):
        """
        :param column: Column to be selected
        :param alias: Optional alias of the column
        :param distinct: Whether to select only distinct values (prepend DISTINCT to column name)
        """
        super().__init__(column, alias)
        self.distinct = distinct

    def __str__(self) -> str:
        if self.distinct:
            return f"DISTINCT {super().__str__()}"

        return super().__str__()
