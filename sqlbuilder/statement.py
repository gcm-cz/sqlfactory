from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Statement(ABC):
    """
    Base class of serializable SQL statement. This class cannot hold any data, it is just an interface
    for other classes to implement.
    """

    @abstractmethod
    def __str__(self) -> str:
        """
        Return SQL statement representing the statement.
        """

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        """Return hash of this statement to be able to use it in unique collections."""
        return hash(str(self))

    def __eq__(self, other: 'Statement'):
        """Compares this statement to other."""
        if not isinstance(other, Statement):
            return False

        return str(self) == str(other)


class StatementWithArgs(Statement):
    """
    Base class of serializable SQL statement with arguments that should be escaped. This class cannot hold any data,
    it is just an interface for other classes to implement.
    """

    @property
    @abstractmethod
    def args(self) -> list[Any]:
        """
        Return arguments representing `%s` placeholders in statement returned by `__str__()`.
        """

    def __hash__(self):
        """Return hash of this statement to be able to use it in unique collections."""
        return super().__hash__() + sum(map(hash, self.args))

    def __eq__(self, other: 'StatementWithArgs'):
        """Compares this statement to other."""
        if not isinstance(other, StatementWithArgs):
            if not self.args:
                return super().__eq__(other)
            else:
                return False

        return self.args == other.args and super().__eq__(other)

    def __repr__(self):
        args = list(map(repr, self.args))
        if args:
            return f"{super().__repr__()} with arguments [{', '.join(args)}]"
        else:
            return super().__repr__()


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


class Raw(StatementWithArgs):
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
