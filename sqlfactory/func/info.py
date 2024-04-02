"""Information functions (https://mariadb.com/kb/en/information-functions/)."""
from typing import Any

from .base import Function
from .. import Statement, StatementWithArgs, Raw, Column


# pylint: disable=too-few-public-methods
class Benchmark(Function):
    """Executes an expression repeatedly."""
    def __init__(self, count: int, expression: Statement):
        super().__init__('BENCHMARK', count, expression)


# pylint: disable=too-few-public-methods
class BinlogGtidPos(Function):
    """Returns a string representation of the corresponding GTID position."""
    def __init__(self):
        super().__init__('BINLOG_GTID_POS')


# pylint: disable=too-few-public-methods
class Charset(Function):
    """Returns the character set."""
    def __init__(self):
        super().__init__('CHARSET')


# pylint: disable=too-few-public-methods
class Coercibility(Function):
    """Returns the collation coercibility value of the string expression."""
    def __init__(self, expression: str):
        super().__init__('COERCIBILITY', expression)


# pylint: disable=too-few-public-methods
class Collation(Function):
    """Collation of the string argument"""
    def __init__(self, expression: str):
        super().__init__('COLLATION', expression)


# pylint: disable=too-few-public-methods
class Collate(Raw):
    """String with collation"""
    def __init__(self, expression: str | Statement, collation: str):
        super().__init__(
            f"{str(expression) if isinstance(expression, Statement) else '%s'} COLLATE {collation}",
            *(
                expression.args if isinstance(expression, StatementWithArgs)
                else [expression] if not isinstance(expression, Statement)
                else []
            )
        )


# pylint: disable=too-few-public-methods
class ConnectionId(Function):
    """Connection ID"""
    def __init__(self):
        super().__init__('CONNECTION_ID')


# pylint: disable=too-few-public-methods
class CurrentRole(Function):
    """Current role name"""
    def __init__(self):
        super().__init__('CURRENT_ROLE')


# pylint: disable=too-few-public-methods
class CurrentUser(Function):
    """Username/host that authenticated the current client"""
    def __init__(self):
        super().__init__('CURRENT_USER')


# pylint: disable=too-few-public-methods
class Database(Function):
    """Current default database"""
    def __init__(self):
        super().__init__('DATABASE')


# pylint: disable=too-few-public-methods
class DecodeHistogram(Function):
    """Returns comma separated numerics corresponding to a probability distribution"""
    def __init__(self, hist_type: Any, histogram: Any):
        super().__init__('DECODE_HISTOGRAM', hist_type, histogram)


# pylint: disable=too-few-public-methods
class Default(Function):
    """Returns the default value for a table column"""
    def __init__(self, column: Column):
        super().__init__('DEFAULT', column)


# pylint: disable=too-few-public-methods
class FoundRows(Function):
    """Returns the number of (potentially) returned rows if there was no LIMIT involved."""
    def __init__(self):
        super().__init__('FOUND_ROWS')


# pylint: disable=too-few-public-methods
class LastInsertId(Function):
    """Returns the value generated for an AUTO_INCREMENT column by the previous INSERT statement."""
    def __init__(self):
        super().__init__('LAST_INSERT_ID')


# pylint: disable=too-few-public-methods
class LastValue(Function):
    """Evaluates expression and returns the last."""
    def __init__(self, expr: Statement, *exprs: Statement):
        super().__init__('LAST_VALUE', expr, *exprs)


# pylint: disable=too-few-public-methods
class RowNumber(Function):
    """Returns the number of accepted rows so far."""
    def __init__(self):
        super().__init__('ROW_NUMBER')


# pylint: disable=too-few-public-methods
class Schema(Function):
    """Current default schema"""
    def __init__(self):
        super().__init__('SCHEMA')


# pylint: disable=too-few-public-methods
class SessionUser(Function):
    """Username/host that authenticated the current client"""
    def __init__(self):
        super().__init__('SESSION_USER')


# pylint: disable=too-few-public-methods
class SystemUser(Function):
    """Username/host that authenticated the current client"""
    def __init__(self):
        super().__init__('SYSTEM_USER')


# pylint: disable=too-few-public-methods
class User(Function):
    """Username/host that authenticated the current client"""
    def __init__(self):
        super().__init__('USER')


# pylint: disable=too-few-public-methods
class Version(Function):
    """Database version"""
    def __init__(self):
        super().__init__('VERSION')
