from sqlfactory import Raw, Column
from sqlfactory.func.control import IfNull


def test_raw():
    raw1 = Raw("hello")
    assert str(raw1) == "hello"
    assert repr(raw1) == "hello"
    assert raw1.args == []

    raw2 = Raw("hello(%s)", "xyz")
    assert str(raw2) == "hello(%s)"
    assert repr(raw2) == "hello(%s) with arguments ['xyz']"
    assert raw2.args == ["xyz"]


def test_uniqueness():
    raw1 = Raw("hello")
    raw2 = Raw("hello")
    assert raw1 == raw2
    assert hash(raw1) == hash(raw2)


def test_uniqueness_of_funcs():
    assert IfNull("a", "b") == IfNull("a", "b")


def test_not_equal_with_string():
    assert Raw("abc") != "abc"
