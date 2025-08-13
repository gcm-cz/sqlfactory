"""Test cases for SQL CASE statement implementation."""

import pytest

from sqlfactory import Select
from sqlfactory.condition.case import Case
from sqlfactory.condition.simple import Eq, Ge, Gt, Lt
from sqlfactory.entities import Column
from sqlfactory.select.aliased import Aliased
from sqlfactory.statement import Value


class TestCase:
    """Test Case class functionality."""

    def test_empty_case(self):
        """Test empty CASE statement raises ValueError."""
        case = Case()
        # Empty case should raise an exception when converted to string
        with pytest.raises(ValueError, match="CASE statement must have at least one WHEN clause"):
            str(case)
        assert case.args == []
        assert not bool(case)  # Empty case is falsy

    def test_case_with_only_else(self):
        """Test CASE statement with only ELSE clause."""
        case = Case().else_("default")
        with pytest.raises(ValueError, match="CASE statement must have at least one WHEN clause"):
            str(case)
        assert case.args == ["default"]
        assert bool(case)  # Has else clause, so it's truthy

    def test_searched_case_basic(self):
        """Test basic searched CASE statement (no expression)."""
        case = Case().when(Eq("status", "active"), "Active").else_("Inactive")

        expected_sql = "(CASE WHEN `status` = %s THEN %s ELSE %s END)"
        expected_args = ["active", "Active", "Inactive"]

        assert str(case) == expected_sql
        assert case.args == expected_args
        assert bool(case)

    def test_searched_case_multiple_when(self):
        """Test searched CASE with multiple WHEN clauses."""
        case = (
            Case()
            .when(Eq("status", "active"), "Active")
            .when(Eq("status", "inactive"), "Inactive")
            .when(Eq("status", "pending"), "Pending")
            .else_("Unknown")
        )

        expected_sql = "(CASE WHEN `status` = %s THEN %s WHEN `status` = %s THEN %s WHEN `status` = %s THEN %s ELSE %s END)"
        expected_args = ["active", "Active", "inactive", "Inactive", "pending", "Pending", "Unknown"]

        assert str(case) == expected_sql
        assert case.args == expected_args

    def test_searched_case_no_else(self):
        """Test searched CASE without ELSE clause."""
        case = Case().when(Eq("status", "active"), "Active")

        expected_sql = "(CASE WHEN `status` = %s THEN %s END)"
        expected_args = ["active", "Active"]

        assert str(case) == expected_sql
        assert case.args == expected_args

    def test_simple_case_with_expression(self):
        """Test simple CASE statement with expression."""
        case = Case("status").when("active", "Active").when("inactive", "Inactive").else_("Unknown")

        expected_sql = "(CASE `status` WHEN %s THEN %s WHEN %s THEN %s ELSE %s END)"
        expected_args = ["active", "Active", "inactive", "Inactive", "Unknown"]

        assert str(case) == expected_sql
        assert case.args == expected_args

    def test_simple_case_with_column_expression(self):
        """Test simple CASE with Column expression."""
        case = Case(Column("user_status")).when(1, "Active").when(0, "Inactive").else_("Unknown")

        expected_sql = "(CASE `user_status` WHEN %s THEN %s WHEN %s THEN %s ELSE %s END)"
        expected_args = [1, "Active", 0, "Inactive", "Unknown"]

        assert str(case) == expected_sql
        assert case.args == expected_args

    def test_case_with_statement_results(self):
        """Test CASE with Statement objects as results."""
        case = Case().when(Eq("age", None), Value("Unknown")).when(Gt("age", 65), Column("senior_status")).else_("Normal")

        expected_sql = "(CASE WHEN `age` IS %s THEN %s WHEN `age` > %s THEN `senior_status` ELSE %s END)"
        expected_args = [None, "Unknown", 65, "Normal"]

        assert str(case) == expected_sql
        assert case.args == expected_args

    def test_complex_case_with_multiple_conditions(self):
        """Test CASE with complex conditions."""
        case = Case().when(Gt("age", 65), "Senior").when(Ge("age", 18), "Adult").when(Gt("age", 0), "Minor").else_("Invalid")

        expected_sql = "(CASE WHEN `age` > %s THEN %s WHEN `age` >= %s THEN %s WHEN `age` > %s THEN %s ELSE %s END)"
        expected_args = [65, "Senior", 18, "Adult", 0, "Minor", "Invalid"]

        assert str(case) == expected_sql
        assert case.args == expected_args

    def test_case_with_raw_string_condition(self):
        """Test CASE with raw string condition."""
        case = Case().when("LENGTH(name) > 10", "Long Name").else_("Short Name")

        expected_sql = "(CASE WHEN LENGTH(name) > 10 THEN %s ELSE %s END)"
        expected_args = ["Long Name", "Short Name"]

        assert str(case) == expected_sql
        assert case.args == expected_args

    def test_nested_case_statements(self):
        """Test nested CASE statements."""
        inner_case = Case("status").when("active", "A").else_("I")
        outer_case = Case().when(Eq("priority", "high"), inner_case).else_("Normal")

        expected_sql = "(CASE WHEN `priority` = %s THEN (CASE `status` WHEN %s THEN %s ELSE %s END) ELSE %s END)"
        expected_args = ["high", "active", "A", "I", "Normal"]

        assert str(outer_case) == expected_sql
        assert outer_case.args == expected_args

    def test_case_alias(self):
        """Test CASE statement with alias using Aliased class."""
        case = Case().when(Eq("status", "active"), "Active").else_("Inactive")
        aliased = Aliased(case, "status_name")

        assert isinstance(aliased, Aliased)
        expected_sql = "(CASE WHEN `status` = %s THEN %s ELSE %s END) AS `status_name`"
        expected_args = ["active", "Active", "Inactive"]

        assert str(aliased) == expected_sql
        assert aliased.args == expected_args
        assert bool(aliased) == bool(case)

    def test_case_in_select(self):
        """Test using CASE expression as a selected column in SELECT."""
        case = Case().when(Eq("status", "active"), "Active").else_("Inactive")
        select = Select(case, table="users")

        expected_sql = "SELECT (CASE WHEN `status` = %s THEN %s ELSE %s END) FROM `users`"
        expected_args = ["active", "Active", "Inactive"]

        assert str(select) == expected_sql
        assert select.args == expected_args

    def test_case_method_chaining(self):
        """Test that CASE methods return self for chaining."""
        case = Case()

        # Test that when() returns self
        result = case.when(Eq("x", 1), "one")
        assert result is case

        # Test that else_() returns self
        result = case.else_("default")
        assert result is case

    def test_case_boolean_evaluation(self):
        """Test boolean evaluation of CASE statements."""
        # Empty case
        empty_case = Case()
        assert not bool(empty_case)

        # Case with WHEN clause
        when_case = Case().when(Eq("x", 1), "one")
        assert bool(when_case)

        # Case with only ELSE clause
        else_case = Case().else_("default")
        assert bool(else_case)

        # Case with both WHEN and ELSE
        full_case = Case().when(Eq("x", 1), "one").else_("default")
        assert bool(full_case)

    def test_case_expression_inheritance(self):
        """Test that Case inherits from Expression and supports operators."""
        case = Case().when(Eq("x", 1), 10).else_(0)

        # Test arithmetic operations (inherited from Expression)
        addition = case + 5
        assert str(addition) == f"({case!s} + %s)"

        # Test comparison operations (inherited from Expression)
        comparison = case > 5
        assert str(comparison) == f"{case!s} > %s"

    def test_aliased_case_boolean(self):
        """Test boolean evaluation of Case with Aliased."""
        # Aliased case with valid underlying case
        case = Case().when(Eq("x", 1), "one")
        aliased = Aliased(case, "result")
        assert bool(aliased)

        # Aliased case with empty underlying case - Aliased statements are always truthy
        # because they represent valid SQL constructs with aliases
        empty_case = Case()
        aliased_empty = Aliased(empty_case, "result")
        assert bool(aliased_empty)  # Aliased is always truthy when it has an alias


class TestCaseEdgeCases:
    """Test edge cases and error conditions."""

    def test_case_with_none_values(self):
        """Test CASE with None values."""
        case = Case().when(Eq("x", None), None).else_(None)

        expected_sql = "(CASE WHEN `x` IS %s THEN %s ELSE %s END)"
        expected_args = [None, None, None]

        assert str(case) == expected_sql
        assert case.args == expected_args

    def test_case_mixed_statement_and_value_conditions(self):
        """Test CASE mixing Statement conditions and raw values."""
        case = Case("priority").when(1, "High").when(2, Column("medium_label")).else_(Value("Low"))

        expected_sql = "(CASE `priority` WHEN %s THEN %s WHEN %s THEN `medium_label` ELSE %s END)"
        expected_args = [1, "High", 2, "Low"]

        assert str(case) == expected_sql
        assert case.args == expected_args

    def test_case_empty_when_clauses_with_else(self):
        """Test CASE with no WHEN clauses but with ELSE."""
        case = Case().else_("always_this")
        expected_args = ["always_this"]
        assert case.args == expected_args
        with pytest.raises(ValueError, match="CASE statement must have at least one WHEN clause"):
            str(case)
