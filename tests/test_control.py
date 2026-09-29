"""Tests for the CASE expression and the rest of the control flow functions."""

import pytest

from sqlfactory import Column, Direction, Eq, Order, Select, Update
from sqlfactory.func.agg import Sum
from sqlfactory.func.control import Case, DecodeOracle, IfNull, Nvl, Nvl2

# ---------------------------------------------------------------------------
# NVL / NVL2 / DECODE_ORACLE
# ---------------------------------------------------------------------------


def test_nvl():
    func = Nvl(Column("column1"), "default")
    assert str(func) == "NVL(`column1`, %s)"
    assert func.args == ["default"]


def test_nvl_is_ifnull_alias():
    assert isinstance(Nvl(Column("column1"), "default"), IfNull)


def test_nvl2():
    func = Nvl2(Column("column1"), "not_null", "is_null")
    assert str(func) == "NVL2(`column1`, %s, %s)"
    assert func.args == ["not_null", "is_null"]


def test_decode_oracle_single_pair():
    func = DecodeOracle(Column("column1"), 1, "one")
    assert str(func) == "DECODE_ORACLE(`column1`, %s, %s)"
    assert func.args == [1, "one"]


def test_decode_oracle_multiple_pairs():
    func = DecodeOracle(Column("column1"), 1, "one", 2, "two")
    assert str(func) == "DECODE_ORACLE(`column1`, %s, %s, %s, %s)"
    assert func.args == [1, "one", 2, "two"]


def test_decode_oracle_with_default():
    func = DecodeOracle(Column("column1"), 1, "one", 2, "two", "other")
    assert str(func) == "DECODE_ORACLE(`column1`, %s, %s, %s, %s, %s)"
    assert func.args == [1, "one", 2, "two", "other"]


def test_decode_oracle_expression_args():
    func = DecodeOracle(Column("column1"), Column("column2"), "match")
    assert str(func) == "DECODE_ORACLE(`column1`, `column2`, %s)"
    assert func.args == ["match"]


# ---------------------------------------------------------------------------
# CASE - searched form
# ---------------------------------------------------------------------------


def test_case_searched_single_when():
    case = Case().when(Column("id") == 1, "one")
    assert str(case) == "CASE WHEN `id` = %s THEN %s END"
    assert case.args == [1, "one"]


def test_case_searched_multiple_when():
    case = Case().when(Column("id") == 1, "one").when(Column("id") == 2, "two")
    assert str(case) == "CASE WHEN `id` = %s THEN %s WHEN `id` = %s THEN %s END"
    assert case.args == [1, "one", 2, "two"]


def test_case_searched_with_else():
    case = Case().when(Column("id") == 1, "one").when(Column("id") == 2, "two").else_("other")
    assert str(case) == "CASE WHEN `id` = %s THEN %s WHEN `id` = %s THEN %s ELSE %s END"
    assert case.args == [1, "one", 2, "two", "other"]


def test_case_searched_condition_with_own_args():
    case = Case().when(Eq(Column("id"), 1) & Eq(Column("status"), "active"), "match").else_("no match")
    assert str(case) == "CASE WHEN (`id` = %s AND `status` = %s) THEN %s ELSE %s END"
    assert case.args == [1, "active", "match", "no match"]


def test_case_searched_statement_result():
    case = Case().when(Column("id") == 1, Column("name")).else_(Column("fallback"))
    assert str(case) == "CASE WHEN `id` = %s THEN `name` ELSE `fallback` END"
    assert case.args == [1]


def test_case_else_none_is_bound_null():
    case = Case().when(Column("id") == 1, "one").else_(None)
    assert str(case) == "CASE WHEN `id` = %s THEN %s ELSE %s END"
    assert case.args == [1, "one", None]


# ---------------------------------------------------------------------------
# CASE - simple form
# ---------------------------------------------------------------------------


def test_case_simple_single_when():
    case = Case(Column("status")).when("A", "Active")
    assert str(case) == "CASE `status` WHEN %s THEN %s END"
    assert case.args == ["A", "Active"]


def test_case_simple_multiple_when_with_else():
    case = Case(Column("status")).when("A", "Active").when("I", "Inactive").else_("Unknown")
    assert str(case) == "CASE `status` WHEN %s THEN %s WHEN %s THEN %s ELSE %s END"
    assert case.args == ["A", "Active", "I", "Inactive", "Unknown"]


def test_case_simple_statement_operand_and_compare():
    case = Case(Column("a")).when(Column("b"), "match")
    assert str(case) == "CASE `a` WHEN `b` THEN %s END"
    assert case.args == ["match"]


def test_case_simple_operand_none():
    # CASE NULL WHEN ... is unusual, but a legitimate, explicit CASE operand -- distinct from omitting it.
    case = Case(None).when(None, "null case")
    assert str(case) == "CASE %s WHEN %s THEN %s END"
    assert case.args == [None, None, "null case"]


# ---------------------------------------------------------------------------
# CASE - constructor pairs form
# ---------------------------------------------------------------------------


def test_case_constructor_cases_searched():
    case = Case(cases=[(Column("id") == 1, "one"), (Column("id") == 2, "two")], else_="other")
    assert str(case) == "CASE WHEN `id` = %s THEN %s WHEN `id` = %s THEN %s ELSE %s END"
    assert case.args == [1, "one", 2, "two", "other"]


def test_case_constructor_cases_simple():
    case = Case(Column("status"), cases=[("A", "Active"), ("I", "Inactive")], else_="Unknown")
    assert str(case) == "CASE `status` WHEN %s THEN %s WHEN %s THEN %s ELSE %s END"
    assert case.args == ["A", "Active", "I", "Inactive", "Unknown"]


def test_case_constructor_cases_and_when_combine():
    case = Case(cases=[(Column("id") == 1, "one")]).when(Column("id") == 2, "two")
    assert str(case) == "CASE WHEN `id` = %s THEN %s WHEN `id` = %s THEN %s END"
    assert case.args == [1, "one", 2, "two"]


# ---------------------------------------------------------------------------
# CASE - errors
# ---------------------------------------------------------------------------


def test_case_without_when_raises_on_render():
    case = Case()
    with pytest.raises(ValueError, match="at least one WHEN"):
        str(case)


def test_case_with_else_only_still_raises():
    case = Case().else_("fallback")
    with pytest.raises(ValueError, match="at least one WHEN"):
        str(case)


# ---------------------------------------------------------------------------
# Integration with Select / Update
# ---------------------------------------------------------------------------


def test_case_in_select():
    q = Select(
        "id",
        Case().when(Column("score") >= 90, "A").when(Column("score") >= 80, "B").else_("C"),
        table="students",
    )
    assert str(q) == ("SELECT `id`, CASE WHEN `score` >= %s THEN %s WHEN `score` >= %s THEN %s ELSE %s END FROM `students`")
    assert q.args == [90, "A", 80, "B", "C"]


def test_case_in_select_where():
    q = Select("id", table="students", where=Eq(Case(Column("status")).when("A", 1).when("I", 0), 1))
    assert str(q) == "SELECT `id` FROM `students` WHERE CASE `status` WHEN %s THEN %s WHEN %s THEN %s END = %s"
    assert q.args == ["A", 1, "I", 0, 1]


def test_case_in_update():
    u = Update("students").set(
        "grade",
        Case().when(Column("score") >= 90, "A").when(Column("score") >= 80, "B").else_("C"),
    )
    assert str(u) == ("UPDATE `students` SET `grade` = CASE WHEN `score` >= %s THEN %s WHEN `score` >= %s THEN %s ELSE %s END")
    assert u.args == [90, "A", 80, "B", "C"]


def test_case_and_nvl2_compose():
    q = Select(
        "id",
        Nvl2(Column("discount"), Case().when(Column("discount") > 0, "Discounted").else_("Full price"), "N/A"),
        table="products",
    )
    assert str(q) == ("SELECT `id`, NVL2(`discount`, CASE WHEN `discount` > %s THEN %s ELSE %s END, %s) FROM `products`")
    assert q.args == [0, "Discounted", "Full price", "N/A"]


def test_case_in_order_by():
    q = Select("id", table="t", order=Order([(Case(Column("status")).when("A", 1).else_(2), Direction.ASC)]))
    assert str(q) == "SELECT `id` FROM `t` ORDER BY CASE `status` WHEN %s THEN %s ELSE %s END ASC"
    assert q.args == ["A", 1, 2]


def test_case_inside_an_aggregate_and_its_window():
    total = Sum(Case().when(Eq("active", 1), Column("amount")).else_(0))
    assert str(total) == "SUM(CASE WHEN `active` = %s THEN `amount` ELSE %s END)"
    assert total.args == [1, 0]

    windowed = Sum(Case().when(Eq("active", 1), Column("amount")).else_(0)).over(partition_by=[Column("category")])
    assert str(windowed) == "SUM(CASE WHEN `active` = %s THEN `amount` ELSE %s END) OVER (PARTITION BY `category`)"
    assert windowed.args == [1, 0]
