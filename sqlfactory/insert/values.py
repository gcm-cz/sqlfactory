"""VALUES() function for usage in ON DUPLICATE KEY UPDATE statements. MySQL / MariaDB specific."""

from ..entities import ColumnArg, Column
from ..func.base import Function


# pylint: disable=too-few-public-methods  # Too few public methods, as everything is handled by super class.
class Values(Function):
    """
    VALUES(<column>) for usage in INSERT INTO ... ON DUPLICATE KEY UPDATE column = VALUES(column) statements.
    """
    def __init__(self, column: ColumnArg):
        if not isinstance(column, Column):
            column = Column(column)

        super().__init__("VALUES", column)
