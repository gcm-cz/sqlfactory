from sqlfactory import Between, Column, Direction, Eq, In, PostgreSQLDialect, Select, SQLiteDialect
from sqlfactory.dialect import MySQLDialect, OracleSQLDialect
from sqlfactory.func.control import IfNull


def test_dialect_context_in():
    cond = In("column", [1, 2, 3])

    with SQLiteDialect():
        assert str(cond) == "`column` IN (?, ?, ?)"
        assert cond.args == [1, 2, 3]

    with PostgreSQLDialect():
        assert str(cond) == '"column" IN (%s, %s, %s)'
        assert cond.args == [1, 2, 3]


def test_dialect_context_between():
    cond = Between("xyz", 1, 2)

    with SQLiteDialect():
        assert str(cond) == "`xyz` BETWEEN ? AND ?"
        assert cond.args == [1, 2]

    with PostgreSQLDialect():
        assert str(cond) == '"xyz" BETWEEN %s AND %s'
        assert cond.args == [1, 2]


def test_dialect_context_simple():
    eq = Eq("column", 1)

    with SQLiteDialect():
        assert str(eq) == "`column` = ?"
        assert eq.args == [1]

    with PostgreSQLDialect():
        assert str(eq) == '"column" = %s'
        assert eq.args == [1]


def test_oracle_dialect():
    cond = In("a", [1, 2, 3])

    sel = Select(IfNull(Column("a"), "xyz"), table="table")

    sel.limit(0, 10)
    sel.order_by("a", Direction.DESC)

    sel.where(Eq("id", 442))
    sel.where(cond)

    with OracleSQLDialect():
        assert str(sel) == 'SELECT IFNULL("a", :1) FROM "table" WHERE ("id" = :2 AND "a" IN (:3, :4, :5)) ORDER BY "a" DESC LIMIT :6, :7'
        assert sel.args == ["xyz", 442, 1, 2, 3, 0, 10]


def test_explicit_dialect():
    cond = In("a", [1, 2, 3])

    sel = Select(IfNull(Column("a"), "xyz"), table="table", dialect=OracleSQLDialect())

    sel.limit(0, 10)
    sel.order_by("a", Direction.DESC)

    sel.where(Eq("id", 442))
    sel.where(cond)

    assert str(sel) == 'SELECT IFNULL("a", :1) FROM "table" WHERE ("id" = :2 AND "a" IN (:3, :4, :5)) ORDER BY "a" DESC LIMIT :6, :7'
    assert sel.args == ["xyz", 442, 1, 2, 3, 0, 10]

    sel.dialect = MySQLDialect()

    assert str(sel) == 'SELECT IFNULL(`a`, %s) FROM `table` WHERE (`id` = %s AND `a` IN (%s, %s, %s)) ORDER BY `a` DESC LIMIT %s, %s'
    assert sel.args == ["xyz", 442, 1, 2, 3, 0, 10]
