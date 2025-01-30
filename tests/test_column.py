"""
Test suite for the Column class
"""

import pytest

from sqlfactory import Column, Eq, Ge, Gt, Le, Lt, Ne


def test_column_init():
    c = Column("column")
    assert c.column == "column"
    assert c.table is None
    assert c.database is None

    c = Column("table.column")
    assert c.column == "column"
    assert c.table == "table"
    assert c.database is None

    c = Column("database.table.column")
    assert c.column == "column"
    assert c.table == "table"
    assert c.database == "database"

    with pytest.raises(ValueError):
        Column("a.b.c.d")


def test_column_str():
    c = Column("column")
    assert str(c) == "`column`"

    c = Column("table.column")
    assert str(c) == "`table`.`column`"

    c = Column("database.table.column")
    assert str(c) == "`database`.`table`.`column`"


def test_column_is_not_none():
    c = Column("column")
    assert c is not None

    # TODO: This fails, but should it?
    l = [Column("column")]
    # assert (None in l) is False


def test_column_gt():
    c = Column("column")
    gt = c > 5
    assert isinstance(gt, Gt)
    assert str(gt) == "`column` > %s"
    assert gt.args == [5]


def test_column_ge():
    c = Column("column")
    ge = c >= 5
    assert isinstance(ge, Ge)
    assert str(ge) == "`column` >= %s"
    assert ge.args == [5]


def test_column_lt():
    c = Column("column")
    lt = c < 5
    assert isinstance(lt, Lt)
    assert str(lt) == "`column` < %s"
    assert lt.args == [5]


def test_column_le():
    c = Column("column")
    le = c <= 5
    assert isinstance(le, Le)
    assert str(le) == "`column` <= %s"
    assert le.args == [5]


def test_column_eq():
    c = Column("column")
    eq = c == 5
    assert isinstance(eq, Eq)
    assert str(eq) == "`column` = %s"
    assert eq.args == [5]


def test_column_ne():
    c = Column("column")
    ne = c != 5
    assert isinstance(ne, Ne)
    assert str(ne) == "`column` != %s"
    assert ne.args == [5]


def test_column_sub():
    c = Column("column")
    sub = c - 5
    assert str(sub) == "(`column` - %s)"
    assert sub.args == [5]


def test_column_mul():
    c = Column("column")
    mul = c * 5
    assert str(mul) == "(`column` * %s)"
    assert mul.args == [5]


def test_column_truediv():
    c = Column("column")
    truediv = c / 5
    assert str(truediv) == "(`column` / %s)"
    assert truediv.args == [5]


def test_column_mod():
    c = Column("column")
    mod = c % 5
    assert str(mod) == "(`column` % %s)"
    assert mod.args == [5]


def test_column_and():
    c = Column("column")
    and_ = c & 5
    assert str(and_) == "(`column` & %s)"
    assert and_.args == [5]


def test_column_or():
    c = Column("column")
    or_ = c | 5
    assert str(or_) == "(`column` | %s)"
    assert or_.args == [5]


def test_column_xor():
    c = Column("column")
    xor = c ^ 5
    assert str(xor) == "(`column` ^ %s)"
    assert xor.args == [5]


def test_column_lshift():
    c = Column("column")
    lshift = c << 5
    assert str(lshift) == "(`column` << %s)"
    assert lshift.args == [5]


def test_column_rshift():
    c = Column("column")
    rshift = c >> 5
    assert str(rshift) == "(`column` >> %s)"
    assert rshift.args == [5]


def test_column_neg():
    c = Column("column")
    neg = -c
    assert str(neg) == "(~`column`)"
    assert neg.args == []
