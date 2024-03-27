from typing import Any

from sqlbuilder.column import ColumnArg, Column
from sqlbuilder.statement import StatementWithArgs, Statement


class Aliased(StatementWithArgs):
    def __init__(self, statement: Statement | ColumnArg, alias: str = None):
        super().__init__()
        self.statement = statement if isinstance(statement, Statement) else Column(statement)
        self.alias = alias

    def __str__(self):
        if self.alias is None:
            return str(self.statement)

        return f"{str(self.statement)} AS `{self.alias}`"

    @property
    def args(self) -> list[Any]:
        return self.statement.args if isinstance(self.statement, StatementWithArgs) else []

    def __getattr__(self, name):
        return getattr(self.statement, name)


class SelectColumn(Aliased):
    def __init__(self, column: ColumnArg, alias: str = None):
        super().__init__(column, alias)
