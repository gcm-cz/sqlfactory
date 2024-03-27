from typing import TypeVar, Generic, overload

from sqlbuilder.statement import StatementWithArgs

T = TypeVar("T")


class Limit(StatementWithArgs):
    @overload
    def __init__(self):
        """No LIMIT statement"""

    @overload
    def __init__(self, limit: int):
        """Just a LIMIT statement without offset"""

    @overload
    def __init__(self, offset: int, limit: int):
        """LIMIT statement with both offset and limit"""

    def __init__(self, offset: int = None, limit: int = None):
        if limit is None:
            limit = offset
            offset = None

        self.offset = offset
        self.limit = limit

    def __str__(self) -> str:
        if self.offset is not None:
            return f"LIMIT %s, %s"
        elif self.limit is not None:
            return f"LIMIT %s"
        else:
            return ""

    def __bool__(self) -> bool:
        return self.offset is not None or self.limit is not None

    @property
    def args(self) -> list[int]:
        if self.offset is not None:
            return [self.offset, self.limit]
        elif self.limit is not None:
            return [self.limit]
        else:
            return []


class WithLimit(Generic[T]):
    """Mixin to provide LIMIT support for query generator."""
    def __init__(self, *args, limit: Limit = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._limit = limit

    def limit(self, offset_or_limit: int, limit: int = None) -> T:
        if self._limit is not None:
            raise AttributeError("Limit has already been specified.")

        self._limit = Limit(offset_or_limit, limit) if limit is not None else Limit(limit=offset_or_limit)
        return self

    def LIMIT(self, offset_or_limit: int, limit: int = None) -> T:
        """Alias for limit() to be more SQL-like with all capitals."""
        return self.limit(offset_or_limit, limit)
