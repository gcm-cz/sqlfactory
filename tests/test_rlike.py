import pytest

from sqlfactory import Column
from sqlfactory.condition.rlike import RLike, NotRLike
from sqlfactory.func.str import Concat


def test_rlike():
    rlike_condition = RLike("`column1`", ".*pattern^d")
    assert str(rlike_condition) == "`column1` RLIKE %s"
    assert rlike_condition.args == [".*pattern^d"]
    assert bool(rlike_condition) is True


def test_rlike_negative():
    rlike_condition = RLike("`column1`", ".wpattern^W", negative=True)
    assert str(rlike_condition) == "`column1` NOT RLIKE %s"
    assert rlike_condition.args == [".wpattern^W"]


def test_rlike_with_statements():
    statement1 = Concat(Column("column1"), "value")
    rlike_condition = RLike(statement1, ".*pattern.*")
    assert str(rlike_condition) == "CONCAT(`column1`, %s) RLIKE %s"
    assert rlike_condition.args == ["value", ".*pattern.*"]


def test_rlike_with_statements_as_arg():
    statement1 = Concat(".d", Column("column1"), "value[0-9]{3}")
    like_condition = RLike("column1", statement1)
    assert str(like_condition) == "`column1` RLIKE CONCAT(%s, `column1`, %s)"
    assert like_condition.args == [".d", "value[0-9]{3}"]


def test_not_rlike():
    not_rlike_condition = NotRLike("`column1`", "[a-z]pattern.*")
    assert str(not_rlike_condition) == "`column1` NOT RLIKE %s"
    assert not_rlike_condition.args == ["[a-z]pattern.*"]
    assert bool(not_rlike_condition) is True

def test_invert_rlike_condition():
    rlike_condition = RLike("`column1`", ".*pattern.*")
    assert str(~rlike_condition) == "`column1` NOT RLIKE %s"
    assert rlike_condition.args == [".*pattern.*"]

def test_double_negation():
    not_rlike_condition = NotRLike("`column1`", ".*pattern.*")
    with pytest.raises(TypeError, match="Cannot use ~ operator on NotRLike conditions"):
        ~not_rlike_condition
