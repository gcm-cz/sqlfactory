import pytest

from sqlfactory import Column
from sqlfactory.condition.between import Between
from sqlfactory.func.str import Concat


def test_between():
    between_condition = Between("`column1`", 5, 10)
    assert str(between_condition) == "`column1` BETWEEN %s AND %s"
    assert between_condition.args == [5, 10]


def test_between_negative():
    between_condition = Between("`column1`", 5, 10, negative=True)
    assert str(between_condition) == "`column1` NOT BETWEEN %s AND %s"
    assert between_condition.args == [5, 10]


def test_between_with_statements():
    statement1 = Column("column2")
    statement2 = Column("column3")
    between_condition = Between("column1", statement1, statement2)
    assert str(between_condition) == "`column1` BETWEEN `column2` AND `column3`"
    assert between_condition.args == []


def test_between_negative_with_statements():
    statement1 = Column("column2")
    statement2 = Column("column3")
    between_condition = Between("column1", statement1, statement2, negative=True)
    assert str(between_condition) == "`column1` NOT BETWEEN `column2` AND `column3`"
    assert between_condition.args == []


def test_between_with_statement_with_args():
    statement1 = Concat(Column("column1"), "foo")
    statement2 = Concat("bar", Column("column2"))
    statement3 = Concat("bar", "foo")

    between_condition = Between(statement1, statement2, statement3)
    assert str(between_condition) == "CONCAT(`column1`, %s) BETWEEN CONCAT(%s, `column2`) AND CONCAT(%s, %s)"
    assert between_condition.args == ["foo", "bar", "bar", "foo"]
