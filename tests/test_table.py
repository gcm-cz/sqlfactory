"""
Test suite for the Table class
"""

import pytest
from sqlfactory import Table, Column


def test_table_init():
    t = Table("table")
    assert t.table == "table"
    assert t.database is None

    t = Table("database.table")
    assert t.table == "table"
    assert t.database == "database"

    with pytest.raises(ValueError):
        Table("a.b.c")


def test_table_str():
    t = Table("table")
    assert str(t) == "`table`"

    t = Table("database.table")
    assert str(t) == "`database`.`table`"


def test_table_getattr():
    t = Table("database.table")
    c = t.column
    assert isinstance(c, Column)
    assert c.column == "column"
    assert c.table == "table"
    assert c.database == "database"
