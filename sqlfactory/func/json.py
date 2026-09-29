# noqa: A005

"""
JSON functions (https://mariadb.com/kb/en/json-functions/).

`JSON_ARRAYAGG` and `JSON_OBJECTAGG` are aggregate functions and live in `sqlfactory.func.agg`, not here. The
``IS JSON`` predicate is a condition, not a function, and lives in `sqlfactory.condition.is_json`.
"""

from __future__ import annotations

from collections.abc import Collection
from typing import Any, ClassVar, Literal

from sqlfactory.dialect import SQLDialect
from sqlfactory.entities import Column, ColumnArg
from sqlfactory.func.base import Function
from sqlfactory.statement import Statement

# A single (path, value) pair, as used by JSON_SET, JSON_INSERT, JSON_REPLACE, JSON_ARRAY_APPEND and JSON_ARRAY_INSERT.
JsonPathValuePair = tuple[str | Statement, Statement | Any]

# A single (key, value) pair, as used by JSON_OBJECT.
JsonKeyValuePair = tuple[Statement | Any, Statement | Any]


def _flatten_pairs(pairs: Collection[tuple[Any, Any]]) -> list[Any]:
    """Flattens (path, value) or (key, value) pairs into a flat argument list, preserving order.

    :raises ValueError: If an element of ``pairs`` is not a 2-tuple (e.g. a bare string, which is otherwise
        silently unpacked into its first two characters).
    """
    flat: list[Any] = []

    for pair in pairs:
        if not isinstance(pair, tuple):
            raise ValueError(f"Expected a 2-tuple, got {pair!r}.")

        first, second = pair
        flat.append(first)
        flat.append(second)

    return flat


class JsonArray(Function):
    """``JSON_ARRAY([value[, value2] ...])`` — returns a JSON array containing the given values. The list may be empty."""

    def __init__(self, *values: Statement | Any) -> None:
        super().__init__("JSON_ARRAY", *values)


class JsonArrayAppend(Function):
    """
    ``JSON_ARRAY_APPEND(json_doc, path, value[, path, value] ...)`` — appends values to the end of the arrays at the
    given paths, returning the result, or ``NULL`` if any argument is ``NULL``.
    """

    def __init__(self, json_doc: Statement | Any, pair: JsonPathValuePair, *pairs: JsonPathValuePair) -> None:
        """
        :param json_doc: JSON document to modify.
        :param pair: First ``(path, value)`` pair to append. At least one pair is required.
        :param pairs: Further ``(path, value)`` pairs, applied left to right.
        """
        super().__init__("JSON_ARRAY_APPEND", json_doc, *_flatten_pairs((pair, *pairs)))


class JsonArrayInsert(Function):
    """
    ``JSON_ARRAY_INSERT(json_doc, path, value[, path, value] ...)`` — inserts values into the arrays at the given
    paths, returning the result, or ``NULL`` if any argument is ``NULL``. Pairs are applied left to right.
    """

    def __init__(self, json_doc: Statement | Any, pair: JsonPathValuePair, *pairs: JsonPathValuePair) -> None:
        """
        :param json_doc: JSON document to modify.
        :param pair: First ``(path, value)`` pair to insert. At least one pair is required.
        :param pairs: Further ``(path, value)`` pairs, applied left to right.
        """
        super().__init__("JSON_ARRAY_INSERT", json_doc, *_flatten_pairs((pair, *pairs)))


class JsonArrayIntersect(Function):
    """``JSON_ARRAY_INTERSECT(arr1, arr2)`` — returns the array of items found in both JSON array arguments. MariaDB 11.2+."""

    def __init__(self, arr1: Statement | Any, arr2: Statement | Any) -> None:
        super().__init__("JSON_ARRAY_INTERSECT", arr1, arr2)


class JsonCompact(Function):
    """``JSON_COMPACT(json_doc)`` — removes all unnecessary whitespace, returning the shortest equivalent document."""

    def __init__(self, json_doc: Statement | Any) -> None:
        super().__init__("JSON_COMPACT", json_doc)


class JsonContains(Function):
    """
    ``JSON_CONTAINS(json_doc, val[, path])`` — returns 1 if ``val`` is contained within ``json_doc`` (optionally
    restricted to ``path``), 0 if not, or ``NULL`` if any argument is ``NULL``.
    """

    def __init__(self, json_doc: Statement | Any, val: Statement | Any, path: str | Statement | None = None) -> None:
        if path is not None:
            super().__init__("JSON_CONTAINS", json_doc, val, path)
        else:
            super().__init__("JSON_CONTAINS", json_doc, val)


class JsonContainsPath(Function):
    """
    ``JSON_CONTAINS_PATH(json_doc, return_arg, path[, path] ...)`` — returns 1 if the document contains the given
    path(s), 0 if not, or ``NULL`` if any argument is ``NULL``.
    """

    def __init__(
        self,
        json_doc: Statement | Any,
        return_arg: Literal["one", "all"] | Statement,
        path: str | Statement,
        *paths: str | Statement,
    ) -> None:
        """
        :param json_doc: JSON document to inspect.
        :param return_arg: ``"one"`` to return 1 if at least one path exists, ``"all"`` to require every path.
        :param path: First path to check. At least one path is required.
        :param paths: Further paths to check.
        """
        super().__init__("JSON_CONTAINS_PATH", json_doc, return_arg, path, *paths)


class JsonDepth(Function):
    """
    ``JSON_DEPTH(json_doc)`` — returns the maximum nesting depth of a JSON document. Scalars and empty arrays/objects
    have depth 1.
    """

    def __init__(self, json_doc: Statement | Any) -> None:
        super().__init__("JSON_DEPTH", json_doc)


class JsonDetailed(Function):
    """``JSON_DETAILED(json_doc[, tab_size])`` — pretty-prints a JSON document, emphasizing nested structures."""

    def __init__(self, json_doc: Statement | Any, tab_size: Statement | int | None = None) -> None:
        if tab_size is not None:
            super().__init__("JSON_DETAILED", json_doc, tab_size)
        else:
            super().__init__("JSON_DETAILED", json_doc)


class JsonEquals(Function):
    """
    ``JSON_EQUALS(json1, json2)`` — returns 1 if the two JSON documents are equal (ignoring key order and numeric
    representation differences), 0 if not, or ``NULL`` if either argument is ``NULL``. MariaDB 10.7+.
    """

    def __init__(self, json1: Statement | Any, json2: Statement | Any) -> None:
        super().__init__("JSON_EQUALS", json1, json2)


class JsonExists(Function):
    """
    ``JSON_EXISTS(json_doc, path)`` — returns 1 if the document has an element at ``path``, 0 if not, or ``NULL`` for
    ``NULL`` input.
    """

    def __init__(self, json_doc: Statement | Any, path: str | Statement) -> None:
        super().__init__("JSON_EXISTS", json_doc, path)


class JsonExtract(Function):
    """
    ``JSON_EXTRACT(json_doc, path[, path] ...)`` — extracts the values matching the given path(s), returning a
    single value, or a JSON array of values if more than one path is given.
    """

    def __init__(self, json_doc: Statement | Any, path: str | Statement, *paths: str | Statement) -> None:
        super().__init__("JSON_EXTRACT", json_doc, path, *paths)


class JsonInsert(Function):
    """
    ``JSON_INSERT(json_doc, path, val[, path, val] ...)`` — inserts data without overwriting existing values,
    returning the result, or ``NULL`` if ``json_doc`` or a ``path`` is ``NULL``.
    """

    def __init__(self, json_doc: Statement | Any, pair: JsonPathValuePair, *pairs: JsonPathValuePair) -> None:
        """
        :param json_doc: JSON document to modify.
        :param pair: First ``(path, val)`` pair to insert. At least one pair is required.
        :param pairs: Further ``(path, val)`` pairs, applied left to right.
        """
        super().__init__("JSON_INSERT", json_doc, *_flatten_pairs((pair, *pairs)))


class JsonKeys(Function):
    """``JSON_KEYS(json_doc[, path])`` — returns the top-level keys of a JSON object (optionally at ``path``) as a JSON array."""

    def __init__(self, json_doc: Statement | Any, path: str | Statement | None = None) -> None:
        if path is not None:
            super().__init__("JSON_KEYS", json_doc, path)
        else:
            super().__init__("JSON_KEYS", json_doc)


class JsonKeyValue(Function):
    """``JSON_KEY_VALUE(obj, json_path)`` — extracts the key/value pairs of the JSON object at ``json_path``. MariaDB 11.2+."""

    def __init__(self, obj: Statement | Any, json_path: str | Statement) -> None:
        super().__init__("JSON_KEY_VALUE", obj, json_path)


class JsonLength(Function):
    """
    ``JSON_LENGTH(json_doc[, path])`` — returns the length of a JSON document (or of the value at ``path``): 1 for a
    scalar, element count for an array, member count for an object.
    """

    def __init__(self, json_doc: Statement | Any, path: str | Statement | None = None) -> None:
        if path is not None:
            super().__init__("JSON_LENGTH", json_doc, path)
        else:
            super().__init__("JSON_LENGTH", json_doc)


class JsonLoose(Function):
    """``JSON_LOOSE(json_doc)`` — adds whitespace to a JSON document to make it more readable."""

    def __init__(self, json_doc: Statement | Any) -> None:
        super().__init__("JSON_LOOSE", json_doc)


class JsonMerge(Function):
    """
    ``JSON_MERGE(json_doc, json_doc[, json_doc] ...)`` — merges JSON documents, preserving all keys and values.

    **Deprecated.** Use :class:`JsonMergePatch` (RFC 7396-compliant) or :class:`JsonMergePreserve` (a synonym of
    this function) instead.
    """

    def __init__(self, doc1: Statement | Any, doc2: Statement | Any, *docs: Statement | Any) -> None:
        super().__init__("JSON_MERGE", doc1, doc2, *docs)


class JsonMergePatch(Function):
    """
    ``JSON_MERGE_PATCH(json_doc, json_doc[, json_doc] ...)`` — merges JSON documents per RFC 7396, where duplicate
    keys are overwritten by the later document rather than combined.
    """

    def __init__(self, doc1: Statement | Any, doc2: Statement | Any, *docs: Statement | Any) -> None:
        super().__init__("JSON_MERGE_PATCH", doc1, doc2, *docs)


class JsonMergePreserve(JsonMerge):
    """
    ``JSON_MERGE_PRESERVE(json_doc, json_doc[, json_doc] ...)`` — synonym for the deprecated :class:`JsonMerge`;
    prefer this name in new code.
    """

    def __init__(self, doc1: Statement | Any, doc2: Statement | Any, *docs: Statement | Any) -> None:
        super().__init__(doc1, doc2, *docs)
        self.function = "JSON_MERGE_PRESERVE"


class JsonNormalize(Function):
    """
    ``JSON_NORMALIZE(json_doc)`` — recursively sorts object keys and removes whitespace, so documents can be compared
    for equality (e.g. byte-for-byte, or with a `UNIQUE` index). MariaDB 10.7+.
    """

    def __init__(self, json_doc: Statement | Any) -> None:
        super().__init__("JSON_NORMALIZE", json_doc)


class JsonObject(Function):
    """
    ``JSON_OBJECT([key, value[, key, value] ...])`` — returns a JSON object built from the given key/value pairs.
    The list may be empty.
    """

    def __init__(self, *pairs: JsonKeyValuePair) -> None:
        super().__init__("JSON_OBJECT", *_flatten_pairs(pairs))


class JsonObjectFilterKeys(Function):
    """
    ``JSON_OBJECT_FILTER_KEYS(obj, array_keys)`` — returns a JSON object keeping only the keys of ``obj`` that are
    also present in the ``array_keys`` JSON array. MariaDB 11.2+.
    """

    def __init__(self, obj: Statement | Any, array_keys: Statement | Any) -> None:
        super().__init__("JSON_OBJECT_FILTER_KEYS", obj, array_keys)


class JsonObjectToArray(Function):
    """``JSON_OBJECT_TO_ARRAY(obj)`` — converts a JSON object into an array of ``[key, value]`` pairs. MariaDB 11.2+."""

    def __init__(self, obj: Statement | Any) -> None:
        super().__init__("JSON_OBJECT_TO_ARRAY", obj)


class JsonOverlaps(Function):
    """
    ``JSON_OVERLAPS(json_doc1, json_doc2)`` — returns 1 if the two documents share at least one key/value pair,
    array element or scalar value, 0 otherwise. MariaDB 10.9+.
    """

    def __init__(self, json_doc1: Statement | Any, json_doc2: Statement | Any) -> None:
        super().__init__("JSON_OVERLAPS", json_doc1, json_doc2)


class JsonPretty(JsonDetailed):
    """
    ``JSON_PRETTY(json_doc[, tab_size])`` — alias of :class:`JsonDetailed`. Available from MariaDB 10.10.3 / 10.9.5
    / 10.8.7 / 10.7.8 / 10.6.12 / 10.5.19 / 10.4.28.
    """

    def __init__(self, json_doc: Statement | Any, tab_size: Statement | int | None = None) -> None:
        super().__init__(json_doc, tab_size)
        self.function = "JSON_PRETTY"


class JsonQuery(Function):
    """
    ``JSON_QUERY(json_doc, path)`` — extracts a JSON object or array at ``path``, or ``NULL`` if the document is
    invalid or nothing matches. See also :class:`JsonValue` for scalar extraction.
    """

    def __init__(self, json_doc: Statement | Any, path: str | Statement) -> None:
        super().__init__("JSON_QUERY", json_doc, path)


class JsonQuote(Function):
    """``JSON_QUOTE(json_value)`` — quotes a string as a JSON string literal, escaping special characters."""

    def __init__(self, json_value: Statement | Any) -> None:
        super().__init__("JSON_QUOTE", json_value)


class JsonRemove(Function):
    """
    ``JSON_REMOVE(json_doc, path[, path] ...)`` — removes the values at the given paths, returning the result, or
    ``NULL`` if any argument is ``NULL``.
    """

    def __init__(self, json_doc: Statement | Any, path: str | Statement, *paths: str | Statement) -> None:
        super().__init__("JSON_REMOVE", json_doc, path, *paths)


class JsonReplace(Function):
    """
    ``JSON_REPLACE(json_doc, path, val[, path, val] ...)`` — replaces existing values at the given paths (does not
    insert new ones), returning the result, or ``NULL`` if any argument is ``NULL``.
    """

    def __init__(self, json_doc: Statement | Any, pair: JsonPathValuePair, *pairs: JsonPathValuePair) -> None:
        """
        :param json_doc: JSON document to modify.
        :param pair: First ``(path, val)`` pair to replace. At least one pair is required.
        :param pairs: Further ``(path, val)`` pairs, applied left to right.
        """
        super().__init__("JSON_REPLACE", json_doc, *_flatten_pairs((pair, *pairs)))


class JsonSchemaValid(Function):
    """
    ``JSON_SCHEMA_VALID(schema, json_doc)`` — returns 1 if ``json_doc`` validates against the JSON Schema (draft
    2020-12, with a few exceptions such as external resources), 0 otherwise. MariaDB 11.1+.
    """

    def __init__(self, schema: Statement | Any, json_doc: Statement | Any) -> None:
        super().__init__("JSON_SCHEMA_VALID", schema, json_doc)


class JsonSearch(Function):
    """
    ``JSON_SEARCH(json_doc, return_arg, search_str[, escape_char[, path] ...])`` — returns the path(s) to string
    value(s) matching ``search_str`` (a ``LIKE`` pattern), or ``NULL`` if nothing matches.
    """

    def __init__(
        self,
        json_doc: Statement | Any,
        return_arg: Literal["one", "all"] | Statement,
        search_str: Statement | Any,
        *paths: str | Statement,
        escape_char: Statement | Any | None = None,
    ) -> None:
        """
        :param json_doc: JSON document to search.
        :param return_arg: ``"one"`` to return the first match, ``"all"`` to return every match as a JSON array.
        :param search_str: ``LIKE``-style pattern to search for.
        :param paths: Paths to restrict the search to.
        :param escape_char: Escape character for ``search_str`` (defaults to MariaDB's own default when omitted).
        """
        args: list[Any] = [json_doc, return_arg, search_str]

        if escape_char is not None or paths:
            args.append(escape_char)
            args.extend(paths)

        super().__init__("JSON_SEARCH", *args)


class JsonSet(Function):
    """
    ``JSON_SET(json_doc, path, val[, path, val] ...)`` — inserts or updates data at the given paths, returning the
    result, or ``NULL`` if any argument (or a path) is ``NULL``/invalid.
    """

    def __init__(self, json_doc: Statement | Any, pair: JsonPathValuePair, *pairs: JsonPathValuePair) -> None:
        """
        :param json_doc: JSON document to modify.
        :param pair: First ``(path, val)`` pair to set. At least one pair is required.
        :param pairs: Further ``(path, val)`` pairs, applied left to right.
        """
        super().__init__("JSON_SET", json_doc, *_flatten_pairs((pair, *pairs)))


class JsonType(Function):
    """
    ``JSON_TYPE(json_val)`` — returns a string naming the type of a JSON value (``OBJECT``, ``ARRAY``, ``INTEGER``,
    ``STRING``, ``BOOLEAN``, ``DOUBLE``, ``NULL``, ...).
    """

    def __init__(self, json_val: Statement | Any) -> None:
        super().__init__("JSON_TYPE", json_val)


class JsonUnquote(Function):
    """
    ``JSON_UNQUOTE(val)`` — unquotes a JSON value, returning a string (resolving escape sequences), or ``NULL`` if
    the argument is ``NULL``.
    """

    def __init__(self, val: Statement | Any) -> None:
        super().__init__("JSON_UNQUOTE", val)


class JsonValid(Function):
    """
    ``JSON_VALID(value)`` — returns 1 if ``value`` is a valid JSON document, 0 if not, or ``NULL`` if the argument
    is ``NULL``.
    """

    def __init__(self, value: Statement | Any) -> None:
        super().__init__("JSON_VALID", value)


class JsonValue(Function):
    """
    ``JSON_VALUE(json_doc, path)`` — extracts a scalar value at ``path``, or ``NULL`` if the document is invalid,
    nothing matches, or the match is not a scalar. See also :class:`JsonQuery` for object/array extraction.
    """

    def __init__(self, json_doc: Statement | Any, path: str | Statement) -> None:
        super().__init__("JSON_VALUE", json_doc, path)


# ---------------------------------------------------------------------------
# JSON_TABLE
# ---------------------------------------------------------------------------


class JsonTableAction:
    """
    ``NULL`` / ``ERROR`` / ``DEFAULT value`` action for a :class:`JsonTableColumn`'s ``ON EMPTY`` / ``ON ERROR``
    clause.

    Use the :attr:`NULL` / :attr:`ERROR` constants, or :meth:`default` for ``DEFAULT``. This is not a
    :class:`~sqlfactory.statement.Statement` itself, as it does not know whether it renders as ``ON EMPTY`` or
    ``ON ERROR`` until the column using it says so.

    **MariaDB requires the ``DEFAULT`` value to be a string literal under server-side ``PREPARE``** — a bound
    placeholder (``?``) is rejected there (only the JSON_TABLE document argument accepts one). :meth:`default`
    still binds its value as a query parameter by default, which works end to end with client-side-interpolating
    drivers (pymysql, aiomysql, mysqlclient). For server-side prepared statements, pass a
    :class:`~sqlfactory.statement.Statement` instead, e.g. ``JsonTableAction.default(Raw("'0'"))``, which is
    rendered as SQL (using its own args) rather than bound.
    """

    NULL: ClassVar["JsonTableAction"]
    ERROR: ClassVar["JsonTableAction"]

    def __init__(self, keyword: Literal["NULL", "ERROR", "DEFAULT"], value: Statement | Any = None) -> None:
        self._keyword = keyword
        self._value = value

    @classmethod
    def default(cls, value: Statement | Any) -> "JsonTableAction":
        """
        ``DEFAULT value``. ``value`` is bound as a query parameter unless it is itself a ``Statement`` (e.g.
        ``Raw("'0'")``), in which case it is rendered as SQL instead — see the class docstring for why that
        matters under server-side ``PREPARE``.
        """
        return cls("DEFAULT", value)

    def render(self, suffix: Literal["EMPTY", "ERROR"], dialect: SQLDialect) -> str:
        """
        Renders this action as ``... ON EMPTY`` or ``... ON ERROR``, depending on ``suffix``.
        @private
        """
        if self._keyword == "DEFAULT":
            value = str(self._value) if isinstance(self._value, Statement) else dialect.placeholder
            return f"DEFAULT {value} ON {suffix}"

        return f"{self._keyword} ON {suffix}"

    @property
    def args(self) -> list[Any]:
        """Query parameter values held by this action (the ``DEFAULT`` value, if any)."""
        if self._keyword != "DEFAULT":
            return []

        return list(self._value.args) if isinstance(self._value, Statement) else [self._value]


JsonTableAction.NULL = JsonTableAction("NULL")
JsonTableAction.ERROR = JsonTableAction("ERROR")


class JsonTableOrdinalityColumn(Statement):
    """``name FOR ORDINALITY`` — a JSON_TABLE column holding the sequential row number, starting from 1."""

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def __str__(self) -> str:
        return f"{self.dialect.quote}{self.name}{self.dialect.quote} FOR ORDINALITY"

    @property
    def args(self) -> list[Any]:
        return []


class JsonTableColumn(Statement):
    """
    ``name type [FORMAT JSON] PATH path [on_empty] [on_error]`` — a JSON_TABLE column extracting a value at
    ``path``. With ``format_json=True``, arrays/objects are returned as serialized JSON text (``type_`` must then be
    a string type) — ``FORMAT JSON`` here is MariaDB 13.1+. MariaDB defaults to ``NULL ON EMPTY`` / ``NULL ON
    ERROR`` when ``on_empty`` / ``on_error`` are omitted.

    **MariaDB requires ``path`` to be a string literal under server-side ``PREPARE``** — a bound placeholder (``?``)
    is rejected there (only the JSON_TABLE document argument accepts one). A bare ``path`` string is still bound as
    a query parameter by default, which works end to end with client-side-interpolating drivers (pymysql, aiomysql,
    mysqlclient). For server-side prepared statements, pass a :class:`~sqlfactory.statement.Statement` instead, e.g.
    ``Raw("'$.name'")``, which is rendered as SQL rather than bound.
    """

    def __init__(
        self,
        name: str,
        type_: str,
        path: str | Statement,
        *,
        format_json: bool = False,
        on_empty: JsonTableAction | None = None,
        on_error: JsonTableAction | None = None,
    ) -> None:
        """
        :param name: Name of the generated column.
        :param type_: SQL type of the generated column (e.g. ``"VARCHAR(50)"``), used verbatim.
        :param path: JSON path to extract the value from. See the class docstring about server-side ``PREPARE``.
        :param format_json: Whether to add ``FORMAT JSON``, returning arrays/objects as serialized JSON text.
            MariaDB 13.1+.
        :param on_empty: Action to take when ``path`` evaluates to no value.
        :param on_error: Action to take when evaluating ``path`` raises an error.
        """
        super().__init__()
        self.name = name
        self.type = type_
        self.path = path
        self.format_json = format_json
        self.on_empty = on_empty
        self.on_error = on_error

    def __str__(self) -> str:
        path = str(self.path) if isinstance(self.path, Statement) else self.dialect.placeholder
        out = f"{self.dialect.quote}{self.name}{self.dialect.quote} {self.type}"

        if self.format_json:
            out += " FORMAT JSON"

        out += f" PATH {path}"

        if self.on_empty is not None:
            out += f" {self.on_empty.render('EMPTY', self.dialect)}"

        if self.on_error is not None:
            out += f" {self.on_error.render('ERROR', self.dialect)}"

        return out

    @property
    def args(self) -> list[Any]:
        out: list[Any] = list(self.path.args) if isinstance(self.path, Statement) else [self.path]

        if self.on_empty is not None:
            out.extend(self.on_empty.args)

        if self.on_error is not None:
            out.extend(self.on_error.args)

        return out


class JsonTableExistsColumn(Statement):
    """
    ``name type EXISTS PATH path`` — a JSON_TABLE column that is 1 if ``path`` exists in the row's document, 0
    otherwise.

    **MariaDB requires ``path`` to be a string literal under server-side ``PREPARE``** — a bound placeholder (``?``)
    is rejected there (only the JSON_TABLE document argument accepts one). A bare ``path`` string is still bound as
    a query parameter by default, which works end to end with client-side-interpolating drivers (pymysql, aiomysql,
    mysqlclient). For server-side prepared statements, pass a :class:`~sqlfactory.statement.Statement` instead, e.g.
    ``Raw("'$.tag'")``, which is rendered as SQL rather than bound.
    """

    def __init__(self, name: str, type_: str, path: str | Statement) -> None:
        super().__init__()
        self.name = name
        self.type = type_
        self.path = path

    def __str__(self) -> str:
        path = str(self.path) if isinstance(self.path, Statement) else self.dialect.placeholder
        return f"{self.dialect.quote}{self.name}{self.dialect.quote} {self.type} EXISTS PATH {path}"

    @property
    def args(self) -> list[Any]:
        return list(self.path.args) if isinstance(self.path, Statement) else [self.path]


class JsonTableNestedColumn(Statement):
    """
    ``NESTED PATH path COLUMNS (column_list)`` — expands a nested JSON array/object at ``path`` into additional
    rows, each carrying the columns defined in its own (possibly further nested) ``COLUMNS`` clause. At least one
    column is required — MariaDB rejects an empty ``COLUMNS ()``.

    **MariaDB requires ``path`` to be a string literal under server-side ``PREPARE``** — a bound placeholder (``?``)
    is rejected there (only the JSON_TABLE document argument accepts one). A bare ``path`` string is still bound as
    a query parameter by default, which works end to end with client-side-interpolating drivers (pymysql, aiomysql,
    mysqlclient). For server-side prepared statements, pass a :class:`~sqlfactory.statement.Statement` instead, e.g.
    ``Raw("'$.sizes[*]'")``, which is rendered as SQL rather than bound.
    """

    def __init__(self, path: str | Statement, column: "JsonTableColumnArg", *columns: "JsonTableColumnArg") -> None:
        """
        :param path: JSON path of the nested array/object to expand into rows.
        :param column: First column of the nested ``COLUMNS`` clause. At least one column is required.
        :param columns: Further columns of the nested ``COLUMNS`` clause.
        """
        super().__init__()
        self.path = path
        self.columns: list[JsonTableColumnArg] = [column, *columns]

    def __str__(self) -> str:
        path = str(self.path) if isinstance(self.path, Statement) else self.dialect.placeholder
        cols = ", ".join(str(column) for column in self.columns)
        return f"NESTED PATH {path} COLUMNS ({cols})"

    @property
    def args(self) -> list[Any]:
        out: list[Any] = list(self.path.args) if isinstance(self.path, Statement) else [self.path]

        for column in self.columns:
            out.extend(column.args)

        return out


# Any column definition usable inside a JSON_TABLE COLUMNS (...) clause.
JsonTableColumnArg = JsonTableOrdinalityColumn | JsonTableColumn | JsonTableExistsColumn | JsonTableNestedColumn


class JsonTable(Statement):
    """
    ``JSON_TABLE(json_doc, path COLUMNS (column_list))`` — expands a JSON document into a relational table, one row
    per match of ``path``. At least one column is required — MariaDB rejects an empty ``COLUMNS ()``.

    This is a table source, not a scalar value: pass it wrapped in :class:`~sqlfactory.select.aliased.Aliased` (for
    an explicit alias) as the ``table=`` argument of :class:`~sqlfactory.select.select.Select`, or pass it directly
    to :meth:`~sqlfactory.mixins.join.WithJoin.join`/:class:`~sqlfactory.select.join.Join` with ``alias=`` — MariaDB
    requires JSON_TABLE to be aliased, so always give it one (``Join`` raises if you don't).

    A ``str`` ``json_doc`` names a column, as in conditions and aggregates. To expand a literal document instead,
    bind it with :class:`~sqlfactory.statement.Value`, e.g. ``JsonTable(Value(json.dumps(ids)), "$[*]", ...)``.

    **MariaDB requires ``path`` to be a string literal under server-side ``PREPARE``** — a bound placeholder (``?``)
    is rejected there; only ``json_doc`` accepts one. A bare ``path`` string is still bound as a query parameter by
    default, which works end to end with client-side-interpolating drivers (pymysql, aiomysql, mysqlclient). For
    server-side prepared statements, pass a :class:`~sqlfactory.statement.Statement` instead, e.g. ``Raw("'$[*]'")``,
    which is rendered as SQL rather than bound.

    Usage:

    >>> from sqlfactory import Aliased, Column, Join, Select, Table
    >>> from sqlfactory.func.json import JsonTable, JsonTableColumn
    >>> jt = JsonTable("data", "$[*]", JsonTableColumn("name", "VARCHAR(50)", "$.name"))
    >>> Select("jt.name", table=[Table("people"), Aliased(jt, alias="jt")])
    >>> "SELECT `jt`.`name` FROM `people`, JSON_TABLE(`data`, %s COLUMNS (`name` VARCHAR(50) PATH %s)) AS `jt`"

    Joined, instead of listed as another table:

    >>> Select("people.id", table="people", join=[Join(jt, alias="jt", on=Column("jt.name") == Column("people.name"))])
    >>> (
    ...     "SELECT `people`.`id` FROM `people` JOIN "
    ...     "JSON_TABLE(`data`, %s COLUMNS (`name` VARCHAR(50) PATH %s)) AS `jt` "
    ...     "ON `jt`.`name` = `people`.`name`"
    ... )
    """

    def __init__(
        self,
        json_doc: ColumnArg | Statement,
        path: str | Statement,
        column: JsonTableColumnArg,
        *columns: JsonTableColumnArg,
    ) -> None:
        """
        :param json_doc: JSON document to expand into rows: a column name, or a Statement (``Value(...)`` for a
            literal document).
        :param path: JSON path selecting the rows. See the class docstring about server-side ``PREPARE``.
        :param column: First column of the ``COLUMNS`` clause. At least one column is required.
        :param columns: Further columns of the ``COLUMNS`` clause.
        """
        super().__init__()
        self.json_doc: Statement = Column(json_doc) if isinstance(json_doc, str) else json_doc
        self.path = path
        self.columns: list[JsonTableColumnArg] = [column, *columns]

    def __str__(self) -> str:
        doc = str(self.json_doc)
        path = str(self.path) if isinstance(self.path, Statement) else self.dialect.placeholder
        cols = ", ".join(str(column) for column in self.columns)
        return f"JSON_TABLE({doc}, {path} COLUMNS ({cols}))"

    @property
    def args(self) -> list[Any]:
        out: list[Any] = list(self.json_doc.args)
        out.extend(self.path.args if isinstance(self.path, Statement) else [self.path])

        for column in self.columns:
            out.extend(column.args)

        return out
