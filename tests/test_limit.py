import pytest

from sqlfactory import Limit, Select


def test_empty_limit():
    assert str(Limit()) == ""
    assert Limit().args == []


def test_with_limit():
    with pytest.raises(AttributeError, match="Limit has already been specified."):
        Select(table="xyz").limit(10).LIMIT(10)


def test_limit_init():
    l = Limit(10)  # Positional only limit
    assert l.offset is None
    assert l.limit == 10

    assert str(l) == "LIMIT %s"
    assert l.args == [10]

    l = Limit(3, 8)  # Positional offset and limit
    assert l.offset == 3
    assert l.limit == 8

    assert str(l) == "LIMIT %s, %s"
    assert l.args == [3, 8]

    l = Limit(7, limit=2)  # Positional offset and keyword limit
    assert l.offset == 7
    assert l.limit == 2

    assert str(l) == "LIMIT %s, %s"
    assert l.args == [7, 2]

    l = Limit(offset=5, limit=1)  # Keyword offset and limit
    assert l.offset == 5
    assert l.limit == 1

    assert str(l) == "LIMIT %s, %s"
    assert l.args == [5, 1]

    with pytest.raises(AttributeError):
        Limit(4, limit=9, offset=5)


def test_limit_select():
    q = Select(table="xyz").limit(10)
    assert str(q) == "SELECT * FROM `xyz` LIMIT %s"
    assert q.args == [10]

    q = Select(table="xyz").limit(3, 8)
    assert str(q) == "SELECT * FROM `xyz` LIMIT %s, %s"
    assert q.args == [3, 8]

    q = Select(table="xyz").limit(7, limit=2)
    assert str(q) == "SELECT * FROM `xyz` LIMIT %s, %s"
    assert q.args == [7, 2]

    q = Select(table="xyz").limit(offset=5, limit=1)
    assert str(q) == "SELECT * FROM `xyz` LIMIT %s, %s"
    assert q.args == [5, 1]

    with pytest.raises(AttributeError):
        Select(table="xyz").limit(4, limit=9, offset=5)
