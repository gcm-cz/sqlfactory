"""A query used as a value of another statement (a scalar subquery) is rendered in parentheses, as SQL writes it."""

import pytest

from sqlfactory import (
    Aliased,
    Between,
    Column,
    Delete,
    Direction,
    Eq,
    Except,
    ExceptAll,
    ExceptDistinct,
    Exists,
    Ge,
    Gt,
    In,
    Insert,
    Intersect,
    IntersectAll,
    IntersectDistinct,
    IsJson,
    IsNotJson,
    Join,
    JsonValueType,
    Le,
    LeftJoin,
    Like,
    Limit,
    Lt,
    Ne,
    NotBetween,
    NotExists,
    NotIn,
    NotLike,
    NotRLike,
    Query,
    Raw,
    RLike,
    Select,
    Statement,
    Table,
    Union,
    UnionAll,
    UnionDistinct,
    Update,
    Value,
    With,
)
from sqlfactory.entities import BinaryExpression, UnaryExpression
from sqlfactory.func.agg import Count, GroupConcat, JsonArrayAgg, JsonObjectAgg, Max, Sum
from sqlfactory.func.control import Case, Coalesce
from sqlfactory.func.datetime import DateAdd, Extract, Interval
from sqlfactory.func.geometry import Point
from sqlfactory.func.info import Collate
from sqlfactory.func.json import JsonExtract, JsonTable, JsonTableColumn
from sqlfactory.func.numeric import Round
from sqlfactory.func.spatial import StDistanceSphere
from sqlfactory.func.str import Concat
from sqlfactory.func.window import Lag
from sqlfactory.statement import operand


def sub(key: str = "k1") -> Select:
    """A scalar subquery with a bound value of its own, so that tests can check the order of args."""
    return Select(Max("t.ts"), table="t", where=Eq("t.k", key))


SUB = "(SELECT MAX(`t`.`ts`) FROM `t` WHERE `t`.`k` = %s)"
"""How `sub()` renders as an operand."""

UNION_VARIANTS = [Union, UnionAll, UnionDistinct, Except, ExceptAll, ExceptDistinct, Intersect, IntersectAll, IntersectDistinct]

# ---------------------------------------------------------------------------
# The Query marker and the helper
# ---------------------------------------------------------------------------


def test_operand_parenthesises_a_query():
    assert operand(sub()) == SUB


def test_operand_renders_other_statements_as_they_are():
    assert operand(Column("o.a")) == "`o`.`a`"
    assert operand(Max("o.a")) == "MAX(`o`.`a`)"
    assert operand(Value(1)) == "%s"
    # Raw SQL is used verbatim, even when it is a query - its author owns the parentheses.
    assert operand(Raw("SELECT 1")) == "SELECT 1"


@pytest.mark.parametrize("query_class", [Select, With, *UNION_VARIANTS])
def test_queries_are_query_statements(query_class):
    assert issubclass(query_class, Query)


@pytest.mark.parametrize(
    "statement_class", [Statement, Column, Table, Raw, Value, Aliased, Max, Eq, Insert, Update, Delete, Join, Limit]
)
def test_other_statements_are_not_queries(statement_class):
    assert not issubclass(statement_class, Query)


def test_table_attribute_access_still_yields_any_column():
    """The marker adds no attribute to `Statement`, so no column name is shadowed on `Table`."""
    column = Table("t").is_query
    assert isinstance(column, Column)
    assert str(column) == "`t`.`is_query`"


class TableValueConstructor(Query):
    """A user-defined query statement: MariaDB's `VALUES (...), ...` table value constructor."""

    def __init__(self, *values):
        super().__init__()
        self._values = values

    def __str__(self):
        return "VALUES " + ", ".join(f"({self.dialect.placeholder})" for _ in self._values)

    @property
    def args(self):
        return list(self._values)


def test_user_defined_query_is_parenthesised():
    cond = Eq("o.a", TableValueConstructor(1))
    assert str(cond) == "`o`.`a` = (VALUES (%s))"
    assert cond.args == [1]

    cond = In("o.a", TableValueConstructor(1, 2))
    assert str(cond) == "`o`.`a` IN (VALUES (%s), (%s))"
    assert cond.args == [1, 2]


def test_top_level_query_is_not_parenthesised():
    assert str(sub()) == SUB[1:-1]
    assert sub().args == ["k1"]


def test_statement_bodies_are_not_parenthesised_twice():
    body = "SELECT `t`.`ts` FROM `t` WHERE `t`.`k` = %s"

    def query() -> Select:
        return Select("t.ts", table="t", where=Eq("t.k", "k1"))

    assert str(In("o.ts", query())) == f"`o`.`ts` IN ({body})"
    assert str(Exists(query())) == f"EXISTS ({body})"
    assert str(Join(query(), alias="j")) == f"JOIN ({body}) AS `j`"
    assert str(Aliased(query(), alias="d")) == f"({body}) AS `d`"
    assert str(Union(query(), query())) == f"({body}) UNION ({body})"
    assert str(With("w").as_(query()).select(Select("w.ts", table="w"))) == f"WITH `w` AS ({body}) SELECT `w`.`ts` FROM `w`"
    assert str(Insert.into("o")("ts").select(query())) == f"INSERT INTO `o` (`ts`) {body}"


# ---------------------------------------------------------------------------
# Conditions
# ---------------------------------------------------------------------------


def test_eq_scalar_subquery():
    cond = Eq("o.ts", Select(Max("t.ts"), table="t"))
    assert str(cond) == "`o`.`ts` = (SELECT MAX(`t`.`ts`) FROM `t`)"
    assert cond.args == []


@pytest.mark.parametrize(("condition", "operator"), [(Eq, "="), (Ne, "!="), (Gt, ">"), (Ge, ">="), (Lt, "<"), (Le, "<=")])
def test_simple_condition_value(condition, operator):
    cond = condition("o.ts", sub("k1"))
    assert str(cond) == f"`o`.`ts` {operator} {SUB}"
    assert cond.args == ["k1"]


@pytest.mark.parametrize(("condition", "operator"), [(Eq, "="), (Ne, "!="), (Gt, ">"), (Ge, ">="), (Lt, "<"), (Le, "<=")])
def test_simple_condition_column(condition, operator):
    cond = condition(sub("k1"), 5)
    assert str(cond) == f"{SUB} {operator} %s"
    assert cond.args == ["k1", 5]


def test_simple_condition_both_sides():
    cond = Eq(sub("k1"), sub("k2"))
    assert str(cond) == f"{SUB} = {SUB}"
    assert cond.args == ["k1", "k2"]


def test_between_every_operand():
    cond = Between(sub("k1"), sub("k2"), sub("k3"))
    assert str(cond) == f"{SUB} BETWEEN {SUB} AND {SUB}"
    assert cond.args == ["k1", "k2", "k3"]


def test_between_mixed_with_values():
    cond = Between(sub("k1"), 1, 2)
    assert str(cond) == f"{SUB} BETWEEN %s AND %s"
    assert cond.args == ["k1", 1, 2]

    cond = NotBetween("o.ts", 1, sub("k1"))
    assert str(cond) == f"`o`.`ts` NOT BETWEEN %s AND {SUB}"
    assert cond.args == [1, "k1"]


@pytest.mark.parametrize(
    ("condition", "operator"), [(Like, "LIKE"), (NotLike, "NOT LIKE"), (RLike, "RLIKE"), (NotRLike, "NOT RLIKE")]
)
def test_like_column(condition, operator):
    cond = condition(sub("k1"), "pattern")
    assert str(cond) == f"{SUB} {operator} %s"
    assert cond.args == ["k1", "pattern"]


@pytest.mark.parametrize(
    ("condition", "operator"), [(Like, "LIKE"), (NotLike, "NOT LIKE"), (RLike, "RLIKE"), (NotRLike, "NOT RLIKE")]
)
def test_like_value(condition, operator):
    cond = condition("o.x", sub("k1"))
    assert str(cond) == f"`o`.`x` {operator} {SUB}"
    assert cond.args == ["k1"]


def test_in_column():
    cond = In(sub("k1"), [1, 2])
    assert str(cond) == f"{SUB} IN (%s, %s)"
    assert cond.args == ["k1", 1, 2]


def test_in_value_list_item():
    cond = NotIn("o.ts", [1, sub("k1"), 2])
    assert str(cond) == f"`o`.`ts` NOT IN (%s, {SUB}, %s)"
    assert cond.args == [1, "k1", 2]


def test_in_column_with_none():
    cond = In(sub("k1"), [1, None])
    assert str(cond) == f"({SUB} IN (%s) OR {SUB} IS NULL)"
    assert cond.args == ["k1", 1, "k1"]

    cond = NotIn(sub("k1"), [None])
    assert str(cond) == f"{SUB} IS NOT NULL"
    assert cond.args == ["k1"]


def test_in_multi_column():
    cond = In((sub("k1"), "o.y"), [(1, sub("k2")), (sub("k3"), 4)])
    assert str(cond) == f"({SUB}, `o`.`y`) IN ((%s, {SUB}), ({SUB}, %s))"
    assert cond.args == ["k1", 1, "k2", "k3", 4]


def test_in_multi_column_with_none():
    cond = In((sub("k1"), "o.y"), [(1, 2), (sub("k2"), None)])
    assert str(cond) == f"(({SUB}, `o`.`y`) IN ((%s, %s)) OR ({SUB} = {SUB} AND `o`.`y` IS %s))"
    assert cond.args == ["k1", 1, 2, "k1", "k2", None]


def test_in_subquery_column():
    cond = In(sub("k1"), Select("t2.ts", table="t2", where=Eq("t2.k", "k2")))
    assert str(cond) == f"{SUB} IN (SELECT `t2`.`ts` FROM `t2` WHERE `t2`.`k` = %s)"
    assert cond.args == ["k1", "k2"]

    cond = NotIn((sub("k1"), "o.y"), Select("t2.ts", "t2.y", table="t2", where=Eq("t2.k", "k2")))
    assert str(cond) == f"({SUB}, `o`.`y`) NOT IN (SELECT `t2`.`ts`, `t2`.`y` FROM `t2` WHERE `t2`.`k` = %s)"
    assert cond.args == ["k1", "k2"]


def test_is_json():
    cond = IsJson(sub("k1"))
    assert str(cond) == f"{SUB} IS JSON"
    assert cond.args == ["k1"]

    cond = IsNotJson(sub("k1"), JsonValueType.OBJECT)
    assert str(cond) == f"{SUB} IS NOT JSON OBJECT"
    assert cond.args == ["k1"]


# ---------------------------------------------------------------------------
# Expressions
# ---------------------------------------------------------------------------


def test_binary_expression():
    expr = Column("o.ts") - sub("k1")
    assert str(expr) == f"(`o`.`ts` - {SUB})"
    assert expr.args == ["k1"]

    expr = BinaryExpression(sub("k1"), "+", 1)
    assert str(expr) == f"({SUB} + %s)"
    assert expr.args == ["k1", 1]


def test_unary_expression():
    expr = UnaryExpression("~", sub("k1"))
    assert str(expr) == f"(~{SUB})"
    assert expr.args == ["k1"]


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------


def test_function_argument():
    func = Coalesce(sub("k1"), 0)
    assert str(func) == f"COALESCE({SUB}, %s)"
    assert func.args == ["k1", 0]


@pytest.mark.parametrize(
    ("func", "sql", "args"),
    [
        (Concat("a", sub("k1"), "b"), f"CONCAT(%s, {SUB}, %s)", ["a", "k1", "b"]),
        (Round(sub("k1")), f"ROUND({SUB})", ["k1"]),
        (JsonExtract(sub("k1"), "$.a"), f"JSON_EXTRACT({SUB}, %s)", ["k1", "$.a"]),
        (Point(sub("k1"), 1), f"POINT({SUB}, %s)", ["k1", 1]),
        (StDistanceSphere(Column("o.p"), sub("k1"), 6371000), f"ST_DISTANCE_SPHERE(`o`.`p`, {SUB}, %s)", ["k1", 6371000]),
        (Max(sub("k1")), f"MAX({SUB})", ["k1"]),
        (Sum(sub("k1"), distinct=True), f"SUM(DISTINCT {SUB})", ["k1"]),
        (Count("o.a", sub("k1"), distinct=True), f"COUNT(DISTINCT `o`.`a`, {SUB})", ["k1"]),
        (JsonObjectAgg(Value("key"), sub("k1")), f"JSON_OBJECTAGG(%s, {SUB})", ["key", "k1"]),
    ],
)
def test_function_family_argument(func, sql, args):
    assert str(func) == sql
    assert func.args == args


def test_group_concat():
    func = GroupConcat("o.x", sub("k1"), distinct=True, order=[(sub("k2"), Direction.DESC)], separator=",", limit=Limit(3))
    assert str(func) == f"GROUP_CONCAT(DISTINCT `o`.`x`, {SUB} ORDER BY {SUB} DESC SEPARATOR %s LIMIT %s)"
    assert func.args == ["k1", "k2", ",", 3]


def test_json_arrayagg():
    func = JsonArrayAgg(sub("k1"), order=[(sub("k2"), Direction.ASC)], limit=Limit(2))
    assert str(func) == f"JSON_ARRAYAGG({SUB} ORDER BY {SUB} ASC LIMIT %s)"
    assert func.args == ["k1", "k2", 2]


def test_window_function():
    func = Sum(sub("k1")).over(partition_by=[sub("k2"), "o.a"], order=[(sub("k3"), Direction.DESC)])
    assert str(func) == f"SUM({SUB}) OVER (PARTITION BY {SUB}, `o`.`a` ORDER BY {SUB} DESC)"
    assert func.args == ["k1", "k2", "k3"]

    func = Lag(sub("k1"), 1).over(order=[("o.id", Direction.ASC)])
    assert str(func) == f"LAG({SUB}, %s) OVER (ORDER BY `o`.`id` ASC)"
    assert func.args == ["k1", 1]


def test_case_simple_form():
    case = Case(sub("k1")).when(sub("k2"), sub("k3")).when(1, "one").else_(sub("k4"))
    assert str(case) == f"CASE {SUB} WHEN {SUB} THEN {SUB} WHEN %s THEN %s ELSE {SUB} END"
    assert case.args == ["k1", "k2", "k3", 1, "one", "k4"]


def test_case_searched_form():
    case = Case().when(Gt("o.ts", sub("k1")), sub("k2")).else_(0)
    assert str(case) == f"CASE WHEN `o`.`ts` > {SUB} THEN {SUB} ELSE %s END"
    assert case.args == ["k1", "k2", 0]


def test_interval():
    interval = Interval(day=sub("k1"))
    assert str(interval) == f"INTERVAL {SUB} DAY"
    assert interval.args == ["k1"]

    func = DateAdd(Column("o.d"), Interval(day=sub("k1")))
    assert str(func) == f"DATE_ADD(`o`.`d`, INTERVAL {SUB} DAY)"
    assert func.args == ["k1"]


def test_extract():
    func = Extract("DAY", sub("k1"))
    assert str(func) == f"EXTRACT(DAY FROM {SUB})"
    assert func.args == ["k1"]


def test_collate():
    stmt = Collate(sub("k1"), "utf8mb4_bin")
    assert str(stmt) == f"{SUB} COLLATE utf8mb4_bin"
    assert stmt.args == ["k1"]


def test_json_table_document():
    jt = JsonTable(Select("t.doc", table="t", where=Eq("t.k", "k1")), "$[*]", JsonTableColumn("a", "INT", "$"))
    assert str(jt) == "JSON_TABLE((SELECT `t`.`doc` FROM `t` WHERE `t`.`k` = %s), %s COLUMNS (`a` INT PATH %s))"
    assert jt.args == ["k1", "$[*]", "$"]


# ---------------------------------------------------------------------------
# Statements
# ---------------------------------------------------------------------------


def test_select_list_item():
    sel = Select(sub("k1"), "o.id", table="o", where=Eq("o.a", 1))
    assert str(sel) == f"SELECT {SUB}, `o`.`id` FROM `o` WHERE `o`.`a` = %s"
    assert sel.args == ["k1", 1]


def test_select_of_a_select():
    sel = Select(sub("k1"))
    assert str(sel) == f"SELECT {SUB}"
    assert sel.args == ["k1"]


def test_aliased():
    stmt = Aliased(sub("k1"), alias="m")
    assert str(stmt) == f"{SUB} AS `m`"
    assert stmt.args == ["k1"]

    stmt = Aliased(sub("k1"))
    assert str(stmt) == SUB
    assert stmt.args == ["k1"]


def test_aliased_union_and_with():
    stmt = Aliased(Union(sub("k1"), sub("k2")), alias="u")
    assert str(stmt) == f"({SUB} UNION {SUB}) AS `u`"
    assert stmt.args == ["k1", "k2"]

    stmt = Aliased(With("w").as_(sub("k1")).select(Select("*", table="w")), alias="c")
    assert str(stmt) == f"(WITH `w` AS ({SUB[1:-1]}) SELECT * FROM `w`) AS `c`"
    assert stmt.args == ["k1"]


def test_group_by():
    sel = Select("o.a", table="o", group_by=[sub("k1")]).group_by(sub("k2"))
    assert str(sel) == f"SELECT `o`.`a` FROM `o` GROUP BY {SUB}, {SUB}"
    assert sel.args == ["k1", "k2"]


def test_having():
    sel = Select("o.a", Count("*"), table="o", group_by=["o.a"], having=Gt(Count("*"), sub("k1")))
    assert str(sel) == f"SELECT `o`.`a`, COUNT(*) FROM `o` GROUP BY `o`.`a` HAVING COUNT(*) > {SUB}"
    assert sel.args == ["k1"]


def test_select_order_by():
    sel = Select("o.a", table="o", where=Eq("o.b", 1), order=[(sub("k1"), Direction.DESC)], limit=Limit(5))
    assert str(sel) == f"SELECT `o`.`a` FROM `o` WHERE `o`.`b` = %s ORDER BY {SUB} DESC LIMIT %s"
    assert sel.args == [1, "k1", 5]


def test_union_order_by():
    union = Union(Select("o.a", table="o"), Select("t.ts", table="t"), order=[(sub("k1"), Direction.ASC)])
    assert str(union) == f"(SELECT `o`.`a` FROM `o`) UNION (SELECT `t`.`ts` FROM `t`) ORDER BY {SUB} ASC"
    assert union.args == ["k1"]


def test_update_set():
    upd = Update("o", set={"ts": sub("k1")}, where=Eq("o.id", 1)).set("a", 2)
    assert str(upd) == f"UPDATE `o` SET `ts` = {SUB}, `a` = %s WHERE `o`.`id` = %s"
    assert upd.args == ["k1", 2, 1]


def test_update_order_by():
    upd = Update("o", set={"a": 1}, order=[(sub("k1"), Direction.ASC)], limit=Limit(1))
    assert str(upd) == f"UPDATE `o` SET `a` = %s ORDER BY {SUB} ASC LIMIT %s"
    assert upd.args == [1, "k1", 1]


def test_delete_where_and_order_by():
    delete = Delete("o", where=Lt("o.ts", sub("k1")), order=[(sub("k2"), Direction.DESC)], limit=Limit(1))
    assert str(delete) == f"DELETE FROM `o` WHERE `o`.`ts` < {SUB} ORDER BY {SUB} DESC LIMIT %s"
    assert delete.args == ["k1", "k2", 1]


def test_insert_values():
    ins = Insert.into("o")("a", "b").values((1, sub("k1")), (sub("k2"), 2))
    assert str(ins) == f"INSERT INTO `o` (`a`, `b`) VALUES (%s, {SUB}), ({SUB}, %s)"
    assert ins.args == [1, "k1", "k2", 2]


def test_insert_on_duplicate_key_update():
    ins = Insert.into("o")("a", "b").values((1, 2)).on_duplicate_key_update(b=sub("k1"), a=3)
    assert str(ins) == f"INSERT INTO `o` (`a`, `b`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `b` = {SUB}, `a` = %s"
    assert ins.args == [1, 2, "k1", 3]


def test_insert_select_on_duplicate_key_update():
    ins = Insert.into("o")("a").select(Select("t.ts", table="t", where=Eq("t.k", "k1"))).on_duplicate_key_update(a=sub("k2"))
    assert str(ins) == f"INSERT INTO `o` (`a`) SELECT `t`.`ts` FROM `t` WHERE `t`.`k` = %s ON DUPLICATE KEY UPDATE `a` = {SUB}"
    assert ins.args == ["k1", "k2"]


# ---------------------------------------------------------------------------
# Other query statements as operands, and nesting
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("union_class", UNION_VARIANTS)
def test_union_as_operand(union_class):
    union = union_class(sub("k1"), sub("k2"))
    cond = Eq("o.ts", union)
    assert str(cond) == f"`o`.`ts` = ({union!s})"
    assert cond.args == ["k1", "k2"]


def test_union_with_limit_as_operand():
    union = UnionAll(sub("k1"), sub("k2"), limit=Limit(1))
    func = Coalesce(union, 0)
    assert str(func) == f"COALESCE(({SUB} UNION ALL {SUB} LIMIT %s), %s)"
    assert func.args == ["k1", "k2", 1, 0]


def test_with_as_operand():
    cte = (
        With("m")
        .as_(Select(Aliased(Max("t.ts"), alias="mx"), table="t", where=Eq("t.k", "k1")))
        .select(Select("m.mx", table="m"))
    )
    cond = Gt("o.ts", cte)
    assert (
        str(cond)
        == "`o`.`ts` > (WITH `m` AS (SELECT MAX(`t`.`ts`) AS `mx` FROM `t` WHERE `t`.`k` = %s) SELECT `m`.`mx` FROM `m`)"
    )
    assert cond.args == ["k1"]


def test_nested_scalar_subqueries():
    outer = Select(Max("t.ts"), table="t", where=Lt("t.ts", sub("k2")))
    cond = Eq("o.ts", outer)
    assert str(cond) == f"`o`.`ts` = (SELECT MAX(`t`.`ts`) FROM `t` WHERE `t`.`ts` < {SUB})"
    assert cond.args == ["k2"]


def test_composed_query():
    """Newest row per owner, with the owner's latest timestamp alongside - the shape that used to need Raw()."""
    latest = Select(Max("t.ts"), table="t", where=Eq("t.o_id", Column("o.id")))
    sel = Select(
        "o.id",
        Aliased(Coalesce(latest, 0), alias="last_ts"),
        table="o",
        where=Eq("o.ts", Select(Max("t2.ts"), table="t2", where=Eq("t2.k", "k1"))) & Gt("o.a", 10),
        order=[(Column("o.id") - Select(Count("*"), table="t"), Direction.ASC)],
    )
    assert str(sel) == (
        "SELECT `o`.`id`, COALESCE((SELECT MAX(`t`.`ts`) FROM `t` WHERE `t`.`o_id` = `o`.`id`), %s) AS `last_ts` "
        "FROM `o` "
        "WHERE (`o`.`ts` = (SELECT MAX(`t2`.`ts`) FROM `t2` WHERE `t2`.`k` = %s) AND `o`.`a` > %s) "
        "ORDER BY (`o`.`id` - (SELECT COUNT(*) FROM `t`)) ASC"
    )
    assert sel.args == [0, "k1", 10]


# ---------------------------------------------------------------------------
# Any Query where a subquery is accepted: JOIN, IN, EXISTS
# ---------------------------------------------------------------------------


def union() -> Union:
    return Union(Select("t.ts", table="t", where=Eq("t.k", "k1")), Select("t2.ts", table="t2", where=Eq("t2.k", "k2")))


UNION_SQL = "(SELECT `t`.`ts` FROM `t` WHERE `t`.`k` = %s) UNION (SELECT `t2`.`ts` FROM `t2` WHERE `t2`.`k` = %s)"
"""How `union()` renders on its own."""


def cte() -> With:
    return With("w").as_(Select("t.ts", table="t", where=Eq("t.k", "k1"))).select(Select("w.ts", table="w"))


CTE_SQL = "WITH `w` AS (SELECT `t`.`ts` FROM `t` WHERE `t`.`k` = %s) SELECT `w`.`ts` FROM `w`"
"""How `cte()` renders on its own."""


def test_join_union():
    join = LeftJoin(union(), alias="u", on=Eq("u.ts", Column("o.ts")))
    assert str(join) == f"LEFT JOIN ({UNION_SQL}) AS `u` ON `u`.`ts` = `o`.`ts`"
    assert join.args == ["k1", "k2"]


def test_join_with():
    join = Join(cte(), alias="c")
    assert str(join) == f"JOIN ({CTE_SQL}) AS `c`"
    assert join.args == ["k1"]


def test_select_join_union():
    sel = Select("o.id", table="o", where=Gt("o.a", 1)).join(union(), alias="u", on=Eq("u.ts", Column("o.ts")))
    assert str(sel) == f"SELECT `o`.`id` FROM `o` JOIN ({UNION_SQL}) AS `u` ON `u`.`ts` = `o`.`ts` WHERE `o`.`a` > %s"
    assert sel.args == ["k1", "k2", 1]


@pytest.mark.parametrize("query", [union, cte, TableValueConstructor])
def test_join_query_without_alias_raises(query):
    with pytest.raises(AttributeError, match="When joining a subselect or JSON_TABLE, alias must be specified."):
        Join(query())


def test_in_union():
    cond = In("o.ts", union())
    assert str(cond) == f"`o`.`ts` IN ({UNION_SQL})"
    assert cond.args == ["k1", "k2"]

    cond = ~In("o.ts", union())
    assert str(cond) == f"`o`.`ts` NOT IN ({UNION_SQL})"
    assert cond.args == ["k1", "k2"]


def test_in_union_multi_column():
    query = Union(Select("t.ts", "t.o_id", table="t", where=Eq("t.k", "k1")), Select("t2.ts", "t2.y", table="t2"))
    cond = NotIn(("o.ts", "o.y"), query)
    assert (
        str(cond) == "(`o`.`ts`, `o`.`y`) NOT IN "
        "((SELECT `t`.`ts`, `t`.`o_id` FROM `t` WHERE `t`.`k` = %s) UNION (SELECT `t2`.`ts`, `t2`.`y` FROM `t2`))"
    )
    assert cond.args == ["k1"]


def test_exists_union():
    cond = Exists(union())
    assert str(cond) == f"EXISTS ({UNION_SQL})"
    assert cond.args == ["k1", "k2"]

    cond = NotExists(union())
    assert str(cond) == f"NOT EXISTS ({UNION_SQL})"
    assert cond.args == ["k1", "k2"]


def test_exists_with():
    cond = Exists(cte(), negative=True)
    assert str(cond) == f"NOT EXISTS ({CTE_SQL})"
    assert cond.args == ["k1"]
