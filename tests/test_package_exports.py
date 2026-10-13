"""The top-level `sqlfactory` package re-exports the commonly used builders, and every module imports on its own."""

import importlib
import pkgutil
import subprocess
import sys
from importlib import resources

import pytest

import sqlfactory
from sqlfactory.condition import is_null
from sqlfactory.func import agg, base, cast, control, datetime, str as str_func
from sqlfactory.mixins import limit
from sqlfactory.condition import exists
from sqlfactory import statement


def test_all_names_resolve_and_are_unique():
    assert len(sqlfactory.__all__) == len(set(sqlfactory.__all__))

    for name in sqlfactory.__all__:
        assert hasattr(sqlfactory, name), name


@pytest.mark.parametrize(
    ("name", "home"),
    [
        # conditions
        ("Exists", exists),
        ("NotExists", exists),
        ("IsNull", is_null),
        ("IsNotNull", is_null),
        # building blocks
        ("Limit", limit),
        ("Value", statement),
        ("Raw", statement),
        ("Function", base),
        # aggregates
        ("Avg", agg),
        ("Count", agg),
        ("GroupConcat", agg),
        ("Max", agg),
        ("Min", agg),
        ("Sum", agg),
        # type conversion
        ("Cast", cast),
        ("CastType", cast),
        ("Convert", cast),
        # control flow
        ("Case", control),
        ("Coalesce", control),
        ("If", control),
        ("IfNull", control),
        ("NullIf", control),
        # strings and dates
        ("Concat", str_func),
        ("Lower", str_func),
        ("Upper", str_func),
        ("Now", datetime),
    ],
)
def test_common_builders_are_reexported(name, home):
    assert name in sqlfactory.__all__
    assert getattr(sqlfactory, name) is getattr(home, name)


def test_top_level_import_works_for_common_builders():
    from sqlfactory import Cast, CastType, Column, Count, Select

    assert str(Select(Count("id"), Cast(Column("a") - Column("b"), CastType.SIGNED), table="t")) == (
        "SELECT COUNT(`id`), CAST((`a` - `b`) AS SIGNED) FROM `t`"
    )


def _all_modules() -> list[str]:
    return ["sqlfactory"] + [m.name for m in pkgutil.walk_packages(sqlfactory.__path__, prefix="sqlfactory.")]


@pytest.mark.parametrize("module", _all_modules())
def test_module_imports_first_without_cycle(module):
    """Importing any module as the very first one (fresh interpreter) must not hit an import cycle."""
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-c", f"import {module}"], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr
    importlib.import_module(module)


def test_py_typed_marker_ships_with_package():
    assert resources.files("sqlfactory").joinpath("py.typed").is_file()
