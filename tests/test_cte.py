import pytest

from sqlfactory import With, Select, Gt, Eq, Column, And, In, Lt, Aliased, Union, Or, Ge, Value, UnionDistinct


def test_cte_simple():
    cte = (
        With("t")
        .as_(Select("a", table="t1", where=Ge("b", "c")))
        .select(Select("*", table=["t2", "t"], where=Eq("t2.c", Column("t.a"))))
    )

    assert str(cte) == "WITH `t` AS (SELECT `a` FROM `t1` WHERE `b` >= %s) SELECT * FROM `t2`, `t` WHERE `t2`.`c` = `t`.`a`"
    assert cte.args == ["c"]


def test_cte_subquery():
    sel = Select(
        "t1.a",
        "t1.b",
        table=["t1", "t2"],
        where=And(
            Gt("t1.a", Column("t2.c")),
            In(
                "t2.c",
                With("t")
                .as_(Select("*", table="t1", where=Lt("t1.a", 5)))
                .select(Select("t2.c", table=["t2", "t"], where=Eq("t2.c", Column("t.a")))),
            ),
        ),
    )

    assert (
        str(sel)
        == "SELECT `t1`.`a`, `t1`.`b` FROM `t1`, `t2` WHERE (`t1`.`a` > `t2`.`c` AND `t2`.`c` IN (WITH `t` AS (SELECT * FROM `t1` WHERE `t1`.`a` < %s) SELECT `t2`.`c` FROM `t2`, `t` WHERE `t2`.`c` = `t`.`a`))"
    )
    assert sel.args == [5]


def test_cte_recursive():
    cte = (
        With("ancestors", recursive=True)
        .as_(
            Union(
                Select("*", table="folks", where=Eq("name", "Alex")),
                Select(
                    "f.*",
                    table=[Aliased("folks", alias="f"), Aliased("ancestors", alias="a")],
                    where=Or(Eq("f.id", Column("a.father")), Eq("f.id", Column("a.mother"))),
                ),
            )
        )
        .select(Select("*", table="ancestors"))
    )

    assert (
        str(cte)
        == "WITH RECURSIVE `ancestors` AS ((SELECT * FROM `folks` WHERE `name` = %s) UNION (SELECT `f`.* FROM `folks` AS `f`, `ancestors` AS `a` WHERE (`f`.`id` = `a`.`father` OR `f`.`id` = `a`.`mother`))) SELECT * FROM `ancestors`"
    )
    assert cte.args == ["Alex"]


def test_cte_columns():
    sel = With(
        "cte",
        ["depth", "from", "to"],
        recursive=True,
        cte=UnionDistinct(
            Select(Value(0), Value(1), Value(1)),
            Select(
                Column("depth") + 1,
                Column("t1.from"),
                Column("t1.to"),
                table=[
                    Aliased("edges", "t1"),
                    Aliased("cte", "t2")
                ],
                where=Eq("t1.from", Column("t2.to"))
            )
        ),
        select=Select("*", table="cte")
    )

    assert str(sel) == "WITH RECURSIVE `cte` (`depth`, `from`, `to`) AS ((SELECT %s, %s, %s) UNION DISTINCT (SELECT (`depth` + %s), `t1`.`from`, `t1`.`to` FROM `edges` AS `t1`, `cte` AS `t2` WHERE `t1`.`from` = `t2`.`to`)) SELECT * FROM `cte`"
    assert sel.args == [0, 1, 1, 1]


def test_cte_incomplete():
    with pytest.raises(AttributeError):
        str(With("test"))

    with pytest.raises(AttributeError):
        str(With("test", cte=Select(Value(1))))

    with pytest.raises(AttributeError):
        str(With("test", select=Select("*", table="test")))

    assert bool(With("test")) is False
    assert bool(With("test", cte=Select(Value(1)))) is False
    assert bool(With("test", select=Select("*", table="test"))) is False
    assert bool(With("test", cte=Select(Value(1)), select=Select("*", table="test"))) is True
