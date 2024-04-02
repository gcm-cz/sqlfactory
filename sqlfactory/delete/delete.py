"""DELETE statement builder"""

from typing import Any

from ..entities import Table
from ..condition.base import ConditionBase
from ..execute import ExecutableStatementWithArgs
from ..mixins.limit import WithLimit, Limit
from ..mixins.order import WithOrder, OrderArg
from ..mixins.where import WithWhere


# pylint: disable=too-many-ancestors  # This is intentional, as this class is a combination of multiple mixins.
class Delete(ExecutableStatementWithArgs, WithWhere['Delete'], WithOrder['Delete'], WithLimit['Delete']):
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
        """
        :param table: Table to delete from
        :param where: WHERE condition
        :param order: Ordering of matched rows, usefull when limiting number of deleted rows.
        :param limit: Limit number of deleted rows.
        """
        super().__init__(where=where, order=order, limit=limit)
        self.table = table if isinstance(table, Table) else Table(table)

    def __str__(self):
        """Construct the DELETE statement."""
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
        """DELETE statement arguments."""
        return (
            (self._where.args if self._where else []) +
            (self._order.args if self._order else []) +
            (self._limit.args if self._limit else [])
        )


# Alias to provide better SQL compatibility
DELETE = Delete
