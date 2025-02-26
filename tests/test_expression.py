from sqlfactory.entities import BinaryExpression, Column


def test_binary_expression():
    exp = BinaryExpression(1, "<", Column("b"))
    assert str(exp) == "(%s < `b`)"
    assert exp.args == [1]
