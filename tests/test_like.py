import pytest

from sqlfactory import Column
from sqlfactory.condition.like import Like, NotLike
from sqlfactory.func.str import Concat


def test_like():
    like_condition = Like("`column1`", "%pattern%")
    assert str(like_condition) == "`column1` LIKE %s"
    assert like_condition.args == ["%pattern%"]
    assert bool(like_condition) is True


def test_like_negative():
    like_condition = Like("`column1`", "%pattern%", negative=True)
    assert str(like_condition) == "`column1` NOT LIKE %s"
    assert like_condition.args == ["%pattern%"]


def test_like_with_statements():
    statement1 = Concat(Column("column1"), "value")
    like_condition = Like(statement1, "%pattern%")
    assert str(like_condition) == "CONCAT(`column1`, %s) LIKE %s"
    assert like_condition.args == ["value", "%pattern%"]


def test_like_with_statements_as_arg():
    statement1 = Concat("%", Column("column1"), "value%")
    like_condition = Like("column1", statement1)
    assert str(like_condition) == "`column1` LIKE CONCAT(%s, `column1`, %s)"
    assert like_condition.args == ["%", "value%"]


def test_like_escape():
    assert Like.escape("a%b_c") == "a%%b__c"
    assert Like.escape("a%%b__c") == "a%%%%b____c"

def test_not_like():
    not_like_condition = NotLike("`column1`", "%pattern%")
    assert str(not_like_condition) == "`column1` NOT LIKE %s"
    assert not_like_condition.args == ["%pattern%"]
    assert bool(not_like_condition) is True

def test_double_negation():
    not_like_condition = NotLike("`column1`", "%pattern%")
    with pytest.raises(TypeError, match="Cannot use ~ operator on NotLike conditions"):
        ~not_like_condition
