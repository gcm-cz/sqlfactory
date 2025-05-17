import pytest

from sqlfactory import INSERT, Column, Insert, Values, Select, Eq, SELECT
from sqlfactory.func.control import IfNull
from sqlfactory.func.datetime import Now
from sqlfactory.func.str import Concat


def test_insert():
    insert_condition = Insert.into("table")("column1", "column2").values((1, 2))
    assert str(insert_condition) == "INSERT INTO `table` (`column1`, `column2`) VALUES (%s, %s)"
    assert insert_condition.args == [1, 2]

    insert_condition_aliased = Insert.into("table").columns("column1", "column2").values((1, 2))
    assert str(insert_condition_aliased) == "INSERT INTO `table` (`column1`, `column2`) VALUES (%s, %s)"
    assert insert_condition_aliased.args == [1, 2]


def test_insert_ignore():
    insert_condition = INSERT.INTO("table", ignore=True)("column1", "column2").VALUES((1, 2))
    assert str(insert_condition) == "INSERT IGNORE INTO `table` (`column1`, `column2`) VALUES (%s, %s)"
    assert insert_condition.args == [1, 2]


def test_insert_replace():
    insert_condition = Insert.into("table", replace=True)("column1", "column2").values((1, 2))
    assert str(insert_condition) == "REPLACE INTO `table` (`column1`, `column2`) VALUES (%s, %s)"
    assert insert_condition.args == [1, 2]


def test_insert_on_duplicate_key_update():
    insert_condition = Insert.into("table")("column1", "column2").values((1, 2)).on_duplicate_key_update(column1=3, column2=4)
    assert (
        str(insert_condition)
        == "INSERT INTO `table` (`column1`, `column2`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `column1` = %s, `column2` = %s"
    )
    assert insert_condition.args == [1, 2, 3, 4]


def test_insert_on_duplicate_key_update_with_args():
    insert_condition = (
        INSERT.INTO("table")("column1", "column2")
        .VALUES((1, 2))
        .ON_DUPLICATE_KEY_UPDATE(column1=Concat(Values("column1"), "foo"), column2=4)
    )
    assert (
        str(insert_condition)
        == "INSERT INTO `table` (`column1`, `column2`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `column1` = CONCAT(VALUES(`column1`), %s), `column2` = %s"
    )
    assert insert_condition.args == [1, 2, "foo", 4]


def test_insert_with_statement_with_args():
    statement1 = Concat(Column("column1"), "foo")
    statement2 = Concat("bar", Column("column2"))

    with pytest.raises(AttributeError):
        insert_condition = Insert.into("table")(statement1, statement2).values((1, 2))


def test_insert_ignore_replace():
    with pytest.raises(AttributeError):
        Insert.into("table", ignore=True, replace=True)


def test_without_columns():
    with pytest.raises(AttributeError):
        str(Insert.into("table").values((1, 2)))

    with pytest.raises(AttributeError):
        str(Insert.into("table")().values((1, 2)))


def test_multiple_column_calls():
    with pytest.raises(AttributeError):
        str(Insert.into("table")("column1")("column2"))


def test_conditional_insert():
    assert bool(Insert("table")("a", "b").values()) is False
    assert bool(Insert("table")("a", "b").values((1, 2), (3, 4))) is True


def test_insert_multiple_rows():
    insert_statement = Insert("table")("a", "b").values((1, 2), (3, 4))
    assert str(insert_statement) == "INSERT INTO `table` (`a`, `b`) VALUES (%s, %s), (%s, %s)"
    assert insert_statement.args == [1, 2, 3, 4]


def test_invalid_number_of_insert_columns():
    with pytest.raises(AttributeError):
        str(Insert("table")("a", "b").values(()))

    with pytest.raises(AttributeError):
        str(Insert("table")("a", "b").values((1,)))

    with pytest.raises(AttributeError):
        str(Insert("table")("a", "b").values((1, 2, 3)))

    with pytest.raises(AttributeError):
        str(Insert("table")("a", "b").values((1, 2), ()))

    with pytest.raises(AttributeError):
        str(Insert("table")("a", "b").values((1, 2), (1, 2, 3)))


def test_insert_expression():
    ins = Insert("table")("a", "b").values((Now(), "hello"))
    assert str(ins) == "INSERT INTO `table` (`a`, `b`) VALUES (NOW(), %s)"
    assert ins.args == ["hello"]

    ins = Insert("table")("a", "b").values(("hello", IfNull(Column("a"), "world")))
    assert str(ins) == "INSERT INTO `table` (`a`, `b`) VALUES (%s, IFNULL(`a`, %s))"
    assert ins.args == ["hello", "world"]


def test_insert_select():
    ins = Insert.into("table")("a", "b").select(Select("column1", "column2", table="table2", where=Eq("column1", 1)))
    assert str(ins) == "INSERT INTO `table` (`a`, `b`) SELECT `column1`, `column2` FROM `table2` WHERE `column1` = %s"
    assert ins.args == [1]


def test_mixing_insert_values_and_select():
    with pytest.raises(AttributeError):
        Insert.into("table")("a", "b").values((1, 2)).select(Select())

    with pytest.raises(AttributeError):
        Insert.into("table")("a", "b").select(Select()).values((1, 2))


def test_insert_select_all_caps():
    ins = INSERT.INTO("table")("column1", "column2").SELECT(SELECT("a", "b", table="table2"))
    assert str(ins) == "INSERT INTO `table` (`column1`, `column2`) SELECT `a`, `b` FROM `table2`"
    assert ins.args == []
