"""Numeric SQL functions (https://mariadb.com/kb/en/numeric-functions/)"""
from typing import Any, overload

from sqlfactory.func.base import Function


# pylint: disable=too-few-public-methods
class Div(Function):
    """
    Integer division.
    """
    def __init__(self, dividend: Any, divisor: Any):
        super().__init__("DIV", dividend, divisor)


# pylint: disable=too-few-public-methods
class Abs(Function):
    """
    Absolute value.
    """
    def __init__(self, value: Any):
        super().__init__("ABS", value)


# pylint: disable=too-few-public-methods
class ACos(Function):
    """
    Arc cosine.
    """
    def __init__(self, value: Any):
        super().__init__("ACOS", value)


# pylint: disable=too-few-public-methods
class ASin(Function):
    """
    Arc sine.
    """
    def __init__(self, value: Any):
        super().__init__("ASIN", value)


# pylint: disable=too-few-public-methods
class ATan(Function):
    """
    Arc tangent.
    """
    def __init__(self, value: Any):
        super().__init__("ATAN", value)


# pylint: disable=too-few-public-methods
class ATan2(Function):
    """
    Arc tangent of two variables.
    """
    def __init__(self, y: Any, x: Any):
        super().__init__("ATAN2", y, x)


# pylint: disable=too-few-public-methods
class Ceil(Function):
    """
    Ceiling value.
    """
    def __init__(self, value: Any):
        super().__init__("CEIL", value)


# pylint: disable=too-few-public-methods
class Ceiling(Function):
    """
    Ceiling value.
    """
    def __init__(self, value: Any):
        super().__init__("CEILING", value)


# pylint: disable=too-few-public-methods
class Conv(Function):
    """
    Convert number from one base to another.
    """
    def __init__(self, number: Any, from_base: Any, to_base: Any):
        super().__init__("CONV", number, from_base, to_base)


# pylint: disable=too-few-public-methods
class Cos(Function):
    """
    Cosine.
    """
    def __init__(self, value: Any):
        super().__init__("COS", value)


# pylint: disable=too-few-public-methods
class Cot(Function):
    """
    Cotangent.
    """
    def __init__(self, value: Any):
        super().__init__("COT", value)


# pylint: disable=too-few-public-methods
class Crc32(Function):
    """
    Computes a cyclic redundancy check (CRC) value.
    """
    def __init__(self, value: Any):
        super().__init__("CRC32", value)


# pylint: disable=too-few-public-methods
class Crc32C(Function):
    """
    Computes a cyclic redundancy check (CRC) value using the Castagnoli polynomial
    """
    def __init__(self, value: Any):
        super().__init__("CRC32C", value)


# pylint: disable=too-few-public-methods
class Degrees(Function):
    """
    Converts radians to degrees.
    """
    def __init__(self, value: Any):
        super().__init__("DEGREES", value)


# pylint: disable=too-few-public-methods
class Exp(Function):
    """
    e raised to power of the argument
    """
    def __init__(self, value: Any):
        super().__init__("EXP", value)


# pylint: disable=too-few-public-methods
class Floor(Function):
    """
    Floor value.
    """
    def __init__(self, value: Any):
        super().__init__("FLOOR", value)


# pylint: disable=too-few-public-methods
class Greatest(Function):
    """
    Return the largest argument
    """
    def __init__(self, *args: Any):
        super().__init__("GREATEST", *args)


# pylint: disable=too-few-public-methods
class Least(Function):
    """
    Return the smallest argument
    """
    def __init__(self, *args: Any):
        super().__init__("LEAST", *args)


# pylint: disable=too-few-public-methods
class Ln(Function):
    """
    Natural logarithm
    """
    def __init__(self, value: Any):
        super().__init__("LN", value)


# pylint: disable=too-few-public-methods
class Log(Function):
    """
    Logarithm
    """
    @overload
    def __init__(self, value: Any): ...


    @overload
    def __init__(self, base: Any, value: Any): ...

    def __init__(self, arg1: Any, arg2: Any = None):
        if arg2 is not None:
            super().__init__("LOG", arg1, arg2)

        else:
            super().__init__("LOG", arg1)


# pylint: disable=too-few-public-methods
class Log10(Function):
    """
    Base-10 logarithm
    """
    def __init__(self, value: Any):
        super().__init__("LOG10", value)


# pylint: disable=too-few-public-methods
class Log2(Function):
    """
    Base-2 logarithm
    """
    def __init__(self, value: Any):
        super().__init__("LOG2", value)


# pylint: disable=too-few-public-methods
class Mod(Function):
    """
    Modulo operation
    """
    def __init__(self, dividend: Any, divisor: Any):
        super().__init__("MOD", dividend, divisor)


# pylint: disable=too-few-public-methods
class Oct(Function):
    """
    Convert number to octal
    """
    def __init__(self, value: Any):
        super().__init__("OCT", value)


# pylint: disable=too-few-public-methods
class Pi(Function):
    """
    Return the value of pi
    """
    def __init__(self):
        super().__init__("PI")


# pylint: disable=too-few-public-methods
class Pow(Function):
    """
    Return X raised to power of Y.
    """
    def __init__(self, x: Any, y: Any):
        super().__init__("POW", x, y)


# pylint: disable=too-few-public-methods
class Power(Function):
    """
    Return X raised to power of Y.
    """
    def __init__(self, x: Any, y: Any):
        super().__init__("POWER", x, y)


# pylint: disable=too-few-public-methods
class Radians(Function):
    """
    Converts degrees to radians.
    """
    def __init__(self, value: Any):
        super().__init__("RADIANS", value)


# pylint: disable=too-few-public-methods
class Rand(Function):
    """
    Return a random floating-point value.
    """
    def __init__(self):
        super().__init__("RAND")


# pylint: disable=too-few-public-methods
class Round(Function):
    """
    Round the argument to the nearest integer.
    """
    def __init__(self, value: Any):
        super().__init__("ROUND", value)


# pylint: disable=too-few-public-methods
class Sign(Function):
    """
    Sign of the argument
    """
    def __init__(self, value: Any):
        super().__init__("SIGN", value)


# pylint: disable=too-few-public-methods
class Sin(Function):
    """
    Sine
    """
    def __init__(self, value: Any):
        super().__init__("SIN", value)


# pylint: disable=too-few-public-methods
class Sqrt(Function):
    """
    Square root
    """
    def __init__(self, value: Any):
        super().__init__("SQRT", value)


# pylint: disable=too-few-public-methods
class Tan(Function):
    """
    Tangent
    """
    def __init__(self, value: Any):
        super().__init__("TAN", value)


# pylint: disable=too-few-public-methods
class Truncate(Function):
    """
    Truncate the argument to D decimal places.
    """
    def __init__(self, value: Any, d: Any):
        super().__init__("TRUNCATE", value, d)


class BitCount(Function):
    """
    Return the number of bits that are set in the argument.
    """
    def __init__(self, value: Any):
        super().__init__("BIT_COUNT", value)
