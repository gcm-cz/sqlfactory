from typing import Any

from ..statement import Statement
from .base import Function


class Ascii(Function):
    """Numeric ASCII value of leftmost character."""
    def __init__(self, arg: Statement | Any):
        super().__init__("ASCII", arg)


class Bin(Function):
    """Returns binary value"""
    def __init__(self, num: Statement | Any):
        super().__init__("BIN", num)


class BitLength(Function):
    """Returns the length of a string in bits"""
    def __init__(self, s: Statement | Any):
        super().__init__("BIT_LENGTH", s)


class Char(Function):
    """Returns string based on the integer values for the individual characters."""
    def __init__(self, *n: Statement | int):
        super().__init__("CHAR", *n)


class CharLength(Function):
    """Length of the string in characters."""
    def __init__(self, s: Statement | Any):
        super().__init__("CHAR_LENGTH", s)


class Chr(Function):
    """Returns string based on integer values of the individual characters."""
    def __init__(self, n: Statement | int):
        super().__init__("CHR", n)


class Concat(Function):
    """Returns concatenated string"""
    def __init__(self, *s: Statement | Any):
        super().__init__("CONCAT", *s)


class ConcatWs(Function):
    """Concatenate with separator"""
    def __init__(self, separator: Statement | Any, *s: Statement | Any):
        super().__init__("CONCAT_WS", separator, *s)


# TODO: Rest of string functions from https://mariadb.com/kb/en/string-functions/
