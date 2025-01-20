"""LIMIT statement"""

from __future__ import annotations

from typing import Any, Generic, Self, TypeVar, overload

from sqlfactory.statement import ConditionalStatement, Statement

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
    def __init__(self, /, offset: int | None, limit: int | None) -> None:
        """
        LIMIT statement with both offset and limit
        :param offset: Pagination offset (how many rows to skip before returning result)
        :param limit: Number of returned rows
        """

    def __init__(  # type: ignore[misc]
        self, offset_or_limit: int | None = None, /, limit: int | None = None, *, offset: int | None = None
    ) -> None:
        """
        LIMIT statement
        :param offset_or_limit: Pagination offset, or limit if second argument is None
        :param limit: Number of returned rows.
        """

        if offset_or_limit is not None and offset is not None and limit is not None:
            raise AttributeError("Unable to specify both positional argument offset and keyword argument offset.")

        if limit is None:
            limit = offset_or_limit
            offset_or_limit = offset

        if offset is not None:
            offset_or_limit = offset

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
    def limit(self, limit: Limit | None, /) -> Self:
        """
        Limit statement
        :param limit: Instance of Limit
        """

    @overload
    def limit(self, limit: int | None, /) -> Self:
        """
        Limit statement
        :param limit: Number of returned rows
        """

    @overload
    def limit(self, offset: int | None, limit: int | None) -> Self:
        """
        Limit statement
        :param offset: Pagination offset (how many rows to skip before returning result)
        :param limit: Number of returned rows
        """

    def limit(  # type: ignore[misc]
        self, offset_or_limit: int | Limit | None = None, /, limit: int | None = None, *, offset: int | None = None
    ) -> Self:
        """Limit statement"""
        if self._limit is not None:
            raise AttributeError("Limit has already been specified.")

        if isinstance(offset_or_limit, Limit):
            self._limit = offset_or_limit

            if limit is not None or offset is not None:
                raise AttributeError("When passing Limit instance as first argument, second argument should not be passed.")

        else:
            if offset_or_limit is not None:
                if offset is not None:
                    raise AttributeError("Unable to specify both positional argument offset and keyword argument offset.")

                self._limit = Limit(offset_or_limit, limit)

            else:
                self._limit = Limit(offset=offset, limit=limit)

        return self

    @overload
    def LIMIT(self, limit: Limit | None, /) -> Self:
        # pylint: disable=invalid-name
        """Alias for limit() to be more SQL-like with all capitals."""

    @overload
    def LIMIT(self, limit: int, /) -> Self:
        # pylint: disable=invalid-name
        """Alias for limit() to be more SQL-like with all capitals."""

    @overload
    def LIMIT(self, offset: int, limit: int, /) -> Self:
        # pylint: disable=invalid-name
        """Alias for limit() to be more SQL-like with all capitals."""

    def LIMIT(self, offset_or_limit: int | Limit | None, limit: int | None = None, /) -> Self:
        # pylint: disable=invalid-name
        """Alias for limit() to be more SQL-like with all capitals."""
        return self.limit(offset_or_limit, limit)  # type: ignore[arg-type]
