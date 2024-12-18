"""LIMIT statement"""
from __future__ import annotations
from typing import TypeVar, Generic, overload, Any

from sqlfactory.statement import Statement, ConditionalStatement

T = TypeVar("T")


class Limit(ConditionalStatement, Statement):
    """LIMIT statement"""

    @overload
    def __init__(self) -> None:
        """No LIMIT statement"""

    @overload
    def __init__(self, limit: int, /) -> None:
        """
        Just a LIMIT statement without offset
        :param limit: Number of returned rows
        """

    @overload
    def __init__(self, offset: int, limit: int, /) -> None:
        """
        LIMIT statement with both offset and limit
        :param offset: Pagination offset (how many rows to skip before returning result)
        :param limit: Number of returned rows
        """

    def __init__(self, offset_or_limit: int | None = None, limit: int | None = None) -> None:
        """
        LIMIT statement
        :param offset_or_limit: Pagination offset, or limit if second argument is None
        :param limit: Number of returned rows.
        """

        if limit is None:
            limit = offset_or_limit
            offset_or_limit = None

        self.offset = offset_or_limit
        self.limit = limit

    def __str__(self) -> str:
        if self.offset is not None:
            return "LIMIT %s, %s"

        if self.limit is not None:
            return "LIMIT %s"

        return ""

    def __bool__(self) -> bool:
        """Return True if statement should be included in query, False otherwise."""
        return self.offset is not None or self.limit is not None

    @property
    def args(self) -> list[int]:
        """Argument values of the limit statement"""
        if self.offset is not None and self.limit is not None:
            return [self.offset, self.limit]

        if self.limit is not None:
            return [self.limit]

        return []


class WithLimit(Generic[T]):
    """Mixin to provide LIMIT support for query generator."""
    def __init__(self, *args: Any, limit: Limit | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._limit = limit

    @overload
    def limit(self, limit: Limit | None, /) -> WithLimit[T]:
        """
        Limit statement
        :param limit: Instance of Limit
        """

    @overload
    def limit(self, limit: int, /) -> WithLimit[T]:
        """
        Limit statement
        :param limit: Number of returned rows
        """

    @overload
    def limit(self, offset: int, limit: int, /) -> WithLimit[T]:
        """
        Limit statement
        :param offset: Pagination offset (how many rows to skip before returning result)
        :param limit: Number of returned rows
        """

    def limit(self, offset_or_limit: int | Limit | None, limit: int | None = None, /) -> WithLimit[T]:
        """Limit statement"""
        if self._limit is not None:
            raise AttributeError("Limit has already been specified.")

        if isinstance(offset_or_limit, Limit):
            self._limit = offset_or_limit

            if limit is not None:
                raise AttributeError(
                    "When passing Limit instance as first argument, second argument should not be passed.")

        else:
            self._limit = Limit(offset_or_limit, limit)

        return self

    # pylint: disable=invalid-name
    @overload
    def LIMIT(self, limit: Limit | None, /) -> WithLimit[T]:
        """Alias for limit() to be more SQL-like with all capitals."""

    # pylint: disable=invalid-name
    @overload
    def LIMIT(self, limit: int, /) -> WithLimit[T]:
        """Alias for limit() to be more SQL-like with all capitals."""

    # pylint: disable=invalid-name
    @overload
    def LIMIT(self, offset: int, limit: int, /) -> WithLimit[T]:
        """Alias for limit() to be more SQL-like with all capitals."""

    # pylint: disable=invalid-name
    def LIMIT(self, offset_or_limit: int | Limit | None, limit: int | None = None, /) -> WithLimit[T]:
        """Alias for limit() to be more SQL-like with all capitals."""
        return self.limit(offset_or_limit, limit)  #type: ignore[arg-type]
