"""LIKE statement"""

from typing import Any

from .base import Condition, StatementOrColumn
from ..entities import Column
from ..statement import Statement, StatementWithArgs


class Like(Condition):
    """
    SQL LIKE statement

    `column` LIKE %s
    `column` NOT LIKE %s
    <statement> LIKE %s
    <statement> NOT LIKE %s
    """
    def __init__(self, column: StatementOrColumn, value: Any | Statement, negative: bool = False):
        args = []

        if not isinstance(column, Statement):
            column = Column(column)

        if isinstance(column, StatementWithArgs):
            args.extend(column.args)

        if isinstance(value, StatementWithArgs):
            args.extend(value.args)
        else:
            args.append(value)

        if isinstance(value, Statement):
            super().__init__(
                f"{str(column)}{' NOT' if negative else ''} LIKE {str(value)}",
                *args,
            )
        else:
            super().__init__(
                f"{str(column)}{' NOT' if negative else ''} LIKE %s",
                *args
            )

    @staticmethod
    def escape(s: str) -> str:
        """
        Escape string for use in LIKE statement
        """
        return s.replace("%", "%%").replace("_", "__")
