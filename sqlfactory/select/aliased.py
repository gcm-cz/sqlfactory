"""Column / Statement aliasing support"""

from typing import Any

from sqlfactory.entities import ColumnArg, Column
from sqlfactory.statement import StatementWithArgs, Statement


# pylint: disable=too-few-public-methods
class Aliased(StatementWithArgs):
    """Aliased generic statement. Only to be used in SELECT statement, where AS statement is only valid."""
    def __init__(self, statement: Statement | ColumnArg, alias: str = None):
        super().__init__()
        self._statement = statement if isinstance(statement, Statement) else Column(statement)
        self.alias = alias

    def __str__(self):
        if self.alias is None:
            return str(self._statement)

        return f"{str(self._statement)} AS `{self.alias}`"

    @property
    def args(self) -> list[Any]:
        return self._statement.args if isinstance(self._statement, StatementWithArgs) else []

    def __getattr__(self, name):
        """Proxy to access attributes of inner (non-aliased) statement."""
        return getattr(self._statement, name)


class SelectColumn(Aliased):
    """Aliased column"""
    def __init__(self, column: ColumnArg, alias: str = None):
        super().__init__(column, alias)
