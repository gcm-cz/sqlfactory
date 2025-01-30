import pytest

from sqlfactory import Column, Eq, Limit, Update
from sqlfactory.func.str import Concat
from sqlfactory.update.update import UPDATE, UpdateColumn


def test_update():
    update_condition = Update("table", where=Eq("id", 1)).set("column1", "foo").set("column2", "bar")

    assert str(update_condition) == "UPDATE `table` SET `column1` = %s, `column2` = %s WHERE `id` = %s"
    assert update_condition.args == ["foo", "bar", 1]
    assert bool(update_condition) is True


def test_update_with_limit():
    update_condition = Update("table", where=Eq("id", 123), limit=Limit(1)).set("column1", "foo").set("column2", "bar")
    assert str(update_condition) == "UPDATE `table` SET `column1` = %s, `column2` = %s WHERE `id` = %s LIMIT %s"
    assert update_condition.args == ["foo", "bar", 123, 1]


def test_update_append():
    update_condition = Update("table", where=Eq("id", 1))
    update_condition.append(UpdateColumn("column1", "value"))

    assert str(update_condition) == "UPDATE `table` SET `column1` = %s WHERE `id` = %s"
    assert update_condition.args == ["value", 1]


def test_update_without_where():
    update_condition = Update("table").set("column1", "foo").set("column2", "bar")

    assert str(update_condition) == "UPDATE `table` SET `column1` = %s, `column2` = %s"
    assert update_condition.args == ["foo", "bar"]


def test_update_without_set():
    update_condition = Update("table", where=Eq("id", 1))
    with pytest.raises(AttributeError):
        str(update_condition)

    assert bool(update_condition) is False


def test_update_with_statement():
    update = UPDATE("table").SET("column", Concat(Column("column"), "foo"))
    assert str(update) == "UPDATE `table` SET `column` = CONCAT(`column`, %s)"
    assert update.args == ["foo"]


def test_update_increment():
    update = UPDATE("table").SET("column", Column("column") + 1)
    assert str(update) == "UPDATE `table` SET `column` = (`column` + %s)"
    assert update.args == [1]


def test_multiple_sets_of_same_column():
    # Updating one column multiple times is an error.
    with pytest.raises(AttributeError):
        UPDATE("table").SET("column", "value1").SET("column", "value2")

    # But updating multiple columns to same value is fine.
    upd = UPDATE("table").SET("column1", "value").SET("column2", "value")
    assert str(upd) == "UPDATE `table` SET `column1` = %s, `column2` = %s"
    assert upd.args == ["value", "value"]


def test_update_column_equality():
    assert (UpdateColumn("foo", "bar") == UpdateColumn("foo", "baz")) is True
    assert (UpdateColumn("foo", "bar") == "foo") is False

    s = set()
    s.add(UpdateColumn("foo", "bar"))
    s.add(UpdateColumn("foo", "baz"))

    assert len(s) == 1


def test_update_column_without_args():
    upd = UpdateColumn("foo", Column("bar"))
    assert str(upd) == "`foo` = `bar`"
    assert upd.args == []
