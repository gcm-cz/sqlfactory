"""Module containing definition of executable SQL statements base classes."""

import inspect
from abc import ABC
from typing import Protocol, Any, overload

from .logger import logger
from .statement import Statement, StatementWithArgs, ConditionalStatement


# pylint: disable=too-few-public-methods, missing-function-docstring  # As this is just a protocol.
class HasQueryWithTupleArgs(Protocol):
    """Protocol defining DB driver with query method that takes arguments as tuple."""
    def query(self, query: str, args: tuple[Any]): ...


# pylint: disable=too-few-public-methods, missing-function-docstring  # As this is just a protocol.
class HasExecuteWithTupleArgs(Protocol):
    """Protocol defining DB driver with execute method that takes arguments as tuple."""
    def execute(self, query: str, args: tuple[Any]): ...


# pylint: disable=too-few-public-methods, missing-function-docstring  # As this is just a protocol.
class HasQueryWithArgs(Protocol):
    """Protocol defining DB driver with query method that takes arguments as multiple arguments."""
    def query(self, query: str, *args: Any): ...


# pylint: disable=too-few-public-methods, missing-function-docstring  # As this is just a protocol.
class HasExecuteWithArgs(Protocol):
    """Protocol defining DB driver with execute method that takes arguments as tuple."""
    def execute(self, query: str, args: tuple[Any]): ...


# pylint: disable=too-few-public-methods, missing-function-docstring  # As this is just a protocol.
class HasAsyncQueryWithTupleArgs(Protocol):
    """Protocol defining DB driver with async query method that takes arguments as tuple."""
    async def query(self, query: str, args: tuple[Any]): ...


# pylint: disable=too-few-public-methods, missing-function-docstring  # As this is just a protocol.
class HasAsyncExecuteWithTupleArgs(Protocol):
    """Protocol defining DB driver with async execute method that takes arguments as tuple."""
    async def execute(self, query: str, args: tuple[Any]): ...


# pylint: disable=too-few-public-methods, missing-function-docstring  # As this is just a protocol.
class HasAsyncQueryWithArgs(Protocol):
    """Protocol defining DB driver with async query method that takes arguments as multiple arguments."""
    async def query(self, query: str, *args: Any): ...


# pylint: disable=too-few-public-methods, missing-function-docstring  # As this is just a protocol.
class HasAsyncExecuteWithArgs(Protocol):
    """Protocol defining DB driver with async execute method that takes arguments as tuple."""
    async def execute(self, query: str, args: tuple[Any]): ...


HasQueryOrExecute = HasQueryWithTupleArgs | HasExecuteWithTupleArgs | HasQueryWithArgs | HasExecuteWithArgs
HasAsyncQueryOrExecute = (
        HasAsyncQueryWithTupleArgs | HasAsyncExecuteWithTupleArgs | HasAsyncQueryWithArgs | HasAsyncExecuteWithArgs
)
MaybeAsyncHasQueryOrExecute = HasQueryOrExecute | HasAsyncQueryOrExecute


class ExecutableStatement(Statement, ABC):
    """
    This is the base class for an executable SQL statement that does not have any arguments.

    This class implements the execute() method. When given a database driver (or cursor) with query() or execute()
    methods, which take an SQL statement as the first argument and then a tuple or variadic arguments following SQL
    argument, it can be used to directly execute the SQL statement. This saves some typing by avoiding the manual
    passing of a string statement and arguments to the query.

    DB-API 2.0 drivers/cursors should all work with this implementation, as cursors should have execute() methods with
    the described semantics.

    Even async is supported. As this class does not process the result of the SQL statement in any way, the return
    value of the driver's execute()/query() method is directly returned. That returned value can be awaitable for async
    methods, so you can directly await it.
    """
    @overload
    def execute(self, trx: HasQueryOrExecute):
        """Execute statement on sync db driver."""

    @overload
    async def execute(self, trx: HasAsyncQueryOrExecute):
        """Execute statement on async db driver"""

    def execute(self, trx: MaybeAsyncHasQueryOrExecute, *args):
        """
        Execute statement on db driver (db-agnostic, just expects method `query` or `execute` on given driver).
        This is just a shortland for calling driver.execute(str(self), *args).
        :param trx: DB driver with query() or execute() method, which accepts either tuple as arguments,
         or multiple arguments following the query.
        :param args: Arguments to pass to the driver's query/execute method.
        :return: The same as db driver's execute/query method. If driver is async, returns awaitable response.
        """
        if hasattr(trx, "query"):
            call = trx.query
        elif hasattr(trx, "execute"):
            call = trx.execute
        else:
            raise AttributeError("trx must define query() or execute() method.")

        sig = inspect.signature(call)
        if any(map(lambda p: p.kind == inspect.Parameter.VAR_POSITIONAL, sig.parameters.values())):
            return call(str(self), *args)

        return call(str(self), tuple(args))


class ExecutableStatementWithArgs(StatementWithArgs, ExecutableStatement, ABC):
    """
    Base class of executable SQL statement with arguments that should be escaped.
    """
    def execute(self, trx: MaybeAsyncHasQueryOrExecute, *args):
        """
        Execute statement on db driver (db-agnostic, just expects method `query` or `execute` on given driver).
        Passes staement arguments to the driver's method. Returns response of the driver's method.
        This is just a shortland for calling driver.execute(str(self), *self.args).

        :param trx: DB driver with query() or execute() method, which accepts either tuple as arguments,
         or multiple arguments following the query.
        :param args: Additional arguments to append to the end of argument list (you probably don't need this).
        :return: The same as db driver's execute/query method. If driver is async, returns awaitable response.
        """
        return super().execute(trx, *self.args, *args)  # type: ignore


class ConditionalExecutableStatement(ExecutableStatement, ConditionalStatement, ABC):
    """
    Mixin that provides conditional execution of the statement (query will be executed only if statement is valid).

    This class is used for example for INSERT statements, to not execute empty INSERT. Or to not execute UPDATE
    if there are no columns to be updated.
    """
    def execute(self, trx: MaybeAsyncHasQueryOrExecute, *args):
        """
        Execute SQL statement using provided db-driver, but only if statement evaluates as True.
        :param trx: DB driver with query() or execute() method, which accepts either tuple as arguments,
        :param args: Arguments to pass to the db driver.
        :return:
        """
        if bool(self):
            return super().execute(trx, *args)  # type: ignore

        if inspect.iscoroutinefunction(getattr(trx, "query", getattr(trx, "execute", None))):
            logger.debug("Not executing statement, because it is false.")

            # pylint: disable=import-outside-toplevel
            import asyncio
            fut = asyncio.get_running_loop().create_future()
            fut.set_result(False)
            return fut

        logger.debug("Not executing statement, because it is false.")
        return False
