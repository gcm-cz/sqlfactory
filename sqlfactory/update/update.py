"""UPDATE statement builder."""

from __future__ import annotations

from typing import Any, Collection, Mapping, Optional, Self, TypeAlias

from sqlfactory.condition.base import ConditionBase
from sqlfactory.dialect import SQLDialect
from sqlfactory.entities import Column, ColumnArg, Table
from sqlfactory.execute import ConditionalExecutableStatement
from sqlfactory.mixins.join import Join, WithJoin
from sqlfactory.mixins.limit import Limit, WithLimit
from sqlfactory.mixins.order import OrderArg, WithOrder
from sqlfactory.mixins.where import WithWhere
from sqlfactory.select.aliased import Aliased, TableReference, table_reference
from sqlfactory.statement import Statement, operand


class UpdateColumn(Statement):
    """
    Represents one field that should be updated.
    """

    def __init__(self, column: ColumnArg, value: Statement | Any) -> None:
        super().__init__()

        self._column = column if isinstance(column, Column) else Column(column)
        self._value = value

    def __str__(self) -> str:
        return f"{self._column!s} = {operand(self._value) if isinstance(self._value, Statement) else self.dialect.placeholder}"

    def __hash__(self) -> int:
        return hash(self._column)

    def __eq__(self, other: UpdateColumn | Any) -> bool:
        if not isinstance(other, UpdateColumn):
            return False

        return str(self._column) == str(other._column)

    @property
    def args(self) -> list[Any]:
        """
        Return arguments for the update statement.
        """
        if isinstance(self._value, Statement):
            return self._value.args

        return [self._value]


class Update(ConditionalExecutableStatement, WithWhere, WithLimit, WithOrder, WithJoin):
    # pylint: disable=too-many-ancestors
    """
    Builds `UPDATE` statement SQL query.

    This is conditional SQL statement, so you can check whether it should be executed (would update any columns)
    by calling bool() on it. Also, if you are using execute() method of the statement, the execution won't be
    performed if bool() returns False.

    Examples:

    >>> from sqlfactory import Update, Eq
    >>> upd = Update("table").set("column1", 1).where(Eq("column2", 2))
    >>> str(upd)
    'UPDATE `table` SET `column1` = %s WHERE `column2` = %s'
    >>> upd.args
    [1, 2]

    >>> from sqlfactory import Update, Table
    >>> t = Table("table")
    >>> upd = Update(t).set(t.column1, 1).where(t.column2 == 2)
    >>> str(upd)
    'UPDATE `table` SET `table`.`column1` = %s WHERE `table`.`column2` = %s'
    >>> upd.args
    [1, 2]

    >>> from sqlfactory import Update
    >>> upd = Update("table", set={"column1": 1}, where=Eq("column2", 2))
    >>> str(upd)
    'UPDATE `table` SET `column1` = %s WHERE `column2` = %s'
    >>> upd.args
    [1, 2]

    >>> from sqlfactory import Update, UpdateColumn
    >>> upd = Update("table", UpdateColumn("column1", 1), where=Eq("column2", 2))
    >>> str(upd)
    'UPDATE `table` SET `column1` = %s WHERE `column2` = %s'
    >>> upd.args
    [1, 2]

    >>> from sqlfactory import Update
    >>> upd = Update(
    ...     ["table1", "table2"],
    ...     set={"table1.value": "foo", "table2.value": "bar"},
    ...     where=Eq("table1.id", Column("table2.id"))
    ... )
    >>> str(upd)
    'UPDATE `table1`, `table2` SET `table1`.`value` = %s, `table2`.`value` = %s WHERE `table1`.`id` = `table2`.`id`'
    >>> upd.args
    ['foo', 'bar']

    >>> from sqlfactory import Update, Join, Eq
    >>> upd = Update(
    ...     "table1",
    ...     join=[Join("table2", Eq("table1.id", Column("table2.id")))],
    ...     set={"table1.value": "foo", "table2.value": "bar"}
    ... )
    >>> str(upd)
    'UPDATE `table1` JOIN `table2` ON `table1`.`id` = `table2`.`id` SET `table1`.`value` = %s, `table2`.`value` = %s'
    >>> upd.args
    ['foo', 'bar']

    The target table can be aliased (`UPDATE <table> AS <alias>`, valid in single- and multi-table UPDATE in MySQL / MariaDB).
    Once aliased, reference its columns through the alias:

    >>> from sqlfactory import Update, Aliased, Table, Eq
    >>> upd = Update(Aliased(Table("h"), alias="t"), set={"t.col": 1}, where=Eq("t.id", 5))
    >>> str(upd)
    'UPDATE `h` AS `t` SET `t`.`col` = %s WHERE `t`.`id` = %s'
    >>> upd.args
    [1, 5]

    **Recipe - guarded UPDATE via self-join (anti-join):** to update only rows for which no "newer" row of the same table
    exists, LEFT JOIN the target table to itself under an alias and keep the rows where the joined side is missing
    (`WHERE x.id IS NULL`). The target may be aliased (below) or left unaliased (`Update("h", ...)`, referencing `h.<column>`);
    the joined copy must be aliased. This form is valid in MySQL / MariaDB, whereas the same guard written as a subquery on the
    target table (`WHERE NOT EXISTS (SELECT ... FROM h ...)`, `WHERE id IN (SELECT ... FROM h ...)`) is rejected with
    error 1093 ("You can't specify target table 'h' for update in FROM clause").

    >>> from sqlfactory import Update, Aliased, Table, LeftJoin, Eq, Gt, Column, IsNull
    >>> upd = Update(
    ...     Aliased(Table("h"), alias="t"),
    ...     join=[LeftJoin("h", alias="x", on=Eq("x.grp", Column("t.grp")) & Gt("x.ver", Column("t.ver")))],
    ...     set={"t.latest": True},
    ...     where=IsNull("x.id"),
    ... )
    >>> str(upd)  # doctest: +NORMALIZE_WHITESPACE
    'UPDATE `h` AS `t` LEFT JOIN `h` AS `x` ON (`x`.`grp` = `t`.`grp` AND `x`.`ver` > `t`.`ver`)
     SET `t`.`latest` = %s WHERE `x`.`id` IS NULL'
    >>> upd.args
    [True]

    Note: `Eq`, `Gt` and other conditions read a bare `str` as a column name on the left side, but bind it as a value on the
    right side - hence `Column("t.grp")` above. See the package documentation for the full rule.
    """

    def __init__(
        self,
        table: TableReference | Collection[TableReference],
        *fields: UpdateColumn,
        join: Collection[Join] | None = None,
        set: Optional[Mapping[str | Column, Any]] = None,  # noqa: A002
        where: Optional[ConditionBase] = None,
        order: OrderArg | None = None,
        limit: Optional[Limit] = None,
        dialect: SQLDialect | None = None,
    ) -> None:
        # pylint: disable=redefined-builtin
        """
        :param table: Table to update (name, `Table` or `Aliased(Table(...), alias=...)`). Or multiple tables, if collection is
            used.
        :param fields: List of UpdateColumn instances containing columns to be updated. This is not very pleasant way
            to create the statement, use set() method instead.
        :param join: Optional join to update multiple tables.
        :param set: Mapping of column names to values to be set. Alternative to specifying columns as UpdateColumn variable
            arguments. You can also use set() method on the Update instance to add another columns to be updated.
        :param where: WHERE condition
        :param order: Optional ordering of the updated rows. Might be needed to avoid violating keys when updating multiple rows.
        :param limit: Limit number of updated rows
        """
        super().__init__(join=join, where=where, order=order, limit=limit, dialect=dialect)

        # Elements are validated by table_reference(), so the collection itself does not need precise type here.
        tables: Collection[Any] = [table] if isinstance(table, (str, Statement)) or not isinstance(table, Collection) else table

        self.table: list[Table | Aliased] = [table_reference(t, "UPDATE") for t in tables]
        """Tables that should be updated."""

        self.fields: list[UpdateColumn] = list(fields)
        """Fields that should be updated."""

        if set:
            for column, value in set.items():
                self.set(column, value)

    def __str__(self) -> str:
        """
        Return the UPDATE statement with %s placeholders for arguments.
        """
        with self.dialect:
            if not self.fields:
                raise AttributeError("At least one column must be updated.")

            query = [f"UPDATE {', '.join(str(t) for t in self.table)}"]

            if self._join:
                query.extend(map(str, self._join))

            query.append(f"SET {', '.join(map(str, self.fields))}")

            if self._where:
                query.append("WHERE")
                query.append(str(self._where))

            if self._order:
                query.append(str(self._order))

            if self._limit:
                query.append(str(self._limit))

            return " ".join(query)

    @property
    def args(self) -> list[Any]:
        """
        Return all arguments used in the UPDATE statement.
        """
        out = []

        if self._join:
            for join in self._join:
                out.extend(join.args)

        for field in self.fields:
            out.extend(field.args)

        if self._where is not None:
            out.extend(self._where.args)

        if self._order is not None:
            out.extend(self._order.args)

        if self._limit is not None:
            out.extend(self._limit.args)

        return out

    def __bool__(self) -> bool:
        """
        Return True if there are any fields to be updated and the statement should be executed.
        """
        return bool(self.fields)

    def append(self, field: UpdateColumn) -> Self:
        """
        Append new UpdateField to this UPDATE statement. Can be used when set() method is not sufficient.
        """
        if field in self.fields:
            raise AttributeError(f"Field '{field}' is already in the list of fields to be updated.")

        self.fields.append(field)
        return self

    def set(self, field: ColumnArg, value: Statement | Any) -> Self:
        """
        Syntactical sugar for creating simple SET UpdateFields.
        :param field: Field name (without quotes).
        :param value: Value to set the field to (will be escaped).
        """
        return self.append(UpdateColumn(field, value))

    def SET(self, field: str, value: Any) -> Self:
        # pylint: disable=invalid-name
        """Alias for `Update.set()` for better SQL compatibility (SQL is often written in all caps)."""
        return self.set(field, value)


UPDATE: TypeAlias = Update  # pylint: disable=invalid-name
"""
Alias for `Update` statement to provide better SQL compatibility, as SQL is often written in all caps.
"""
