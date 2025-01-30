import pytest

from sqlfactory import Delete, Direction, Eq, In, Join
from sqlfactory.entities import Column, Table
from sqlfactory.mixins.limit import Limit


def test_delete():
    delete_condition = Delete("table", where=In("id", [1, 2, 3]), order=[("column1", Direction.ASC)], limit=Limit(10))

    assert str(delete_condition) == "DELETE FROM `table` WHERE `id` IN (%s, %s, %s) ORDER BY `column1` ASC LIMIT %s"
    assert delete_condition.args == [1, 2, 3, 10]


def test_delete_with_table_instance():
    delete_condition = Delete(Table("table"), where=In("id", [1, 2, 3]), order=[("column1", Direction.ASC)], limit=Limit(10))

    assert str(delete_condition) == "DELETE FROM `table` WHERE `id` IN (%s, %s, %s) ORDER BY `column1` ASC LIMIT %s"
    assert delete_condition.args == [1, 2, 3, 10]


def test_delete_without_order_limit():
    delete_condition = Delete("table", where=In("id", [1, 2, 3]))

    assert str(delete_condition) == "DELETE FROM `table` WHERE `id` IN (%s, %s, %s)"
    assert delete_condition.args == [1, 2, 3]


def test_delete_without_where_order_limit():
    delete_condition = Delete("table")
    assert str(delete_condition) == "DELETE FROM `table`"
    assert delete_condition.args == []


def test_delete_with_join():
    delete = Delete(
        "table", delete=["table"], join=[Join("table2", on=Eq("table.id", Column("table2.id")))], where=Eq("table2.value", 10)
    )
    assert str(delete) == "DELETE `table` FROM `table` JOIN `table2` ON `table`.`id` = `table2`.`id` WHERE `table2`.`value` = %s"
    assert delete.args == [10]


def test_delete_with_join_all():
    delete = Delete("table", join=[Join("table2", on=Eq("table.id", Column("table2.id")))], where=Eq("table2.value", 10))
    assert str(delete) == "DELETE FROM `table` JOIN `table2` ON `table`.`id` = `table2`.`id` WHERE `table2`.`value` = %s"
    assert delete.args == [10]


def test_delete_invalid_arg():
    with pytest.raises(TypeError):
        Delete("table", delete="table")
