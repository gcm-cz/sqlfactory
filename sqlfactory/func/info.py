"""Information functions (https://mariadb.com/kb/en/information-functions/)."""

from typing import Any

from sqlfactory.entities import Column, ColumnArg
from sqlfactory.func.base import Function
from sqlfactory.statement import Statement, operand


class Benchmark(Function):
    """Executes an expression repeatedly."""

    def __init__(self, count: int, expression: Statement) -> None:
        super().__init__("BENCHMARK", count, expression)


class BinlogGtidPos(Function):
    """
    `BINLOG_GTID_POS(binlog_filename, binlog_offset)`

    Takes an old-style binary log position (a file name and a file offset) and returns a string representation
    of the corresponding GTID position, or NULL if the position is not found in the current binlog.
    """

    def __init__(self, binlog_filename: Statement | Any, binlog_offset: Statement | Any) -> None:
        super().__init__("BINLOG_GTID_POS", binlog_filename, binlog_offset)


class Charset(Function):
    """`CHARSET(str)` -- returns the character set of the string argument."""

    def __init__(self, expression: Statement | Any) -> None:
        super().__init__("CHARSET", expression)


class Coercibility(Function):
    """Returns the collation coercibility value of the string expression."""

    def __init__(self, expression: Statement | Any) -> None:
        super().__init__("COERCIBILITY", expression)


class Collation(Function):
    """Collation of the string argument"""

    def __init__(self, expression: Statement | Any) -> None:
        super().__init__("COLLATION", expression)


class Collate(Statement):
    """String with collation"""

    def __init__(self, expression: str | Statement, collation: str) -> None:
        super().__init__()

        self._expression = expression
        self._collation = collation

    def __str__(self) -> str:
        return (
            f"{operand(self._expression) if isinstance(self._expression, Statement) else self.dialect.placeholder} "
            f"COLLATE {self._collation}"
        )

    @property
    def args(self) -> list[Any]:
        return self._expression.args if isinstance(self._expression, Statement) else [self._expression]


class ConnectionId(Function):
    """Connection ID"""

    def __init__(self) -> None:
        super().__init__("CONNECTION_ID")


class CurrentRole(Function):
    """Current role name"""

    def __init__(self) -> None:
        super().__init__("CURRENT_ROLE")


class CurrentUser(Function):
    """Username/host that authenticated the current client"""

    def __init__(self) -> None:
        super().__init__("CURRENT_USER")


class Database(Function):
    """Current default database"""

    def __init__(self) -> None:
        super().__init__("DATABASE")


class DecodeHistogram(Function):
    """Returns comma separated numerics corresponding to a probability distribution"""

    def __init__(self, hist_type: Any, histogram: Any) -> None:
        super().__init__("DECODE_HISTOGRAM", hist_type, histogram)


class Default(Function):
    """`DEFAULT(col_name)` -- returns the default value for a table column."""

    def __init__(self, column: ColumnArg) -> None:
        super().__init__("DEFAULT", Column(column) if isinstance(column, str) else column)


class FoundRows(Function):
    """Returns the number of (potentially) returned rows if there was no LIMIT involved."""

    def __init__(self) -> None:
        super().__init__("FOUND_ROWS")


class LastInsertId(Function):
    """
    `LAST_INSERT_ID()`, `LAST_INSERT_ID(expr)`

    With no argument, returns the first automatically generated AUTO_INCREMENT value from the most recent INSERT
    statement. With `expr`, sets the value that the next call to `LAST_INSERT_ID()` returns, without touching any
    AUTO_INCREMENT sequence -- used e.g. as `INSERT ... ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id)` to recover
    the id of the row that was updated, or `seq = LAST_INSERT_ID(seq + 1)` to hand out a value from a self-maintained
    sequence column.
    """

    def __init__(self, expr: Statement | Any = None) -> None:
        if expr is not None:
            super().__init__("LAST_INSERT_ID", expr)
        else:
            super().__init__("LAST_INSERT_ID")


class LastValue(Function):
    """Evaluates expression and returns the last."""

    def __init__(self, expr: Statement | Any, *exprs: Statement | Any) -> None:
        super().__init__("LAST_VALUE", expr, *exprs)


class RowCount(Function):
    """`ROW_COUNT()` -- returns the number of rows updated, inserted or deleted by the preceding statement, or -1
    if the preceding statement did not affect any rows the way those do (e.g. a SELECT)."""

    def __init__(self) -> None:
        super().__init__("ROW_COUNT")


class RowNumber(Function):
    """Returns the number of accepted rows so far."""

    def __init__(self) -> None:
        super().__init__("ROW_NUMBER")


class Schema(Function):
    """Current default schema"""

    def __init__(self) -> None:
        super().__init__("SCHEMA")


class SessionUser(Function):
    """Username/host that authenticated the current client"""

    def __init__(self) -> None:
        super().__init__("SESSION_USER")


class SystemUser(Function):
    """Username/host that authenticated the current client"""

    def __init__(self) -> None:
        super().__init__("SYSTEM_USER")


class User(Function):
    """Username/host that authenticated the current client"""

    def __init__(self) -> None:
        super().__init__("USER")


class Version(Function):
    """Database version"""

    def __init__(self) -> None:
        super().__init__("VERSION")
