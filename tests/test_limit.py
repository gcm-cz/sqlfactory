import pytest

from sqlfactory import Limit, Select


def test_empty_limit():
    assert str(Limit()) == ""
    assert Limit().args == []


def test_with_limit():
    with pytest.raises(AttributeError, match="Limit has already been specified."):
        Select(table="xyz").limit(10).LIMIT(10)
