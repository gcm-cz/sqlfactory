from sqlfactory import Eq, Value
from sqlfactory.entities import BinaryExpression, Column


def test_binary_expression():
    exp = BinaryExpression(1, "<", Column("b"))
    assert str(exp) == "(%s < `b`)"
    assert exp.args == [1]


def test_binary_expression_with_column():
    exp = BinaryExpression(Column("a"), "<", Column("b"))
    assert str(exp) == "(`a` < `b`)"
    assert exp.args == []


def test_eq_with_explicit_cast():
    exp = Eq(Value(1), Column("a"))
    assert str(exp) == "%s = `a`"
    assert exp.args == [1]
