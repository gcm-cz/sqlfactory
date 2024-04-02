"""Classes representing database entities."""

from __future__ import annotations
from typing import Any

from .statement import Statement, Raw, StatementWithArgs
from .condition.simple import Gt, Ge, Eq, Lt, Le, Ne


class Column(Statement):
    """
    Column (optionally with table and database) as statement.

    Provides shorthand for creating conditional SQL statements and arithmetic SQL statements. You can use Column
    instance to directly create condition using simple operators (==, !=, <, <=, >, >=) or arithmetic operations
    (+, -, *, /, %).

    >>> Column("table.column") == 5
    >>> # Produces Eq(Column("table.column"), 5)

    >>> Column("table.column") + 5
    >>> # Produces Raw("`table`.`column` + %s", 5)
    """
    def __init__(self, column: str):
        super().__init__()

        self._column = column.split(".")
        if len(self._column) > 3:
            raise ValueError("Invalid column name (contains more than <database>.<table>.<column>).")

    def __str__(self) -> str:
        return ".".join(map(lambda x: f"`{x}`" if not x.startswith("`") else x, self._column))

    @property
    def column(self) -> str:
        """Returns column part of the column name."""
        return self._column[-1]

    @property
    def table(self) -> str | None:
        """Returns table part of the column name, if specified. If column specification does not contain table name,
        returns None."""
        try:
            return self._column[-2]
        except IndexError:
            return None

    @property
    def database(self) -> str | None:
        """Returns database part of the column name, if specified. If column specification does not contain database
        name, returns None."""
        try:
            return self._column[-3]
        except IndexError:
            return None

    def __hash__(self):
        return hash(str(self))

    def __gt__(self, other: Statement | Any) -> Gt:
        """Shorthand to produce conditional SQL statement <column> > <other>."""
        return Gt(self, other)

    def __ge__(self, other: Statement | Any) -> Ge:
        """Shorthand to produce conditional SQL statement <column> >= <other>."""
        return Ge(self, other)

    def __lt__(self, other: Statement | Any) -> Lt:
        """Shorthand to produce conditional SQL statement <column> < <other>."""
        return Lt(self, other)

    def __le__(self, other: Statement | Any) -> Le:
        """Shorthand to produce conditional SQL statement <column> <= <other>."""
        return Le(self, other)

    def __eq__(self, other: Statement | Any) -> Eq:
        """Shorthand to produce conditional SQL statement <column> = <other>."""
        return Eq(self, other)

    def __ne__(self, other: Statement | Any) -> Ne:
        """Shorthand to produce conditional SQL statement <column> != <other>."""
        return Ne(self, other)

    def __add__(self, other) -> StatementWithArgs:
        return Raw(
            f"{str(self)} + {str(other) if isinstance(other, Statement) else '%s'}",
            *other.args if isinstance(other, StatementWithArgs)
            else [other] if not isinstance(other, Statement)
            else []
        )

    def __sub__(self, other) -> StatementWithArgs:
        return Raw(
            f"{str(self)} - {str(other) if isinstance(other, Statement) else '%s'}",
            *other.args if isinstance(other, StatementWithArgs)
            else [other] if not isinstance(other, Statement)
            else []
        )

    def __mul__(self, other) -> StatementWithArgs:
        return Raw(
            f"{str(self)} * {str(other) if isinstance(other, Statement) else '%s'}",
            *other.args if isinstance(other, StatementWithArgs)
            else [other] if not isinstance(other, Statement)
            else []
        )

    def __truediv__(self, other) -> StatementWithArgs:
        return Raw(
            f"{str(self)} / {str(other) if isinstance(other, Statement) else '%s'}",
            *other.args if isinstance(other, StatementWithArgs)
            else [other] if not isinstance(other, Statement)
            else []
        )

    def __mod__(self, other) -> StatementWithArgs:
        return Raw(
            f"{str(self)} % {str(other) if isinstance(other, Statement) else '%s'}",
            *other.args if isinstance(other, StatementWithArgs)
            else [other] if not isinstance(other, Statement)
            else []
        )

    def __and__(self, other) -> StatementWithArgs:
        return Raw(
            f"{str(self)} & {str(other) if isinstance(other, Statement) else '%s'}",
            *other.args if isinstance(other, StatementWithArgs)
            else [other] if not isinstance(other, Statement)
            else []
        )

    def __or__(self, other) -> StatementWithArgs:
        return Raw(
            f"{str(self)} | {str(other) if isinstance(other, Statement) else '%s'}",
            *other.args if isinstance(other, StatementWithArgs)
            else [other] if not isinstance(other, Statement)
            else []
        )

    def __xor__(self, other) -> StatementWithArgs:
        return Raw(
            f"{str(self)} ^ {str(other) if isinstance(other, Statement) else '%s'}",
            *other.args if isinstance(other, StatementWithArgs)
            else [other] if not isinstance(other, Statement)
            else []
        )

    def __lshift__(self, other):
        return Raw(
            f"{str(self)} << {str(other) if isinstance(other, Statement) else '%s'}",
            *other.args if isinstance(other, StatementWithArgs)
            else [other] if not isinstance(other, Statement)
            else []
        )

    def __rshift__(self, other):
        return Raw(
            f"{str(self)} >> {str(other) if isinstance(other, Statement) else '%s'}",
            *other.args if isinstance(other, StatementWithArgs)
            else [other] if not isinstance(other, Statement)
            else []
        )

    def __neg__(self):
        return Raw(f"~{str(self)}")


class Table(Statement):
    """
    Table (optionally with database) as statement

    By accessing Table's undefined attributes, instance of Column is returned. This allows to easily access columns of
    that table, and reference them in SQL statements.

    >>> Table("database.table").column_name == 5
    >>> # Produces Eq(Column("database.table.column_name"), 5)
    """

    def __init__(self, table: str):
        """
        :param table: Table name (optionally with database in form <database>.<table>). If database is not specified,
            it is assumed that table is in default database and SQL constructed will not contain any database name.
        """
        super().__init__()
        self._table = table.split(".")

        if len(self._table) > 2:
            raise ValueError("Invalid table name (contains more than <database>.<table>).")

    def __str__(self):
        return ".".join(map(lambda x: f"`{x}`" if not x.startswith("`") else x, self._table))

    @property
    def table(self) -> str | None:
        """Returns table part of the table name"""
        return self._table[-1]

    @property
    def database(self) -> str | None:
        """Returns database part of the table name, if specified. If table specification does not contain database,
        returns None."""
        try:
            return self._table[-2]
        except IndexError:
            return None

    def __getattr__(self, name: str) -> Column:
        """Returns column of that table."""
        return Column(f"{'.'.join(self._table)}.{name}")


# Alias for column that can be passed as instance of column or as string.
ColumnArg = Column | str
