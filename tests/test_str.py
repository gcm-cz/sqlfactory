"""Tests for the string functions added/fixed beyond the pre-existing 35 in tests/test_functions.py."""

import pytest

from sqlfactory import Column, Eq, Select, Update
from sqlfactory.func.str import (
    Char,
    CharacterLength,
    Elt,
    ExportSet,
    ExtractValue,
    Field,
    FindInSet,
    Format,
    FromBase64,
    Insert,
    Lcase,
    LengthB,
    LoadFile,
    Locate,
    MakeSet,
    Mid,
    NaturalSortKey,
    Position,
    Quote,
    RegexpInstr,
    RegexpReplace,
    RegexpSubstr,
    Soundex,
    Strcmp,
    Substr,
    Substring,
    ToChar,
    Trim,
    TrimDirection,
    TrimOracle,
    Ucase,
    UpdateXml,
    WeightString,
    WeightStringAs,
    WeightStringFlag,
)

# ---------------------------------------------------------------------------
# CHAR([...] USING charset)
# ---------------------------------------------------------------------------


def test_char_using_charset():
    func = Char(77, 97, using="utf8mb4")
    assert str(func) == "CHAR(%s, %s USING utf8mb4)"
    assert func.args == [77, 97]


def test_char_without_using_is_unchanged():
    func = Char(77)
    assert str(func) == "CHAR(%s)"
    assert func.args == [77]


def test_char_rejects_non_identifier_charset():
    with pytest.raises(ValueError, match="bare charset identifier"):
        Char(77, using="utf8mb4; DROP TABLE t")


# ---------------------------------------------------------------------------
# CHARACTER_LENGTH (synonym for CHAR_LENGTH)
# ---------------------------------------------------------------------------


def test_character_length():
    func = CharacterLength(Column("column1"))
    assert str(func) == "CHARACTER_LENGTH(`column1`)"
    assert func.args == []


def test_character_length_is_char_length_synonym():
    from sqlfactory.func.str import CharLength

    assert isinstance(CharacterLength("x"), CharLength)


# ---------------------------------------------------------------------------
# ELT
# ---------------------------------------------------------------------------


def test_elt():
    func = Elt(2, "a", "b", "c")
    assert str(func) == "ELT(%s, %s, %s, %s)"
    assert func.args == [2, "a", "b", "c"]


def test_elt_minimum_args():
    func = Elt(1, "a")
    assert str(func) == "ELT(%s, %s)"
    assert func.args == [1, "a"]


# ---------------------------------------------------------------------------
# EXPORT_SET
# ---------------------------------------------------------------------------


def test_export_set_minimal():
    func = ExportSet(5, "Y", "N")
    assert str(func) == "EXPORT_SET(%s, %s, %s)"
    assert func.args == [5, "Y", "N"]


def test_export_set_with_separator():
    func = ExportSet(5, "Y", "N", ",")
    assert str(func) == "EXPORT_SET(%s, %s, %s, %s)"
    assert func.args == [5, "Y", "N", ","]


def test_export_set_with_number_of_bits():
    func = ExportSet(5, "Y", "N", ",", 4)
    assert str(func) == "EXPORT_SET(%s, %s, %s, %s, %s)"
    assert func.args == [5, "Y", "N", ",", 4]


def test_export_set_number_of_bits_requires_separator():
    with pytest.raises(ValueError, match="number_of_bits"):
        ExportSet(5, "Y", "N", number_of_bits=4)


# ---------------------------------------------------------------------------
# EXTRACTVALUE / UPDATEXML
# ---------------------------------------------------------------------------


def test_extract_value():
    func = ExtractValue("<a><b>1</b></a>", "/a/b")
    assert str(func) == "EXTRACTVALUE(%s, %s)"
    assert func.args == ["<a><b>1</b></a>", "/a/b"]


def test_update_xml():
    func = UpdateXml("<a><b>1</b></a>", "/a/b", "<c>2</c>")
    assert str(func) == "UPDATEXML(%s, %s, %s)"
    assert func.args == ["<a><b>1</b></a>", "/a/b", "<c>2</c>"]


# ---------------------------------------------------------------------------
# FIELD / FIND_IN_SET / MAKE_SET
# ---------------------------------------------------------------------------


def test_field():
    func = Field("b", "a", "b", "c")
    assert str(func) == "FIELD(%s, %s, %s, %s)"
    assert func.args == ["b", "a", "b", "c"]


def test_find_in_set():
    func = FindInSet("b", "a,b,c")
    assert str(func) == "FIND_IN_SET(%s, %s)"
    assert func.args == ["b", "a,b,c"]


def test_make_set():
    func = MakeSet(5, "a", "b", "c")
    assert str(func) == "MAKE_SET(%s, %s, %s, %s)"
    assert func.args == [5, "a", "b", "c"]


# ---------------------------------------------------------------------------
# FORMAT
# ---------------------------------------------------------------------------


def test_format():
    func = Format(1234.5678, 2)
    assert str(func) == "FORMAT(%s, %s)"
    assert func.args == [1234.5678, 2]


def test_format_with_locale():
    func = Format(1234.5678, 2, "de_DE")
    assert str(func) == "FORMAT(%s, %s, %s)"
    assert func.args == [1234.5678, 2, "de_DE"]


# ---------------------------------------------------------------------------
# FROM_BASE64
# ---------------------------------------------------------------------------


def test_from_base64():
    func = FromBase64("aGVsbG8=")
    assert str(func) == "FROM_BASE64(%s)"
    assert func.args == ["aGVsbG8="]


# ---------------------------------------------------------------------------
# INSERT (string function)
# ---------------------------------------------------------------------------


def test_insert_function():
    func = Insert("hello world", 1, 5, "HELLO")
    assert str(func) == "INSERT(%s, %s, %s, %s)"
    assert func.args == ["hello world", 1, 5, "HELLO"]


# ---------------------------------------------------------------------------
# LCASE / UCASE (synonyms)
# ---------------------------------------------------------------------------


def test_lcase():
    func = Lcase("ABC")
    assert str(func) == "LCASE(%s)"
    assert func.args == ["ABC"]


def test_ucase():
    func = Ucase("abc")
    assert str(func) == "UCASE(%s)"
    assert func.args == ["abc"]


def test_lcase_is_lower_synonym():
    from sqlfactory.func.str import Lower

    assert isinstance(Lcase("x"), Lower)


def test_ucase_is_upper_synonym():
    from sqlfactory.func.str import Upper

    assert isinstance(Ucase("x"), Upper)


# ---------------------------------------------------------------------------
# LENGTHB / LOAD_FILE / NATURAL_SORT_KEY / QUOTE / SOUNDEX / STRCMP
# ---------------------------------------------------------------------------


def test_length_b():
    func = LengthB("ABC")
    assert str(func) == "LENGTHB(%s)"
    assert func.args == ["ABC"]


def test_load_file():
    func = LoadFile("/etc/hostname")
    assert str(func) == "LOAD_FILE(%s)"
    assert func.args == ["/etc/hostname"]


def test_natural_sort_key():
    func = NaturalSortKey("a10")
    assert str(func) == "NATURAL_SORT_KEY(%s)"
    assert func.args == ["a10"]


def test_quote():
    func = Quote("it's")
    assert str(func) == "QUOTE(%s)"
    assert func.args == ["it's"]


def test_soundex():
    func = Soundex("hello")
    assert str(func) == "SOUNDEX(%s)"
    assert func.args == ["hello"]


def test_strcmp():
    func = Strcmp("a", "b")
    assert str(func) == "STRCMP(%s, %s)"
    assert func.args == ["a", "b"]


# ---------------------------------------------------------------------------
# LOCATE (fixed: optional `pos`)
# ---------------------------------------------------------------------------


def test_locate_without_pos_is_unchanged():
    func = Locate("A", "ABC")
    assert str(func) == "LOCATE(%s, %s)"
    assert func.args == ["A", "ABC"]


def test_locate_with_pos():
    func = Locate("l", "hello", 4)
    assert str(func) == "LOCATE(%s, %s, %s)"
    assert func.args == ["l", "hello", 4]


# ---------------------------------------------------------------------------
# POSITION(substr IN str)
# ---------------------------------------------------------------------------


def test_position():
    func = Position("l", "hello")
    assert str(func) == "POSITION(%s IN %s)"
    assert func.args == ["l", "hello"]


def test_position_with_columns():
    func = Position(Column("needle"), Column("haystack"))
    assert str(func) == "POSITION(`needle` IN `haystack`)"
    assert func.args == []


# ---------------------------------------------------------------------------
# REGEXP_INSTR / REGEXP_REPLACE / REGEXP_SUBSTR
# ---------------------------------------------------------------------------


def test_regexp_instr():
    func = RegexpInstr("hello world", "wor")
    assert str(func) == "REGEXP_INSTR(%s, %s)"
    assert func.args == ["hello world", "wor"]


def test_regexp_replace():
    func = RegexpReplace("hello world", "wor", "X")
    assert str(func) == "REGEXP_REPLACE(%s, %s, %s)"
    assert func.args == ["hello world", "wor", "X"]


def test_regexp_substr():
    func = RegexpSubstr("hello world", "wor")
    assert str(func) == "REGEXP_SUBSTR(%s, %s)"
    assert func.args == ["hello world", "wor"]


# ---------------------------------------------------------------------------
# SUBSTR / SUBSTRING / MID (fixed: optional `length`)
# ---------------------------------------------------------------------------


def test_substr_without_length():
    func = Substr("ABC", 1)
    assert str(func) == "SUBSTR(%s, %s)"
    assert func.args == ["ABC", 1]


def test_substr_with_length_is_unchanged():
    func = Substr("ABC", 1, 2)
    assert str(func) == "SUBSTR(%s, %s, %s)"
    assert func.args == ["ABC", 1, 2]


def test_substring_without_length():
    func = Substring("ABC", 1)
    assert str(func) == "SUBSTRING(%s, %s)"
    assert func.args == ["ABC", 1]


def test_mid_without_length():
    func = Mid("hello", 2)
    assert str(func) == "MID(%s, %s)"
    assert func.args == ["hello", 2]


def test_mid_with_length_is_unchanged():
    func = Mid("ABC", 1, 2)
    assert str(func) == "MID(%s, %s, %s)"
    assert func.args == ["ABC", 1, 2]


# ---------------------------------------------------------------------------
# TO_CHAR (fixed: optional `fmt`)
# ---------------------------------------------------------------------------


def test_to_char_without_fmt_is_unchanged():
    func = ToChar("2024-01-01")
    assert str(func) == "TO_CHAR(%s)"
    assert func.args == ["2024-01-01"]


def test_to_char_with_fmt():
    func = ToChar(Column("created_at"), "YYYY-MM-DD")
    assert str(func) == "TO_CHAR(`created_at`, %s)"
    assert func.args == ["YYYY-MM-DD"]


# ---------------------------------------------------------------------------
# TRIM (fixed: full BOTH/LEADING/TRAILING [remstr] FROM grammar) / TRIM_ORACLE
# ---------------------------------------------------------------------------


def test_trim_plain_is_unchanged():
    func = Trim(" ABC ")
    assert str(func) == "TRIM(%s)"
    assert func.args == [" ABC "]


def test_trim_remstr_only():
    func = Trim("xxhelloxx", "x")
    assert str(func) == "TRIM(%s FROM %s)"
    assert func.args == ["x", "xxhelloxx"]


def test_trim_direction_only():
    func = Trim("  x  ", direction=TrimDirection.LEADING)
    assert str(func) == "TRIM(LEADING FROM %s)"
    assert func.args == ["  x  "]


def test_trim_direction_and_remstr():
    func = Trim(Column("q.error"), "\n", TrimDirection.TRAILING)
    assert str(func) == "TRIM(TRAILING %s FROM `q`.`error`)"
    assert func.args == ["\n"]


def test_trim_both_direction_explicit():
    func = Trim("xxhelloxx", "x", TrimDirection.BOTH)
    assert str(func) == "TRIM(BOTH %s FROM %s)"
    assert func.args == ["x", "xxhelloxx"]


def test_trim_oracle_plain():
    func = TrimOracle("  x  ")
    assert str(func) == "TRIM_ORACLE(%s)"
    assert func.args == ["  x  "]


def test_trim_oracle_full_form():
    func = TrimOracle("xxhelloxx", "x", TrimDirection.LEADING)
    assert str(func) == "TRIM_ORACLE(LEADING %s FROM %s)"
    assert func.args == ["x", "xxhelloxx"]


def test_trim_oracle_is_a_trim():
    assert isinstance(TrimOracle("x"), Trim)


# ---------------------------------------------------------------------------
# WEIGHT_STRING
# ---------------------------------------------------------------------------


def test_weight_string_plain():
    func = WeightString("x")
    assert str(func) == "WEIGHT_STRING(%s)"
    assert func.args == ["x"]


def test_weight_string_as_char():
    func = WeightString("x", as_type=WeightStringAs.CHAR, length=4)
    assert str(func) == "WEIGHT_STRING(%s AS CHAR(4))"
    assert func.args == ["x"]


def test_weight_string_as_binary():
    func = WeightString("x", as_type=WeightStringAs.BINARY, length=4)
    assert str(func) == "WEIGHT_STRING(%s AS BINARY(4))"
    assert func.args == ["x"]


def test_weight_string_level():
    func = WeightString("x", level=1)
    assert str(func) == "WEIGHT_STRING(%s LEVEL 1)"
    assert func.args == ["x"]


def test_weight_string_level_with_flag():
    func = WeightString("x", level=1, flag=WeightStringFlag.DESC)
    assert str(func) == "WEIGHT_STRING(%s LEVEL 1 DESC)"
    assert func.args == ["x"]


def test_weight_string_as_and_level_combined():
    func = WeightString("x", as_type=WeightStringAs.CHAR, length=4, level=1, flag=WeightStringFlag.REVERSE)
    assert str(func) == "WEIGHT_STRING(%s AS CHAR(4) LEVEL 1 REVERSE)"
    assert func.args == ["x"]


def test_weight_string_as_type_requires_length():
    with pytest.raises(ValueError, match="as_type"):
        WeightString("x", as_type=WeightStringAs.CHAR)


def test_weight_string_length_requires_as_type():
    with pytest.raises(ValueError, match="as_type"):
        WeightString("x", length=4)


def test_weight_string_flag_requires_level():
    with pytest.raises(ValueError, match="flag"):
        WeightString("x", flag=WeightStringFlag.DESC)


def test_weight_string_rejects_non_positive_length():
    with pytest.raises(ValueError, match="length"):
        WeightString("x", as_type=WeightStringAs.CHAR, length=0)


def test_weight_string_rejects_non_positive_level():
    with pytest.raises(ValueError, match="level"):
        WeightString("x", level=0)


# ---------------------------------------------------------------------------
# Integration with Select / Update
# ---------------------------------------------------------------------------


def test_string_functions_compose_in_select():
    q = Select(
        "id",
        Trim(Column("email"), " "),
        Position("@", Column("email")),
        table="users",
        where=Eq(RegexpReplace(Column("phone"), r"\D", ""), "5551234567"),
    )
    assert str(q) == (
        "SELECT `id`, TRIM(%s FROM `email`), POSITION(%s IN `email`) FROM `users` WHERE REGEXP_REPLACE(`phone`, %s, %s) = %s"
    )
    assert q.args == [" ", "@", r"\D", "", "5551234567"]


def test_string_functions_compose_in_update():
    u = Update("users").set("email", Trim(Column("email"), direction=TrimDirection.TRAILING))
    assert str(u) == "UPDATE `users` SET `email` = TRIM(TRAILING FROM `email`)"
    assert u.args == []
