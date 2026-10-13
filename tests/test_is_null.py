"""Tests for the IS [NOT] NULL predicate (`sqlfactory.condition.is_null`)."""

import pytest

from sqlfactory import Column, Eq, IsNotNull, IsNull, Ne, Select, Value
from sqlfactory.condition.is_null import IsNotNull as IsNotNullDirect
from sqlfactory.condition.is_null import IsNull as IsNullDirect
from sqlfactory.dialect import PostgreSQLDialect
from sqlfactory.func.str import Lower


def test_top_level_and_condition_package_exports():
    assert IsNull is IsNullDirect
    assert IsNotNull is IsNotNullDirect


def test_is_null_bare_str_is_column():
    cond = IsNull("t.deleted_at")
    assert str(cond) == "`t`.`deleted_at` IS NULL"
    assert cond.args == []
    assert bool(cond) is True


def test_is_not_null_bare_str_is_column():
    cond = IsNotNull("deleted_at")
    assert str(cond) == "`deleted_at` IS NOT NULL"
    assert cond.args == []
    assert bool(cond) is True


def test_is_null_negative_flag():
    assert str(IsNull("a", negative=True)) == "`a` IS NOT NULL"


def test_is_null_statement():
    cond = IsNull(Lower(Value("X")))
    assert str(cond) == "LOWER(%s) IS NULL"
    assert cond.args == ["X"]


def test_is_null_subquery_is_parenthesised():
    cond = IsNull(Select("a", table="t", where=Eq("b", 1)))
    assert str(cond) == "(SELECT `a` FROM `t` WHERE `b` = %s) IS NULL"
    assert cond.args == [1]


def test_is_null_never_binds_a_placeholder():
    """Unlike Eq(col, None), which renders `IS %s` with a None argument, IsNull is a literal `IS NULL`."""
    assert str(Eq("a", None)) == "`a` IS %s"
    assert Eq("a", None).args == [None]
    assert str(Ne("a", None)) == "`a` IS NOT %s"
    assert str(IsNull("a")) == "`a` IS NULL"
    assert str(IsNotNull(Column("a"))) == "`a` IS NOT NULL"


def test_is_null_dialect():
    sel = Select("a", table="t", where=IsNull("b") & IsNotNull("c"), dialect=PostgreSQLDialect())
    assert str(sel) == 'SELECT "a" FROM "t" WHERE ("b" IS NULL AND "c" IS NOT NULL)'


def test_is_null_invert():
    inverted = ~IsNull("a")
    assert isinstance(inverted, IsNotNull)
    assert str(inverted) == "`a` IS NOT NULL"


def test_is_null_negative_flag_invert():
    inverted = ~IsNull("a", negative=True)
    assert not isinstance(inverted, IsNotNull)
    assert str(inverted) == "`a` IS NULL"


def test_is_not_null_invert_raises():
    with pytest.raises(TypeError):
        ~IsNotNull("a")


def test_is_null_combines_with_other_conditions():
    cond = IsNull("a") | Eq("b", 1)
    assert str(cond) == "(`a` IS NULL OR `b` = %s)"
    assert cond.args == [1]
