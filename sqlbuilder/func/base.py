"""Base classes for SQL functions"""

from typing import Any

from ..statement import StatementWithArgs, Statement


class Function(StatementWithArgs):
    """Generic function with name and variable number of arguments."""
    def __init__(self, function: str, *args: Statement | Any):
        self.function = function
        self._args = args

    def _args_placeholders(self) -> list[str]:
        out: list[str] = []

        for arg in self._args:
            if isinstance(arg, Statement):
                out.append(str(arg))
            else:
                out.append("%s")

        return out

    def __str__(self):
        return f"{self.function}({', '.join(self._args_placeholders())})"

    @property
    def args(self) -> list[Any]:
        out = []
        for arg in self._args:
            if isinstance(arg, StatementWithArgs):
                out.extend(arg.args)
            elif not isinstance(arg, Statement):
                out.append(arg)

        return out
