import asyncio
import inspect
from typing import Protocol, Any, overload, Collection

from .logger import logger
from .statement import Statement, StatementWithArgs, ConditionalStatement


class HasQueryWithTupleArgs(Protocol):
    """Protocol defining DB driver with query method that takes arguments as tuple."""
    def query(self, query: str, args: tuple[Any]): ...


class HasExecuteWithTupleArgs(Protocol):
    """Protocol defining DB driver with execute method that takes arguments as tuple."""
    def execute(self, query: str, args: tuple[Any]): ...


class HasQueryWithArgs(Protocol):
    """Protocol defining DB driver with query method that takes arguments as multiple arguments."""
    def query(self, query: str, *args: Any): ...


class HasExecuteWithArgs(Protocol):
    """Protocol defining DB driver with execute method that takes arguments as tuple."""
    def execute(self, query: str, args: tuple[Any]): ...


class HasAsyncQueryWithTupleArgs(Protocol):
    """Protocol defining DB driver with async query method that takes arguments as tuple."""
    async def query(self, query: str, args: tuple[Any]): ...


class HasAsyncExecuteWithTupleArgs(Protocol):
    """Protocol defining DB driver with async execute method that takes arguments as tuple."""
    async def execute(self, query: str, args: tuple[Any]): ...


class HasAsyncQueryWithArgs(Protocol):
    """Protocol defining DB driver with async query method that takes arguments as multiple arguments."""
    async def query(self, query: str, *args: Any): ...


class HasAsyncExecuteWithArgs(Protocol):
    """Protocol defining DB driver with async execute method that takes arguments as tuple."""
    async def execute(self, query: str, args: tuple[Any]): ...


HasQueryOrExecute = HasQueryWithTupleArgs | HasExecuteWithTupleArgs | HasQueryWithArgs | HasExecuteWithArgs
HasAsyncQueryOrExecute = HasAsyncQueryWithTupleArgs | HasAsyncExecuteWithTupleArgs | HasAsyncQueryWithArgs | HasAsyncExecuteWithArgs
MaybeAsyncHasQueryOrExecute = HasQueryOrExecute | HasAsyncQueryOrExecute


class ExecutableStatement(Statement):
    """
    Base class of serializable SQL statement.
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
        else:
            return call(str(self), tuple(args))


class ExecutableStatementWithArgs(StatementWithArgs, ExecutableStatement):
    """
    Base class of serializable SQL statement with arguments that should be escaped.
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


class ConditionalExecutableStatement(ConditionalStatement):
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
        elif inspect.iscoroutinefunction(getattr(trx, "query", getattr(trx, "execute", None))):
            logger.debug("Not executing statement, because it is false.")
            fut = asyncio.get_running_loop().create_future()
            fut.set_result(False)
            return fut
        else:
            logger.debug("Not executing statement, because it is false.")
            return False
