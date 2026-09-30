"""Base classes for building SQL statements."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar

from sqlfactory.dialect import MySQLDialect, SQLDialect


class Statement(ABC):
    """
    Base class of serializable SQL statement with arguments that should be escaped. This class cannot hold any data,
    it is just an interface for other classes to implement.

    Any class that needs SQL argument substitution should inherit from this class, as there are checks that tests
    whether passed object is instance of this class.

    To retrieve SQL statement, call `str()` on the instance. To retrieve arguments, access `args` property.

    ```python
    class CustomStatement(Statement):
        def __str__() -> str:
            return "SELECT * FROM table WHERE column = %s"

        @property
        def args() -> list[Any]:
            return [3]

    statement = CustomStatement()
    print(str(statement))  # SELECT * FROM table WHERE column = %s
    print(statement.args)  # [3]
    """

    default_dialect: ClassVar[SQLDialect] = MySQLDialect()
    """
    Default SQL dialect for all SQL statements, if not overwritten by explicit dialect or dialect context.
    """

    def __init__(self, *args: Any, dialect: SQLDialect | None = None, **kwargs: Any) -> None:
        self._explicit_dialect: SQLDialect | None = dialect
        super().__init__(*args, **kwargs)

    @property
    def dialect(self) -> SQLDialect:
        """
        Dialect for building this particular statement. Priorities are:

        - explicit dialect passed to class constructor
        - dialect set in the context (`with SQLDialect(): ...`)
        - default dialect (`Statement.default_dialect`)
        """

        if self._explicit_dialect is not None:
            return self._explicit_dialect

        dialect = SQLDialect.dialect_context.get()
        if dialect:
            return dialect

        return self.__class__.default_dialect

    @dialect.setter
    def dialect(self, dialect: SQLDialect | None) -> None:
        self._explicit_dialect = dialect

    @abstractmethod
    def __str__(self) -> str:
        """Return SQL statement representing the statement."""

    @property
    @abstractmethod
    def args(self) -> list[Any]:
        """Return arguments representing `%s` placeholders in statement returned by `__str__()`. Number of items
        in returned list must match number of `%s` placeholders in string returned by calling `__str__()`."""

    def __hash__(self) -> int:
        """Return hash of this statement to be able to use it in unique collections."""
        return hash(str(self)) + sum(map(hash, self.args))

    def __eq__(self, other: "Statement") -> bool:  # type: ignore[override]
        """Compares this statement to other."""
        if str(self) != str(other):
            return False

        return isinstance(other, Statement) and self.args == other.args

    def __repr__(self) -> str:
        """Representation of statement including the arguments, if any."""
        args = list(map(repr, self.args))
        if args:
            return f"{self.__str__()} with arguments [{', '.join(args)}]"

        return self.__str__()


class Query(Statement, ABC):
    """
    A query expression - `SELECT`, `UNION` and its variants, `WITH` - which `operand()` wraps in parentheses when it is
    used as a value of another statement (a scalar subquery, a derived table, ...). Subclass it for your own statement
    classes that render a query expression.
    """


def operand(statement: Statement) -> str:
    """
    Render `statement` as an operand of another statement - a function argument, either side of a comparison or of an
    arithmetic operator, a value in `UPDATE ... SET`, an `ORDER BY` expression, a selected column, an aliased or joined
    derived table, ... A `Query` is wrapped in parentheses, which is how SQL writes a subquery; any other statement
    renders as is.

    >>> operand(Column("a"))
    >>> "`a`"

    >>> operand(Select(Max("ts"), table="t"))
    >>> "(SELECT MAX(`ts`) FROM `t`)"

    Positions where a query is a statement body rather than a value (`INSERT ... SELECT`, the parts of a `UNION`,
    a CTE, `IN (SELECT ...)`, `EXISTS (SELECT ...)`) render it themselves, and so does `str()` of the query itself.
    """
    if isinstance(statement, Query):
        return f"({statement!s})"

    return str(statement)


class ConditionalStatement(ABC):
    # pylint: disable=too-few-public-methods  # As this is just an interface.
    """
    Mixin that provides conditional execution of the statement (query will be executed only if statement is valid).

    This class is used for example for INSERT statements, to not execute empty INSERT. Or to not execute UPDATE
    if there are no columns to be updated.
    """

    @abstractmethod
    def __bool__(self) -> bool:
        """
        Return True if the statement should be executed.
        """


class Raw(Statement):
    """
    RAW string statement (with optional args), that won't be processed in any way.
    """

    def __init__(self, sql: str, *args: Any) -> None:
        """
        :param sql: SQL part of the statement with optional %s placeholders for arguments.
        :param args: Arguments to be escaped and substituted in the statement
        """
        super().__init__()
        self._statement = sql
        self._args = args

    def __str__(self) -> str:
        return self._statement

    @property
    def args(self) -> list[Any]:
        return list(self._args)


class Value(Statement):
    """
    To provide literal value for places expecting statement, you can use `Value` class.
    """

    def __init__(self, value: Any) -> None:
        super().__init__()

        self._value = value

    def __str__(self) -> str:
        return self.dialect.placeholder

    @property
    def args(self) -> list[Any]:
        return [self._value]
