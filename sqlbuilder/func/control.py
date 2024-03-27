from typing import Any

from ..statement import Statement
from .base import Function


class IfNull(Function):
    def __init__(self, *args: Statement | Any):
        super().__init__("IFNULL", *args)


class NullIf(Function):
    def __init__(self, expr1: Statement | Any, expr2: Statement | Any):
        super().__init__("NULLIF", expr1, expr2)


class If(Function):
    def __init__(self, expr: Statement | Any, if_true: Statement | Any, if_false: Statement | Any):
        super().__init__("IF", expr, if_true, if_false)
