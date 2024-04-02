"""LIMIT statement"""

from typing import TypeVar, Generic, overload

from sqlfactory.statement import StatementWithArgs, ConditionalStatement

T = TypeVar("T")


class Limit(ConditionalStatement, StatementWithArgs):
    """LIMIT statement"""

    @overload
    def __init__(self):
        """No LIMIT statement"""

    @overload
    def __init__(self, limit: int):
        """
        Just a LIMIT statement without offset
        :param limit: Number of returned rows
        """

    @overload
    def __init__(self, offset: int, limit: int):
        """
        LIMIT statement with both offset and limit
        :param offset: Pagination offset (how many rows to skip before returning result)
        :param limit: Number of returned rows
        """

    def __init__(self, offset_or_limit: int = None, limit: int = None):
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
        if self.offset is not None:
            return [self.offset, self.limit]

        if self.limit is not None:
            return [self.limit]

        return []


class WithLimit(Generic[T]):
    """Mixin to provide LIMIT support for query generator."""
    def __init__(self, *args, limit: Limit = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._limit = limit

    @overload
    def limit(self, limit: Limit) -> T:
        """
        Limit statement
        :param limit: Instance of Limit
        """

    @overload
    def limit(self, limit: int) -> T:
        """
        Limit statement
        :param limit: Number of returned rows
        """

    @overload
    def limit(self, offset: int, limit: int) -> T:
        """
        Limit statement
        :param offset: Pagination offset (how many rows to skip before returning result)
        :param limit: Number of returned rows
        """

    def limit(self, offset_or_limit: int | Limit | None, limit: int = None) -> T:
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
    def LIMIT(self, limit: Limit) -> T:
        """Alias for limit() to be more SQL-like with all capitals."""

    # pylint: disable=invalid-name
    @overload
    def LIMIT(self, limit: int) -> T:
        """Alias for limit() to be more SQL-like with all capitals."""

    # pylint: disable=invalid-name
    @overload
    def LIMIT(self, offset: int, limit: int) -> T:
        """Alias for limit() to be more SQL-like with all capitals."""

    # pylint: disable=invalid-name
    def LIMIT(self, offset_or_limit: int, limit: int = None) -> T:
        """Alias for limit() to be more SQL-like with all capitals."""
        return self.limit(offset_or_limit, limit)
