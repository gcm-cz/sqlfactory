from sqlfactory import Column, Insert, Raw
from sqlfactory.func.info import (
    Benchmark,
    BinlogGtidPos,
    Charset,
    Coercibility,
    Collate,
    Collation,
    ConnectionId,
    CurrentRole,
    CurrentUser,
    Database,
    DecodeHistogram,
    Default,
    FoundRows,
    LastInsertId,
    LastValue,
    RowCount,
    RowNumber,
    Schema,
    SessionUser,
    SystemUser,
    User,
    Version,
)


def test_benchmark():
    benchmark_func = Benchmark(1000, Raw("SELECT 1"))
    assert str(benchmark_func) == "BENCHMARK(%s, SELECT 1)"
    assert benchmark_func.args == [1000]


def test_binlog_gtid_pos():
    binlog_gtid_pos_func = BinlogGtidPos("binlog.000002", 1023)
    assert str(binlog_gtid_pos_func) == "BINLOG_GTID_POS(%s, %s)"
    assert binlog_gtid_pos_func.args == ["binlog.000002", 1023]


def test_binlog_gtid_pos_with_statement_args():
    binlog_gtid_pos_func = BinlogGtidPos(Column("binlog_filename"), Column("binlog_offset"))
    assert str(binlog_gtid_pos_func) == "BINLOG_GTID_POS(`binlog_filename`, `binlog_offset`)"
    assert binlog_gtid_pos_func.args == []


def test_charset():
    charset_func = Charset("expression")
    assert str(charset_func) == "CHARSET(%s)"
    assert charset_func.args == ["expression"]


def test_charset_with_column():
    charset_func = Charset(Column("column"))
    assert str(charset_func) == "CHARSET(`column`)"
    assert charset_func.args == []


def test_coercibility():
    coercibility_func = Coercibility("expression")
    assert str(coercibility_func) == "COERCIBILITY(%s)"
    assert coercibility_func.args == ["expression"]


def test_coercibility_with_column():
    coercibility_func = Coercibility(Column("column"))
    assert str(coercibility_func) == "COERCIBILITY(`column`)"
    assert coercibility_func.args == []


def test_collation():
    collation_func = Collation("expression")
    assert str(collation_func) == "COLLATION(%s)"
    assert collation_func.args == ["expression"]


def test_collation_with_column():
    collation_func = Collation(Column("column"))
    assert str(collation_func) == "COLLATION(`column`)"
    assert collation_func.args == []


def test_collate():
    collate_func = Collate("expression", "collation")
    assert str(collate_func) == "%s COLLATE collation"
    assert collate_func.args == ["expression"]


def test_connection_id():
    connection_id_func = ConnectionId()
    assert str(connection_id_func) == "CONNECTION_ID()"
    assert connection_id_func.args == []


def test_current_role():
    current_role_func = CurrentRole()
    assert str(current_role_func) == "CURRENT_ROLE()"
    assert current_role_func.args == []


def test_current_user():
    current_user_func = CurrentUser()
    assert str(current_user_func) == "CURRENT_USER()"
    assert current_user_func.args == []


def test_database():
    database_func = Database()
    assert str(database_func) == "DATABASE()"
    assert database_func.args == []


def test_decode_histogram():
    decode_histogram_func = DecodeHistogram("hist_type", "histogram")
    assert str(decode_histogram_func) == "DECODE_HISTOGRAM(%s, %s)"
    assert decode_histogram_func.args == ["hist_type", "histogram"]


def test_default():
    default_func = Default(Column("column"))
    assert str(default_func) == "DEFAULT(`column`)"
    assert default_func.args == []


def test_default_with_string_column_name():
    default_func = Default("column")
    assert str(default_func) == "DEFAULT(`column`)"
    assert default_func.args == []


def test_found_rows():
    found_rows_func = FoundRows()
    assert str(found_rows_func) == "FOUND_ROWS()"
    assert found_rows_func.args == []


def test_last_insert_id():
    last_insert_id_func = LastInsertId()
    assert str(last_insert_id_func) == "LAST_INSERT_ID()"
    assert last_insert_id_func.args == []


def test_last_insert_id_with_column():
    last_insert_id_func = LastInsertId(Column("id"))
    assert str(last_insert_id_func) == "LAST_INSERT_ID(`id`)"
    assert last_insert_id_func.args == []


def test_last_insert_id_with_value():
    last_insert_id_func = LastInsertId(5)
    assert str(last_insert_id_func) == "LAST_INSERT_ID(%s)"
    assert last_insert_id_func.args == [5]


def test_last_insert_id_in_insert_on_duplicate_key_update():
    # The canonical use of LAST_INSERT_ID(expr): recover the id of the row that was updated by ON DUPLICATE KEY
    # UPDATE, which does not otherwise set LAST_INSERT_ID() the way a plain INSERT does.
    insert_stmt = Insert.into("t1")("id", "val").values((2, 99)).on_duplicate_key_update(id=LastInsertId(Column("id")), val=25)
    assert (
        str(insert_stmt) == "INSERT INTO `t1` (`id`, `val`) VALUES (%s, %s) "
        "ON DUPLICATE KEY UPDATE `id` = LAST_INSERT_ID(`id`), `val` = %s"
    )
    assert insert_stmt.args == [2, 99, 25]


def test_last_value():
    last_value_func = LastValue(Raw("SELECT 1"), Raw("SELECT 2"))
    assert str(last_value_func) == "LAST_VALUE(SELECT 1, SELECT 2)"
    assert last_value_func.args == []


def test_last_value_with_plain_value():
    # LAST_VALUE() accepts any mix of expressions, including plain values, e.g.
    # `last_value(@a:=a, @b:=b, 1)` in MariaDB's own documentation.
    last_value_func = LastValue(Raw("@a:=a"), Raw("@b:=b"), 1)
    assert str(last_value_func) == "LAST_VALUE(@a:=a, @b:=b, %s)"
    assert last_value_func.args == [1]


def test_row_count():
    row_count_func = RowCount()
    assert str(row_count_func) == "ROW_COUNT()"
    assert row_count_func.args == []


def test_row_number():
    row_number_func = RowNumber()
    assert str(row_number_func) == "ROW_NUMBER()"
    assert row_number_func.args == []


def test_schema():
    schema_func = Schema()
    assert str(schema_func) == "SCHEMA()"
    assert schema_func.args == []


def test_session_user():
    session_user_func = SessionUser()
    assert str(session_user_func) == "SESSION_USER()"
    assert session_user_func.args == []


def test_system_user():
    system_user_func = SystemUser()
    assert str(system_user_func) == "SYSTEM_USER()"
    assert system_user_func.args == []


def test_user():
    user_func = User()
    assert str(user_func) == "USER()"
    assert user_func.args == []


def test_version():
    version_func = Version()
    assert str(version_func) == "VERSION()"
    assert version_func.args == []
