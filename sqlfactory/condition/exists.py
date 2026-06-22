"""EXISTS condition, used for checking whether a subquery returns any rows."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, NoReturn

from sqlfactory.condition.base import ConditionBase

if TYPE_CHECKING:
    from sqlfactory.select.cte import With  # pragma: no cover
    from sqlfactory.select.select import Select  # pragma: no cover


class Exists(ConditionBase):
    """
    `EXISTS` condition for checking whether a subquery returns at least one row.

    Usage:

    ```python
    # EXISTS (SELECT `id` FROM `orders` WHERE `orders`.`user_id` = `users`.`id`)
    Exists(Select("id", table="orders", where=Eq("orders.user_id", Column("users.id"))))
    ```

    Negated using `negative=True` or the dedicated `NotExists` class:

    ```python
    # NOT EXISTS (SELECT `id` FROM `orders`)
    Exists(Select("id", table="orders"), negative=True)
    ```
    """

    def __init__(self, select: Select | With, *, negative: bool = False) -> None:
        """
        :param select: Subquery to check for existence of rows.
        :param negative: Whether to perform negative comparison (NOT EXISTS).
        """
        super().__init__()

        self._select = select
        self._negative = negative

    def __str__(self) -> str:
        return f"{'NOT ' if self._negative else ''}EXISTS ({self._select!s})"

    @property
    def args(self) -> list[Any]:
        return list(self._select.args)

    def __bool__(self) -> bool:
        return True

    def __invert__(self) -> "Exists":
        """
        Allows using the `~` operator to negate the EXISTS condition, converting it to a NOT EXISTS condition.
        Note: Cannot use ~ operator on NotExists conditions.
        """
        return NotExists(self._select)


class NotExists(Exists):
    """
    `NOT EXISTS` condition for checking whether a subquery returns no rows.

    This is a dedicated class for NOT EXISTS conditions, which is equivalent to using Exists with negative=True.
    It provides a more intuitive API for NOT EXISTS conditions.

    Usage:

    ```python
    # NOT EXISTS (SELECT `id` FROM `orders` WHERE `orders`.`user_id` = `users`.`id`)
    NotExists(Select("id", table="orders", where=Eq("orders.user_id", Column("users.id"))))
    ```
    """

    def __init__(self, select: Select | With) -> None:
        """
        :param select: Subquery to check for absence of rows.
        """
        super().__init__(select, negative=True)

    def __invert__(self) -> NoReturn:
        """
        Allows using the `~` operator to negate the NOT EXISTS condition, converting it to an EXISTS condition.
        Note: Cannot use ~ operator on NotExists conditions.
        """
        raise TypeError("Cannot use ~ operator on NotExists conditions")
