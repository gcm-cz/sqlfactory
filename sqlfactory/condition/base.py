"""Base classes to implement SQL conditions."""

from __future__ import annotations

from abc import ABC
from collections.abc import Iterable
from typing import Any

from ..statement import StatementWithArgs, ConditionalStatement, Statement
StatementOrColumn = str | Statement


class ConditionBase(StatementWithArgs, ConditionalStatement, ABC):
    """
    Generic condition interface, that can be chained with other conditions using & or | operators. All condition
    classes should inherit from this one, as there are checks through the library for instances of this class.
    """
    def __and__(self, other: ConditionBase) -> And:
        if isinstance(self, And):
            out = self
        else:
            out = And(self)

        if isinstance(other, And):
            out.extend(other.sub_conditions)
        else:
            out.append(other)

        return out

    def __or__(self, other: ConditionBase) -> Or:
        if isinstance(self, Or):
            out = self
        else:
            out = Or(self)

        if isinstance(other, Or):
            out.extend(other.sub_conditions)
        else:
            out.append(other)

        return out


class Condition(ConditionBase):
    """
    Generic RAW condition with optional arguments.
    """

    def __init__(self, condition: str, *args: Any):
        """
        :param condition: Condition (such as "`column` = %s")
        :param args: Optional arguments used in condition.
        """
        self.condition = condition
        self._args = list(args)

    def __str__(self):
        return self.condition

    @property
    def args(self) -> list[Any]:
        return self._args

    def __bool__(self) -> bool:
        return bool(self.condition)


class CompoundCondition(ConditionBase):
    """
    Base class for joining multiple conditions together using specified operator. As there are only two operators
    (AND and OR), this class is not meant to be used directly, but rather through And and Or classes.
    """
    def __init__(self, operator: str, *conditions: ConditionBase | str):
        """
        :param operator: Which operator to use for joining specific conditions.
        :param conditions: Conditions to join using given operator.
        """
        self.operator = operator
        self._sub_conditions: list[ConditionBase] = [
            Condition(condition) if isinstance(condition, str) else condition
            for condition in conditions
        ]

    def append(self, condition: ConditionBase | str, *args: Any) -> CompoundCondition:
        """
        Append another condition to be joined.
        :param condition: Condition to append
        :param args: Optional arguments for given condition, if condition is passed as string.
        """
        if isinstance(condition, str):
            condition = Condition(condition, *args)
        elif args:
            raise AttributeError("*args can be used only for str conditions.")

        self._sub_conditions.append(condition)
        return self

    def extend(self, conditions: Iterable[ConditionBase]):
        """
        Extend condition with list of conditions.
        :param conditions: Conditions to extend this condition with
        """
        self._sub_conditions.extend(conditions)
        return self

    @property
    def sub_conditions(self) -> list[ConditionBase]:
        """
        Return filtered list of conditions, which are valid.
        """
        return list(filter(bool, self._sub_conditions))

    def __str__(self):
        """
        Create SQL statement of joined conditions.
        """
        sub_conditions = list(map(str, self.sub_conditions))
        if sub_conditions:
            return "(" + f" {self.operator} ".join(sub_conditions) + ")" if len(sub_conditions) > 1 else sub_conditions[0]

        return "TRUE"

    @property
    def args(self) -> list[Any]:
        """
        Return arguments from all sub conditions in correct order.
        """
        out = []

        for cond in self.sub_conditions:
            out.extend(cond.args)

        return out

    def __bool__(self):
        """
        Is this compound condition non-empty?
        """
        return bool(self.sub_conditions)


class And(CompoundCondition):
    """
    Compound condition joined by AND.

    Usage:
        >>> And(Equals("id", 1), Equals("name", "hello"))
        >>> "(`id` = 1 AND `name` = 'hello')"

    Of course, condition can be another compound condition:
        >>> And(Equals("id", 1), Or(Equals("name", "hello"), Equals("name", "world")))
        >>> "(`id` = 1 AND (`name` = 'hello' OR `name` = 'world'))"
    """
    def __init__(self, *conditions: ConditionBase | str):
        super().__init__("AND", *conditions)


class Or(CompoundCondition):
    """
    Compound condition joined by OR.

    Usage:
        >>> Or(Equals("id", 1), Equals("name", "hello"))
        >>> "(`id` = 1 OR `name` = 'hello')"
    """
    def __init__(self, *conditions: ConditionBase | str):
        super().__init__("OR", *conditions)
