"""String functions (https://mariadb.com/kb/en/string-functions/)"""

import re
from enum import Enum
from typing import Any

from sqlfactory.func.base import Function
from sqlfactory.statement import Statement

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class Ascii(Function):
    """Numeric ASCII value of leftmost character."""

    def __init__(self, arg: Statement | Any) -> None:
        super().__init__("ASCII", arg)


class Bin(Function):
    """Returns binary value"""

    def __init__(self, num: Statement | Any) -> None:
        super().__init__("BIN", num)


class BitLength(Function):
    """Returns the length of a string in bits"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("BIT_LENGTH", s)


class Char(Function):
    """
    ``CHAR(N,... [USING charset_name])`` — returns string based on the integer values for the individual
    characters, optionally interpreted using the given character set (the default is binary).
    """

    def __init__(self, *n: Statement | int, using: str | None = None) -> None:
        if using is not None and not _IDENTIFIER_RE.match(using):
            raise ValueError(f"`using` must be a bare charset identifier, got {using!r}.")

        self._using = using
        super().__init__("CHAR", *n)

    def __str__(self) -> str:
        suffix = f" USING {self._using}" if self._using is not None else ""
        return f"CHAR({', '.join(self._args_placeholders())}{suffix})"


class CharLength(Function):
    """Length of the string in characters."""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("CHAR_LENGTH", s)


class CharacterLength(CharLength):
    """Synonym for CHAR_LENGTH()."""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__(s)
        self.function = "CHARACTER_LENGTH"


class Chr(Function):
    """Returns string based on integer values of the individual characters."""

    def __init__(self, n: Statement | int) -> None:
        super().__init__("CHR", n)


class Concat(Function):
    """Returns concatenated string"""

    def __init__(self, *s: Statement | Any) -> None:
        super().__init__("CONCAT", *s)


class ConcatWs(Function):
    """Concatenate with separator"""

    def __init__(self, separator: Statement | Any, *s: Statement | Any) -> None:
        super().__init__("CONCAT_WS", separator, *s)


class Elt(Function):
    """``ELT(N, str1[, str2, str3, ...])`` — returns the string at the N-th (1-indexed) position."""

    def __init__(self, n: Statement | int, s1: Statement | Any, *rest: Statement | Any) -> None:
        super().__init__("ELT", n, s1, *rest)


class ExportSet(Function):
    """
    ``EXPORT_SET(bits, on, off[, separator[, number_of_bits]])`` — returns a string representation of the bits
    in ``bits``, using ``on``/``off`` for each set/unset bit, joined by ``separator`` (``,`` if omitted), examining
    only the lowest ``number_of_bits`` bits if given.
    """

    def __init__(
        self,
        bits: Statement | Any,
        on: Statement | Any,
        off: Statement | Any,
        separator: Statement | Any | None = None,
        number_of_bits: Statement | int | None = None,
    ) -> None:
        args: list[Statement | Any] = [bits, on, off]

        if separator is not None:
            args.append(separator)

            if number_of_bits is not None:
                args.append(number_of_bits)

        elif number_of_bits is not None:
            raise ValueError("`number_of_bits` requires `separator` to be given.")

        super().__init__("EXPORT_SET", *args)


class ExtractValue(Function):
    """``EXTRACTVALUE(xml_frag, xpath_expr)`` — extracts a value from XML matching an XPath expression."""

    def __init__(self, xml_frag: Statement | Any, xpath_expr: Statement | Any) -> None:
        super().__init__("EXTRACTVALUE", xml_frag, xpath_expr)


class Field(Function):
    """``FIELD(pattern, str1[, str2, ...])`` — returns the (1-indexed) position of ``pattern`` in the list."""

    def __init__(self, pattern: Statement | Any, s1: Statement | Any, *rest: Statement | Any) -> None:
        super().__init__("FIELD", pattern, s1, *rest)


class FindInSet(Function):
    """``FIND_IN_SET(pattern, strlist)`` — the (1-indexed) position of ``pattern`` in a comma-separated ``strlist``."""

    def __init__(self, pattern: Statement | Any, strlist: Statement | Any) -> None:
        super().__init__("FIND_IN_SET", pattern, strlist)


class Format(Function):
    """
    ``FORMAT(num, decimal_position[, locale])`` — formats ``num`` with grouped thousands, rounded to
    ``decimal_position`` decimals, optionally formatted per ``locale`` (e.g. ``'de_DE'``).
    """

    def __init__(
        self,
        num: Statement | Any,
        decimal_position: Statement | int,
        locale: Statement | Any | None = None,
    ) -> None:
        if locale is not None:
            super().__init__("FORMAT", num, decimal_position, locale)
        else:
            super().__init__("FORMAT", num, decimal_position)


class FromBase64(Function):
    """``FROM_BASE64(str)`` — decodes a base-64 encoded string, returning a binary string."""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("FROM_BASE64", s)


class Hex(Function):
    """Returns a hexadecimal string representation of a decimal or string value."""

    def __init__(self, n: Statement | Any) -> None:
        super().__init__("HEX", n)


class Insert(Function):
    """
    ``INSERT(str, pos, len, newstr)`` — inserts ``newstr`` into ``str`` at position ``pos``, replacing ``len``
    characters (``str`` is returned unmodified if ``pos`` is out of range; if ``len`` is longer than the rest of
    ``str``, everything from ``pos`` onward is replaced).

    Named after the MariaDB function, same as ``sqlfactory.insert.Insert`` (the ``INSERT`` statement) is named
    after its statement -- the two are never imported under the same name at once, since function classes are not
    re-exported from the top-level ``sqlfactory`` package.
    """

    def __init__(
        self,
        s: Statement | Any,
        pos: Statement | int,
        length: Statement | int,
        newstr: Statement | Any,
    ) -> None:
        super().__init__("INSERT", s, pos, length, newstr)


class InStr(Function):
    """Returns the position of the first occurrence of substring in string"""

    def __init__(self, s: Statement | Any, substring: Statement | Any) -> None:
        super().__init__("INSTR", s, substring)


class Left(Function):
    """Returns the leftmost number of characters"""

    def __init__(self, s: Statement | Any, n: Statement | int) -> None:
        super().__init__("LEFT", s, n)


class Length(Function):
    """Returns the length of a string in bytes"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("LENGTH", s)


class LengthB(Function):
    """``LENGTHB(str)`` — length of a string in bytes. A synonym for LENGTH() outside of Oracle mode."""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("LENGTHB", s)


class LoadFile(Function):
    """``LOAD_FILE(file_name)`` — reads the named file on the server and returns its contents as a string."""

    def __init__(self, file_name: Statement | Any) -> None:
        super().__init__("LOAD_FILE", file_name)


class Locate(Function):
    """``LOCATE(substr, str[, pos])`` — position of the first occurrence of substring in string, optionally
    starting the search at position ``pos``."""

    def __init__(
        self,
        substring: Statement | Any,
        s: Statement | Any,
        pos: Statement | int | None = None,
    ) -> None:
        if pos is not None:
            super().__init__("LOCATE", substring, s, pos)
        else:
            super().__init__("LOCATE", substring, s)


class Lower(Function):
    """Converts a string to lower-case"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("LOWER", s)


class Lcase(Lower):
    """Synonym for LOWER()."""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__(s)
        self.function = "LCASE"


class Lpad(Function):
    """Left-pad a string with another string"""

    def __init__(self, s: Statement | Any, n: Statement | int, pad: Statement | Any) -> None:
        super().__init__("LPAD", s, n, pad)


class Ltrim(Function):
    """Removes leading spaces"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("LTRIM", s)


class MakeSet(Function):
    """``MAKE_SET(bits, str1[, str2, ...])`` — comma-joins those of ``str1, str2, ...`` whose corresponding bit
    (bit 0 for ``str1``, bit 1 for ``str2``, ...) is set in ``bits``."""

    def __init__(self, bits: Statement | Any, s1: Statement | Any, *rest: Statement | Any) -> None:
        super().__init__("MAKE_SET", bits, s1, *rest)


class Mid(Function):
    """``MID(str, pos[, len])`` — synonym for SUBSTRING(str, pos[, len])."""

    def __init__(
        self,
        s: Statement | Any,
        start: Statement | int,
        length: Statement | int | None = None,
    ) -> None:
        if length is not None:
            super().__init__("MID", s, start, length)
        else:
            super().__init__("MID", s, start)


class NaturalSortKey(Function):
    """``NATURAL_SORT_KEY(str)`` — sort key for natural (human) ordering, where runs of digits sort by numeric
    value rather than character by character. MariaDB 10.7+."""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("NATURAL_SORT_KEY", s)


class OctetLength(Function):
    """Returns the length of a string in bytes"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("OCTET_LENGTH", s)


class Ord(Function):
    """Numeric value of leftmost character"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("ORD", s)


class Position(Function):
    """``POSITION(substr IN str)`` — synonym for LOCATE(substr, str), written with the ODBC ``IN`` syntax."""

    def __init__(self, substring: Statement | Any, s: Statement | Any) -> None:
        super().__init__("POSITION", substring, s)

    def __str__(self) -> str:
        substring_placeholder, s_placeholder = self._args_placeholders()
        return f"POSITION({substring_placeholder} IN {s_placeholder})"


class Quote(Function):
    """``QUOTE(str)`` — quotes a string, producing a result usable as a properly escaped data value in SQL."""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("QUOTE", s)


class RegexpInstr(Function):
    """``REGEXP_INSTR(subject, pattern)`` — the (1-indexed, in characters) position of the first match of
    ``pattern`` in ``subject``, or 0 if it does not match."""

    def __init__(self, subject: Statement | Any, pattern: Statement | Any) -> None:
        super().__init__("REGEXP_INSTR", subject, pattern)


class RegexpReplace(Function):
    """``REGEXP_REPLACE(subject, pattern, replace)`` — replaces every match of ``pattern`` in ``subject`` with
    ``replace``."""

    def __init__(self, subject: Statement | Any, pattern: Statement | Any, replace: Statement | Any) -> None:
        super().__init__("REGEXP_REPLACE", subject, pattern, replace)


class RegexpSubstr(Function):
    """``REGEXP_SUBSTR(subject, pattern)`` — the substring of ``subject`` matching ``pattern``, or an empty
    string if it does not match."""

    def __init__(self, subject: Statement | Any, pattern: Statement | Any) -> None:
        super().__init__("REGEXP_SUBSTR", subject, pattern)


class Repeat(Function):
    """Repeat a string the specified number of times"""

    def __init__(self, s: Statement | Any, n: Statement | int) -> None:
        super().__init__("REPEAT", s, n)


class Replace(Function):
    """Replace occurrences of a specified string"""

    def __init__(self, s: Statement | Any, from_: Statement | Any, to: Statement | Any) -> None:
        super().__init__("REPLACE", s, from_, to)


class Reverse(Function):
    """Reverse a string"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("REVERSE", s)


class Right(Function):
    """Returns the rightmost number of characters"""

    def __init__(self, s: Statement | Any, n: Statement | int) -> None:
        super().__init__("RIGHT", s, n)


class RPad(Function):
    """Right-pad a string with another string"""

    def __init__(self, s: Statement | Any, n: Statement | int, pad: Statement | Any) -> None:
        super().__init__("RPAD", s, n, pad)


class RTrim(Function):
    """Removes trailing spaces"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("RTRIM", s)


class SFormat(Function):
    """Format a string. MariaDB 10.7+."""

    def __init__(self, format_: Statement | Any, *args: Statement | Any) -> None:
        super().__init__("SFORMAT", format_, *args)


class Soundex(Function):
    """``SOUNDEX(str)`` — returns a soundex string from ``str``."""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("SOUNDEX", s)


class Space(Function):
    """Returns a string of spaces"""

    def __init__(self, n: Statement | int) -> None:
        super().__init__("SPACE", n)


class Strcmp(Function):
    """``STRCMP(expr1, expr2)`` — 0 if the strings are equal, -1/1 if ``expr1`` sorts before/after ``expr2``."""

    def __init__(self, expr1: Statement | Any, expr2: Statement | Any) -> None:
        super().__init__("STRCMP", expr1, expr2)


class Substr(Function):
    """``SUBSTR(str, pos[, len])`` — synonym for SUBSTRING(str, pos[, len])."""

    def __init__(
        self,
        s: Statement | Any,
        start: Statement | int,
        length: Statement | int | None = None,
    ) -> None:
        if length is not None:
            super().__init__("SUBSTR", s, start, length)
        else:
            super().__init__("SUBSTR", s, start)


class Substring(Function):
    """``SUBSTRING(str, pos[, len])`` — substring of ``str`` starting at (1-indexed; negative counts from the
    end of the string) position ``pos``, optionally exactly ``len`` characters long."""

    def __init__(
        self,
        s: Statement | Any,
        start: Statement | int,
        length: Statement | int | None = None,
    ) -> None:
        if length is not None:
            super().__init__("SUBSTRING", s, start, length)
        else:
            super().__init__("SUBSTRING", s, start)


class SubstringIndex(Function):
    """Returns a substring"""

    def __init__(self, s: Statement | Any, delimiter: Statement | Any, count: Statement | int) -> None:
        super().__init__("SUBSTRING_INDEX", s, delimiter, count)


class ToBase64(Function):
    """Converts a string to base64"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("TO_BASE64", s)


class ToChar(Function):
    """``TO_CHAR(expr[, fmt])`` — converts a date/datetime/time/timestamp (or string) expression to a string,
    optionally per a format string (e.g. ``'YYYY-MM-DD'``). MariaDB 10.6+."""

    def __init__(self, n: Statement | Any, fmt: Statement | Any | None = None) -> None:
        if fmt is not None:
            super().__init__("TO_CHAR", n, fmt)
        else:
            super().__init__("TO_CHAR", n)


class TrimDirection(str, Enum):
    """Direction for :class:`Trim` / :class:`TrimOracle` -- which end(s) to remove ``remstr`` from."""

    BOTH = "BOTH"
    LEADING = "LEADING"
    TRAILING = "TRAILING"


class Trim(Function):
    """
    ``TRIM([{BOTH | LEADING | TRAILING} [remstr] FROM] str)`` — removes ``remstr`` (spaces, if omitted) from the
    given end(s) (both, if omitted) of ``str``.

    ``Trim(s)`` renders the plain ``TRIM(str)`` form. Give ``remstr`` and/or ``direction`` to render the full
    clause -- e.g. ``Trim(q.error, "\\n", TrimDirection.TRAILING)`` renders ``TRIM(TRAILING %s FROM `q`.`error`)``.
    """

    def __init__(
        self,
        s: Statement | Any,
        remstr: Statement | Any | None = None,
        direction: TrimDirection | None = None,
    ) -> None:
        self._direction = direction
        self._has_clause = remstr is not None or direction is not None

        if remstr is not None:
            super().__init__("TRIM", remstr, s)
        else:
            super().__init__("TRIM", s)

    def __str__(self) -> str:
        placeholders = self._args_placeholders()

        if not self._has_clause:
            return f"{self.function}({placeholders[0]})"

        if len(placeholders) == 2:
            remstr_part = f"{placeholders[0]} "
            s_placeholder = placeholders[1]
        else:
            remstr_part = ""
            s_placeholder = placeholders[0]

        direction_part = f"{self._direction.value} " if self._direction is not None else ""
        return f"{self.function}({direction_part}{remstr_part}FROM {s_placeholder})"


class TrimOracle(Trim):
    """
    Synonym for the Oracle-mode form of TRIM -- same syntax as :class:`Trim` and available in any SQL mode, but
    returns ``NULL`` instead of an empty string when the trimmed result would be empty.
    """

    def __init__(
        self,
        s: Statement | Any,
        remstr: Statement | Any | None = None,
        direction: TrimDirection | None = None,
    ) -> None:
        super().__init__(s, remstr, direction)
        self.function = "TRIM_ORACLE"


class Unhex(Function):
    """Converts a hexadecimal pairs of digits to the character represented by the number."""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("UNHEX", s)


class UpdateXml(Function):
    """``UPDATEXML(xml_target, xpath_expr, new_xml)`` — replaces, within ``xml_target``, the fragment matched by
    ``xpath_expr`` with ``new_xml``."""

    def __init__(
        self,
        xml_target: Statement | Any,
        xpath_expr: Statement | Any,
        new_xml: Statement | Any,
    ) -> None:
        super().__init__("UPDATEXML", xml_target, xpath_expr, new_xml)


class Upper(Function):
    """Converts a string to upper-case"""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__("UPPER", s)


class Ucase(Upper):
    """Synonym for UPPER()."""

    def __init__(self, s: Statement | Any) -> None:
        super().__init__(s)
        self.function = "UCASE"


class WeightStringAs(str, Enum):
    """Comparison type for :class:`WeightString`'s ``AS`` clause."""

    CHAR = "CHAR"
    BINARY = "BINARY"


class WeightStringFlag(str, Enum):
    """Sort-direction flag for :class:`WeightString`'s ``LEVEL`` clause."""

    ASC = "ASC"
    DESC = "DESC"
    REVERSE = "REVERSE"


class WeightString(Function):
    """
    ``WEIGHT_STRING(str [AS {CHAR|BINARY}(N)] [LEVEL n [flag]])`` — the sort/comparison weight MariaDB would use
    for ``str`` under the current collation.

    ``N`` (with ``as_type``/``length``) and ``n`` (``level``) are spliced into the SQL text rather than bound --
    verified against a live server, MariaDB's grammar does not accept a placeholder in either position -- so both
    are validated as positive integers for that reason.

    MariaDB's grammar also allows a comma-separated list of levels, each with its own flag
    (``LEVEL n1 [flag1], n2 [flag2], ...``); this class models only a single level, which covers every documented
    example and the common case. Use :class:`sqlfactory.statement.Raw` for the multi-level form.
    """

    def __init__(
        self,
        s: Statement | Any,
        *,
        as_type: WeightStringAs | None = None,
        length: int | None = None,
        level: int | None = None,
        flag: WeightStringFlag | None = None,
    ) -> None:
        if (as_type is None) != (length is None):
            raise ValueError("`as_type` and `length` must be given together.")

        if length is not None and (not isinstance(length, int) or length < 1):
            raise ValueError(f"`length` must be a positive integer, got {length!r}.")

        if flag is not None and level is None:
            raise ValueError("`flag` requires `level` to be given.")

        if level is not None and (not isinstance(level, int) or level < 1):
            raise ValueError(f"`level` must be a positive integer, got {level!r}.")

        self._as_type = as_type
        self._length = length
        self._level = level
        self._flag = flag

        super().__init__("WEIGHT_STRING", s)

    def __str__(self) -> str:
        (s_placeholder,) = self._args_placeholders()

        suffix = ""
        if self._as_type is not None:
            suffix += f" AS {self._as_type.value}({self._length})"

        if self._level is not None:
            suffix += f" LEVEL {self._level}"
            if self._flag is not None:
                suffix += f" {self._flag.value}"

        return f"{self.function}({s_placeholder}{suffix})"
