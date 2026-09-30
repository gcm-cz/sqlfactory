"""
Type conversion: `CAST(expr AS type)`, `CONVERT(expr, type)`, `CONVERT(expr USING charset)` and the `BINARY expr`
operator (https://mariadb.com/kb/en/cast/, https://mariadb.com/kb/en/convert/, https://mariadb.com/kb/en/binary-operator/).

The target type is a `CastType` member when it is a bare keyword, and a class when it takes parameters:

```python
Cast(JsonValue(Column("doc"), "$.accountId"), CastType.UNSIGNED)  # CAST(JSON_VALUE(`doc`, %s) AS UNSIGNED)
Cast(Column("price"), CastDecimal(10, 2))                         # CAST(`price` AS DECIMAL(10,2))
Cast(Column("name"), CastChar(charset="utf8mb4"))                 # CAST(`name` AS CHAR CHARACTER SET utf8mb4)
Convert(Column("name"), using="latin1")                           # CONVERT(`name` USING latin1)
Binary(Column("name")) == "abc"                                   # BINARY `name` = %s
```

MariaDB takes no placeholder inside a type, so its parameters (lengths, precisions, character set and collation names)
are part of the SQL text. They are validated before they get there: numbers must be `int`s, names must be bare
identifiers (a letter followed by letters, digits and underscores). Anything else raises `TypeError` / `ValueError`.
"""

import re
from enum import StrEnum
from typing import Any, ClassVar, Literal, overload

from sqlfactory.condition.base import ConditionBase
from sqlfactory.entities import Expression
from sqlfactory.statement import Statement, operand

_IDENTIFIER = re.compile(r"[A-Za-z][A-Za-z0-9_]*")


def _number(value: object) -> int:
    """Validate a length, precision or scale, which is spliced into the SQL of a type."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"Type parameter must be an int, got {value!r}.")

    if value < 0:
        raise ValueError(f"Type parameter must not be negative, got {value!r}.")

    return value


def _identifier(name: object) -> str:
    """Validate a character set or collation name, which is spliced into the SQL."""
    if not isinstance(name, str) or not _IDENTIFIER.fullmatch(name):
        raise ValueError(f"Character set or collation name must be a bare identifier, got {name!r}.")

    return name


class CastType(StrEnum):
    """
    Target type of `Cast` / `Convert` that is written as a bare keyword, e.g. `CAST(x AS UNSIGNED)`. A type with
    parameters is a class instead: `CastBinary`, `CastChar`, `CastVarchar`, `CastVarchar2`, `CastNChar`,
    `CastDecimal`, `CastDouble`, `CastTime`, `CastDatetime`, `CastIntervalDaySecond`.
    """

    BINARY = "BINARY"
    """`BINARY` - binary string. `CastBinary(N)` for `BINARY(N)`."""

    CHAR = "CHAR"
    """
    `CHAR` - character string in the character set and collation of the connection. `CastChar(...)` for a length, a
    character set or a collation.
    """

    NCHAR = "NCHAR"
    """`NCHAR` - character string in the national character set (utf8mb3). `CastNChar(N)` for `NCHAR(N)`."""

    DATE = "DATE"
    """`DATE`"""

    DATETIME = "DATETIME"
    """`DATETIME` - without fractional seconds. `CastDatetime(D)` for `DATETIME(D)`."""

    TIME = "TIME"
    """`TIME` - without fractional seconds. `CastTime(D)` for `TIME(D)`."""

    DECIMAL = "DECIMAL"
    """`DECIMAL` - `DECIMAL(10,0)`. `CastDecimal(M[, D])` for `DECIMAL(M[,D])`."""

    DOUBLE = "DOUBLE"
    """`DOUBLE`. `CastDouble(M, D)` for `DOUBLE(M,D)`."""

    FLOAT = "FLOAT"
    """`FLOAT`. MariaDB 10.4.5+."""

    INT = "INT"
    """`INT` - same as `SIGNED`."""

    INTEGER = "INTEGER"
    """`INTEGER` - same as `SIGNED`."""

    SIGNED = "SIGNED"
    """`SIGNED` - signed 64-bit integer."""

    SIGNED_INT = "SIGNED INT"
    """`SIGNED INT` - same as `SIGNED`."""

    SIGNED_INTEGER = "SIGNED INTEGER"
    """`SIGNED INTEGER` - same as `SIGNED`."""

    UNSIGNED = "UNSIGNED"
    """`UNSIGNED` - unsigned 64-bit integer."""

    UNSIGNED_INT = "UNSIGNED INT"
    """`UNSIGNED INT` - same as `UNSIGNED`."""

    UNSIGNED_INTEGER = "UNSIGNED INTEGER"
    """`UNSIGNED INTEGER` - same as `UNSIGNED`."""

    INET4 = "INET4"
    """`INET4` - IPv4 address. MariaDB 10.10+."""

    INET6 = "INET6"
    """`INET6` - IPv6 (or IPv4-mapped) address. MariaDB 10.5+."""

    UUID = "UUID"
    """`UUID`. MariaDB 10.7+."""

    XMLTYPE = "XMLTYPE"
    """`XMLTYPE`. MariaDB 12.3+."""


class _ParameterisedType:
    """Target type with parameters. Subclasses build the SQL of the type from validated parameters."""

    _sql: str

    def __str__(self) -> str:
        return self._sql


class CastBinary(_ParameterisedType):
    """
    `BINARY(N)` - binary string of at most `N` bytes; a shorter value is padded with `0x00` bytes. `CastType.BINARY`
    for `BINARY` without a length.
    """

    def __init__(self, length: int) -> None:
        self._sql = f"BINARY({_number(length)})"


class _CastString(_ParameterisedType):
    """
    Character string type with the attributes MariaDB accepts after it in a cast:
    `keyword[(N)] [CHARACTER SET charset] [BINARY | COLLATE collation]`.
    """

    _keyword: ClassVar[str]

    def _render(self, length: int | None, charset: str | None, collate: str | None, binary: bool) -> str:
        sql = self._keyword if length is None else f"{self._keyword}({_number(length)})"

        if charset is not None:
            sql += f" CHARACTER SET {_identifier(charset)}"

        if binary:
            sql += " BINARY"

        if collate is not None:
            sql += f" COLLATE {_identifier(collate)}"

        return sql


class CastChar(_CastString):
    """
    `CHAR[(N)] [CHARACTER SET charset] [BINARY | COLLATE collation]` - character string of at most `N` characters.

    Without a character set, the string is in the character set of the connection. `binary=True` renders `BINARY`,
    which selects the binary (`_bin`) collation of that character set; `collate="binary"` renders `COLLATE binary`,
    which is something else - the `binary` character set, i.e. a binary string. `collate="DEFAULT"` renders
    `COLLATE DEFAULT`, the default collation of the character set.

    ```python
    CastChar(10)                                            # CHAR(10)
    CastChar(charset="utf8mb4")                             # CHAR CHARACTER SET utf8mb4
    CastChar(10, charset="utf8mb4", collate="utf8mb4_bin")  # CHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin
    CastChar(charset="latin1", binary=True)                 # CHAR CHARACTER SET latin1 BINARY
    ```

    `CastType.CHAR` is the same as `CastChar()`.
    """

    _keyword = "CHAR"

    @overload
    def __init__(self, length: int | None = None, *, charset: str | None = None, collate: str | None = None) -> None:
        """`CHAR[(N)] [CHARACTER SET charset] [COLLATE collation]`"""

    @overload
    def __init__(self, length: int | None = None, *, charset: str | None = None, binary: Literal[True]) -> None:
        """`CHAR[(N)] [CHARACTER SET charset] BINARY`"""

    def __init__(
        self, length: int | None = None, *, charset: str | None = None, collate: str | None = None, binary: bool = False
    ) -> None:
        """
        :param length: Maximum number of characters, `CHAR(N)`.
        :param charset: Character set name, `CHARACTER SET charset`.
        :param collate: Collation name, `COLLATE collation`. Not together with `binary`.
        :param binary: `BINARY`, the binary collation of the character set. Not together with `collate`.
        """
        self._sql = self._render(length, charset, collate, binary)


class CastVarchar(_CastString):
    """
    `VARCHAR(N) [CHARACTER SET charset] [BINARY | COLLATE collation]` - character string of at most `N` characters.
    The length is required. Otherwise the same as `CastChar`. The KB lists it for Oracle mode; MariaDB 11.4 accepts
    it in any SQL mode.
    """

    _keyword = "VARCHAR"

    @overload
    def __init__(self, length: int, *, charset: str | None = None, collate: str | None = None) -> None:
        """`VARCHAR(N) [CHARACTER SET charset] [COLLATE collation]`"""

    @overload
    def __init__(self, length: int, *, charset: str | None = None, binary: Literal[True]) -> None:
        """`VARCHAR(N) [CHARACTER SET charset] BINARY`"""

    def __init__(self, length: int, *, charset: str | None = None, collate: str | None = None, binary: bool = False) -> None:
        """
        :param length: Maximum number of characters, `VARCHAR(N)`.
        :param charset: Character set name, `CHARACTER SET charset`.
        :param collate: Collation name, `COLLATE collation`. Not together with `binary`.
        :param binary: `BINARY`, the binary collation of the character set. Not together with `collate`.
        """
        self._sql = self._render(_number(length), charset, collate, binary)


class CastVarchar2(CastVarchar):
    """`VARCHAR2(N) [...]` - synonym of `CastVarchar`, in Oracle mode (`sql_mode=ORACLE`) only."""

    _keyword = "VARCHAR2"


class CastNChar(_ParameterisedType):
    """
    `NCHAR(N)` - character string of at most `N` characters in the national character set (utf8mb3). `CastType.NCHAR`
    for `NCHAR` without a length.
    """

    def __init__(self, length: int) -> None:
        self._sql = f"NCHAR({_number(length)})"


class CastDecimal(_ParameterisedType):
    """
    `DECIMAL(M[,D])` - fixed-point number with `M` digits in total, `D` of them after the decimal point (0 when
    omitted). `CastType.DECIMAL` for `DECIMAL` without parameters.
    """

    def __init__(self, precision: int, scale: int | None = None) -> None:
        """
        :param precision: Total number of digits, `M`.
        :param scale: Number of digits after the decimal point, `D`.
        """
        if scale is None:
            self._sql = f"DECIMAL({_number(precision)})"
        else:
            self._sql = f"DECIMAL({_number(precision)},{_number(scale)})"


class CastDouble(_ParameterisedType):
    """
    `DOUBLE(M,D)` - double-precision floating-point number rounded to `M` digits in total, `D` of them after the
    decimal point. `CastType.DOUBLE` for `DOUBLE` without parameters. (`DOUBLE PRECISION` is not a cast type in
    MariaDB.)
    """

    def __init__(self, precision: int, scale: int) -> None:
        """
        :param precision: Total number of digits, `M`.
        :param scale: Number of digits after the decimal point, `D`.
        """
        self._sql = f"DOUBLE({_number(precision)},{_number(scale)})"


class CastTime(_ParameterisedType):
    """`TIME(D)` - time with `D` digits of fractional seconds. `CastType.TIME` for `TIME` without them."""

    def __init__(self, precision: int) -> None:
        self._sql = f"TIME({_number(precision)})"


class CastDatetime(_ParameterisedType):
    """
    `DATETIME(D)` - date and time with `D` digits of fractional seconds. `CastType.DATETIME` for `DATETIME` without
    them.
    """

    def __init__(self, precision: int) -> None:
        self._sql = f"DATETIME({_number(precision)})"


class CastIntervalDaySecond(_ParameterisedType):
    """
    `INTERVAL DAY_SECOND(D)` - the value as a `DAY_SECOND` interval string (`'D hh:mm:ss.ff'`) with `D` digits of
    fractional seconds. The precision is required. MariaDB 10.4+.
    """

    def __init__(self, precision: int) -> None:
        self._sql = f"INTERVAL DAY_SECOND({_number(precision)})"


CastTypeArg = (
    CastType
    | CastBinary
    | CastChar
    | CastVarchar
    | CastNChar
    | CastDecimal
    | CastDouble
    | CastTime
    | CastDatetime
    | CastIntervalDaySecond
)
"""Any target type of `Cast` / `Convert`."""


def _cast_type(type_: object) -> CastTypeArg:
    """Check the target type at runtime too, as it is spliced into the SQL - never a plain string."""
    if not isinstance(type_, CastTypeArg):
        raise TypeError(f"Target type must be a CastType member or a Cast* type class, got {type_!r}.")

    return type_


class _Conversion(Expression):
    """Conversion of a single expression, which follows the scalar-function convention of the library."""

    def __init__(self, expr: Statement | Any) -> None:
        super().__init__()
        self._expr = expr

    def _operand(self) -> str:
        return operand(self._expr) if isinstance(self._expr, Statement) else self.dialect.placeholder

    @property
    def args(self) -> list[Any]:
        return self._expr.args if isinstance(self._expr, Statement) else [self._expr]


class Cast(_Conversion):
    """
    `CAST(expr AS type)` - converts `expr` to `type`, a `CastType` member or a parameterised type class.

    ```python
    Cast(JsonValue(Column("doc"), "$.accountId"), CastType.UNSIGNED)  # CAST(JSON_VALUE(`doc`, %s) AS UNSIGNED)
    Cast(Column("price"), CastDecimal(10, 2))                         # CAST(`price` AS DECIMAL(10,2))
    Cast("2024-01-02 03:04:05.123", CastDatetime(3))                  # CAST(%s AS DATETIME(3))
    ```

    A `Statement` `expr` renders as SQL (a query in parentheses, as a scalar subquery); anything else, including a
    plain `str`, is bound as a value. To change the collation of the result, wrap it in
    `sqlfactory.func.info.Collate`.
    """

    def __init__(self, expr: Statement | Any, type_: CastTypeArg) -> None:
        """
        :param expr: Value or expression to convert.
        :param type_: Target type.
        """
        super().__init__(expr)
        self._type = _cast_type(type_)

    def __str__(self) -> str:
        return f"CAST({self._operand()} AS {self._type})"


class Convert(_Conversion):
    """
    `CONVERT(expr, type)` - the ODBC spelling of `CAST(expr AS type)`, taking the same target types as `Cast`.

    `CONVERT(expr USING charset)` - converts a string to another character set, given as `using=`.

    ```python
    Convert(Column("id"), CastType.CHAR)       # CONVERT(`id`, CHAR)
    Convert(Column("name"), using="utf8mb4")   # CONVERT(`name` USING utf8mb4)
    ```

    A `Statement` `expr` renders as SQL (a query in parentheses, as a scalar subquery); anything else, including a
    plain `str`, is bound as a value.
    """

    @overload
    def __init__(self, expr: Statement | Any, type_: CastTypeArg) -> None:
        """`CONVERT(expr, type)`"""

    @overload
    def __init__(self, expr: Statement | Any, *, using: str) -> None:
        """`CONVERT(expr USING charset)`"""

    def __init__(self, expr: Statement | Any, type_: CastTypeArg | None = None, *, using: str | None = None) -> None:
        """
        :param expr: Value or expression to convert.
        :param type_: Target type, `CONVERT(expr, type)`. Not together with `using`.
        :param using: Character set name, `CONVERT(expr USING charset)`. Not together with `type_`.
        """
        if (type_ is None) == (using is None):
            raise TypeError("Convert() takes either a target type or using=, exactly one of them.")

        super().__init__(expr)
        self._type = _cast_type(type_) if using is None else None
        self._using = _identifier(using) if using is not None else None

    def __str__(self) -> str:
        if self._using is not None:
            return f"CONVERT({self._operand()} USING {self._using})"

        return f"CONVERT({self._operand()}, {self._type})"


class Binary(_Conversion):
    """
    `BINARY expr` - the `BINARY` operator: casts `expr` to a binary string, so that a comparison is done byte by byte
    (case sensitive, trailing spaces significant). Same as `CAST(expr AS BINARY)`.

    ```python
    Binary(Column("name")) == "abc"   # BINARY `name` = %s
    Binary(Eq("name", "abc"))         # BINARY (`name` = %s)
    ```

    `BINARY` binds tighter than any comparison or arithmetic operator, so a condition passed as `expr` is put in
    parentheses to keep its meaning, as in the second example.
    """

    def __str__(self) -> str:
        sql = self._operand()

        if isinstance(self._expr, ConditionBase):
            sql = f"({sql})"

        return f"BINARY {sql}"
