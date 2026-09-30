"""Tests for the IS JSON predicate (`sqlfactory.condition.is_json`)."""

import pytest

from sqlfactory import Column, Value
from sqlfactory.condition.is_json import IsJson, IsNotJson, JsonValueType


def test_is_json_bare_str_wraps_into_column():
    cond = IsJson("doc")
    assert str(cond) == "`doc` IS JSON"
    assert cond.args == []
    assert bool(cond) is True


def test_is_json_statement_column():
    cond = IsJson(Column("doc"))
    assert str(cond) == "`doc` IS JSON"
    assert cond.args == []


def test_is_json_literal_value():
    cond = IsJson(Value('{"a": 42}'))
    assert str(cond) == "%s IS JSON"
    assert cond.args == ['{"a": 42}']


def test_is_json_with_value_type():
    cond = IsJson(Column("doc"), JsonValueType.OBJECT)
    assert str(cond) == "`doc` IS JSON OBJECT"
    assert cond.args == []


def test_is_json_with_unique_true():
    cond = IsJson(Column("doc"), unique=True)
    assert str(cond) == "`doc` IS JSON WITH UNIQUE KEYS"


def test_is_json_with_unique_false():
    cond = IsJson(Column("doc"), unique=False)
    assert str(cond) == "`doc` IS JSON WITHOUT UNIQUE KEYS"


def test_is_json_negative():
    cond = IsJson(Column("doc"), negative=True)
    assert str(cond) == "`doc` IS NOT JSON"


def test_is_json_full():
    cond = IsJson(Column("doc"), JsonValueType.ARRAY, unique=True, negative=True)
    assert str(cond) == "`doc` IS NOT JSON ARRAY WITH UNIQUE KEYS"


def test_is_json_invert():
    cond = IsJson(Column("doc"), JsonValueType.SCALAR, unique=False)
    inverted = ~cond
    assert isinstance(inverted, IsNotJson)
    assert str(inverted) == "`doc` IS NOT JSON SCALAR WITHOUT UNIQUE KEYS"


def test_is_not_json_basic():
    cond = IsNotJson(Column("doc"))
    assert str(cond) == "`doc` IS NOT JSON"
    assert cond.args == []
    assert bool(cond) is True


def test_is_not_json_invert_raises():
    cond = IsNotJson(Column("doc"))
    with pytest.raises(TypeError):
        ~cond
