import pytest

from sqlfactory import Column, Eq, Exists, NotExists, Select


def test_exists():
    cond = Exists(Select("id", table="orders", where=Eq("orders.user_id", Column("users.id"))))
    assert str(cond) == "EXISTS (SELECT `id` FROM `orders` WHERE `orders`.`user_id` = `users`.`id`)"
    assert cond.args == []


def test_exists_with_args():
    cond = Exists(Select("id", table="orders", where=Eq("orders.status", "paid")))
    assert str(cond) == "EXISTS (SELECT `id` FROM `orders` WHERE `orders`.`status` = %s)"
    assert cond.args == ["paid"]


def test_exists_negative():
    cond = Exists(Select("id", table="orders"), negative=True)
    assert str(cond) == "NOT EXISTS (SELECT `id` FROM `orders`)"
    assert cond.args == []


def test_not_exists():
    cond = NotExists(Select("id", table="orders", where=Eq("orders.status", "paid")))
    assert str(cond) == "NOT EXISTS (SELECT `id` FROM `orders` WHERE `orders`.`status` = %s)"
    assert cond.args == ["paid"]


def test_exists_is_truthy():
    assert bool(Exists(Select("id", table="orders"))) is True


def test_invert_exists():
    cond = Exists(Select("id", table="orders"))
    assert str(~cond) == "NOT EXISTS (SELECT `id` FROM `orders`)"


def test_invert_not_exists_raises():
    cond = NotExists(Select("id", table="orders"))
    with pytest.raises(TypeError, match="Cannot use ~ operator on NotExists conditions"):
        ~cond


def test_exists_in_select_where():
    sel = Select("id", table="users").where(
        Exists(Select("id", table="orders", where=Eq("orders.user_id", Column("users.id"))))
    )
    assert (
        str(sel)
        == "SELECT `id` FROM `users` WHERE EXISTS (SELECT `id` FROM `orders` WHERE `orders`.`user_id` = `users`.`id`)"
    )
    assert sel.args == []

