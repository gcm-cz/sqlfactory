from typing import Any, Collection, Generic, Self, TypeVar, overload

from ..condition import ConditionBase
from ..entities import Table
from ..statement import Statement

T = TypeVar("T")


class Join(Statement):
    """
    Produces `JOIN` statement

    Usage:

    >>> Join("table2", on=Eq("table1.id", "table2.id"))
    >>> "JOIN `table2` ON `table1`.`id` = `table2`.`id`"

    >>> Join("table2", on=Eq("table1.id", "t2.id"), alias="t2")
    >>> "JOIN `table2` AS `t2` ON `table1`.`id` = `t2`.`id`"
    """

    def __init__(self, table: str | Table, on: ConditionBase | None = None, alias: str | None = None) -> None:
        """
        :param table: Table to be joined
        :param on: ON condition
        :param alias: Optional alias of the joined table.
        """
        if isinstance(table, str):
            table = Table(table)

        self.table = table
        """Table to be joined"""

        self.on = on
        """ON join condition"""

        self.alias = alias
        """Optional alias for the joined table."""

    @property
    def join_spec(self) -> str:
        """
        Returns the JOIN type itself for generation of SQL query.
        @private
        """
        return "JOIN"

    def __str__(self) -> str:
        if self.alias:
            table = f"{self.table!s} AS `{self.alias}`"
        else:
            table = str(self.table)

        if self.on:
            return f"{self.join_spec} {table} ON {self.on!s}"

        return f"{self.join_spec} {table}"

    @property
    def args(self) -> list[Any]:
        """Argument values of the JOIN statement."""
        return self.on.args if self.on else []


class LeftJoin(Join):
    """
    Produces `LEFT JOIN` statement

    Usage:

    >>> LeftJoin("table2", on=Eq("table1.id", "table2.id"))
    >>> "LEFT JOIN `table2` ON `table1`.`id` = `table2`.`id`"
    """

    @property
    def join_spec(self) -> str:
        return "LEFT JOIN"


class LeftOuterJoin(Join):
    """
    Produces `LEFT OUTER JOIN` statement

    Usage:

    >>> LeftOuterJoin("table2", on=Eq("table1.id", "table2.id"))
    >>> "LEFT OUTER JOIN `table2` ON `table1`.`id` = `table2`.`id`"
    """

    @property
    def join_spec(self) -> str:
        return "LEFT OUTER JOIN"


class RightJoin(Join):
    """
    Produces `RIGHT JOIN` statement

    Usage:

    >>> RightJoin("table2", on=Eq("table1.id", "table2.id"))
    >>> "RIGHT JOIN `table2` ON `table1`.`id` = `table2`.`id`"
    """

    @property
    def join_spec(self) -> str:
        return "RIGHT JOIN"


class RightOuterJoin(Join):
    """
    Produces `RIGHT OUTER JOIN` statement

    Usage:

    >>> RightOuterJoin("table2", on=Eq("table1.id", "table2.id"))
    >>> "RIGHT OUTER JOIN `table2` ON `table1`.`id` = `table2`.`id`"
    """

    @property
    def join_spec(self) -> str:
        return "RIGHT OUTER JOIN"


class InnerJoin(Join):
    """
    Produces `INNER JOIN` statement

    Usage:

    >>> InnerJoin("table2", on=Eq("table1.id", "table2.id"))
    >>> "INNER JOIN `table2` ON `table1`.`id` = `table2`.`id`"
    """

    @property
    def join_spec(self) -> str:
        return "INNER JOIN"


class CrossJoin(Join):
    """
    Produces `CROSS JOIN` statement

    Usage:

    >>> CrossJoin("table2", on=Eq("table1.id", "table2.id"))
    >>> "CROSS JOIN `table2` ON `table1`.`id` = `table2`.`id`"
    """

    @property
    def join_spec(self) -> str:
        return "CROSS JOIN"


class WithJoin(Generic[T]):
    """Mixin to provide JOIN support for query generator."""

    def __init__(self, *args: Any, join: Collection[Join] | None = None, **kwargs: Any) -> None:
        """
        :param join: List of JOIN clauses
        """
        super().__init__(*args, **kwargs)
        self._join = list(join) if join is not None else []

    def _append_join(self, join: Join) -> Self:
        """Append join to list of joins."""
        if not self._join:
            self._join = []

        if join not in self._join:
            self._join.append(join)

        return self

    @overload
    def join(self, join: Join, /) -> Self:
        """Append JOIN clause to the query (any Join instance)."""

    @overload
    def join(self, table: str | Table, on: ConditionBase | None = None, alias: str | None = None) -> Self:
        """Append JOIN clause to the query.
        JOIN `table` AS <alias> ON (<condition>)"""

    def join(self, table: str | Table | Join, on: ConditionBase | None = None, alias: str | None = None) -> Self:
        """Append JOIN clause to the query.
        JOIN `table` AS <alias> ON (<condition>)
        """
        if isinstance(table, Join):
            if on is not None or alias is not None:
                raise AttributeError("When passing Join instance directly, on or alias attributes cannot be specified.")

            return self._append_join(table)

        return self._append_join(Join(table, on, alias))

    @overload
    def JOIN(self, join: Join, /) -> Self:  # pylint: disable=invalid-name
        """Alias for join() to be more SQL-like with all capitals."""

    @overload
    def JOIN(self, table: str | Table, on: ConditionBase | None = None, alias: str | None = None) -> Self:
        # pylint: disable=invalid-name
        """Alias for join() to be more SQL-like with all capitals."""

    def JOIN(self, table: str | Table | Join, on: ConditionBase | None = None, alias: str | None = None) -> Self:
        # pylint: disable=invalid-name
        """Alias for join() to be more SQL-like with all capitals."""
        return self.join(table, on, alias)  # type: ignore[arg-type]  # mypy searches in overloads

    def left_join(self, table: str, on: ConditionBase | None = None, alias: str | None = None) -> Self:
        """Append LEFT JOIN clause to the query."""
        return self.join(LeftJoin(table, on, alias))

    def LEFT_JOIN(self, table: str, on: ConditionBase | None = None, alias: str | None = None) -> Self:
        # pylint: disable=invalid-name
        """Alias for left_join() to be more SQL-like with all capitals."""
        return self.left_join(table, on, alias)
