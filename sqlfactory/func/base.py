"""Base classes for SQL functions"""

from typing import Any

from sqlfactory.entities import Expression
from sqlfactory.statement import Statement, ValueArg, operand


class Function(Expression):
    """
    Generic function with name and variable number of arguments.

    **Bare `str` rule:** arguments of scalar functions are values - a bare `str` is bound as a placeholder argument, it is
    *not* a column name: `Lower("x")` renders `LOWER(%s)` with args `["x"]`. Wrap column names in `Column(...)`:
    ``Lower(Column("t.x"))`` renders ``LOWER(`t`.`x`)``. (This is the opposite of conditions, whose first argument is a
    column.) Exceptions that take a column name as `str` are typed as `sqlfactory.entities.ColumnArg` - notably the
    aggregate and window functions (`Count("id")` renders ``COUNT(`id`)``).

    Custom function: `Function("SOUNDEX", Column("name"))` renders ``SOUNDEX(`name`)``.
    """

    def __init__(self, function: str, *args: ValueArg) -> None:
        super().__init__()

        self.function = function
        self._args = args

    def _args_placeholders(self) -> list[str]:
        out: list[str] = []

        for arg in self._args:
            if isinstance(arg, Statement):
                out.append(operand(arg))
            else:
                out.append(self.dialect.placeholder)

        return out

    def __str__(self) -> str:
        return f"{self.function}({', '.join(self._args_placeholders())})"

    @property
    def args(self) -> list[Any]:
        out = []
        for arg in self._args:
            if isinstance(arg, Statement):
                out.extend(arg.args)
            elif not isinstance(arg, Statement):
                out.append(arg)

        return out
