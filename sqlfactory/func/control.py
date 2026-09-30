"""Control flow functions (https://mariadb.com/kb/en/control-flow-functions/)"""

from collections.abc import Iterable
from typing import Any, Self

from sqlfactory.entities import Expression
from sqlfactory.func.base import Function
from sqlfactory.statement import Statement

# Sentinel to distinguish "not provided" from an explicit `None` value, as `None` is a legitimate CASE operand or
# result (rendered as a bound NULL), while an omitted CASE operand or ELSE clause changes the rendered SQL.
_NOT_SET: Any = object()


class IfNull(Function):
    """If expr1 is not NULL, IFNULL() returns expr1; otherwise it returns expr2."""

    def __init__(self, expr1: Statement | Any, expr2: Statement | Any) -> None:
        super().__init__("IFNULL", expr1, expr2)


class Nvl(IfNull):
    """Synonym for `IFNULL()`. MariaDB 10.3+."""

    def __init__(self, expr1: Statement | Any, expr2: Statement | Any) -> None:
        super().__init__(expr1, expr2)
        self.function = "NVL"


class NullIf(Function):
    """Returns NULL if expr1 = expr2 is true, otherwise returns expr1."""

    def __init__(self, expr1: Statement | Any, expr2: Statement | Any) -> None:
        super().__init__("NULLIF", expr1, expr2)


class If(Function):
    """If expr1 is TRUE (expr1 <> 0 and expr1 <> NULL) then IF() returns expr2; otherwise it returns expr3."""

    def __init__(self, expr: Statement | Any, if_true: Statement | Any, if_false: Statement | Any) -> None:
        super().__init__("IF", expr, if_true, if_false)


class Nvl2(Function):
    """If expr1 is not NULL, NVL2() returns expr2; otherwise it returns expr3. MariaDB 10.3+."""

    def __init__(self, expr1: Statement | Any, expr2: Statement | Any, expr3: Statement | Any) -> None:
        super().__init__("NVL2", expr1, expr2, expr3)


class Coalesce(Function):
    """Returns first non-NULL parameter."""

    def __init__(self, expr: Statement | Any, *args: Statement | Any) -> None:
        super().__init__("COALESCE", expr, *args)


class DecodeOracle(Function):
    """
    `DECODE_ORACLE(expr, search1, result1 [, search2, result2 ...] [, default])`

    Compares `expr` against each `search`, in order, and returns the `result` of the first one that matches
    (using NULL-safe comparison, i.e. `NULL` matches `NULL`, unlike the simple `CASE`/`=` comparison). If none
    matches, `default` is returned, or `NULL` if `default` was not given.

    Synonym for the Oracle-mode `DECODE()` function, but available in any SQL mode. MariaDB 10.3+.
    """

    def __init__(self, expr: Statement | Any, search1: Statement | Any, result1: Statement | Any, *rest: Statement | Any) -> None:
        """
        :param expr: Expression to compare against each search value.
        :param search1: First search value.
        :param result1: Result returned when `expr` matches `search1`.
        :param rest: Any number of further `search, result` pairs, optionally followed by a trailing `default`
            value (an odd number of extra arguments).
        """
        super().__init__("DECODE_ORACLE", expr, search1, result1, *rest)


class Case(Expression):
    """
    `CASE` expression, usable anywhere a value is expected (select column, condition operand, `UPDATE` value,
    `ORDER BY`, inside aggregates, ...).

    MariaDB provides two forms, both supported by this single class:

    - Searched form -- no operand passed to the constructor. Each `when()` condition is evaluated on its own and
      would usually be a `ConditionBase` (or other `Statement`), rendered as-is (not as a placeholder):

      ```python
      Case().when(Column("score") >= 90, "A").when(Column("score") >= 80, "B").else_("C")
      # CASE WHEN `score` >= %s THEN %s WHEN `score` >= %s THEN %s ELSE %s END
      ```

    - Simple form -- operand passed to the constructor. Each `when()` compare value is matched against the operand
      using implicit equality:

      ```python
      Case(Column("status")).when("A", "Active").when("I", "Inactive").else_("Unknown")
      # CASE `status` WHEN %s THEN %s WHEN %s THEN %s ELSE %s END
      ```

    Clauses can also be supplied through the constructor, if that fits better:

    ```python
    Case(Column("status"), cases=[("A", "Active"), ("I", "Inactive")], else_="Unknown")
    ```

    As with other functions, `Statement` arguments (e.g. `Column`, another `Case`, a condition) render as SQL and
    contribute their own `args`; anything else becomes a placeholder and is added to `.args`. Argument order always
    follows placeholder order: operand (if any), then each WHEN's condition/compare value followed by its THEN
    result, in the order added, then the ELSE result (if any).

    At least one `WHEN` clause is required -- rendering (`str()`) a `Case` with none configured raises `ValueError`.
    """

    def __init__(
        self,
        value: Statement | Any = _NOT_SET,
        cases: Iterable[tuple[Statement | Any, Statement | Any]] = (),
        *,
        else_: Statement | Any = _NOT_SET,
    ) -> None:
        """
        :param value: Operand for the simple form (`CASE value WHEN ...`). If omitted, the searched form
            (`CASE WHEN ...`) is used.
        :param cases: Optional `(condition_or_compare_value, result)` pairs to seed the `WHEN` clauses with,
            equivalent to calling `when()` for each pair in order.
        :param else_: Optional `ELSE` result. If omitted, no `ELSE` clause is rendered, and `CASE` evaluates to
            `NULL` when nothing matches.
        """
        super().__init__()

        self._value = value
        self._whens: list[tuple[Statement | Any, Statement | Any]] = list(cases)
        self._else = else_

    def when(self, condition: Statement | Any, result: Statement | Any) -> Self:
        """
        Add another `WHEN condition THEN result` clause.

        :param condition: In the searched form, a `ConditionBase` or other `Statement` evaluated as a boolean.
            In the simple form, the value compared against the constructor's operand.
        :param result: Value returned when `condition` matches.
        """
        self._whens.append((condition, result))
        return self

    def else_(self, result: Statement | Any) -> Self:
        """
        Set (or replace) the `ELSE result` clause.

        :param result: Value returned when no `WHEN` clause matched.
        """
        self._else = result
        return self

    def _render(self, value: Statement | Any) -> str:
        return str(value) if isinstance(value, Statement) else self.dialect.placeholder

    @staticmethod
    def _arg(value: Statement | Any) -> list[Any]:
        return list(value.args) if isinstance(value, Statement) else [value]

    def __str__(self) -> str:
        if not self._whens:
            raise ValueError("Case must have at least one WHEN clause.")

        parts = ["CASE"]

        if self._value is not _NOT_SET:
            parts.append(self._render(self._value))

        for condition, result in self._whens:
            parts.append(f"WHEN {self._render(condition)} THEN {self._render(result)}")

        if self._else is not _NOT_SET:
            parts.append(f"ELSE {self._render(self._else)}")

        parts.append("END")

        return " ".join(parts)

    @property
    def args(self) -> list[Any]:
        out: list[Any] = []

        if self._value is not _NOT_SET:
            out.extend(self._arg(self._value))

        for condition, result in self._whens:
            out.extend(self._arg(condition))
            out.extend(self._arg(result))

        if self._else is not _NOT_SET:
            out.extend(self._arg(self._else))

        return out
