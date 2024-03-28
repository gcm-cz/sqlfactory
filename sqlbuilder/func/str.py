"""String functions (https://mariadb.com/kb/en/string-functions/)"""

from typing import Any

from ..statement import Statement
from .base import Function


# pylint: disable=too-few-public-methods
class Ascii(Function):
    """Numeric ASCII value of leftmost character."""
    def __init__(self, arg: Statement | Any):
        super().__init__("ASCII", arg)


# pylint: disable=too-few-public-methods
class Bin(Function):
    """Returns binary value"""
    def __init__(self, num: Statement | Any):
        super().__init__("BIN", num)


# pylint: disable=too-few-public-methods
class BitLength(Function):
    """Returns the length of a string in bits"""
    def __init__(self, s: Statement | Any):
        super().__init__("BIT_LENGTH", s)


# pylint: disable=too-few-public-methods
class Char(Function):
    """Returns string based on the integer values for the individual characters."""
    def __init__(self, *n: Statement | int):
        super().__init__("CHAR", *n)


# pylint: disable=too-few-public-methods
class CharLength(Function):
    """Length of the string in characters."""
    def __init__(self, s: Statement | Any):
        super().__init__("CHAR_LENGTH", s)


# pylint: disable=too-few-public-methods
class Chr(Function):
    """Returns string based on integer values of the individual characters."""
    def __init__(self, n: Statement | int):
        super().__init__("CHR", n)


# pylint: disable=too-few-public-methods
class Concat(Function):
    """Returns concatenated string"""
    def __init__(self, *s: Statement | Any):
        super().__init__("CONCAT", *s)


# pylint: disable=too-few-public-methods
class ConcatWs(Function):
    """Concatenate with separator"""
    def __init__(self, separator: Statement | Any, *s: Statement | Any):
        super().__init__("CONCAT_WS", separator, *s)


# pylint: disable=too-few-public-methods
class Hex(Function):
    """Returns a hexadecimal string representation of a decimal or string value."""
    def __init__(self, n: Statement | Any):
        super().__init__("HEX", n)


# pylint: disable=too-few-public-methods
class InStr(Function):
    """Returns the position of the first occurrence of substring in string"""
    def __init__(self, s: Statement | Any, substring: Statement | Any):
        super().__init__("INSTR", s, substring)


# pylint: disable=too-few-public-methods
class Left(Function):
    """Returns the leftmost number of characters"""
    def __init__(self, s: Statement | Any, n: Statement | int):
        super().__init__("LEFT", s, n)


# pylint: disable=too-few-public-methods
class Length(Function):
    """Returns the length of a string"""
    def __init__(self, s: Statement | Any):
        super().__init__("LENGTH", s)


# pylint: disable=too-few-public-methods
class Locate(Function):
    """Returns the position of the first occurrence of substring in string"""
    def __init__(self, substring: Statement | Any, s: Statement | Any):
        super().__init__("LOCATE", substring, s)


# pylint: disable=too-few-public-methods
class Lower(Function):
    """Converts a string to lower-case"""
    def __init__(self, s: Statement | Any):
        super().__init__("LOWER", s)


# pylint: disable=too-few-public-methods
class Lpad(Function):
    """Left-pad a string with another string"""
    def __init__(self, s: Statement | Any, n: Statement | int, pad: Statement | Any):
        super().__init__("LPAD", s, n, pad)


# pylint: disable=too-few-public-methods
class Ltrim(Function):
    """Removes leading spaces"""
    def __init__(self, s: Statement | Any):
        super().__init__("LTRIM", s)


# pylint: disable=too-few-public-methods
class Mid(Function):
    """Returns a substring"""
    def __init__(self, s: Statement | Any, start: Statement | int, length: Statement | int):
        super().__init__("MID", s, start, length)


# pylint: disable=too-few-public-methods
class OctetLength(Function):
    """Returns the length of a string in bytes"""
    def __init__(self, s: Statement | Any):
        super().__init__("OCTET_LENGTH", s)


# pylint: disable=too-few-public-methods
class Ord(Function):
    """Numeric value of leftmost character"""
    def __init__(self, s: Statement | Any):
        super().__init__("ORD", s)


# pylint: disable=too-few-public-methods
class Repeat(Function):
    """Repeat a string the specified number of times"""
    def __init__(self, s: Statement | Any, n: Statement | int):
        super().__init__("REPEAT", s, n)


# pylint: disable=too-few-public-methods
class Replace(Function):
    """Replace occurrences of a specified string"""
    def __init__(self, s: Statement | Any, from_: Statement | Any, to: Statement | Any):
        super().__init__("REPLACE", s, from_, to)


# pylint: disable=too-few-public-methods
class Reverse(Function):
    """Reverse a string"""
    def __init__(self, s: Statement | Any):
        super().__init__("REVERSE", s)


# pylint: disable=too-few-public-methods
class Right(Function):
    """Returns the rightmost number of characters"""
    def __init__(self, s: Statement | Any, n: Statement | int):
        super().__init__("RIGHT", s, n)


# pylint: disable=too-few-public-methods
class RPad(Function):
    """Right-pad a string with another string"""
    def __init__(self, s: Statement | Any, n: Statement | int, pad: Statement | Any):
        super().__init__("RPAD", s, n, pad)


# pylint: disable=too-few-public-methods
class RTrim(Function):
    """Removes trailing spaces"""
    def __init__(self, s: Statement | Any):
        super().__init__("RTRIM", s)


# pylint: disable=too-few-public-methods
class SFormat(Function):
    """Format a string"""
    def __init__(self, format_: Statement | Any, *args: Statement | Any):
        super().__init__("SFORMAT", format_, *args)


# pylint: disable=too-few-public-methods
class Space(Function):
    """Returns a string of spaces"""
    def __init__(self, n: Statement | int):
        super().__init__("SPACE", n)


# pylint: disable=too-few-public-methods
class Substr(Function):
    """Returns a substring"""
    def __init__(self, s: Statement | Any, start: Statement | int, length: Statement | int):
        super().__init__("SUBSTR", s, start, length)


# pylint: disable=too-few-public-methods
class Substring(Function):
    """Returns a substring"""
    def __init__(self, s: Statement | Any, start: Statement | int, length: Statement | int):
        super().__init__("SUBSTRING", s, start, length)


# pylint: disable=too-few-public-methods
class SubstringIndex(Function):
    """Returns a substring"""
    def __init__(self, s: Statement | Any, delimiter: Statement | Any, count: Statement | int):
        super().__init__("SUBSTRING_INDEX", s, delimiter, count)


# pylint: disable=too-few-public-methods
class ToBase64(Function):
    """Converts a string to base64"""
    def __init__(self, s: Statement | Any):
        super().__init__("TO_BASE64", s)


# pylint: disable=too-few-public-methods
class ToChar(Function):
    """Converts a date/time/timestamp type expression to a string"""
    def __init__(self, n: Statement | Any):
        super().__init__("TO_CHAR", n)


# pylint: disable=too-few-public-methods
class Trim(Function):
    """Removes leading and trailing spaces"""
    def __init__(self, s: Statement | Any):
        super().__init__("TRIM", s)


# pylint: disable=too-few-public-methods
class Unhex(Function):
    """Converts a hexadecimal pairs of digits to the character represented by the number."""
    def __init__(self, s: Statement | Any):
        super().__init__("UNHEX", s)


# pylint: disable=too-few-public-methods
class Upper(Function):
    """Converts a string to upper-case"""
    def __init__(self, s: Statement | Any):
        super().__init__("UPPER", s)
