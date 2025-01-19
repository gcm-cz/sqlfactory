"""Module containing definition of executable SQL statements base classes."""

import inspect
from abc import ABC
from typing import Any, Awaitable, Protocol, TypeAlias, TypeVar, cast, overload

from .logger import logger
from .statement import ConditionalStatement, Statement

R_co = TypeVar("R_co", covariant=True)


class HasQueryWithTupleArgs(Protocol[R_co]):
    # pylint: disable=too-few-public-methods, missing-function-docstring  # As this is just a protocol.
    """Protocol defining DB driver with query method that takes arguments as tuple."""

    def query(self, query: str, args: tuple[Any]) -> R_co: ...


class HasExecuteWithTupleArgs(Protocol[R_co]):
    # pylint: disable=too-few-public-methods, missing-function-docstring  # As this is just a protocol.
    """Protocol defining DB driver with execute method that takes arguments as tuple."""

    def execute(self, query: str, args: tuple[Any]) -> R_co: ...


class HasQueryWithArgs(Protocol[R_co]):
    # pylint: disable=too-few-public-methods, missing-function-docstring  # As this is just a protocol.
    """Protocol defining DB driver with query method that takes arguments as multiple arguments."""

    def query(self, query: str, *args: Any) -> R_co: ...


class HasExecuteWithArgs(Protocol[R_co]):
    # pylint: disable=too-few-public-methods, missing-function-docstring  # As this is just a protocol.
    """Protocol defining DB driver with execute method that takes arguments as tuple."""

    def execute(self, query: str, *args: Any) -> R_co: ...


class HasAsyncQueryWithTupleArgs(Protocol[R_co]):
    # pylint: disable=too-few-public-methods, missing-function-docstring  # As this is just a protocol.
    """Protocol defining DB driver with async query method that takes arguments as tuple."""

    async def query(self, query: str, args: tuple[Any]) -> R_co: ...


class HasAsyncExecuteWithTupleArgs(Protocol[R_co]):
    # pylint: disable=too-few-public-methods, missing-function-docstring  # As this is just a protocol.
    """Protocol defining DB driver with async execute method that takes arguments as tuple."""

    async def execute(self, query: str, args: tuple[Any]) -> R_co: ...


class HasAsyncQueryWithArgs(Protocol[R_co]):
    # pylint: disable=too-few-public-methods, missing-function-docstring  # As this is just a protocol.
    """Protocol defining DB driver with async query method that takes arguments as multiple arguments."""

    async def query(self, query: str, *args: Any) -> R_co: ...


class HasAsyncExecuteWithArgs(Protocol[R_co]):
    # pylint: disable=too-few-public-methods, missing-function-docstring  # As this is just a protocol.
    """Protocol defining DB driver with async execute method that takes arguments as tuple."""

    async def execute(self, query: str, args: tuple[Any]) -> R_co: ...


HasQueryOrExecute: TypeAlias = (
    HasQueryWithTupleArgs[R_co] | HasExecuteWithTupleArgs[R_co] | HasQueryWithArgs[R_co] | HasExecuteWithArgs[R_co]
)

HasAsyncQueryOrExecute: TypeAlias = (
    HasAsyncQueryWithTupleArgs[R_co]
    | HasAsyncExecuteWithTupleArgs[R_co]
    | HasAsyncQueryWithArgs[R_co]
    | HasAsyncExecuteWithArgs[R_co]
)
MaybeAsyncHasQueryOrExecute: TypeAlias = HasQueryOrExecute[R_co] | HasAsyncQueryOrExecute[R_co]


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
    async def execute(self, trx: HasAsyncQueryOrExecute[R_co], *args: Any) -> R_co:
        """Execute statement on async db driver"""

    @overload
    def execute(self, trx: HasQueryOrExecute[R_co], *args: Any) -> R_co:
        """Execute statement on sync db driver."""

    def execute(self, trx: MaybeAsyncHasQueryOrExecute[R_co], *args: Any) -> R_co | Awaitable[R_co]:
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
        if any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in sig.parameters.values()):
            return call(str(self), *self.args, *args)

        return call(str(self), tuple(self.args + list(args)))


class ConditionalExecutableStatement(ExecutableStatement, ConditionalStatement, ABC):
    """
    Mixin that provides conditional execution of the statement (query will be executed only if statement is valid).

    This class is used for example for INSERT statements, to not execute empty INSERT. Or to not execute UPDATE
    if there are no columns to be updated.
    """

    @overload  # type: ignore[override]
    async def execute(self, trx: HasAsyncQueryOrExecute[R_co], *args: Any) -> R_co | bool:
        """Execute statement on async db driver"""

    @overload
    def execute(self, trx: HasQueryOrExecute[R_co], *args: Any) -> R_co | bool:
        # pylint: disable=invalid-overridden-method
        """Execute statement on sync db driver."""

    def execute(self, trx: MaybeAsyncHasQueryOrExecute[R_co], *args: Any) -> R_co | bool | Awaitable[R_co | bool]:
        # pylint: disable=invalid-overridden-method
        """
        Execute SQL statement using provided db-driver, but only if statement evaluates as True.
        :param trx: DB driver with query() or execute() method, which accepts either tuple as arguments,
        :param args: Arguments to pass to the db driver.
        :return:
        """
        if bool(self):
            return cast(R_co, super().execute(trx, *args))

        if inspect.iscoroutinefunction(getattr(trx, "query", getattr(trx, "execute", None))):
            logger.debug("Not executing statement, because it is false.")

            # pylint: disable=import-outside-toplevel
            import asyncio

            fut = asyncio.get_running_loop().create_future()
            fut.set_result(False)
            return fut

        logger.debug("Not executing statement, because it is false.")
        return False
