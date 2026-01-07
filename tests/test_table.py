"""
Test suite for the Table class
"""

from abc import ABC
from typing import ClassVar

import pytest

from sqlfactory import Column, Statement, Table


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


def test_table_is_not_abstract():
    class BaseClass(ABC):
        table: ClassVar[Table] = Table("table")

    bc = BaseClass()
    assert str(bc.table) == "`table`"
