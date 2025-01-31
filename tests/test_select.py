import pytest

from sqlfactory import Aliased, Column, ColumnList, Direction, Eq, Join, Limit, Select, SelectColumn
from sqlfactory.func.agg import Count
from sqlfactory.func.control import IfNull


def test_select():
    select_condition = (
        Select("column1", "column2", table="table").where(Eq("id", 1)).order_by("column2", Direction.ASC).limit(2, 10)
    )

    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` WHERE `id` = %s ORDER BY `column2` ASC LIMIT %s, %s"
    assert select_condition.args == [1, 2, 10]


def test_select_with_join():
    select_condition = Select("column1", "column2", table="table").join("table2", on=Eq("table.id", Column("table2.id")))

    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` JOIN `table2` ON `table`.`id` = `table2`.`id`"
    assert select_condition.args == []


def test_select_with_left_join():
    select_condition = Select("column1", "column2", table="table").left_join("table2", on=Eq("table.id", Column("table2.id")))

    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` LEFT JOIN `table2` ON `table`.`id` = `table2`.`id`"
    assert select_condition.args == []


def test_select_with_right_join():
    select_condition = Select("column1", "column2", table="table").right_join("table2", on=Eq("table.id", Column("table2.id")))

    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` RIGHT JOIN `table2` ON `table`.`id` = `table2`.`id`"
    assert select_condition.args == []


def test_select_with_group_by():
    select_condition = Select("column1", "column2", table="table").group_by("column1")

    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` GROUP BY `column1`"
    assert select_condition.args == []


def test_select_without_where_order_limit():
    select_condition = Select("column1", "column2", table="table")
    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table`"
    assert select_condition.args == []


def test_select_add():
    select_condition = Select("column1", table="table").add("column2")

    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table`"
    assert select_condition.args == []


def test_select_JOIN():
    select_condition = Select("column1", "column2", table="table").JOIN("table2", on=Eq("table.id", Column("table2.id")))

    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` JOIN `table2` ON `table`.`id` = `table2`.`id`"
    assert select_condition.args == []


def test_select_LEFT_JOIN():
    select_condition = Select("column1", "column2", table="table").LEFT_JOIN("table2", on=Eq("table.id", Column("table2.id")))

    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` LEFT JOIN `table2` ON `table`.`id` = `table2`.`id`"
    assert select_condition.args == []


def test_select_RIGHT_JOIN():
    select_condition = Select("column1", "column2", table="table").RIGHT_JOIN("table2", on=Eq("table.id", Column("table2.id")))

    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` RIGHT JOIN `table2` ON `table`.`id` = `table2`.`id`"
    assert select_condition.args == []


def test_select_GROUP_BY():
    select_condition = Select("column1", "column2", table="table").GROUP_BY("column1")
    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` GROUP BY `column1`"
    assert select_condition.args == []


def test_select_order_by():
    select_condition = Select("column1", "column2", table="table").order_by("column1", Direction.ASC)

    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` ORDER BY `column1` ASC"
    assert select_condition.args == []


def test_select_limit():
    select_condition = Select("column1", "column2", table="table").limit(5)

    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` LIMIT %s"
    assert select_condition.args == [5]


def test_select_limit_instance():
    select_condition = Select("column1", "column2", table="table").limit(Limit(10))

    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` LIMIT %s"
    assert select_condition.args == [10]


def test_select_limit_instance_invalid():
    with pytest.raises(AttributeError):
        Select("column1", table="table").limit(Limit(10), 100)


def test_select_where():
    select_condition = Select("column1", "column2", table="table").where(Eq("column1", "value"))

    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` WHERE `column1` = %s"
    assert select_condition.args == ["value"]


def test_select_having():
    select_condition = Select("column1", "column2", table="table").group_by("column1").having(Eq("column1", "value"))
    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` GROUP BY `column1` HAVING `column1` = %s"
    assert select_condition.args == ["value"]


def test_select_limit_with_offset():
    select_condition = Select("column1", "column2", table="table").limit(5, 10)

    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` LIMIT %s, %s"
    assert select_condition.args == [5, 10]


def test_select_HAVING():
    select_condition = Select("column1", "column2", table="table").group_by("column1").HAVING(Eq("column1", "value"))

    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` GROUP BY `column1` HAVING `column1` = %s"
    assert select_condition.args == ["value"]


def test_select_order_by_desc():
    select_condition = Select("column1", "column2", table="table").order_by("column1", Direction.DESC)

    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` ORDER BY `column1` DESC"
    assert select_condition.args == []


def test_select_order_by_multiple_columns():
    select_condition = (
        Select("column1", "column2", table="table").order_by("column1", Direction.ASC).ORDER_BY("column2", Direction.DESC)
    )

    assert str(select_condition) == "SELECT `column1`, `column2` FROM `table` ORDER BY `column1` ASC, `column2` DESC"
    assert select_condition.args == []


def test_errors():
    # The table argument is required
    with pytest.raises(AttributeError):
        Select()

    # Positional columns and select cannot be mixed.
    with pytest.raises(AttributeError):
        Select("column1", select=ColumnList("column2"), table="test")

    # The select argument must be a ColumnList, not regular list.
    with pytest.raises(TypeError):
        Select(select=["column1"], table="test")

    # Multiple group_by statements are not allowed.
    with pytest.raises(AttributeError):
        Select("column1", table="table").group_by("column1").group_by("column2")

    # join() with instance of Join class cannot have additional arguments.
    with pytest.raises(AttributeError):
        (Select("column1", table="table").join(Join("table2"), Eq("table.id", Column("table2.id"))))

    with pytest.raises(AttributeError, match="Where has already been specified."):
        (Select(table="xyz").where(Eq("column1", "value")).WHERE(Eq("column2", "value")))


def test_column_list():
    # Empty initialized
    column_list = ColumnList()
    assert len(column_list) == 0

    assert repr(column_list) == "[]"

    # Try to insert multiple statements
    column_list.add(IfNull("a", "b"))
    column_list.add(IfNull("a", "b"))
    assert len(column_list) == 1

    column_list.add(IfNull("a", "c"))
    assert len(column_list) == 2

    assert str(column_list) == "IFNULL(%s, %s), IFNULL(%s, %s)"
    assert column_list.args == ["a", "b", "a", "c"]


def test_column_list_uniqueness():
    column_list = ColumnList()
    column_list.add("column1")
    column_list.add("column1")
    assert len(column_list) == 1

    column_list.add("column2")
    assert len(column_list) == 2

    assert str(column_list) == "`column1`, `column2`"
    assert column_list.args == []


def test_column_list_update():
    column_list = ColumnList()
    column_list.update(["column1", "column2"])
    assert len(column_list) == 2

    column_list.update(["column1", "column3"])
    assert len(column_list) == 3

    assert str(column_list) == "`column1`, `column2`, `column3`"
    assert column_list.args == []


def test_column_list_aliased():
    column_list = ColumnList()
    column_list.add(SelectColumn("column1", "alias1"))
    column_list.add(SelectColumn("column2", "alias1"))

    assert len(column_list) == 2
    # Technically, this is correct, as for position-based cursors, we can access both columns.
    assert str(column_list) == "`column1` AS `alias1`, `column2` AS `alias1`"


def test_aliased_without_alias():
    # Because why not?
    aliased = Aliased("stmt")
    assert str(aliased) == "`stmt`"


def test_aliased_with_args():
    aliased = Aliased(IfNull("a", "b"), "alias")
    assert str(aliased) == "IFNULL(%s, %s) AS `alias`"
    assert aliased.args == ["a", "b"]

    # Test aliased statement property access
    assert aliased.function == "IFNULL"


def test_select_count_star():
    sel = Select(Count("*"), table="table_with_rows")
    assert str(sel) == "SELECT COUNT(*) FROM `table_with_rows`"
    assert sel.args == []


def test_select_column_compare():
    # Test comparison of SelectColumn instances
    assert SelectColumn("column1") == SelectColumn("column1")
    assert SelectColumn("column1") != SelectColumn("column2")
    assert SelectColumn("column1") != SelectColumn("column1", "alias")
    assert SelectColumn("column1") != "column1"
    assert SelectColumn("column1") == Column("column1")


def test_select_column_uniqueness_regression():
    sel = ColumnList()
    sel.add("column1")
    sel.add(SelectColumn("column2", alias="column3"))

    assert len(sel) == 2


def test_multiple_tables():
    sel = Select("table1.t", "table2.u", table=["table1", "table2"])
    assert str(sel) == "SELECT `table1`.`t`, `table2`.`u` FROM `table1`, `table2`"
    assert sel.args == []


def test_column_list_non_statement():
    cl = ColumnList()
    with pytest.raises(AttributeError):
        "column1" in cl


def test_select_for_update():
    sel = Select("a", "b", table="tbl", for_update=True)
    assert str(sel) == "SELECT `a`, `b` FROM `tbl` FOR UPDATE"
    assert sel.args == []


def test_distinct():
    col = SelectColumn("table.column", distinct=True)
    assert str(col) == "DISTINCT `table`.`column`"

    col = SelectColumn("table.column", distinct=False)
    assert str(col) == "`table`.`column`"
