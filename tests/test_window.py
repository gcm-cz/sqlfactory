"""Tests for window functions."""

import pytest

from sqlfactory import Aliased, Direction, Select
from sqlfactory.func.agg import Avg, Count, Max, Min, Std, Sum
from sqlfactory.func.window import (
    CumeDist,
    DenseRank,
    FirstValue,
    Frame,
    FrameBound,
    FrameType,
    Lag,
    LastValue,
    Lead,
    Median,
    NthValue,
    Ntile,
    OverClause,
    PercentileCont,
    PercentileDisc,
    PercentRank,
    Rank,
    RowNumber,
)


# ---------------------------------------------------------------------------
# FrameBound
# ---------------------------------------------------------------------------

def test_frame_bound_constants():
    assert str(FrameBound.UNBOUNDED_PRECEDING) == "UNBOUNDED PRECEDING"
    assert str(FrameBound.CURRENT_ROW) == "CURRENT ROW"
    assert str(FrameBound.UNBOUNDED_FOLLOWING) == "UNBOUNDED FOLLOWING"


def test_frame_bound_preceding():
    b = FrameBound.preceding(3)
    assert str(b) == "%s PRECEDING"
    assert b.args == [3]


def test_frame_bound_following():
    b = FrameBound.following(2)
    assert str(b) == "%s FOLLOWING"
    assert b.args == [2]


# ---------------------------------------------------------------------------
# Frame
# ---------------------------------------------------------------------------

def test_frame_single_bound():
    f = Frame(FrameType.ROWS, FrameBound.UNBOUNDED_PRECEDING)
    assert str(f) == "ROWS UNBOUNDED PRECEDING"
    assert f.args == []


def test_frame_between():
    f = Frame(FrameType.ROWS, FrameBound.UNBOUNDED_PRECEDING, FrameBound.CURRENT_ROW)
    assert str(f) == "ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW"
    assert f.args == []


def test_frame_range_numeric():
    f = Frame(FrameType.RANGE, FrameBound.preceding(2), FrameBound.following(2))
    assert str(f) == "RANGE BETWEEN %s PRECEDING AND %s FOLLOWING"
    assert f.args == [2, 2]


def test_frame_groups():
    f = Frame(FrameType.GROUPS, FrameBound.UNBOUNDED_PRECEDING, FrameBound.UNBOUNDED_FOLLOWING)
    assert str(f) == "GROUPS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING"


# ---------------------------------------------------------------------------
# OverClause
# ---------------------------------------------------------------------------

def test_over_clause_empty():
    assert str(OverClause()) == "OVER ()"
    assert OverClause().args == []


def test_over_clause_partition_by_string():
    o = OverClause(partition_by=["category"])
    assert str(o) == "OVER (PARTITION BY `category`)"
    assert o.args == []


def test_over_clause_partition_by_multiple():
    o = OverClause(partition_by=["dept", "region"])
    assert str(o) == "OVER (PARTITION BY `dept`, `region`)"


def test_over_clause_partition_by_statement_with_args():
    from sqlfactory import Raw
    # Raw statement with an argument value used directly in partition_by
    expr = Raw("`category` = %s", "electronics")
    o = OverClause(partition_by=[expr])
    assert str(o) == "OVER (PARTITION BY `category` = %s)"
    assert o.args == ["electronics"]


def test_over_clause_order():
    o = OverClause(order=[("price", Direction.DESC)])
    assert str(o) == "OVER (ORDER BY `price` DESC)"
    assert o.args == []


def test_over_clause_partition_and_order():
    o = OverClause(partition_by=["category"], order=[("price", Direction.DESC)])
    assert str(o) == "OVER (PARTITION BY `category` ORDER BY `price` DESC)"


def test_over_clause_with_frame():
    o = OverClause(
        order=[("date", Direction.ASC)],
        frame=Frame(FrameType.ROWS, FrameBound.UNBOUNDED_PRECEDING, FrameBound.CURRENT_ROW),
    )
    assert str(o) == "OVER (ORDER BY `date` ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)"


def test_over_clause_full():
    o = OverClause(
        partition_by=["category"],
        order=[("price", Direction.DESC)],
        frame=Frame(FrameType.ROWS, FrameBound.preceding(1), FrameBound.CURRENT_ROW),
    )
    assert str(o) == "OVER (PARTITION BY `category` ORDER BY `price` DESC ROWS BETWEEN %s PRECEDING AND CURRENT ROW)"
    assert o.args == [1]


# ---------------------------------------------------------------------------
# Pure window functions
# ---------------------------------------------------------------------------

def test_row_number():
    f = RowNumber().over(partition_by=["dept"], order=[("salary", Direction.DESC)])
    assert str(f) == "ROW_NUMBER() OVER (PARTITION BY `dept` ORDER BY `salary` DESC)"
    assert f.args == []


def test_rank():
    f = Rank().over(order=[("score", Direction.ASC)])
    assert str(f) == "RANK() OVER (ORDER BY `score` ASC)"


def test_dense_rank():
    f = DenseRank().over(partition_by=["dept"])
    assert str(f) == "DENSE_RANK() OVER (PARTITION BY `dept`)"


def test_percent_rank():
    f = PercentRank().over()
    assert str(f) == "PERCENT_RANK() OVER ()"


def test_cume_dist():
    f = CumeDist().over(order=[("score", Direction.ASC)])
    assert str(f) == "CUME_DIST() OVER (ORDER BY `score` ASC)"


def test_ntile():
    f = Ntile(4).over(order=[("price", Direction.ASC)])
    assert str(f) == "NTILE(%s) OVER (ORDER BY `price` ASC)"
    assert f.args == [4]


def test_lag_simple():
    f = Lag("price").over(order=[("date", Direction.ASC)])
    assert str(f) == "LAG(`price`) OVER (ORDER BY `date` ASC)"
    assert f.args == []


def test_lag_with_offset():
    f = Lag("price", offset=1).over(order=[("date", Direction.ASC)])
    assert str(f) == "LAG(`price`, %s) OVER (ORDER BY `date` ASC)"
    assert f.args == [1]


def test_lag_with_offset_and_default():
    f = Lag("price", offset=1, default=0).over(order=[("date", Direction.ASC)])
    assert str(f) == "LAG(`price`, %s, %s) OVER (ORDER BY `date` ASC)"
    assert f.args == [1, 0]


def test_lead_simple():
    f = Lead("price").over(order=[("date", Direction.ASC)])
    assert str(f) == "LEAD(`price`) OVER (ORDER BY `date` ASC)"
    assert f.args == []


def test_lead_with_offset():
    f = Lead("price", offset=2).over(order=[("date", Direction.ASC)])
    assert str(f) == "LEAD(`price`, %s) OVER (ORDER BY `date` ASC)"
    assert f.args == [2]


def test_lead_with_offset_and_default():
    f = Lead("price", offset=2, default=0).over(order=[("date", Direction.ASC)])
    assert str(f) == "LEAD(`price`, %s, %s) OVER (ORDER BY `date` ASC)"
    assert f.args == [2, 0]


def test_first_value():
    f = FirstValue("price").over(partition_by=["category"], order=[("date", Direction.ASC)])
    assert str(f) == "FIRST_VALUE(`price`) OVER (PARTITION BY `category` ORDER BY `date` ASC)"
    assert f.args == []


def test_last_value():
    f = LastValue("price").over(partition_by=["category"], order=[("date", Direction.ASC)])
    assert str(f) == "LAST_VALUE(`price`) OVER (PARTITION BY `category` ORDER BY `date` ASC)"


def test_nth_value():
    f = NthValue("price", 2).over(partition_by=["category"])
    assert str(f) == "NTH_VALUE(`price`, %s) OVER (PARTITION BY `category`)"
    assert f.args == [2]


# ---------------------------------------------------------------------------
# MEDIAN
# ---------------------------------------------------------------------------

def test_median_no_partition():
    m = Median("price")
    assert str(m) == "MEDIAN(`price`) OVER ()"
    assert m.args == []


def test_median_partition_by():
    m = Median("price", partition_by=["category"])
    assert str(m) == "MEDIAN(`price`) OVER (PARTITION BY `category`)"
    assert m.args == []


def test_median_column_and_partition_args_flow():
    from sqlfactory import Raw
    m = Median(Raw("`a` + %s", 1), partition_by=[Raw("`b` = %s", 2)])
    assert str(m) == "MEDIAN(`a` + %s) OVER (PARTITION BY `b` = %s)"
    assert m.args == [1, 2]


# ---------------------------------------------------------------------------
# PERCENTILE_CONT / PERCENTILE_DISC
# ---------------------------------------------------------------------------

def test_percentile_cont_basic():
    f = PercentileCont(0.5, order=("price", Direction.ASC))
    assert str(f) == "PERCENTILE_CONT(%s) WITHIN GROUP (ORDER BY `price` ASC) OVER ()"
    assert f.args == [0.5]


def test_percentile_cont_partition_by():
    f = PercentileCont(0.5, order=("price", Direction.ASC), partition_by=["category"])
    assert str(f) == "PERCENTILE_CONT(%s) WITHIN GROUP (ORDER BY `price` ASC) OVER (PARTITION BY `category`)"
    assert f.args == [0.5]


def test_percentile_disc_basic():
    f = PercentileDisc(0.25, order=("price", Direction.DESC), partition_by=["category"])
    assert str(f) == "PERCENTILE_DISC(%s) WITHIN GROUP (ORDER BY `price` DESC) OVER (PARTITION BY `category`)"
    assert f.args == [0.25]


def test_percentile_function_args_order():
    """Placeholder order must be fraction, then WITHIN GROUP's ORDER BY args, then OVER's PARTITION BY args."""
    from sqlfactory import Raw
    f = PercentileCont(0.9, order=(Raw("`a` + %s", 1), Direction.ASC), partition_by=[Raw("`b` = %s", 2)])
    assert str(f) == "PERCENTILE_CONT(%s) WITHIN GROUP (ORDER BY `a` + %s ASC) OVER (PARTITION BY `b` = %s)"
    assert f.args == [0.9, 1, 2]


def test_percentile_function_rejects_multiple_sort_keys():
    """WITHIN GROUP (ORDER BY ...) takes exactly one sort key -- MariaDB and PostgreSQL both reject more than
    one. mypy already rejects this at the type level (see tests/test_typing.yml); this is the runtime backstop
    for a caller that bypasses typing."""
    with pytest.raises(ValueError, match="exactly one sort key"):
        PercentileCont(0.5, order=[("price", Direction.ASC), ("other", Direction.DESC)])  # type: ignore[arg-type]


def test_median_and_percentile_in_select():
    q = Select(
        "name",
        Aliased(Median("star_rating", partition_by=["name"]), alias="med"),
        Aliased(PercentileCont(0.5, order=("star_rating", Direction.ASC), partition_by=["name"]), alias="pc"),
        Aliased(PercentileDisc(0.5, order=("star_rating", Direction.ASC), partition_by=["name"]), alias="pd"),
        table="book_rating",
    )
    assert str(q) == (
        "SELECT `name`, "
        "MEDIAN(`star_rating`) OVER (PARTITION BY `name`) AS `med`, "
        "PERCENTILE_CONT(%s) WITHIN GROUP (ORDER BY `star_rating` ASC) OVER (PARTITION BY `name`) AS `pc`, "
        "PERCENTILE_DISC(%s) WITHIN GROUP (ORDER BY `star_rating` ASC) OVER (PARTITION BY `name`) AS `pd` "
        "FROM `book_rating`"
    )
    assert q.args == [0.5, 0.5]


# ---------------------------------------------------------------------------
# Aggregate functions used as window functions
# ---------------------------------------------------------------------------

def test_sum_over():
    f = Sum("price").over(partition_by=["category"])
    assert str(f) == "SUM(`price`) OVER (PARTITION BY `category`)"
    assert f.args == []


def test_avg_over():
    f = Avg("salary").over(partition_by=["dept"], order=[("hire_date", Direction.ASC)])
    assert str(f) == "AVG(`salary`) OVER (PARTITION BY `dept` ORDER BY `hire_date` ASC)"


def test_count_over():
    f = Count("*").over()
    assert str(f) == "COUNT(*) OVER ()"
    assert f.args == []


def test_max_over():
    f = Max("score").over(partition_by=["group"])
    assert str(f) == "MAX(`score`) OVER (PARTITION BY `group`)"


def test_min_over():
    f = Min("score").over(partition_by=["group"])
    assert str(f) == "MIN(`score`) OVER (PARTITION BY `group`)"


def test_std_over():
    f = Std("value").over(partition_by=["group"])
    assert str(f) == "STD(`value`) OVER (PARTITION BY `group`)"


# ---------------------------------------------------------------------------
# Reusable OverClause
# ---------------------------------------------------------------------------

def test_reusable_over_clause():
    window = OverClause(partition_by=["dept"], order=[("salary", Direction.DESC)])
    r = RowNumber().over(window)
    rk = Rank().over(window)
    assert str(r) == "ROW_NUMBER() OVER (PARTITION BY `dept` ORDER BY `salary` DESC)"
    assert str(rk) == "RANK() OVER (PARTITION BY `dept` ORDER BY `salary` DESC)"


# ---------------------------------------------------------------------------
# Integration with Select
# ---------------------------------------------------------------------------

def test_window_function_in_select():
    q = Select(
        "id",
        "category",
        "price",
        Aliased(
            RowNumber().over(partition_by=["category"], order=[("price", Direction.DESC)]),
            alias="row_num",
        ),
        table="products",
    )
    assert str(q) == (
        "SELECT `id`, `category`, `price`, "
        "ROW_NUMBER() OVER (PARTITION BY `category` ORDER BY `price` DESC) AS `row_num` "
        "FROM `products`"
    )
    assert q.args == []


def test_multiple_window_functions_in_select():
    q = Select(
        "id",
        "price",
        Aliased(Sum("price").over(partition_by=["category"]), alias="cat_total"),
        Aliased(Ntile(4).over(order=[("price", Direction.ASC)]), alias="quartile"),
        table="products",
    )
    assert str(q) == (
        "SELECT `id`, `price`, "
        "SUM(`price`) OVER (PARTITION BY `category`) AS `cat_total`, "
        "NTILE(%s) OVER (ORDER BY `price` ASC) AS `quartile` "
        "FROM `products`"
    )
    assert q.args == [4]


def test_window_function_args_flow_through_select():
    q = Select(
        Aliased(Lag("price", offset=1, default=0).over(order=[("date", Direction.ASC)]), alias="prev_price"),
        Aliased(NthValue("price", 3).over(partition_by=["category"]), alias="third_price"),
        table="prices",
    )
    assert q.args == [1, 0, 3]


def test_window_with_frame_in_select():
    q = Select(
        "id",
        "price",
        Aliased(
            Avg("price").over(
                order=[("date", Direction.ASC)],
                frame=Frame(FrameType.ROWS, FrameBound.preceding(2), FrameBound.CURRENT_ROW),
            ),
            alias="moving_avg",
        ),
        table="prices",
    )
    assert str(q) == (
        "SELECT `id`, `price`, "
        "AVG(`price`) OVER (ORDER BY `date` ASC ROWS BETWEEN %s PRECEDING AND CURRENT ROW) AS `moving_avg` "
        "FROM `prices`"
    )
    assert q.args == [2]





