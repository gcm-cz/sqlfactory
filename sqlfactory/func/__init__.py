"""
SQL functions to be used in the statements. Includes functions known to MariaDB 10.11, additional functions can be defined
on demand or in your code.
"""

# pylint: disable=redefined-builtin
from sqlfactory.func import (
    agg,
    base,
    cast,
    control,
    datetime,
    enc,
    geometry,
    info,
    json,
    misc,
    numeric,
    spatial,
    str,  # noqa: A004
    window,
)

__all__ = [
    "agg",
    "base",
    "cast",
    "control",
    "datetime",
    "enc",
    "geometry",
    "info",
    "json",
    "misc",
    "numeric",
    "spatial",
    "str",
    "window",
]
