"""JOIN statements for SQL queries."""

from typing import Any

from sqlfactory.entities import Table
from sqlfactory.condition.base import ConditionBase
from sqlfactory.statement import StatementWithArgs


class Join(StatementWithArgs):
    """JOIN statement"""
    def __init__(self, table: str | Table, on: ConditionBase = None, alias: str = None):
        if isinstance(table, str):
            table = Table(table)

        self.table = table
        self.on = on
        self.alias = alias

    @property
    def join_spec(self) -> str:
        """
        Returns the JOIN type itself for generation of SQL query.
        """
        return "JOIN"

    def __str__(self):
        if self.alias:
            table = f"{str(self.table)} AS `{self.alias}`"
        else:
            table = str(self.table)

        if self.on:
            return f"{self.join_spec} {table} ON {str(self.on)}"

        return f"{self.join_spec} {table}"

    @property
    def args(self) -> list[Any]:
        return self.on.args if self.on else []


class LeftJoin(Join):
    """LEFT JOIN statement"""

    @property
    def join_spec(self) -> str:
        return "LEFT JOIN"


class LeftOuterJoin(Join):
    """LEFT OUTER JOIN statement"""

    @property
    def join_spec(self) -> str:
        return "LEFT OUTER JOIN"


class RightJoin(Join):
    """RIGHT JOIN statement"""
    @property
    def join_spec(self) -> str:
        return "RIGHT JOIN"


class RightOuterJoin(Join):
    """RIGHT OUTER JOIN statement"""
    @property
    def join_spec(self) -> str:
        return "RIGHT OUTER JOIN"


class InnerJoin(Join):
    """INNER JOIN statement"""
    @property
    def join_spec(self) -> str:
        return "INNER JOIN"


class CrossJoin(Join):
    """CROSS JOIN statement"""
    @property
    def join_spec(self) -> str:
        return "CROSS JOIN"
