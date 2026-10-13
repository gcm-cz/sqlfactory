"""DELETE statement builder"""

from typing import Any, Collection, TypeAlias

from sqlfactory.condition.base import ConditionBase
from sqlfactory.dialect import SQLDialect
from sqlfactory.entities import Table
from sqlfactory.execute import ExecutableStatement
from sqlfactory.mixins.join import WithJoin
from sqlfactory.mixins.limit import Limit, WithLimit
from sqlfactory.mixins.order import OrderArg, WithOrder
from sqlfactory.mixins.where import WithWhere
from sqlfactory.select.aliased import Aliased, TableReference, table_reference
from sqlfactory.select.join import Join


class Delete(ExecutableStatement, WithWhere, WithOrder, WithLimit, WithJoin):
    """
    `DELETE` statement

    Usage:

    >>> from sqlfactory import Delete, In
    >>> Delete("table", where=In("id", [1, 2, 3]))
    >>> "DELETE FROM `table` WHERE `id` IN (1,2,3)"

    More advanced DELETE with JOINs is also supported:

    >>> from sqlfactory import Delete, Join, Eq
    >>> Delete("table", delete=["table"], join=[Join("table2", on=Eq("table.id", "table2.id"))], where=Eq("table2.value", 10))
    >>> "DELETE `table` FROM `table` JOIN `table2` ON `table`.`id` = `table2`.`id` WHERE `table2`.`value` = 10"

    The table can be aliased. With JOINs, list the alias in `delete` (multi-table syntax, supported by MySQL and MariaDB):

    >>> from sqlfactory import Delete, Aliased, Table, LeftJoin, Eq, Gt, Column, IsNotNull
    >>> Delete(
    ...     Aliased(Table("h"), alias="t"),
    ...     delete=["t"],
    ...     join=[LeftJoin("h", alias="x", on=Eq("x.grp", Column("t.grp")) & Gt("x.ver", Column("t.ver")))],
    ...     where=IsNotNull("x.id"),
    ... )
    >>> "DELETE `t` FROM `h` AS `t` LEFT JOIN `h` AS `x` ON (`x`.`grp` = `t`.`grp` AND `x`.`ver` > `t`.`ver`) "
    ... "WHERE `x`.`id` IS NOT NULL"

    Without `delete`, an aliased table renders the single-table form `DELETE FROM <table> AS <alias> ...`, which not every
    server accepts (MySQL supports it since 8.0.16, check your MariaDB version) - use the multi-table form above
    (`delete=["<alias>"]`) for portability.
    """

    def __init__(
        self,
        table: TableReference,
        where: ConditionBase | None = None,
        order: OrderArg | None = None,
        limit: Limit | None = None,
        *,
        delete: Collection[Table | str] | None = None,
        join: Collection[Join] | None = None,
        dialect: SQLDialect | None = None,
    ) -> None:
        """
        :param table: Table to delete from (name, `Table` or `Aliased(Table(...), alias=...)`).
        :param where: WHERE condition
        :param order: Ordering of matched rows, usefull when limiting number of deleted rows.
        :param limit: Limit number of deleted rows.
        """
        super().__init__(where=where, order=order, limit=limit, join=join, dialect=dialect)

        self.table: Table | Aliased = table_reference(table, "DELETE")
        """Main table to delete from."""

        if delete is not None and (not isinstance(delete, Collection) or isinstance(delete, (str, bytes))):
            raise TypeError("delete argument must be a collection of tables to delete from")

        self.delete = [d if isinstance(d, Table) else Table(d) for d in delete] if delete is not None else []
        """When using join, specify tables to delete from to prevent deleting from joined tables."""

    def __str__(self) -> str:
        """Construct the DELETE statement."""
        with self.dialect:
            q: list[str] = []

            if not self.delete:
                q.append(f"DELETE FROM {self.table!s}")
            else:
                q.append(f"DELETE {', '.join(str(t) for t in self.delete)} FROM {self.table!s}")

            if self._join:
                q.extend(map(str, self._join))

            if self._where:
                q.append("WHERE")
                q.append(str(self._where))

            if self._order:
                q.append(str(self._order))

            if self._limit:
                q.append(str(self._limit))

            return " ".join(q)

    @property
    def args(self) -> list[Any]:
        """DELETE statement arguments."""
        out = []

        if self._join:
            for join in self._join:
                out.extend(join.args)

        return (
            out
            + (self._where.args if self._where else [])
            + (self._order.args if self._order else [])
            + (self._limit.args if self._limit else [])
        )


DELETE: TypeAlias = Delete  # pylint: disable=invalid-name
"""
Alias for `Delete` statement to provide better SQL compatibility, as SQL is often written in all caps.
"""
