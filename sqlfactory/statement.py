"""Base classes for building SQL statements."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Statement(ABC):
    """
    Base class of serializable SQL statement with arguments that should be escaped. This class cannot hold any data,
    it is just an interface for other classes to implement.

    Any class that needs SQL argument substitution should inherit from this class, as there are checks that tests
    whether passed object is instance of this class.

    To retrieve SQL statement, call `str()` on the instance. To retrieve arguments, access `args` property.
    """

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

    def __eq__(self, other: 'Statement') -> bool:
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


# pylint: disable=too-few-public-methods  # As this is just an interface.
class ConditionalStatement(ABC):
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

    def __init__(self, sql: str, *args: Any):
        super().__init__()
        self._statement = sql
        self._args = args

    def __str__(self):
        return self._statement

    @property
    def args(self) -> list[Any]:
        return list(self._args)
