from typing import Any

from ..column import Table
from ..condition.base import ConditionBase
from ..execute import ExecutableStatementWithArgs
from ..mixins.limit import WithLimit, Limit
from ..mixins.order import WithOrder, OrderArg
from ..mixins.where import WithWhere


class Delete(ExecutableStatementWithArgs, WithWhere, WithOrder, WithLimit):
    """
    DELETE statement

    >>> Delete("table", where=In("id", [1, 2, 3]))
    >>> "DELETE FROM `table` WHERE `id` IN (1,2,3)"
    """
    def __init__(
            self,
            table: Table | str,
            where: ConditionBase = None,
            order: OrderArg = None,
            limit: Limit = None
    ):
        super().__init__(where=where, order=order, limit=limit)
        self.table = table if isinstance(table, Table) else Table(table)

    def __str__(self):
        q = [f"DELETE FROM {str(self.table)}"]

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
        return (
            (self._where.args if self._where else []) +
            (self._order.args if self._order else []) +
            (self._limit.args if self._limit else [])
        )


# Alias to provide better SQL compatibility
DELETE = Delete
