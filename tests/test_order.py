from sqlbuilder import Order, Direction
from sqlbuilder.func.control import IfNull


def test_empty_order():
    assert str(Order()) == ""
    assert Order().args == []


def test_order_with_args():
    order = Order([(IfNull("a", "b"), Direction.ASC)])
    assert str(order) == "ORDER BY IFNULL(%s, %s) ASC"
    assert order.args == ["a", "b"]
