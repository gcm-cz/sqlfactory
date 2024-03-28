import pytest
from sqlbuilder.entities import Table
from sqlbuilder.condition.simple import Eq
from sqlbuilder.select.join import Join, LeftJoin, LeftOuterJoin, RightJoin, RightOuterJoin, InnerJoin, CrossJoin


def test_join():
    join = Join(Table("table"), Eq("alias.column1", "value"), "alias")
    assert str(join) == "JOIN `table` AS `alias` ON `alias`.`column1` = %s"
    assert join.args == ["value"]


def test_join_without_on():
    join = Join("table", alias="alias")
    assert str(join) == "JOIN `table` AS `alias`"
    assert join.args == []


def test_left_join():
    join = LeftJoin(Table("table"), Eq("alias.column1", "value"), "alias")
    assert str(join) == "LEFT JOIN `table` AS `alias` ON `alias`.`column1` = %s"
    assert join.args == ["value"]


def test_left_outer_join():
    join = LeftOuterJoin(Table("table"), Eq("alias.column1", "value"), "alias")
    assert str(join) == "LEFT OUTER JOIN `table` AS `alias` ON `alias`.`column1` = %s"
    assert join.args == ["value"]


def test_right_join():
    join = RightJoin(Table("table"), Eq("alias.column1", "value"), "alias")
    assert str(join) == "RIGHT JOIN `table` AS `alias` ON `alias`.`column1` = %s"
    assert join.args == ["value"]


def test_right_outer_join():
    join = RightOuterJoin(Table("table"), Eq("alias.column1", "value"), "alias")
    assert str(join) == "RIGHT OUTER JOIN `table` AS `alias` ON `alias`.`column1` = %s"
    assert join.args == ["value"]


def test_inner_join():
    join = InnerJoin(Table("table"), Eq("alias.column1", "value"), "alias")
    assert str(join) == "INNER JOIN `table` AS `alias` ON `alias`.`column1` = %s"
    assert join.args == ["value"]


def test_cross_join():
    join = CrossJoin(Table("table"), Eq("alias.column1", "value"), "alias")
    assert str(join) == "CROSS JOIN `table` AS `alias` ON `alias`.`column1` = %s"
    assert join.args == ["value"]
