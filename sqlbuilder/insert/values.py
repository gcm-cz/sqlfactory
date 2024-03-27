from ..column import ColumnArg, Column
from ..func.base import Function


class Values(Function):
    """
    VALUES(<column>) for usage in INSERT INTO ... ON DUPLICATE KEY UPDATE column = VALUES(column) statements.
    """
    def __init__(self, column: ColumnArg):
        if not isinstance(column, Column):
            column = Column(column)

        super().__init__("VALUES", column)
