# noqa: A005

"""SELECT statement builder."""

from __future__ import annotations

from collections.abc import Collection
from functools import reduce
from typing import Any, Self, overload

from ..condition.base import ConditionBase
from ..entities import ColumnArg, Table
from ..execute import ExecutableStatement
from ..mixins.limit import Limit, WithLimit
from ..mixins.order import OrderArg, WithOrder
from ..mixins.where import WithWhere
from ..statement import Statement
from .column_list import ColumnList
from .join import Join, LeftJoin


class Select(ExecutableStatement, WithWhere["Select"], WithOrder["Select"], WithLimit["Select"]):
    # pylint: disable=too-many-arguments  # Yes, SELECT is complex.
    """
    SELECT statement

    >>> from sqlfactory import Eq
    >>> cursor: Cursor = ...
    >>>
    >>> (Select("column1", "column2", "column3", table="table_name")
    >>>     .where(Eq("column1", 1))
    >>>     .order_by("column2")
    >>>     .limit(2, 10)
    >>>     .execute(cursor))

    Known limitations:
    - JOINs are not checked for uniqueness, so it is possible to add same JOIN multiple times. For now, it is up to
      user to ensure that JOINs are unique. This may be changed in the future, but it is not simple task, as joins
      needs to be in certain order.
    """

    def __init__(
        self,
        *columns: Statement | ColumnArg,
        select: ColumnList | None = None,
        table: Table | str | Statement | Collection[Table | str | Statement] | None = None,
        join: Collection[Join] | None = None,
        where: ConditionBase | None = None,
        group_by: ColumnList | Collection[Statement | ColumnArg] | None = None,
        having: ConditionBase | None = None,
        order: OrderArg | None = None,
        limit: Limit | None = None,
        for_update: bool = False,
    ) -> None:
        """
        :param columns: Columns to select.
        :param select: Columns to select as instance of ColumnList.
        :param table: Table to select from.
        :param join: Join statements
        :param where: Where condition
        :param group_by: Group by columns
        :param having: Having condition
        :param order: Order by columns
        :param limit: Limit results
        :param for_update: Lock rows for update
        """
        super().__init__(where=where, order=order, limit=limit)

        if columns and select:
            raise AttributeError("Cannot specify individual columns when attribute select is present.")

        if select and not isinstance(select, ColumnList):
            raise TypeError("Select argument must be instance of ColumnList.")

        self.columns = select or ColumnList(columns)

        if not table:
            raise AttributeError("Missing required keyword argument table.")

        if not isinstance(table, Collection) or isinstance(table, str):
            table = [table]

        self.table: list[Statement] = [Table(t) if isinstance(t, str) else t for t in table]
        self._join = list(join) if join is not None else None
        self._group_by = ColumnList(group_by) if group_by is not None and not isinstance(group_by, ColumnList) else group_by
        self._having = having
        self._for_update = for_update

    def add(self, column: Statement | Any) -> Self:
        """Add new statement or column to the set of selected columns"""
        self.columns.add(column)
        return self

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
    def JOIN(self, table: str | Table, on: ConditionBase | None = None, alias: str | None = None) -> Self:  # pylint: disable=invalid-name
        """Alias for join() to be more SQL-like with all capitals."""

    def JOIN(self, table: str | Table | Join, on: ConditionBase | None = None, alias: str | None = None) -> Self:  # pylint: disable=invalid-name
        """Alias for join() to be more SQL-like with all capitals."""
        return self.join(table, on, alias)  # type: ignore[arg-type]  # mypy searches in overloads

    def left_join(self, table: str, on: ConditionBase | None = None, alias: str | None = None) -> Self:
        """Append LEFT JOIN clause to the query."""
        return self.join(LeftJoin(table, on, alias))

    # pylint: disable=invalid-name
    def LEFT_JOIN(self, table: str, on: ConditionBase | None = None, alias: str | None = None) -> Self:
        """Alias for left_join() to be more SQL-like with all capitals."""
        return self.left_join(table, on, alias)

    def group_by(self, column: Statement | ColumnArg, *columns: Statement | ColumnArg) -> Self:
        """
        GROUP BY clause.

        >>> Select().group_by("column1", "column2", "column3")
        """
        if self._group_by is not None:
            raise AttributeError("GROUP BY has already been specified.")

        self._group_by = ColumnList([column, *list(columns)])
        return self

    # pylint: disable=invalid-name
    def GROUP_BY(self, column: Statement | ColumnArg, *columns: Statement | ColumnArg) -> Self:
        """Alias for group_by() to be more SQL-like with all capitals."""
        return self.group_by(column, *columns)

    def having(self, condition: ConditionBase) -> Self:
        """HAVING clause"""
        self._having = condition
        return self

    # pylint: disable=invalid-name
    def HAVING(self, condition: ConditionBase) -> Self:
        """Alias for having() to be more SQL-like with all capitals."""
        return self.having(condition)

    def __str__(self) -> str:
        out: list[str] = ["SELECT", str(self.columns) if self.columns else "*", f"FROM {', '.join(map(str, self.table))}"]

        if self._join:
            out.extend(map(str, self._join))

        if self._where:
            out.append("WHERE")
            out.append(str(self._where))

        if self._group_by:
            out.append("GROUP BY")
            out.append(str(self._group_by))

        if self._having:
            out.append("HAVING")
            out.append(str(self._having))

        if self._order:
            out.append(str(self._order))

        if self._limit:
            out.append(str(self._limit))

        if self._for_update:
            out.append("FOR UPDATE")

        return " ".join(out)

    @property
    def args(self) -> list[Any]:
        """Argument values for the SELECT statement."""
        out = self.columns.args

        if self._join:
            for join in self._join:
                out.extend(join.args)

        return (
            out
            + reduce(lambda acc, t: acc + (t.args if isinstance(t, Statement) else []), self.table, [])
            + (self._where.args if self._where else [])
            + (self._group_by.args if self._group_by else [])
            + (self._having.args if self._having else [])
            + (self._order.args if self._order else [])
            + (self._limit.args if self._limit else [])
        )


SELECT = Select
