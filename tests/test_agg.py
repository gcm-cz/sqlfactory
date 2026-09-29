"""Tests for aggregate functions added on top of the pre-existing AVG/BIT_AND/BIT_OR/BIT_XOR/COUNT/MAX/MIN/STD/SUM."""

import pytest

from sqlfactory import Column, Direction, Limit, PostgreSQLDialect, Raw, Select, SQLiteDialect
from sqlfactory.func.agg import (
    Avg,
    Count,
    GroupConcat,
    JsonArrayAgg,
    JsonObjectAgg,
    Max,
    Min,
    Std,
    Stddev,
    StddevPop,
    StddevSamp,
    Sum,
    Variance,
    VarPop,
    VarSamp,
)

# ---------------------------------------------------------------------------
# DISTINCT on the pre-existing AVG/MAX/MIN/SUM constructors
# ---------------------------------------------------------------------------


def test_avg_distinct():
    f = Avg("column1", distinct=True)
    assert str(f) == "AVG(DISTINCT `column1`)"
    assert f.args == []


def test_avg_not_distinct_by_default():
    f = Avg("column1")
    assert str(f) == "AVG(`column1`)"
    assert f.args == []


def test_max_distinct():
    f = Max("column1", distinct=True)
    assert str(f) == "MAX(DISTINCT `column1`)"
    assert f.args == []


def test_min_distinct():
    f = Min("column1", distinct=True)
    assert str(f) == "MIN(DISTINCT `column1`)"
    assert f.args == []


def test_sum_distinct():
    f = Sum("column1", distinct=True)
    assert str(f) == "SUM(DISTINCT `column1`)"
    assert f.args == []


def test_distinct_with_statement_column():
    # Distinct-wrapping must also work when column is already a Statement (not a plain string), and must carry
    # over that statement's own args.
    f = Avg(Raw("column1 + %s", 1), distinct=True)
    assert str(f) == "AVG(DISTINCT column1 + %s)"
    assert f.args == [1]


def test_sum_distinct_dialect_sqlite():
    # Regression: DISTINCT must be rendered lazily (at str() time), not baked in eagerly at construction using
    # whatever dialect happened to be active then - otherwise the column's own placeholders/quoting are frozen
    # to the wrong dialect once the whole statement is rendered under a different one.
    query = Select(Sum(Column("a") * 2, distinct=True), table="t", dialect=SQLiteDialect())
    assert str(query) == "SELECT SUM(DISTINCT (`a` * ?)) FROM `t`"


def test_sum_distinct_dialect_postgresql():
    query = Select(Sum(Column("a") * 2, distinct=True), table="t", dialect=PostgreSQLDialect())
    assert str(query) == 'SELECT SUM(DISTINCT ("a" * %s)) FROM "t"'


def test_count_distinct_dialect_sqlite():
    query = Select(Count(Column("a"), Column("b") + 1, distinct=True), table="t", dialect=SQLiteDialect())
    assert str(query) == "SELECT COUNT(DISTINCT `a`, (`b` + ?)) FROM `t`"


def test_count_distinct_dialect_postgresql():
    query = Select(Count(Column("a"), Column("b") + 1, distinct=True), table="t", dialect=PostgreSQLDialect())
    assert str(query) == 'SELECT COUNT(DISTINCT "a", ("b" + %s)) FROM "t"'


# ---------------------------------------------------------------------------
# COUNT(DISTINCT expr, expr, ...) - multiple-expression form
# ---------------------------------------------------------------------------


def test_count_multiple_columns_distinct():
    f = Count("a", "b", distinct=True)
    assert str(f) == "COUNT(DISTINCT `a`, `b`)"
    assert f.args == []


def test_count_multiple_columns_without_distinct_raises():
    with pytest.raises(ValueError, match="distinct=True"):
        Count("a", "b")


def test_count_star():
    # Backward-compatible call form: bare COUNT(*), no distinct.
    f = Count("*")
    assert str(f) == "COUNT(*)"
    assert f.args == []


def test_count_star_distinct_raises():
    # COUNT(DISTINCT *) is not valid SQL -- MariaDB rejects '*' combined with DISTINCT.
    with pytest.raises(ValueError, match=r"\*"):
        Count("*", distinct=True)


def test_count_star_with_extra_columns_raises():
    with pytest.raises(ValueError, match=r"\*"):
        Count("*", "b", distinct=True)


# ---------------------------------------------------------------------------
# DISTINCT combined with OVER (window functions)
# ---------------------------------------------------------------------------


def test_avg_distinct_over_raises():
    with pytest.raises(ValueError, match="window function"):
        Avg("column1", distinct=True).over()


def test_sum_distinct_over_raises():
    with pytest.raises(ValueError, match="window function"):
        Sum("column1", distinct=True).over()


def test_count_distinct_over_raises():
    with pytest.raises(ValueError, match="window function"):
        Count("column1", distinct=True).over()


def test_avg_over_without_distinct_is_allowed():
    f = Avg("column1").over()
    assert str(f) == "AVG(`column1`) OVER ()"


def test_sum_over_without_distinct_is_allowed():
    f = Sum("column1").over()
    assert str(f) == "SUM(`column1`) OVER ()"


def test_count_over_without_distinct_is_allowed():
    f = Count("column1").over()
    assert str(f) == "COUNT(`column1`) OVER ()"


def test_min_distinct_over_is_allowed():
    # MariaDB accepts MIN(DISTINCT ...)/MAX(DISTINCT ...) as window functions, unlike AVG/SUM/COUNT.
    f = Min("column1", distinct=True).over()
    assert str(f) == "MIN(DISTINCT `column1`) OVER ()"


def test_max_distinct_over_is_allowed():
    f = Max("column1", distinct=True).over()
    assert str(f) == "MAX(DISTINCT `column1`) OVER ()"


# ---------------------------------------------------------------------------
# GROUP_CONCAT
# ---------------------------------------------------------------------------


def test_group_concat_single_column():
    f = GroupConcat("name")
    assert str(f) == "GROUP_CONCAT(`name`)"
    assert f.args == []


def test_group_concat_multiple_columns():
    f = GroupConcat("first_name", "last_name")
    assert str(f) == "GROUP_CONCAT(`first_name`, `last_name`)"
    assert f.args == []


def test_group_concat_distinct():
    f = GroupConcat("name", distinct=True)
    assert str(f) == "GROUP_CONCAT(DISTINCT `name`)"
    assert f.args == []


def test_group_concat_order():
    f = GroupConcat("name", order=[("name", Direction.DESC)])
    assert str(f) == "GROUP_CONCAT(`name` ORDER BY `name` DESC)"
    assert f.args == []


def test_group_concat_separator():
    f = GroupConcat("name", separator=", ")
    assert str(f) == "GROUP_CONCAT(`name` SEPARATOR %s)"
    assert f.args == [", "]


def test_group_concat_separator_as_statement():
    # The escape hatch documented on the class: pass a Statement (e.g. Raw) to get a real SQL literal instead of
    # a driver-interpolated placeholder.
    f = GroupConcat("name", separator=Raw("', '"))
    assert str(f) == "GROUP_CONCAT(`name` SEPARATOR ', ')"
    assert f.args == []


def test_group_concat_limit():
    f = GroupConcat("name", limit=Limit(10))
    assert str(f) == "GROUP_CONCAT(`name` LIMIT %s)"
    assert f.args == [10]


def test_group_concat_limit_with_offset():
    f = GroupConcat("name", limit=Limit(5, 10))
    assert str(f) == "GROUP_CONCAT(`name` LIMIT %s, %s)"
    assert f.args == [5, 10]


def test_group_concat_all_clauses():
    # Proves args order end to end: expression args, then ORDER BY args, then separator, then LIMIT args - using
    # Statement-valued expressions (not just plain columns) in both the expr list and ORDER BY, so a wrong order
    # would actually be caught rather than coincidentally matching (all involved args here are distinguishable).
    f = GroupConcat(
        Raw("CONCAT(a, %s)", "X"),
        "last_name",
        distinct=True,
        order=[(Raw("FIELD(b, %s, %s)", 1, 2), Direction.DESC)],
        separator=" - ",
        limit=Limit(2, 5),
    )
    assert str(f) == (
        "GROUP_CONCAT(DISTINCT CONCAT(a, %s), `last_name` ORDER BY FIELD(b, %s, %s) DESC SEPARATOR %s LIMIT %s, %s)"
    )
    assert f.args == ["X", 1, 2, " - ", 2, 5]


def test_group_concat_column_as_statement():
    f = GroupConcat(Column("name"))
    assert str(f) == "GROUP_CONCAT(`name`)"
    assert f.args == []


def test_group_concat_not_windowable():
    # GROUP_CONCAT cannot be used as a window function - it must not expose .over().
    assert not hasattr(GroupConcat("name"), "over")


# ---------------------------------------------------------------------------
# JSON_ARRAYAGG
# ---------------------------------------------------------------------------


def test_json_arrayagg_basic():
    f = JsonArrayAgg("name")
    assert str(f) == "JSON_ARRAYAGG(`name`)"
    assert f.args == []


def test_json_arrayagg_distinct():
    f = JsonArrayAgg("name", distinct=True)
    assert str(f) == "JSON_ARRAYAGG(DISTINCT `name`)"
    assert f.args == []


def test_json_arrayagg_order():
    f = JsonArrayAgg("name", order=[("name", Direction.DESC)])
    assert str(f) == "JSON_ARRAYAGG(`name` ORDER BY `name` DESC)"
    assert f.args == []


def test_json_arrayagg_limit():
    f = JsonArrayAgg("name", limit=Limit(3))
    assert str(f) == "JSON_ARRAYAGG(`name` LIMIT %s)"
    assert f.args == [3]


def test_json_arrayagg_all_clauses():
    f = JsonArrayAgg("name", distinct=True, order=[("name", Direction.ASC)], limit=Limit(1, 2))
    assert str(f) == "JSON_ARRAYAGG(DISTINCT `name` ORDER BY `name` ASC LIMIT %s, %s)"
    assert f.args == [1, 2]


def test_json_arrayagg_not_windowable():
    assert not hasattr(JsonArrayAgg("name"), "over")


# ---------------------------------------------------------------------------
# JSON_OBJECTAGG
# ---------------------------------------------------------------------------


def test_json_objectagg():
    f = JsonObjectAgg("name", "price")
    assert str(f) == "JSON_OBJECTAGG(`name`, `price`)"
    assert f.args == []


def test_json_objectagg_statement_args():
    f = JsonObjectAgg(Column("name"), Raw("price * %s", 2))
    assert str(f) == "JSON_OBJECTAGG(`name`, price * %s)"
    assert f.args == [2]


def test_json_objectagg_not_windowable():
    assert not hasattr(JsonObjectAgg("name", "price"), "over")


# ---------------------------------------------------------------------------
# STDDEV / STDDEV_POP / STDDEV_SAMP
# ---------------------------------------------------------------------------


def test_stddev_pop():
    f = StddevPop("column1")
    assert str(f) == "STDDEV_POP(`column1`)"
    assert f.args == []


def test_stddev_samp():
    f = StddevSamp("column1")
    assert str(f) == "STDDEV_SAMP(`column1`)"
    assert f.args == []


def test_stddev_is_synonym_of_std():
    f = Stddev("column1")
    assert str(f) == "STDDEV(`column1`)"
    assert f.args == []
    assert isinstance(f, Std)


def test_stddev_pop_over():
    f = StddevPop("column1").over(partition_by=["dept"])
    assert str(f) == "STDDEV_POP(`column1`) OVER (PARTITION BY `dept`)"


def test_stddev_samp_over():
    f = StddevSamp("column1").over()
    assert str(f) == "STDDEV_SAMP(`column1`) OVER ()"


def test_stddev_over():
    f = Stddev("column1").over()
    assert str(f) == "STDDEV(`column1`) OVER ()"


# ---------------------------------------------------------------------------
# VAR_POP / VAR_SAMP / VARIANCE
# ---------------------------------------------------------------------------


def test_var_pop():
    f = VarPop("column1")
    assert str(f) == "VAR_POP(`column1`)"
    assert f.args == []


def test_var_samp():
    f = VarSamp("column1")
    assert str(f) == "VAR_SAMP(`column1`)"
    assert f.args == []


def test_variance_is_synonym_of_var_pop():
    f = Variance("column1")
    assert str(f) == "VARIANCE(`column1`)"
    assert f.args == []
    assert isinstance(f, VarPop)


def test_var_pop_over():
    f = VarPop("column1").over(order=[("date", Direction.ASC)])
    assert str(f) == "VAR_POP(`column1`) OVER (ORDER BY `date` ASC)"


def test_var_samp_over():
    f = VarSamp("column1").over()
    assert str(f) == "VAR_SAMP(`column1`) OVER ()"


def test_variance_over():
    f = Variance("column1").over()
    assert str(f) == "VARIANCE(`column1`) OVER ()"


# ---------------------------------------------------------------------------
# Composition: new aggregates used together inside a real Select
# ---------------------------------------------------------------------------


def test_compose_in_select():
    query = Select(
        "department",
        GroupConcat("name", order=[("name", Direction.ASC)], separator=", "),
        JsonArrayAgg("name", distinct=True),
        VarPop("salary").over(partition_by=["department"]),
        table="employees",
        group_by=["department"],
    )

    assert str(query) == (
        "SELECT `department`, GROUP_CONCAT(`name` ORDER BY `name` ASC SEPARATOR %s), "
        "JSON_ARRAYAGG(DISTINCT `name`), VAR_POP(`salary`) OVER (PARTITION BY `department`) "
        "FROM `employees` GROUP BY `department`"
    )
    assert query.args == [", "]
