from sqlfactory import Column, In
from sqlfactory.func.str import Concat


def test_in_single_column():
    in_condition = In("column1", [1, 2, 3])
    assert str(in_condition) == "`column1` IN (%s, %s, %s)"
    assert in_condition.args == [1, 2, 3]


def test_in_single_column_statement():
    in_condition = In(Column("column1"), [1, 2, 3])
    assert str(in_condition) == "`column1` IN (%s, %s, %s)"
    assert in_condition.args == [1, 2, 3]


def test_in_single_column_with_statement():
    statement1 = Concat(Column("column1"), "value")
    in_condition = In(statement1, [1, 2, 3])
    assert str(in_condition) == "CONCAT(`column1`, %s) IN (%s, %s, %s)"
    assert in_condition.args == ["value", 1, 2, 3]


def test_in_tuple_columns():
    in_condition = In(("column1", "column2"), [(1, 2), (3, 4)])
    assert str(in_condition) == "(`column1`, `column2`) IN ((%s, %s), (%s, %s))"
    assert in_condition.args == [1, 2, 3, 4]


def test_in_tuple_columns_with_null():
    in_condition = In(("column1", "column2"), [(1, 2), (None, None), (1, None), (None, 2)])
    assert (
        str(in_condition)
        == "((`column1`, `column2`) IN ((%s, %s)) OR (`column1` IS %s AND `column2` IS %s) OR (`column1` = %s AND `column2` IS %s) OR (`column1` IS %s AND `column2` = %s))"
    )
    assert in_condition.args == [1, 2, None, None, 1, None, None, 2]


def test_in_with_only_none_in_values():
    in_condition = In("column1", [None])
    assert str(in_condition) == "`column1` IS NULL"
    assert in_condition.args == []


def test_in_tuple_only_none_in_values():
    in_condition = In(("column1", "column2"), [(None, None)])
    assert str(in_condition) == "(`column1` IS %s AND `column2` IS %s)"
    assert in_condition.args == [None, None]


def test_not_in_tuple_columns_with_null():
    in_condition = In(("column1", "column2"), [(1, 2), (None, None), (1, None), (None, 2)], negative=True)
    assert (
        str(in_condition)
        == "((`column1`, `column2`) NOT IN ((%s, %s)) AND (`column1` IS NOT %s AND `column2` IS NOT %s) AND (`column1` != %s AND `column2` IS NOT %s) AND (`column1` IS NOT %s AND `column2` != %s))"
    )
    assert in_condition.args == [1, 2, None, None, 1, None, None, 2]


def test_in_tuple_columns_statement():
    in_condition = In((Column("column1"), Column("column2")), [(1, 2), (3, 4)])
    assert str(in_condition) == "(`column1`, `column2`) IN ((%s, %s), (%s, %s))"
    assert in_condition.args == [1, 2, 3, 4]


def test_in_tuple_columns_with_statements():
    statement1 = Concat(Column("column1"), "value")
    statement2 = Concat(Column("column2"), "value")
    in_condition = In((statement1, statement2), [(1, 2), (3, 4)])
    assert str(in_condition) == "(CONCAT(`column1`, %s), CONCAT(`column2`, %s)) IN ((%s, %s), (%s, %s))"
    assert in_condition.args == ["value", "value", 1, 2, 3, 4]


def test_in_with_args():
    statement1 = Concat(Column("column3"), "foo")
    statement2 = Concat(Column("column4"), "bar")
    in_condition = In("column1", [statement1, statement2])
    assert str(in_condition) == "`column1` IN (CONCAT(`column3`, %s), CONCAT(`column4`, %s))"
    assert in_condition.args == ["foo", "bar"]


def test_in_tuple_columns_with_args():
    statement1 = Concat(Column("column3"), "foo")
    statement2 = Concat(Column("column4"), "bar")
    in_condition = In(("column1", "column2"), [(statement1, statement2), (statement1, statement2)])
    assert (
        str(in_condition)
        == "(`column1`, `column2`) IN ((CONCAT(`column3`, %s), CONCAT(`column4`, %s)), (CONCAT(`column3`, %s), CONCAT(`column4`, %s)))"
    )
    assert in_condition.args == ["foo", "bar", "foo", "bar"]


def test_in_with_none_in_args():
    in_condition = In("column1", [1, 2, 3, None])
    assert str(in_condition) == "(`column1` IN (%s, %s, %s) OR `column1` IS NULL)"
    assert in_condition.args == [1, 2, 3]


def test_in_with_statement_and_none_in_args():
    in_condition = In(Concat(Column("column1"), "foo"), [1, 2, 3, None])
    assert str(in_condition) == "(CONCAT(`column1`, %s) IN (%s, %s, %s) OR CONCAT(`column1`, %s) IS NULL)"
    assert in_condition.args == ["foo", 1, 2, 3, "foo"]


def test_in_only_none_as_args():
    in_condition = In("column1", [None])
    assert str(in_condition) == "`column1` IS NULL"
    assert in_condition.args == []


def test_in_with_statement_and_only_none_as_args():
    in_condition = In(Concat(Column("column1"), "foo"), [None])
    assert str(in_condition) == "CONCAT(`column1`, %s) IS NULL"
    assert in_condition.args == ["foo"]


def test_empty_in():
    in_condition = In("column1", [])
    assert str(in_condition) == "FALSE"
    assert in_condition.args == []


def test_empty_in_tuple_columns():
    in_condition = In(("column1", "column2"), [])
    assert str(in_condition) == "FALSE"
    assert in_condition.args == []


def test_empty_in_with_statement():
    in_condition = In(Concat(Column("column1"), "foo"), [])
    assert str(in_condition) == "FALSE"
    assert in_condition.args == []


def test_empty_in_tuple_columns_with_statement():
    in_condition = In((Concat(Column("column1"), "foo"), Concat(Column("column2"), "bar")), [])
    assert str(in_condition) == "FALSE"
    assert in_condition.args == []
