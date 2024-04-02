"""
Test suite for examples from the README.
"""

from dataclasses import dataclass
from typing import Any

from sqlfactory import SELECT, Table, Select, And, Eq, In, Insert, INSERT, Update, SelectColumn, Column, Direction


def test_select_books():
    sql = "SELECT `column1`, `column2`, `column3` FROM `books` WHERE (`column1` = %s AND `column2` IN (%s, %s, %s))"
    sql_with_table = "SELECT `books`.`column1`, `books`.`column2`, `books`.`column3` FROM `books` WHERE (`books`.`column1` = %s AND `books`.`column2` IN (%s, %s, %s))"
    args = ["value", 1, 2, 3]

    # The most naive and most explicit approach
    case1 = Select("column1", "column2", "column3", table="books", where=And(Eq("column1", "value"), In("column2", [1, 2, 3])))
    assert str(case1) == sql
    assert case1.args == args

    # A little more like a SQL:
    case2 = SELECT("column1", "column2", "column3", table="books") \
        .WHERE(Eq("column1", "value") & In("column2", [1, 2, 3]))
    assert str(case2) == sql
    assert case2.args == args

    # A little more like a python, but still SQL:
    books = Table("books")
    case3 = SELECT(books.column1, books.column2, books.column3, table=books) \
        .WHERE((books.column1 == "value") & In(books.column2, [1, 2, 3]))

    assert str(case3) == sql_with_table
    assert case3.args == args


def test_insert_books():
    sql = "INSERT INTO `books` (`column1`, `column2`, `column3`) VALUES (%s, %s, %s), (%s, %s, %s)"
    sql_with_table = "INSERT INTO `books` (`books`.`column1`, `books`.`column2`, `books`.`column3`) VALUES (%s, %s, %s), (%s, %s, %s)"
    args = ["value1", "value2", "value3", "value4", "value5", "value6"]

    case1 = Insert.into("books")("column1", "column2", "column3").VALUES(
        ("value1", "value2", "value3"),
        ("value4", "value5", "value6")
    )
    assert str(case1) == sql
    assert case1.args == args

    # Of course, you can use Table object as well
    books = Table("books")
    case2 = INSERT.INTO(books)(books.column1, books.column2, books.column3).VALUES(
        ("value1", "value2", "value3"),
        ("value4", "value5", "value6")
    )
    assert str(case2) == sql_with_table
    assert case2.args == args

    # The INTO is not necessary, you can call INSERT constructor directly:
    case3 = INSERT("books")("column1", "column2", "column3").VALUES(
        ("value1", "value2", "value3"),
        ("value4", "value5", "value6")
    )

    assert str(case3) == sql
    assert case3.args == args


def test_update_books():
    sql = "UPDATE `books` SET `column1` = %s, `column2` = %s WHERE `column3` = %s"
    sql_with_table = "UPDATE `books` SET `books`.`column1` = %s, `books`.`column2` = %s WHERE `books`.`column3` = %s"
    args = ["value1", "value2", "value3"]

    case1 = Update("books") \
        .set("column1", "value1") \
        .set("column2", "value2") \
        .where(Eq("column3", "value3"))
    assert str(case1) == sql
    assert case1.args == args

    # Of course, you can use Table object as well
    books = Table("books")
    case2 = Update(books) \
        .set(books.column1, "value1") \
        .set(books.column2, "value2") \
        .where(books.column3 == "value3")
    assert str(case2) == sql_with_table
    assert case2.args == args


class Cursor:
    def execute(self, query: str, args: tuple):
        return query, args


@dataclass
class Book:
    id: int
    title: str
    author: str
    year: str


def select_books_by_authors(c: Cursor, authors: list[str], book_properties: list[str] = None, offset: int = 0,
                            limit: int = 10):
    """
    Returns books written by specific authors. Returns list of books paginated by specified offset and limit, ordered
    by book title and author name.
    """

    if book_properties is None:
        book_properties = {"title", "author", "year"}

    property_column = {
        "title": SelectColumn("books.title", alias="title"),
        "author": SelectColumn("authors.name", alias="author"),
        "year": SelectColumn("books.year", alias="year")
    }

    select = (
        # Map dataclass attributes to SQL columns by using mapping table.
        Select(*[property_column[book_property] for book_property in book_properties], table="books")

        # As Eq expects firt argument to be column and second argument to be value, we need to provide hint, that
        # authors.id is a column, not a value.
        .join("authors", on=Eq("books.author", Column("authors.id")))

        # In is intelligent, it will work even when authors list is empty (will produce False, which in turn will
        # return empty result, as no author has been matched).
        .where(In("authors.name", authors))

        # Multiple ORDER BY columns is supported
        .order_by("title", Direction.ASC)
        .order_by("authors.name", Direction.ASC)

        # Limit and offset are supported as well
        .limit(offset, limit)
    )

    return select.execute(c)


@dataclass
class BookUpdate:
    id: int
    title: str = None
    author: str = None
    year: int = None


def update_books(c: Cursor, books: list[BookUpdate]) -> list[tuple[str, tuple[Any]]]:
    """Update multiple books at once. Attributes that has None value won't be modified at all."""
    out = []

    for book in books:
        update = Update("books", where=Eq("id", book.id))

        if book.title is not None:
            update.set("title", book.title)
        if book.author is not None:
            update.set("author", book.author)
        if book.year is not None:
            update.set("year", book.year)

        # It can even be done as one-liner, but it gets ugly pretty quickly, so it's not recommended for readability:
        # list(map(update.set, [(attr, getattr(book, attr)) for attr in ["title", "author", "year"] if getattr(book, attr) is not None]))

        # Will be executed only if any of the columns should be updated.
        out.append(update.execute(c))

    return out


def test_select_books_by_authors():
    c = Cursor()
    sql, args = select_books_by_authors(c, ["John Doe"], ["title", "author"])
    assert sql == "SELECT `books`.`title` AS `title`, `authors`.`name` AS `author` FROM `books` JOIN `authors` ON `books`.`author` = `authors`.`id` WHERE `authors`.`name` IN (%s) ORDER BY `title` ASC, `authors`.`name` ASC LIMIT %s, %s"
    assert args == ("John Doe", 0, 10)


def test_update_books_func():
    c = Cursor()
    row1, row2 = update_books(c, [BookUpdate(1, title="New Title"), BookUpdate(2, author="New Author")])

    assert row1[0] == "UPDATE `books` SET `title` = %s WHERE `id` = %s"
    assert row1[1] == ("New Title", 1)

    assert row2[0] == "UPDATE `books` SET `author` = %s WHERE `id` = %s"
    assert row2[1] == ("New Author", 2)
