import pytest
from sqlbuilder import Delete, In, Direction
from sqlbuilder.column import Table
from sqlbuilder.mixins.limit import Limit


def test_delete():
    delete_condition = Delete(
        "table",
        where=In("id", [1, 2, 3]),
        order=[("column1", Direction.ASC)],
        limit=Limit(10)
    )

    assert str(delete_condition) == "DELETE FROM `table` WHERE `id` IN (%s, %s, %s) ORDER BY `column1` ASC LIMIT %s"
    assert delete_condition.args == [1, 2, 3, 10]


def test_delete_with_table_instance():
    delete_condition = Delete(
        Table("table"),
        where=In("id", [1, 2, 3]),
        order=[("column1", Direction.ASC)],
        limit=Limit(10)
    )

    assert str(delete_condition) == "DELETE FROM `table` WHERE `id` IN (%s, %s, %s) ORDER BY `column1` ASC LIMIT %s"
    assert delete_condition.args == [1, 2, 3, 10]


def test_delete_without_order_limit():
    delete_condition = Delete(
        "table",
        where=In("id", [1, 2, 3])
    )

    assert str(delete_condition) == "DELETE FROM `table` WHERE `id` IN (%s, %s, %s)"
    assert delete_condition.args == [1, 2, 3]


def test_delete_without_where_order_limit():
    delete_condition = Delete("table")
    assert str(delete_condition) == "DELETE FROM `table`"
    assert delete_condition.args == []
