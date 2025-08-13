"""SQL CASE statement implementation."""

from __future__ import annotations

from typing import Any, Self

from sqlfactory.condition.base import Condition, ConditionBase, StatementOrColumn
from sqlfactory.entities import Column, Expression
from sqlfactory.statement import Statement

# Sentinel value to distinguish between "no else clause" and "else clause with None value"
_NO_ELSE = object()


class Case(Expression):
    """
    SQL CASE statement implementation that supports both simple and searched case expressions.

    Supports the SQL CASE syntax:
    ```sql
    CASE
        WHEN condition1 THEN result1
        WHEN condition2 THEN result2
        WHEN conditionN THEN resultN
        ELSE result
    END
    ```

    And simple CASE syntax:
    ```sql
    CASE expression
        WHEN value1 THEN result1
        WHEN value2 THEN result2
        WHEN valueN THEN resultN
        ELSE result
    END
    ```

    Examples:

    Simple searched CASE:
    ```python
    case = Case().when(Eq("status", "active"), "Active").when(Eq("status", "inactive"), "Inactive").else_("Unknown")
    # CASE WHEN `status` = %s THEN %s WHEN `status` = %s THEN %s ELSE %s END
    # args: ["active", "Active", "inactive", "Inactive", "Unknown"]
    ```

    Simple CASE with expression:
    ```python
    case = Case("status").when("active", "Active").when("inactive", "Inactive").else_("Unknown")
    # CASE `status` WHEN %s THEN %s WHEN %s THEN %s ELSE %s END
    # args: ["active", "Active", "inactive", "Inactive", "Unknown"]
    ```

    Complex CASE with conditions:
    ```python
    case = (Case()
        .when(Gt("age", 65), "Senior")
        .when(Ge("age", 18), "Adult")
        .when(Gt("age", 0), "Minor")
        .else_("Invalid"))
    # CASE WHEN `age` > %s THEN %s WHEN `age` >= %s THEN %s WHEN `age` > %s THEN %s ELSE %s END
    # args: [65, "Senior", 18, "Adult", 0, "Minor", "Invalid"]
    ```

    Using CASE in SELECT with Aliased:
    ```python
    from sqlfactory.entities import Aliased
    case_expr = Case().when(Eq("status", 1), "Active").else_("Inactive")
    select = Select(Aliased(case_expr, "status_name"), table="users")
    # SELECT (CASE WHEN `status` = %s THEN %s ELSE %s END) AS `status_name` FROM `users`
    ```
    """

    def __init__(self, expression: StatementOrColumn | None = None) -> None:
        """
        Initialize a CASE statement.

        :param expression: Optional expression for simple CASE statements (CASE expression WHEN value THEN result).
                          If None, creates a searched CASE statement (CASE WHEN condition THEN result).
        """
        super().__init__()

        self._expression: Statement | None = None
        if expression is not None:
            if not isinstance(expression, Statement):
                expression = Column(expression)
            self._expression = expression

        self._when_clauses: list[tuple[Statement | Any, Statement | Any]] = []
        self._else_clause: Statement | Any | object = _NO_ELSE

    def when(self, condition_or_value: ConditionBase | StatementOrColumn | Any, result: Statement | Any) -> Self:
        """
        Add a WHEN clause to the CASE statement.

        :param condition_or_value: For searched CASE (no expression in constructor): A condition (ConditionBase instance)
                                  For simple CASE (expression in constructor): A value to compare against the expression
        :param result: The result to return when the condition/value matches
        :return: Self for method chaining
        """
        # For simple CASE statements (with expression), condition_or_value is just a value
        # For searched CASE statements (no expression), condition_or_value should be a condition
        if self._expression is None and not isinstance(condition_or_value, (ConditionBase, Statement)):
            # If no expression and condition_or_value is not a condition/statement, wrap it as a statement
            # This allows for raw string conditions
            if isinstance(condition_or_value, str):
                condition_or_value = Condition(condition_or_value)

        self._when_clauses.append((condition_or_value, result))
        return self

    def else_(self, result: Statement | Any) -> Self:
        """
        Add an ELSE clause to the CASE statement.

        :param result: The default result to return when no WHEN conditions match
        :return: Self for method chaining
        """
        self._else_clause = result
        return self

    def __str__(self) -> str:
        """Generate the SQL CASE statement."""
        if not self._when_clauses:
            # MySQL (and standard SQL) require at least one WHEN clause in a CASE expression.
            # CASE with only ELSE is invalid, so we always raise here.
            raise ValueError("CASE statement must have at least one WHEN clause")

        parts = ["CASE"]

        if self._expression is not None:
            parts.append(str(self._expression))

        # Add WHEN clauses
        for condition_or_value, result in self._when_clauses:
            if isinstance(condition_or_value, Statement):
                condition_str = str(condition_or_value)
            else:
                condition_str = self.dialect.placeholder

            if isinstance(result, Statement):
                result_str = str(result)
            else:
                result_str = self.dialect.placeholder

            parts.append(f"WHEN {condition_str} THEN {result_str}")

        if self._else_clause is not _NO_ELSE:
            if isinstance(self._else_clause, Statement):
                parts.append(f"ELSE {self._else_clause!s}")
            else:
                parts.append(f"ELSE {self.dialect.placeholder}")

        parts.append("END")
        return f"({' '.join(parts)})"

    @property
    def args(self) -> list[Any]:
        """Return the arguments for the CASE statement."""
        args = []

        if self._expression is not None:
            args.extend(self._expression.args)

        for condition_or_value, result in self._when_clauses:
            if isinstance(condition_or_value, Statement):
                args.extend(condition_or_value.args)
            else:
                args.append(condition_or_value)

            if isinstance(result, Statement):
                args.extend(result.args)
            else:
                args.append(result)

        if self._else_clause is not _NO_ELSE:
            if isinstance(self._else_clause, Statement):
                args.extend(self._else_clause.args)
            else:
                args.append(self._else_clause)

        return args

    def __bool__(self) -> bool:
        """A CASE statement is valid if it has at least one WHEN clause or an ELSE clause."""
        return bool(self._when_clauses) or self._else_clause is not _NO_ELSE
