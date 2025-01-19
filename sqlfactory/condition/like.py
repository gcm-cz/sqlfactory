"""LIKE statement"""

from typing import Any

from ..entities import Column
from ..statement import Statement
from .base import Condition, StatementOrColumn


class Like(Condition):
    """
    SQL LIKE statement

    `column` LIKE %s
    `column` NOT LIKE %s
    <statement> LIKE %s
    <statement> NOT LIKE %s
    """

    def __init__(self, column: StatementOrColumn, value: Any | Statement, negative: bool = False) -> None:
        args = []

        if not isinstance(column, Statement):
            column = Column(column)

        if isinstance(column, Statement):
            args.extend(column.args)

        if isinstance(value, Statement):
            args.extend(value.args)
        else:
            args.append(value)

        if isinstance(value, Statement):
            super().__init__(
                f"{column!s}{' NOT' if negative else ''} LIKE {value!s}",
                *args,
            )
        else:
            super().__init__(f"{column!s}{' NOT' if negative else ''} LIKE %s", *args)

    @staticmethod
    def escape(s: str) -> str:
        """
        Escape string for use in LIKE statement
        """
        return s.replace("%", "%%").replace("_", "__")
