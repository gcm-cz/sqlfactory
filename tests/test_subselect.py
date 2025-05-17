import pytest

from sqlfactory import Aliased, Column, Eq, In, Join, Select
from sqlfactory.condition.base import And
from sqlfactory.condition.in_condition import NotIn
from sqlfactory.entities import Table
from sqlfactory.func.agg import Count, Sum
from sqlfactory.mixins.join import LeftJoin
from sqlfactory.select.aliased import SelectColumn


def test_select_from_select():
    sel = Select(
        "package.id",
        "t1.total_price",
        table=[
            "package",
            Aliased(
                Select(
                    "product.package_id",
                    Aliased(Sum("price"), alias="total_price"),
                    table="product",
                    where=Eq("product.is_default", 2),
                    group_by=("product.package_id",),
                ),
                alias="t1",
            ),
        ],
        where=Eq("package.id", 1) & Eq("t1.package_id", Column("package.id")),
    )

    assert (
        str(sel)
        == "SELECT `package`.`id`, `t1`.`total_price` FROM `package`, (SELECT `product`.`package_id`, SUM(`price`) AS `total_price` FROM `product` WHERE `product`.`is_default` = %s GROUP BY `product`.`package_id`) AS `t1` WHERE (`package`.`id` = %s AND `t1`.`package_id` = `package`.`id`)"
    )
    assert sel.args == [2, 1]


def test_select_in_join():
    sel = Select(
        "package.id",
        "t1.total_price",
        table="package",
        join=[
            Join(
                Select(
                    "product.package_id",
                    Aliased(Sum("price"), alias="total_price"),
                    table="product",
                    where=Eq("product.is_default", 2),
                    group_by=("product.package_id",),
                ),
                alias="t1",
                on=Eq("t1.package_id", Column("package.id")),
            )
        ],
        where=Eq("package.id", 1),
    )

    assert (
        str(sel)
        == "SELECT `package`.`id`, `t1`.`total_price` FROM `package` JOIN (SELECT `product`.`package_id`, SUM(`price`) AS `total_price` FROM `product` WHERE `product`.`is_default` = %s GROUP BY `product`.`package_id`) AS `t1` ON `t1`.`package_id` = `package`.`id` WHERE `package`.`id` = %s"
    )
    assert sel.args == [2, 1]


def test_select_from_select_with_join():
    ids = [1, 2, 3]
    sel = Select(
        SelectColumn("filtered_product.product_id"),
        table=Aliased(
            Select(
                SelectColumn("product_tag.product_id"),
                table=Table("product"),
                group_by=["product_tag.product_id"],
                having=Eq(Count("product_tag.tag_id", distinct=True), len(ids)),
                where=In("product_tag.tag_id", ids),
            ),
            alias="filtered_product",
        ),
        join=[
            LeftJoin(
                table="product_tag",
                alias="extra_product",
                on=And(
                    Eq("filtered_product.product_id", Column("extra_product.product_id")),
                    NotIn("extra_product.tag_id", ids),
                ),
            ),
        ],
        where=Eq("extra_product.product_id", None),
    )
    assert (
        str(sel)
        == "SELECT `filtered_product`.`product_id` FROM (SELECT `product_tag`.`product_id` FROM `product` WHERE `product_tag`.`tag_id` IN (%s, %s, %s) GROUP BY `product_tag`.`product_id` HAVING COUNT(DISTINCT `product_tag`.`tag_id`) = %s) AS `filtered_product` LEFT JOIN `product_tag` AS `extra_product` ON (`filtered_product`.`product_id` = `extra_product`.`product_id` AND `extra_product`.`tag_id` NOT IN (%s, %s, %s)) WHERE `extra_product`.`product_id` IS %s"
    )
    assert sel.args == [1, 2, 3, 3, 1, 2, 3, None]


def test_select_in_join_without_alias():
    with pytest.raises(AttributeError, match="When joining a subselect, alias must be specified."):
        Join(Select(table="test"))


def test_select_in():
    cond = In("package.id", Select("product.package_id", table="product", where=Eq("product.is_default", 2)))

    assert str(cond) == "`package`.`id` IN (SELECT `product`.`package_id` FROM `product` WHERE `product`.`is_default` = %s)"
    assert cond.args == [2]


def test_select_in_multiple():
    cond = In(
        ("package.id", "package.is_default"),
        Select("product.package_id", "product.is_default", table="product", where=Eq("product.is_default", 2)),
        negative=True,
    )

    assert (
        str(cond)
        == "(`package`.`id`, `package`.`is_default`) NOT IN (SELECT `product`.`package_id`, `product`.`is_default` FROM `product` WHERE `product`.`is_default` = %s)"
    )
    assert cond.args == [2]
