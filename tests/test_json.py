"""Tests for JSON functions (`sqlfactory.func.json`)."""

import pytest

from sqlfactory import Aliased, Column, InnerJoin, IsJson, Join, OracleSQLDialect, Raw, Select, Table, Update, Value
from sqlfactory.func.json import (
    JsonArray,
    JsonArrayAppend,
    JsonArrayInsert,
    JsonArrayIntersect,
    JsonCompact,
    JsonContains,
    JsonContainsPath,
    JsonDepth,
    JsonDetailed,
    JsonEquals,
    JsonExists,
    JsonExtract,
    JsonInsert,
    JsonKeys,
    JsonKeyValue,
    JsonLength,
    JsonLoose,
    JsonMerge,
    JsonMergePatch,
    JsonMergePreserve,
    JsonNormalize,
    JsonObject,
    JsonObjectFilterKeys,
    JsonObjectToArray,
    JsonOverlaps,
    JsonPretty,
    JsonQuery,
    JsonQuote,
    JsonRemove,
    JsonReplace,
    JsonSchemaValid,
    JsonSearch,
    JsonSet,
    JsonTable,
    JsonTableAction,
    JsonTableColumn,
    JsonTableExistsColumn,
    JsonTableNestedColumn,
    JsonTableOrdinalityColumn,
    JsonType,
    JsonUnquote,
    JsonValid,
    JsonValue,
)

# ---------------------------------------------------------------------------
# Simple scalar functions
# ---------------------------------------------------------------------------


def test_json_array_empty():
    f = JsonArray()
    assert str(f) == "JSON_ARRAY()"
    assert f.args == []


def test_json_array_values():
    f = JsonArray(56, 3.1416, "hello", None)
    assert str(f) == "JSON_ARRAY(%s, %s, %s, %s)"
    assert f.args == [56, 3.1416, "hello", None]


def test_json_array_append_single_pair():
    f = JsonArrayAppend(Column("doc"), ("$.B", 5))
    assert str(f) == "JSON_ARRAY_APPEND(`doc`, %s, %s)"
    assert f.args == ["$.B", 5]


def test_json_array_append_multiple_pairs():
    f = JsonArrayAppend(Column("doc"), ("$.B", 5), ("$.C", 6))
    assert str(f) == "JSON_ARRAY_APPEND(`doc`, %s, %s, %s, %s)"
    assert f.args == ["$.B", 5, "$.C", 6]


def test_json_array_insert_single_pair():
    f = JsonArrayInsert(Column("doc"), ("$[1]", 6))
    assert str(f) == "JSON_ARRAY_INSERT(`doc`, %s, %s)"
    assert f.args == ["$[1]", 6]


def test_json_array_insert_multiple_pairs():
    f = JsonArrayInsert(Column("doc"), ("$[1]", 6), ("$[2]", 7))
    assert str(f) == "JSON_ARRAY_INSERT(`doc`, %s, %s, %s, %s)"
    assert f.args == ["$[1]", 6, "$[2]", 7]


def test_json_array_intersect():
    f = JsonArrayIntersect(Column("a"), Column("b"))
    assert str(f) == "JSON_ARRAY_INTERSECT(`a`, `b`)"
    assert f.args == []


def test_json_compact():
    f = JsonCompact(Column("doc"))
    assert str(f) == "JSON_COMPACT(`doc`)"
    assert f.args == []


def test_json_contains_without_path():
    f = JsonContains(Column("doc"), '{"C": 1}')
    assert str(f) == "JSON_CONTAINS(`doc`, %s)"
    assert f.args == ['{"C": 1}']


def test_json_contains_with_path():
    f = JsonContains(Column("doc"), '{"C": 1}', "$.B")
    assert str(f) == "JSON_CONTAINS(`doc`, %s, %s)"
    assert f.args == ['{"C": 1}', "$.B"]


def test_json_contains_path_single():
    f = JsonContainsPath(Column("doc"), "one", "$.A")
    assert str(f) == "JSON_CONTAINS_PATH(`doc`, %s, %s)"
    assert f.args == ["one", "$.A"]


def test_json_contains_path_multiple():
    f = JsonContainsPath(Column("doc"), "all", "$.A", "$.D")
    assert str(f) == "JSON_CONTAINS_PATH(`doc`, %s, %s, %s)"
    assert f.args == ["all", "$.A", "$.D"]


def test_json_depth():
    f = JsonDepth(Column("doc"))
    assert str(f) == "JSON_DEPTH(`doc`)"
    assert f.args == []


def test_json_detailed_without_tab_size():
    f = JsonDetailed(Column("doc"))
    assert str(f) == "JSON_DETAILED(`doc`)"
    assert f.args == []


def test_json_detailed_with_tab_size():
    f = JsonDetailed(Column("doc"), 4)
    assert str(f) == "JSON_DETAILED(`doc`, %s)"
    assert f.args == [4]


def test_json_equals():
    f = JsonEquals(Column("a"), Column("b"))
    assert str(f) == "JSON_EQUALS(`a`, `b`)"
    assert f.args == []


def test_json_exists():
    f = JsonExists(Column("doc"), "$.key2")
    assert str(f) == "JSON_EXISTS(`doc`, %s)"
    assert f.args == ["$.key2"]


def test_json_extract_single_path():
    f = JsonExtract(Column("doc"), "$[1]")
    assert str(f) == "JSON_EXTRACT(`doc`, %s)"
    assert f.args == ["$[1]"]


def test_json_extract_multiple_paths():
    f = JsonExtract(Column("doc"), "$[1]", "$[2]")
    assert str(f) == "JSON_EXTRACT(`doc`, %s, %s)"
    assert f.args == ["$[1]", "$[2]"]


def test_json_insert_single_pair():
    f = JsonInsert(Column("doc"), ("$.C", "[3, 4]"))
    assert str(f) == "JSON_INSERT(`doc`, %s, %s)"
    assert f.args == ["$.C", "[3, 4]"]


def test_json_insert_multiple_pairs():
    f = JsonInsert(Column("doc"), ("$.C", 1), ("$.D", 2))
    assert str(f) == "JSON_INSERT(`doc`, %s, %s, %s, %s)"
    assert f.args == ["$.C", 1, "$.D", 2]


def test_json_keys_without_path():
    f = JsonKeys(Column("doc"))
    assert str(f) == "JSON_KEYS(`doc`)"
    assert f.args == []


def test_json_keys_with_path():
    f = JsonKeys(Column("doc"), "$.C")
    assert str(f) == "JSON_KEYS(`doc`, %s)"
    assert f.args == ["$.C"]


def test_json_key_value():
    f = JsonKeyValue(Column("obj"), "$[0][1]")
    assert str(f) == "JSON_KEY_VALUE(`obj`, %s)"
    assert f.args == ["$[0][1]"]


def test_json_length_without_path():
    f = JsonLength(Column("doc"))
    assert str(f) == "JSON_LENGTH(`doc`)"
    assert f.args == []


def test_json_length_with_path():
    f = JsonLength(Column("doc"), "$.C")
    assert str(f) == "JSON_LENGTH(`doc`, %s)"
    assert f.args == ["$.C"]


def test_json_loose():
    f = JsonLoose(Column("doc"))
    assert str(f) == "JSON_LOOSE(`doc`)"
    assert f.args == []


def test_json_merge():
    f = JsonMerge(Column("a"), Column("b"), Column("c"))
    assert str(f) == "JSON_MERGE(`a`, `b`, `c`)"
    assert f.args == []


def test_json_merge_patch():
    f = JsonMergePatch(Column("a"), Column("b"))
    assert str(f) == "JSON_MERGE_PATCH(`a`, `b`)"
    assert f.args == []


def test_json_merge_preserve():
    f = JsonMergePreserve(Column("a"), Column("b"))
    assert str(f) == "JSON_MERGE_PRESERVE(`a`, `b`)"
    assert f.args == []
    assert isinstance(f, JsonMerge)


def test_json_normalize():
    f = JsonNormalize(Column("val"))
    assert str(f) == "JSON_NORMALIZE(`val`)"
    assert f.args == []


def test_json_object_empty():
    f = JsonObject()
    assert str(f) == "JSON_OBJECT()"
    assert f.args == []


def test_json_object_pairs():
    f = JsonObject(("id", 1), ("name", "Monty"))
    assert str(f) == "JSON_OBJECT(%s, %s, %s, %s)"
    assert f.args == ["id", 1, "name", "Monty"]


def test_json_object_filter_keys():
    f = JsonObjectFilterKeys(Column("obj1"), Column("keys"))
    assert str(f) == "JSON_OBJECT_FILTER_KEYS(`obj1`, `keys`)"
    assert f.args == []


def test_json_object_to_array():
    f = JsonObjectToArray(Column("obj1"))
    assert str(f) == "JSON_OBJECT_TO_ARRAY(`obj1`)"
    assert f.args == []


def test_json_overlaps():
    f = JsonOverlaps(Column("a"), Column("b"))
    assert str(f) == "JSON_OVERLAPS(`a`, `b`)"
    assert f.args == []


def test_json_pretty_without_tab_size():
    f = JsonPretty(Column("doc"))
    assert str(f) == "JSON_PRETTY(`doc`)"
    assert f.args == []
    assert isinstance(f, JsonDetailed)


def test_json_pretty_with_tab_size():
    f = JsonPretty(Column("doc"), 2)
    assert str(f) == "JSON_PRETTY(`doc`, %s)"
    assert f.args == [2]


def test_json_query():
    f = JsonQuery(Column("doc"), "$.key1")
    assert str(f) == "JSON_QUERY(`doc`, %s)"
    assert f.args == ["$.key1"]


def test_json_quote():
    f = JsonQuote("A")
    assert str(f) == "JSON_QUOTE(%s)"
    assert f.args == ["A"]


def test_json_remove_single_path():
    f = JsonRemove(Column("doc"), "$.C")
    assert str(f) == "JSON_REMOVE(`doc`, %s)"
    assert f.args == ["$.C"]


def test_json_remove_multiple_paths():
    f = JsonRemove(Column("doc"), "$.C", "$.D")
    assert str(f) == "JSON_REMOVE(`doc`, %s, %s)"
    assert f.args == ["$.C", "$.D"]


def test_json_replace_single_pair():
    f = JsonReplace(Column("doc"), ("$.B[1]", 4))
    assert str(f) == "JSON_REPLACE(`doc`, %s, %s)"
    assert f.args == ["$.B[1]", 4]


def test_json_replace_multiple_pairs():
    f = JsonReplace(Column("doc"), ("$.B[1]", 4), ("$.A", 5))
    assert str(f) == "JSON_REPLACE(`doc`, %s, %s, %s, %s)"
    assert f.args == ["$.B[1]", 4, "$.A", 5]


def test_json_schema_valid():
    f = JsonSchemaValid(Column("schema"), Column("doc"))
    assert str(f) == "JSON_SCHEMA_VALID(`schema`, `doc`)"
    assert f.args == []


def test_json_search_minimal():
    f = JsonSearch(Column("doc"), "one", "AB")
    assert str(f) == "JSON_SEARCH(`doc`, %s, %s)"
    assert f.args == ["one", "AB"]


def test_json_search_with_escape_char_only():
    f = JsonSearch(Column("doc"), "one", "AB", escape_char="\\")
    assert str(f) == "JSON_SEARCH(`doc`, %s, %s, %s)"
    assert f.args == ["one", "AB", "\\"]


def test_json_search_with_paths_only():
    f = JsonSearch(Column("doc"), "one", "AB", "$[0]", "$[1]")
    assert str(f) == "JSON_SEARCH(`doc`, %s, %s, %s, %s, %s)"
    assert f.args == ["one", "AB", None, "$[0]", "$[1]"]


def test_json_search_with_escape_char_and_paths():
    f = JsonSearch(Column("doc"), "one", "AB", "$[0]", escape_char="\\")
    assert str(f) == "JSON_SEARCH(`doc`, %s, %s, %s, %s)"
    assert f.args == ["one", "AB", "\\", "$[0]"]


def test_json_set_single_pair():
    f = JsonSet(Column("priv"), ("$.locked", True))
    assert str(f) == "JSON_SET(`priv`, %s, %s)"
    assert f.args == ["$.locked", True]


def test_json_set_multiple_pairs():
    f = JsonSet(Column("priv"), ("$.locked", True), ("$.reason", "x"))
    assert str(f) == "JSON_SET(`priv`, %s, %s, %s, %s)"
    assert f.args == ["$.locked", True, "$.reason", "x"]


def test_json_set_pair_not_tuple_raises():
    """A bare 2-character string looks like an iterable pair and would otherwise silently mis-pair."""
    with pytest.raises(ValueError, match="tuple"):
        JsonSet(Column("doc"), "$a")


def test_json_type():
    f = JsonType(Column("doc"))
    assert str(f) == "JSON_TYPE(`doc`)"
    assert f.args == []


def test_json_unquote():
    f = JsonUnquote(Raw('"Monty"'))
    assert str(f) == 'JSON_UNQUOTE("Monty")'
    assert f.args == []


def test_json_valid():
    f = JsonValid(Column("doc"))
    assert str(f) == "JSON_VALID(`doc`)"
    assert f.args == []


def test_json_value():
    f = JsonValue(Column("doc"), "$.key1")
    assert str(f) == "JSON_VALUE(`doc`, %s)"
    assert f.args == ["$.key1"]


# ---------------------------------------------------------------------------
# JSON_TABLE
# ---------------------------------------------------------------------------


def test_json_table_action_null():
    assert JsonTableAction.NULL.render("EMPTY", Column.default_dialect) == "NULL ON EMPTY"
    assert JsonTableAction.NULL.args == []


def test_json_table_action_error():
    assert JsonTableAction.ERROR.render("ERROR", Column.default_dialect) == "ERROR ON ERROR"
    assert JsonTableAction.ERROR.args == []


def test_json_table_action_default():
    action = JsonTableAction.default(0)
    assert action.render("EMPTY", Column.default_dialect) == "DEFAULT %s ON EMPTY"
    assert action.args == [0]


def test_json_table_action_default_statement():
    """A Statement default value (needed under server-side PREPARE) renders as SQL, not a bound placeholder."""
    action = JsonTableAction.default(Raw("'0'"))
    assert action.render("EMPTY", Column.default_dialect) == "DEFAULT '0' ON EMPTY"
    assert action.args == []


def test_json_table_ordinality_column():
    col = JsonTableOrdinalityColumn("idx")
    assert str(col) == "`idx` FOR ORDINALITY"
    assert col.args == []


def test_json_table_column_minimal():
    col = JsonTableColumn("name", "VARCHAR(50)", "$.name")
    assert str(col) == "`name` VARCHAR(50) PATH %s"
    assert col.args == ["$.name"]


def test_json_table_column_format_json():
    col = JsonTableColumn("tags", "VARCHAR(100)", "$.tags", format_json=True)
    assert str(col) == "`tags` VARCHAR(100) FORMAT JSON PATH %s"
    assert col.args == ["$.tags"]


def test_json_table_column_statement_path():
    col = JsonTableColumn("name", "VARCHAR(50)", Raw("'$.name'"))
    assert str(col) == "`name` VARCHAR(50) PATH '$.name'"
    assert col.args == []


def test_json_table_column_on_empty_on_error_keywords():
    col = JsonTableColumn("age", "INT", "$.age", on_empty=JsonTableAction.NULL, on_error=JsonTableAction.ERROR)
    assert str(col) == "`age` INT PATH %s NULL ON EMPTY ERROR ON ERROR"
    assert col.args == ["$.age"]


def test_json_table_column_on_empty_on_error_default():
    col = JsonTableColumn("age", "INT", "$.age", on_empty=JsonTableAction.default(-1), on_error=JsonTableAction.default(0))
    assert str(col) == "`age` INT PATH %s DEFAULT %s ON EMPTY DEFAULT %s ON ERROR"
    assert col.args == ["$.age", -1, 0]


def test_json_table_exists_column():
    col = JsonTableExistsColumn("has_tag", "INT", "$.tag")
    assert str(col) == "`has_tag` INT EXISTS PATH %s"
    assert col.args == ["$.tag"]


def test_json_table_exists_column_statement_path():
    col = JsonTableExistsColumn("has_tag", "INT", Raw("'$.tag'"))
    assert str(col) == "`has_tag` INT EXISTS PATH '$.tag'"
    assert col.args == []


def test_json_table_nested_column():
    nested = JsonTableNestedColumn("$.sizes[*]", JsonTableColumn("size", "VARCHAR(32)", "$"))
    assert str(nested) == "NESTED PATH %s COLUMNS (`size` VARCHAR(32) PATH %s)"
    assert nested.args == ["$.sizes[*]", "$"]


def test_json_table_nested_column_statement_path():
    nested = JsonTableNestedColumn(Raw("'$.sizes[*]'"), JsonTableOrdinalityColumn("i"))
    assert str(nested) == "NESTED PATH '$.sizes[*]' COLUMNS (`i` FOR ORDINALITY)"
    assert nested.args == []


def test_json_table_full():
    jt = JsonTable(
        Column("data"),
        "$[*]",
        JsonTableOrdinalityColumn("row_num"),
        JsonTableColumn("name", "VARCHAR(10)", "$.name"),
        JsonTableNestedColumn("$.sizes[*]", JsonTableColumn("size", "VARCHAR(32)", "$")),
    )
    assert str(jt) == (
        "JSON_TABLE(`data`, %s COLUMNS ("
        "`row_num` FOR ORDINALITY, "
        "`name` VARCHAR(10) PATH %s, "
        "NESTED PATH %s COLUMNS (`size` VARCHAR(32) PATH %s)))"
    )
    assert jt.args == ["$[*]", "$.name", "$.sizes[*]", "$"]


def test_json_table_statement_doc_and_path():
    jt = JsonTable(Raw("@json"), Raw("'$[*]'"), JsonTableOrdinalityColumn("i"))
    assert str(jt) == "JSON_TABLE(@json, '$[*]' COLUMNS (`i` FOR ORDINALITY))"
    assert jt.args == []


def test_json_table_str_doc_is_a_column():
    jt = JsonTable("people.tags", "$[*]", JsonTableOrdinalityColumn("i"))
    assert str(jt) == "JSON_TABLE(`people`.`tags`, %s COLUMNS (`i` FOR ORDINALITY))"
    assert jt.args == ["$[*]"]


def test_json_table_literal_doc_and_path():
    jt = JsonTable(Value("[1,2,3]"), "$[*]", JsonTableOrdinalityColumn("i"))
    assert str(jt) == "JSON_TABLE(%s, %s COLUMNS (`i` FOR ORDINALITY))"
    assert jt.args == ["[1,2,3]", "$[*]"]


def test_json_table_composed_in_select():
    jt = JsonTable(
        Column("data"),
        "$[*]",
        JsonTableColumn("name", "VARCHAR(50)", "$.name"),
        JsonTableColumn("age", "INT", "$.age", on_empty=JsonTableAction.NULL, on_error=JsonTableAction.default(0)),
    )
    sel = Select("jt.name", "jt.age", table=[Table("people"), Aliased(jt, alias="jt")])
    assert str(sel) == (
        "SELECT `jt`.`name`, `jt`.`age` FROM `people`, "
        "JSON_TABLE(`data`, %s COLUMNS (`name` VARCHAR(50) PATH %s, "
        "`age` INT PATH %s NULL ON EMPTY DEFAULT %s ON ERROR)) AS `jt`"
    )
    assert sel.args == ["$[*]", "$.name", "$.age", 0]


def test_json_table_joined():
    jt = JsonTable(Column("people.tags"), "$[*]", JsonTableColumn("tag", "VARCHAR(20)", "$"))
    j = Join(jt, alias="jt", on=Column("jt.tag") == "vip")

    sel = Select("people.id", table="people", join=[j])
    assert str(sel) == (
        "SELECT `people`.`id` FROM `people` "
        "JOIN JSON_TABLE(`people`.`tags`, %s COLUMNS (`tag` VARCHAR(20) PATH %s)) AS `jt` ON `jt`.`tag` = %s"
    )
    assert sel.args == ["$[*]", "$", "vip"]

    inner = InnerJoin(jt, alias="jt2", on=Column("jt2.tag") == "vip")
    assert str(inner).startswith("INNER JOIN JSON_TABLE(")


def test_json_table_joined_without_alias_raises():
    jt = JsonTable(Column("people.tags"), "$[*]", JsonTableColumn("tag", "VARCHAR(20)", "$"))
    with pytest.raises(AttributeError, match="When joining a subselect or JSON_TABLE, alias must be specified."):
        Join(jt)


# ---------------------------------------------------------------------------
# Composition: JsonSet in UPDATE ... SET, JsonValue and IsJson in WHERE
# ---------------------------------------------------------------------------


def test_composed_update_set_where_oracle_dialect():
    """Locks args/placeholder order under OracleSQLDialect's numbered, stateful placeholders."""
    upd = Update(
        "docs",
        set={"data": JsonSet(Column("data"), ("$.tag", Raw("'x'")))},
        where=(JsonValue(Column("data"), "$.id") == 1) & IsJson(Column("data")),
        dialect=OracleSQLDialect(),
    )

    assert str(upd) == (
        'UPDATE "docs" SET "data" = JSON_SET("data", :1, \'x\') WHERE (JSON_VALUE("data", :2) = :3 AND "data" IS JSON)'
    )
    assert upd.args == ["$.tag", "$.id", 1]
