from collections.abc import Iterable

import pytest
from typing import Any

from sqlfactory import Select, Eq, Insert


class DbDriverWithExecuteTuple():
    def execute(self, query: str, args: tuple[Any]) -> tuple[str, Iterable[Any]]:
        return query, args


class DbDriverWithExecuteArgs():
    def execute(self, query: str, *args: Any) -> tuple[str, Iterable[Any]]:
        return query, args


class DbDriverWithQueryTuple():
    def query(self, query: str, args: tuple[Any]) -> tuple[str, Iterable[Any]]:
        return query, args


class DbDriverWithQueryArgs():
    def query(self, query: str, *args: Any) -> tuple[str, Iterable[Any]]:
        return query, args


class AsyncDbDriverWithExecuteTuple():
    async def execute(self, query: str, args: tuple[Any]) -> tuple[str, Iterable[Any]]:
        return query, args


class AsyncDbDriverWithExecuteArgs():
    async def execute(self, query: str, *args: Any) -> tuple[str, Iterable[Any]]:
        return query, args


class AsyncDbDriverWithQueryTuple():
    async def query(self, query: str, args: tuple[Any]) -> tuple[str, Iterable[Any]]:
        return query, args


class AsyncDbDriverWithQueryArgs():
    async def query(self, query: str, *args: Any) -> tuple[str, Iterable[Any]]:
        return query, args


class InvalidDbDriver():
    pass


def test_execute_tuple():
    sql, args = Select("abc", table="table", where=Eq("id", 1)).execute(DbDriverWithExecuteTuple())
    assert sql == "SELECT `abc` FROM `table` WHERE `id` = %s"
    assert args == (1, )


def test_execute_args():
    sql, args = Select("abc", table="table", where=Eq("id", 1)).execute(DbDriverWithExecuteArgs())
    assert sql == "SELECT `abc` FROM `table` WHERE `id` = %s"
    assert args == (1, )


def test_query_tuple():
    sql, args = Select("abc", table="table", where=Eq("id", 1)).execute(DbDriverWithQueryTuple())
    assert sql == "SELECT `abc` FROM `table` WHERE `id` = %s"
    assert args == (1, )


def test_query_args():
    sql, args = Select("abc", table="table", where=Eq("id", 1)).execute(DbDriverWithQueryArgs())
    assert sql == "SELECT `abc` FROM `table` WHERE `id` = %s"
    assert args == (1, )


@pytest.mark.asyncio
async def test_async_execute_tuple():
    sql, args = await Select("abc", table="table", where=Eq("id", 1)).execute(AsyncDbDriverWithExecuteTuple())
    assert sql == "SELECT `abc` FROM `table` WHERE `id` = %s"
    assert args == (1, )


@pytest.mark.asyncio
async def test_async_execute_args():
    sql, args = await Select("abc", table="table", where=Eq("id", 1)).execute(AsyncDbDriverWithExecuteArgs())
    assert sql == "SELECT `abc` FROM `table` WHERE `id` = %s"
    assert args == (1, )


@pytest.mark.asyncio
async def test_async_query_tuple():
    sql, args = await Select("abc", table="table", where=Eq("id", 1)).execute(AsyncDbDriverWithQueryTuple())
    assert sql == "SELECT `abc` FROM `table` WHERE `id` = %s"
    assert args == (1, )


@pytest.mark.asyncio
async def test_async_query_args():
    sql, args = await Select("abc", table="table", where=Eq("id", 1)).execute(AsyncDbDriverWithQueryArgs())
    assert sql == "SELECT `abc` FROM `table` WHERE `id` = %s"
    assert args == (1, )


def test_invalid_db_driver():
    with pytest.raises(AttributeError, match=r"trx must define query\(\) or execute\(\) method."):
        Select("abc", table="table", where=Eq("id", 1)).execute(InvalidDbDriver())


def test_conditional_execute_does_not_execute():
    # Empty insert does not execute
    assert Insert("table")("a", "b").values().execute(DbDriverWithExecuteTuple()) is False


def test_conditional_execute_executes():
    # Non-empty insert executes
    assert Insert("table")("a", "b").values((1, 2)).execute(DbDriverWithExecuteTuple()) == (
        "INSERT INTO `table` (`a`, `b`) VALUES (%s, %s)",
        (1, 2)
    )


@pytest.mark.asyncio
async def test_async_conditional_execute_does_not_execute():
    # Empty insert does not execute
    assert await Insert("table")("a", "b").values().execute(AsyncDbDriverWithExecuteTuple()) is False


@pytest.mark.asyncio
async def test_async_conditional_execute_executes():
    # Non-empty insert executes
    assert await Insert("table")("a", "b").values((1, 2)).execute(AsyncDbDriverWithExecuteTuple()) == (
        "INSERT INTO `table` (`a`, `b`) VALUES (%s, %s)",
        (1, 2)
    )
