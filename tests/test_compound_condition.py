import pytest

from sqlfactory.condition.base import And, Condition, Or


def test_and():
    and_condition = And(Condition("`column1` = %s", 5), Condition("`column2` = %s", 10))
    assert str(and_condition) == "(`column1` = %s AND `column2` = %s)"
    assert and_condition.args == [5, 10]


def test_or():
    or_condition = Or(Condition("`column1` = %s", 5), Condition("`column2` = %s", 10))
    assert str(or_condition) == "(`column1` = %s OR `column2` = %s)"
    assert or_condition.args == [5, 10]


def test_and_operator():
    condition1 = Condition("`column1` = %s", 5)
    condition2 = Condition("`column2` = %s", 10)
    and_condition = condition1 & condition2
    assert str(and_condition) == "(`column1` = %s AND `column2` = %s)"
    assert and_condition.args == [5, 10]


def test_or_operator():
    condition1 = Condition("`column1` = %s", 5)
    condition2 = Condition("`column2` = %s", 10)
    or_condition = condition1 | condition2
    assert str(or_condition) == "(`column1` = %s OR `column2` = %s)"
    assert or_condition.args == [5, 10]


def test_multiple_and_or():
    condition1 = Condition("`column1` = %s", 5)
    condition2 = Condition("`column2` = %s", 10)
    condition3 = Condition("`column3` = %s", 15)
    condition4 = Condition("`column4` = %s", 20)

    combined_condition = (condition1 & condition2) | (condition3 & condition4)
    assert str(combined_condition) == "((`column1` = %s AND `column2` = %s) OR (`column3` = %s AND `column4` = %s))"
    assert combined_condition.args == [5, 10, 15, 20]


def test_empty_and_or():
    empty_and = And()
    assert str(empty_and) == "TRUE"
    assert empty_and.args == []

    empty_or = Or()
    assert str(empty_or) == "FALSE"
    assert empty_or.args == []


def test_combinations():
    condition1 = Condition("`column1` = %s", 5)
    condition2 = Condition("`column2` = %s", 10)
    condition3 = Condition("`column3` = %s", 15)
    condition4 = Condition("`column4` = %s", 20)

    combined_condition = condition1 & Or(condition2, condition3 & condition4)
    assert str(combined_condition) == "(`column1` = %s AND (`column2` = %s OR (`column3` = %s AND `column4` = %s)))"
    assert combined_condition.args == [5, 10, 15, 20]


def test_extend_and_or():
    condition1 = Condition("`column1` = %s", 5)
    condition2 = Condition("`column2` = %s", 10)
    condition3 = Condition("`column3` = %s", 15)
    condition4 = Condition("`column4` = %s", 20)

    combined_conditions_and = condition1 & condition2 & (condition3 & condition4)
    assert str(combined_conditions_and) == "(`column1` = %s AND `column2` = %s AND `column3` = %s AND `column4` = %s)"

    combined_conditions_or = condition1 | condition2 | (condition3 | condition4)
    assert str(combined_conditions_or) == "(`column1` = %s OR `column2` = %s OR `column3` = %s OR `column4` = %s)"


def test_raw_condition():
    condition = And()
    condition.append("`column1` = %s", 5)
    condition.append("`column2` = %s", 10)

    assert str(condition) == "(`column1` = %s AND `column2` = %s)"
    assert condition.args == [5, 10]

    with pytest.raises(AttributeError):
        condition.append(Condition("`column1` = %s"), 10)
