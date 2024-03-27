"""
Test suite for the condition.simple module.
"""
import pytest

from sqlbuilder import Column
from sqlbuilder.condition.simple import Equals, NotEquals, GreaterThanOrEquals, GreaterThan, LessThanOrEquals, LessThan
from sqlbuilder.func.str import Concat


def test_equals():
    eq = Equals("column", 5)
    assert str(eq) == "`column` = %s"
    assert eq.args == [5]

    eq = Equals("column", None)
    assert str(eq) == "`column` IS %s"
    assert eq.args == [None]


def test_not_equals():
    ne = NotEquals("column", 5)
    assert str(ne) == "`column` != %s"
    assert ne.args == [5]

    ne = NotEquals("column", None)
    assert str(ne) == "`column` IS NOT %s"
    assert ne.args == [None]


def test_greater_than_or_equals():
    ge = GreaterThanOrEquals("column", 5)
    assert str(ge) == "`column` >= %s"
    assert ge.args == [5]


def test_greater_than():
    gt = GreaterThan("column", 5)
    assert str(gt) == "`column` > %s"
    assert gt.args == [5]


def test_less_than_or_equals():
    le = LessThanOrEquals("column", 5)
    assert str(le) == "`column` <= %s"
    assert le.args == [5]


def test_less_than():
    lt = LessThan("column", 5)
    assert str(lt) == "`column` < %s"
    assert lt.args == [5]


def test_equals_statement():
    eq = Equals(Concat(Column("column1"), "foo"), Concat(Column("column2"), "bar"))
    assert str(eq) == "CONCAT(`column1`, %s) = CONCAT(`column2`, %s)"
    assert eq.args == ["foo", "bar"]
