from typing import Any

from sqlfactory import (
    Column,
    Direction,
    Eq,
    Except,
    ExceptAll,
    ExceptDistinct,
    Intersect,
    IntersectAll,
    IntersectDistinct,
    Limit,
    Select,
    Union,
    UnionAll,
    UnionDistinct,
)
from sqlfactory.func.control import IfNull


def test_simple_union():
    sel = Union(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
    )

    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) UNION (SELECT `a`, `b` FROM `table2`)"
    assert sel.args == []


def test_union_append():
    sel = Union(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
    )

    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) UNION (SELECT `a`, `b` FROM `table2`)"
    assert sel.args == []

    sel.append(Select("a", "b", table="table3"))

    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) UNION (SELECT `a`, `b` FROM `table2`) UNION (SELECT `a`, `b` FROM `table3`)"
    assert sel.args == []


def test_union_order_limit():
    sel = Union(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
        Select("a", "b", table="table3"),
        order=[("a", "ASC")],
    )

    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) UNION (SELECT `a`, `b` FROM `table2`) UNION (SELECT `a`, `b` FROM `table3`) ORDER BY `a` ASC"
    assert sel.args == []

    sel = Union(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
        Select("a", "b", table="table3"),
        limit=Limit(5, 10),
    )

    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) UNION (SELECT `a`, `b` FROM `table2`) UNION (SELECT `a`, `b` FROM `table3`) LIMIT %s, %s"
    assert sel.args == [5, 10]

    sel = Union(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
        Select("a", "b", table="table3"),
        order=[("a", Direction.DESC)],
        limit=Limit(5, 10),
    )

    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) UNION (SELECT `a`, `b` FROM `table2`) UNION (SELECT `a`, `b` FROM `table3`) ORDER BY `a` DESC LIMIT %s, %s"
    assert sel.args == [5, 10]


def test_union_all():
    sel = UnionAll(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
    )

    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) UNION ALL (SELECT `a`, `b` FROM `table2`)"
    assert sel.args == []


def test_union_distinct():
    sel = UnionDistinct(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
    )

    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) UNION DISTINCT (SELECT `a`, `b` FROM `table2`)"
    assert sel.args == []


def test_union_args():
    sel = Union(
        Select("a", "b", table="table1", where=Eq("id", 123)),
        Select("a", "b", table="table2", where=Eq("id", 456)),
        order=[(IfNull(Column("a"), 3), Direction.DESC)],
        limit=Limit(5, 10),
    )

    assert str(sel) == "(SELECT `a`, `b` FROM `table1` WHERE `id` = %s) UNION (SELECT `a`, `b` FROM `table2` WHERE `id` = %s) ORDER BY IFNULL(`a`, %s) DESC LIMIT %s, %s"
    assert sel.args == [123, 456, 3, 5, 10]


def test_intersect():
    sel = Intersect(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
    )
    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) INTERSECT (SELECT `a`, `b` FROM `table2`)"
    assert sel.args == []


def test_intersect_all():
    sel = IntersectAll(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
    )
    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) INTERSECT ALL (SELECT `a`, `b` FROM `table2`)"
    assert sel.args == []


def test_intersect_distinct():
    sel = IntersectDistinct(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
    )
    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) INTERSECT DISTINCT (SELECT `a`, `b` FROM `table2`)"
    assert sel.args == []


def test_except():
    sel = Except(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
    )
    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) EXCEPT (SELECT `a`, `b` FROM `table2`)"
    assert sel.args == []


def test_except_all():
    sel = ExceptAll(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
    )
    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) EXCEPT ALL (SELECT `a`, `b` FROM `table2`)"
    assert sel.args == []


def test_except_distinct():
    sel = ExceptDistinct(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
    )
    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) EXCEPT DISTINCT (SELECT `a`, `b` FROM `table2`)"
    assert sel.args == []


def test_intersect_order_limit():
    sel = Intersect(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
        order=[("a", Direction.ASC)],
    )
    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) INTERSECT (SELECT `a`, `b` FROM `table2`) ORDER BY `a` ASC"
    assert sel.args == []

    sel = Intersect(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
        limit=Limit(5, 10),
    )
    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) INTERSECT (SELECT `a`, `b` FROM `table2`) LIMIT %s, %s"
    assert sel.args == [5, 10]

    sel = Intersect(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
        order=[("a", Direction.DESC)],
        limit=Limit(5, 10),
    )
    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) INTERSECT (SELECT `a`, `b` FROM `table2`) ORDER BY `a` DESC LIMIT %s, %s"
    assert sel.args == [5, 10]


def test_except_order_limit():
    sel = Except(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
        order=[("a", Direction.ASC)],
    )
    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) EXCEPT (SELECT `a`, `b` FROM `table2`) ORDER BY `a` ASC"
    assert sel.args == []

    sel = Except(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
        limit=Limit(5, 10),
    )
    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) EXCEPT (SELECT `a`, `b` FROM `table2`) LIMIT %s, %s"
    assert sel.args == [5, 10]

    sel = Except(
        Select("a", "b", table="table1"),
        Select("a", "b", table="table2"),
        order=[("a", Direction.DESC)],
        limit=Limit(5, 10),
    )
    assert str(sel) == "(SELECT `a`, `b` FROM `table1`) EXCEPT (SELECT `a`, `b` FROM `table2`) ORDER BY `a` DESC LIMIT %s, %s"
    assert sel.args == [5, 10]


def test_union_executable():
    u = Union()

    assert not bool(u)

    class FakeCursor:
        def __init__(self):
            self.executed = False

        def execute(self, query: str, args: tuple[Any]) -> None:
            print(f"Executed {query} with args {args}")
            self.executed = True

    c = FakeCursor()
    u.execute(c)

    assert c.executed is False


    u.append(Select("1"))

    u.execute(c)
    assert c.executed is True
