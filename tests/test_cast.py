"""Tests for CAST, CONVERT and the BINARY operator."""

import pytest

from sqlfactory import Column, Direction, Eq, Select, Update
from sqlfactory.func.cast import (
    Binary,
    Cast,
    CastBinary,
    CastChar,
    CastDatetime,
    CastDecimal,
    CastDouble,
    CastIntervalDaySecond,
    CastNChar,
    CastTime,
    CastType,
    CastVarchar,
    CastVarchar2,
    Convert,
)
from sqlfactory.func.info import Collate
from sqlfactory.func.json import JsonValue

# ---------------------------------------------------------------------------
# Target types
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("type_", "sql"),
    [
        (CastType.BINARY, "BINARY"),
        (CastType.CHAR, "CHAR"),
        (CastType.NCHAR, "NCHAR"),
        (CastType.DATE, "DATE"),
        (CastType.DATETIME, "DATETIME"),
        (CastType.TIME, "TIME"),
        (CastType.DECIMAL, "DECIMAL"),
        (CastType.DOUBLE, "DOUBLE"),
        (CastType.FLOAT, "FLOAT"),
        (CastType.INT, "INT"),
        (CastType.INTEGER, "INTEGER"),
        (CastType.SIGNED, "SIGNED"),
        (CastType.SIGNED_INT, "SIGNED INT"),
        (CastType.SIGNED_INTEGER, "SIGNED INTEGER"),
        (CastType.UNSIGNED, "UNSIGNED"),
        (CastType.UNSIGNED_INT, "UNSIGNED INT"),
        (CastType.UNSIGNED_INTEGER, "UNSIGNED INTEGER"),
        (CastType.INET4, "INET4"),
        (CastType.INET6, "INET6"),
        (CastType.UUID, "UUID"),
        (CastType.XMLTYPE, "XMLTYPE"),
    ],
)
def test_keyword_types(type_, sql):
    func = Cast("value", type_)
    assert str(func) == f"CAST(%s AS {sql})"
    assert func.args == ["value"]


def test_every_keyword_type_is_tested():
    assert len(CastType) == 21


@pytest.mark.parametrize(
    ("type_", "sql"),
    [
        (CastBinary(16), "BINARY(16)"),
        (CastChar(), "CHAR"),
        (CastChar(10), "CHAR(10)"),
        (CastChar(charset="utf8mb4"), "CHAR CHARACTER SET utf8mb4"),
        (CastChar(collate="utf8mb4_czech_ci"), "CHAR COLLATE utf8mb4_czech_ci"),
        (CastChar(collate="DEFAULT"), "CHAR COLLATE DEFAULT"),
        (CastChar(collate="binary"), "CHAR COLLATE binary"),
        (CastChar(binary=True), "CHAR BINARY"),
        (CastChar(binary=False), "CHAR"),
        (CastChar(charset="latin1", binary=True), "CHAR CHARACTER SET latin1 BINARY"),
        (CastChar(charset="utf8mb4", collate="DEFAULT"), "CHAR CHARACTER SET utf8mb4 COLLATE DEFAULT"),
        (CastChar(10, charset="utf8mb4", collate="utf8mb4_bin"), "CHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin"),
        (CastChar(0), "CHAR(0)"),
        (CastVarchar(3), "VARCHAR(3)"),
        (CastVarchar(3, charset="latin1"), "VARCHAR(3) CHARACTER SET latin1"),
        (CastVarchar(3, collate="latin1_bin"), "VARCHAR(3) COLLATE latin1_bin"),
        (CastVarchar(3, binary=True), "VARCHAR(3) BINARY"),
        (CastVarchar(3, charset="latin1", collate="latin1_bin"), "VARCHAR(3) CHARACTER SET latin1 COLLATE latin1_bin"),
        (CastVarchar2(3), "VARCHAR2(3)"),
        (CastVarchar2(3, charset="latin1", binary=True), "VARCHAR2(3) CHARACTER SET latin1 BINARY"),
        (CastNChar(2), "NCHAR(2)"),
        (CastDecimal(5), "DECIMAL(5)"),
        (CastDecimal(10, 2), "DECIMAL(10,2)"),
        (CastDecimal(10, 0), "DECIMAL(10,0)"),
        (CastDouble(10, 2), "DOUBLE(10,2)"),
        (CastTime(3), "TIME(3)"),
        (CastTime(0), "TIME(0)"),
        (CastDatetime(6), "DATETIME(6)"),
        (CastIntervalDaySecond(2), "INTERVAL DAY_SECOND(2)"),
    ],
)
def test_parameterised_types(type_, sql):
    func = Cast("value", type_)
    assert str(func) == f"CAST(%s AS {sql})"
    assert func.args == ["value"]


def test_varchar2_is_varchar_alias():
    assert isinstance(CastVarchar2(3), CastVarchar)


# ---------------------------------------------------------------------------
# Validation of what is spliced into the SQL
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "build",
    [
        lambda: CastBinary("16"),
        lambda: CastChar("10) ; DROP TABLE t; -- "),
        lambda: CastChar(10.5),
        lambda: CastChar(True),
        lambda: CastVarchar(None),
        lambda: CastNChar("2"),
        lambda: CastDecimal("10", 2),
        lambda: CastDecimal(10, "2"),
        lambda: CastDouble(10, 2.0),
        lambda: CastTime("3"),
        lambda: CastDatetime(False),
        lambda: CastIntervalDaySecond("2"),
    ],
)
def test_type_parameter_must_be_int(build):
    with pytest.raises(TypeError, match="must be an int"):
        build()


@pytest.mark.parametrize(
    "build",
    [
        lambda: CastBinary(-1),
        lambda: CastChar(-1),
        lambda: CastDecimal(-1),
        lambda: CastDecimal(10, -2),
        lambda: CastTime(-3),
    ],
)
def test_type_parameter_must_not_be_negative(build):
    with pytest.raises(ValueError, match="must not be negative"):
        build()


@pytest.mark.parametrize(
    "name",
    [
        "utf8mb4 COLLATE utf8mb4_bin",
        "utf8mb4; DROP TABLE t",
        "utf8mb4)",
        "`utf8mb4`",
        "'utf8mb4'",
        "",
        "1abc",
        "_utf8mb4",
        "utf8-mb4",
        8,
    ],
)
def test_names_must_be_bare_identifiers(name):
    with pytest.raises(ValueError, match="bare identifier"):
        CastChar(charset=name)

    with pytest.raises(ValueError, match="bare identifier"):
        CastVarchar(3, collate=name)

    with pytest.raises(ValueError, match="bare identifier"):
        Convert("abc", using=name)


def test_target_type_must_not_be_a_string():
    with pytest.raises(TypeError, match="Target type"):
        Cast("value", "UNSIGNED) ; DROP TABLE t; -- ")

    with pytest.raises(TypeError, match="Target type"):
        Convert("value", "UNSIGNED")


# ---------------------------------------------------------------------------
# CAST
# ---------------------------------------------------------------------------


def test_cast_statement():
    func = Cast(Column("price"), CastDecimal(10, 2))
    assert str(func) == "CAST(`price` AS DECIMAL(10,2))"
    assert func.args == []


def test_cast_str_binds_as_value():
    func = Cast("price", CastType.SIGNED)
    assert str(func) == "CAST(%s AS SIGNED)"
    assert func.args == ["price"]


def test_cast_function_with_args():
    func = Cast(JsonValue(Column("doc"), "$.accountId"), CastType.UNSIGNED)
    assert str(func) == "CAST(JSON_VALUE(`doc`, %s) AS UNSIGNED)"
    assert func.args == ["$.accountId"]


def test_cast_query_is_parenthesised():
    func = Cast(Select(Column("t.a"), table="t", where=Eq("t.id", 5)), CastType.CHAR)
    assert str(func) == "CAST((SELECT `t`.`a` FROM `t` WHERE `t`.`id` = %s) AS CHAR)"
    assert func.args == [5]


def test_cast_none_binds_null():
    func = Cast(None, CastType.DATE)
    assert str(func) == "CAST(%s AS DATE)"
    assert func.args == [None]


# ---------------------------------------------------------------------------
# CONVERT
# ---------------------------------------------------------------------------


def test_convert_type():
    func = Convert(Column("id"), CastType.CHAR)
    assert str(func) == "CONVERT(`id`, CHAR)"
    assert func.args == []


def test_convert_parameterised_type_and_value():
    func = Convert("1.555", CastDecimal(10, 2))
    assert str(func) == "CONVERT(%s, DECIMAL(10,2))"
    assert func.args == ["1.555"]


def test_convert_using():
    func = Convert(Column("name"), using="utf8mb4")
    assert str(func) == "CONVERT(`name` USING utf8mb4)"
    assert func.args == []


def test_convert_using_value():
    func = Convert("abc", using="binary")
    assert str(func) == "CONVERT(%s USING binary)"
    assert func.args == ["abc"]


def test_convert_query_is_parenthesised():
    func = Convert(Select(Column("t.a"), table="t", where=Eq("t.id", 5)), using="latin1")
    assert str(func) == "CONVERT((SELECT `t`.`a` FROM `t` WHERE `t`.`id` = %s) USING latin1)"
    assert func.args == [5]


def test_convert_needs_type_or_using():
    with pytest.raises(TypeError, match="exactly one"):
        Convert(Column("name"))


def test_convert_not_both_type_and_using():
    with pytest.raises(TypeError, match="exactly one"):
        Convert(Column("name"), CastType.CHAR, using="utf8mb4")


# ---------------------------------------------------------------------------
# BINARY operator
# ---------------------------------------------------------------------------


def test_binary_column():
    func = Binary(Column("name"))
    assert str(func) == "BINARY `name`"
    assert func.args == []


def test_binary_value():
    func = Binary("abc")
    assert str(func) == "BINARY %s"
    assert func.args == ["abc"]


def test_binary_comparison():
    cond = Binary(Column("name")) == "abc"
    assert str(cond) == "BINARY `name` = %s"
    assert cond.args == ["abc"]


def test_binary_condition_is_parenthesised():
    func = Binary(Eq("name", "abc"))
    assert str(func) == "BINARY (`name` = %s)"
    assert func.args == ["abc"]


def test_binary_query_is_parenthesised():
    func = Binary(Select(Column("t.a"), table="t", where=Eq("t.id", 5)))
    assert str(func) == "BINARY (SELECT `t`.`a` FROM `t` WHERE `t`.`id` = %s)"
    assert func.args == [5]


# ---------------------------------------------------------------------------
# Composition
# ---------------------------------------------------------------------------


def test_cast_in_select_where_and_order():
    account = Cast(JsonValue(Column("doc"), "$.accountId"), CastType.UNSIGNED)
    sel = Select(Column("id"), account, table="acc", where=account == 42).order_by(account, Direction.ASC)

    assert str(sel) == (
        "SELECT `id`, CAST(JSON_VALUE(`doc`, %s) AS UNSIGNED) FROM `acc` "
        "WHERE CAST(JSON_VALUE(`doc`, %s) AS UNSIGNED) = %s "
        "ORDER BY CAST(JSON_VALUE(`doc`, %s) AS UNSIGNED) ASC"
    )
    assert sel.args == ["$.accountId", "$.accountId", 42, "$.accountId"]


def test_binary_and_cast_in_where():
    sel = Select(
        Column("id"),
        table="acc",
        where=(Binary(Column("name")) == "abc") & (Cast(Column("price"), CastDecimal(10, 2)) > 10),
    )

    assert str(sel) == "SELECT `id` FROM `acc` WHERE (BINARY `name` = %s AND CAST(`price` AS DECIMAL(10,2)) > %s)"
    assert sel.args == ["abc", 10]


def test_convert_in_update():
    upd = Update("acc").set("price", Convert(Cast(Column("price"), CastDecimal(10, 1)), CastType.CHAR)).where(Eq("id", 1))

    assert str(upd) == "UPDATE `acc` SET `price` = CONVERT(CAST(`price` AS DECIMAL(10,1)), CHAR) WHERE `id` = %s"
    assert upd.args == [1]


def test_collate_on_cast():
    func = Collate(Cast(Column("name"), CastChar(charset="utf8mb4")), "utf8mb4_bin")
    assert str(func) == "CAST(`name` AS CHAR CHARACTER SET utf8mb4) COLLATE utf8mb4_bin"
    assert func.args == []
