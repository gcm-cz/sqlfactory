"""UPDATE statement builder."""

from __future__ import annotations

from typing import Any, Optional

from ..condition.base import ConditionBase
from ..entities import ColumnArg, Column, Table
from ..execute import ExecutableStatementWithArgs, ConditionalExecutableStatement
from ..mixins.limit import WithLimit, Limit
from ..mixins.where import WithWhere
from ..statement import StatementWithArgs, Statement


class UpdateColumn(StatementWithArgs):
    """
    Represents one field that should be updated.
    """
    def __init__(self, column: ColumnArg, value: Statement | Any):
        self._column = column if isinstance(column, Column) else Column(column)
        self._value = value

    def __str__(self):
        return f"{str(self._column)} = {str(self._value) if isinstance(self._value, Statement) else '%s'}"

    def __hash__(self):
        return hash(self._column)

    def __eq__(self, other: UpdateColumn):
        if not isinstance(other, UpdateColumn):
            return False

        return str(self._column) == str(other._column)

    @property
    def args(self) -> list[Any]:
        """
        Return arguments for the update statement.
        """
        if isinstance(self._value, StatementWithArgs):
            return self._value.args

        if not isinstance(self._value, Statement):
            return [self._value]

        return []


# pylint: disable=too-many-ancestors  # This is intentional, as this class is a combination of multiple mixins.
class Update(ExecutableStatementWithArgs, ConditionalExecutableStatement, WithWhere['Update'], WithLimit['Update']):
    """
    Builds UPDATE statement SQL query.

    This is conditional SQL statement, so you can check whether it should be executed (would update any columns)
    by calling bool() on it. Also, if you are using execute() method of the statement, the execution won't be
    performed if bool() returns False.

    >>> Update("table").set("column1", 1).where(Eq("column2", 2))

    >>> t = Table("table")
    >>> Update(t).set(t.column1, 1).where(t.column2 == 2)
    """
    def __init__(
            self,
            table: Table | str,
            *fields: UpdateColumn,
            where: Optional[ConditionBase] = None,
            limit: Optional[Limit] = None
    ):
        """
        :param table: Table to update.
        :param fields: List of UpdateColumn instances containing columns to be updated. This is not very pleasant way
            to create the statement, use set() method instead.
        :param where: WHERE condition
        :param limit: Limit number of updated rows
        """
        super().__init__(where=where, limit=limit)
        self.table = table if isinstance(table, Table) else Table(table)
        self.fields: list[UpdateColumn] = list(fields)

    def __str__(self) -> str:
        """
        Return the UPDATE statement with %s placeholders for arguments.
        """
        if not self.fields:
            raise AttributeError("At least one column must be updated.")

        query = [
            f"UPDATE {str(self.table)}",
            f"SET {', '.join(map(str, self.fields))}"
        ]

        if self._where:
            query.append("WHERE")
            query.append(str(self._where))

        if self._limit:
            query.append(str(self._limit))

        return " ".join(query)

    @property
    def args(self) -> list[Any]:
        """
        Return all arguments used in the UPDATE statement.
        """
        out = []

        for field in self.fields:
            out.extend(field.args)

        if self._where is not None:
            out.extend(self._where.args)

        if self._limit is not None:
            out.extend(self._limit.args)

        return out

    def __bool__(self):
        """
        Return True if there are any fields to be updated and the statement should be executed.
        """
        return bool(self.fields)

    def append(self, field: UpdateColumn):
        """
        Append new UpdateField to this UPDATE statement. Can be used when set() method is not sufficient.
        """
        if field in self.fields:
            raise AttributeError(f"Field '{field}' is already in the list of fields to be updated.")

        self.fields.append(field)
        return self

    def set(self, field: ColumnArg, value: Statement | Any):
        """
        Syntactical sugar for creating simple SET UpdateFields.
        :param field: Field name (without quotes).
        :param value: Value to set the field to (will be escaped).
        :return:
        """
        return self.append(UpdateColumn(field, value))

    # pylint: disable=invalid-name
    def SET(self, field: str, value: Any):
        """Alias for set() for better SQL compatibility"""
        return self.set(field, value)


# Alias for Update to provide better SQL compatibility
UPDATE = Update
