from sqlfactory import Column, Raw
from sqlfactory.func.agg import AggregateFunction, Avg, BitAnd, BitOr, BitXor, Count, Max, Min, Std, Sum
from sqlfactory.func.control import If, IfNull, NullIf
from sqlfactory.func.str import (
    Ascii,
    Bin,
    BitLength,
    Char,
    CharLength,
    Chr,
    Concat,
    ConcatWs,
    Hex,
    InStr,
    Left,
    Length,
    Locate,
    Lower,
    Lpad,
    Ltrim,
    Mid,
    OctetLength,
    Ord,
    Repeat,
    Replace,
    Reverse,
    Right,
    RPad,
    RTrim,
    SFormat,
    Space,
    Substr,
    Substring,
    SubstringIndex,
    ToBase64,
    ToChar,
    Trim,
    Unhex,
    Upper,
)


def test_aggregate_function():
    agg_func = AggregateFunction("AGG", "column1")
    assert str(agg_func) == "AGG(`column1`)"
    assert agg_func.args == []


def test_avg():
    avg_func = Avg("column1")
    assert str(avg_func) == "AVG(`column1`)"
    assert avg_func.args == []


def test_bit_and():
    bit_and_func = BitAnd("column1")
    assert str(bit_and_func) == "BIT_AND(`column1`)"
    assert bit_and_func.args == []


def test_bit_or():
    bit_or_func = BitOr("column1")
    assert str(bit_or_func) == "BIT_OR(`column1`)"
    assert bit_or_func.args == []


def test_bit_xor():
    bit_xor_func = BitXor("column1")
    assert str(bit_xor_func) == "BIT_XOR(`column1`)"
    assert bit_xor_func.args == []


def test_count():
    count_func = Count("column1")
    assert str(count_func) == "COUNT(`column1`)"
    assert count_func.args == []


def test_count_distinct():
    count_func = Count("column1", distinct=True)
    assert str(count_func) == "COUNT(DISTINCT `column1`)"
    assert count_func.args == []

    count_func = Count("*", distinct=True)
    assert str(count_func) == "COUNT(DISTINCT *)"
    assert count_func.args == []

    count_func = Count(Column("foo"), distinct=True)
    assert str(count_func) == "COUNT(DISTINCT `foo`)"
    assert count_func.args == []


def test_max():
    max_func = Max("column1")
    assert str(max_func) == "MAX(`column1`)"
    assert max_func.args == []


def test_min():
    min_func = Min("column1")
    assert str(min_func) == "MIN(`column1`)"
    assert min_func.args == []


def test_std():
    std_func = Std("column1")
    assert str(std_func) == "STD(`column1`)"
    assert std_func.args == []


def test_sum():
    sum_func = Sum("column1")
    assert str(sum_func) == "SUM(`column1`)"
    assert sum_func.args == []


def test_sum_expression():
    sum_func = Sum(Column("column1") + Column("column2"))
    assert str(sum_func) == "SUM((`column1` + `column2`))"
    assert sum_func.args == []

    sum_func = Sum(Raw("column1 + %s", 123))
    assert str(sum_func) == "SUM(column1 + %s)"
    assert sum_func.args == [123]


def test_ifnull():
    ifnull_func = IfNull(Column("column1"), "default")
    assert str(ifnull_func) == "IFNULL(`column1`, %s)"
    assert ifnull_func.args == ["default"]


def test_nullif():
    nullif_func = NullIf(Column("column1"), Column("column2"))
    assert str(nullif_func) == "NULLIF(`column1`, `column2`)"
    assert nullif_func.args == []


def test_if():
    if_func = If(Column("column1") == Column("column2"), "true_value", "false_value")
    assert str(if_func) == "IF(`column1` = `column2`, %s, %s)"
    assert if_func.args == ["true_value", "false_value"]


def test_ascii():
    ascii_func = Ascii(Column("column1"))
    assert str(ascii_func) == "ASCII(`column1`)"
    assert ascii_func.args == []


def test_bin():
    bin_func = Bin(Column("column1"))
    assert str(bin_func) == "BIN(`column1`)"
    assert bin_func.args == []


def test_bit_length():
    bit_length_func = BitLength(Column("column1"))
    assert str(bit_length_func) == "BIT_LENGTH(`column1`)"
    assert bit_length_func.args == []


def test_char():
    char_func = Char(Column("column1"))
    assert str(char_func) == "CHAR(`column1`)"
    assert char_func.args == []


def test_char_length():
    char_length_func = CharLength(Column("column1"))
    assert str(char_length_func) == "CHAR_LENGTH(`column1`)"
    assert char_length_func.args == []


def test_chr():
    chr_func = Chr(Column("column1"))
    assert str(chr_func) == "CHR(`column1`)"
    assert chr_func.args == []


def test_concat():
    concat_func = Concat(Column("column1"), Column("column2"))
    assert str(concat_func) == "CONCAT(`column1`, `column2`)"
    assert concat_func.args == []


def test_concat_ws():
    concat_ws_func = ConcatWs("separator", Column("column1"), Column("column2"))
    assert str(concat_ws_func) == "CONCAT_WS(%s, `column1`, `column2`)"
    assert concat_ws_func.args == ["separator"]


def test_repeat():
    repeat_func = Repeat("A", 3)
    assert str(repeat_func) == "REPEAT(%s, %s)"
    assert repeat_func.args == ["A", 3]


def test_replace():
    replace_func = Replace("ABC", "A", "B")
    assert str(replace_func) == "REPLACE(%s, %s, %s)"
    assert replace_func.args == ["ABC", "A", "B"]


def test_reverse():
    reverse_func = Reverse("ABC")
    assert str(reverse_func) == "REVERSE(%s)"
    assert reverse_func.args == ["ABC"]


def test_right():
    right_func = Right("ABC", 2)
    assert str(right_func) == "RIGHT(%s, %s)"
    assert right_func.args == ["ABC", 2]


def test_rpad():
    rpad_func = RPad("A", 3, "B")
    assert str(rpad_func) == "RPAD(%s, %s, %s)"
    assert rpad_func.args == ["A", 3, "B"]


def test_rtrim():
    rtrim_func = RTrim("ABC   ")
    assert str(rtrim_func) == "RTRIM(%s)"
    assert rtrim_func.args == ["ABC   "]


def test_sformat():
    sformat_func = SFormat("A%sC", "B")
    assert str(sformat_func) == "SFORMAT(%s, %s)"
    assert sformat_func.args == ["A%sC", "B"]


def test_space():
    space_func = Space(3)
    assert str(space_func) == "SPACE(%s)"
    assert space_func.args == [3]


def test_substr():
    substr_func = Substr("ABC", 1, 2)
    assert str(substr_func) == "SUBSTR(%s, %s, %s)"
    assert substr_func.args == ["ABC", 1, 2]


def test_substring():
    substring_func = Substring("ABC", 1, 2)
    assert str(substring_func) == "SUBSTRING(%s, %s, %s)"
    assert substring_func.args == ["ABC", 1, 2]


def test_substring_index():
    substring_index_func = SubstringIndex("ABC", "B", 1)
    assert str(substring_index_func) == "SUBSTRING_INDEX(%s, %s, %s)"
    assert substring_index_func.args == ["ABC", "B", 1]


def test_to_base64():
    to_base64_func = ToBase64("ABC")
    assert str(to_base64_func) == "TO_BASE64(%s)"
    assert to_base64_func.args == ["ABC"]


def test_to_char():
    to_char_func = ToChar(123)
    assert str(to_char_func) == "TO_CHAR(%s)"
    assert to_char_func.args == [123]


def test_trim():
    trim_func = Trim(" ABC ")
    assert str(trim_func) == "TRIM(%s)"
    assert trim_func.args == [" ABC "]


def test_unhex():
    unhex_func = Unhex("414243")
    assert str(unhex_func) == "UNHEX(%s)"
    assert unhex_func.args == ["414243"]


def test_upper():
    upper_func = Upper("abc")
    assert str(upper_func) == "UPPER(%s)"
    assert upper_func.args == ["abc"]


def test_ord():
    ord_func = Ord("A")
    assert str(ord_func) == "ORD(%s)"
    assert ord_func.args == ["A"]


def test_octet_length():
    octet_length_func = OctetLength("ABC")
    assert str(octet_length_func) == "OCTET_LENGTH(%s)"
    assert octet_length_func.args == ["ABC"]


def test_mid():
    mid_func = Mid("ABC", 1, 2)
    assert str(mid_func) == "MID(%s, %s, %s)"
    assert mid_func.args == ["ABC", 1, 2]


def test_ltrim():
    ltrim_func = Ltrim(" ABC ")
    assert str(ltrim_func) == "LTRIM(%s)"
    assert ltrim_func.args == [" ABC "]


def test_lpad():
    lpad_func = Lpad("A", 3, "B")
    assert str(lpad_func) == "LPAD(%s, %s, %s)"
    assert lpad_func.args == ["A", 3, "B"]


def test_lower():
    lower_func = Lower("ABC")
    assert str(lower_func) == "LOWER(%s)"
    assert lower_func.args == ["ABC"]


def test_locate():
    locate_func = Locate("A", "ABC")
    assert str(locate_func) == "LOCATE(%s, %s)"
    assert locate_func.args == ["A", "ABC"]


def test_length():
    length_func = Length("ABC")
    assert str(length_func) == "LENGTH(%s)"
    assert length_func.args == ["ABC"]


def test_left():
    left_func = Left("ABC", 2)
    assert str(left_func) == "LEFT(%s, %s)"
    assert left_func.args == ["ABC", 2]


def test_instr():
    instr_func = InStr("ABC", "A")
    assert str(instr_func) == "INSTR(%s, %s)"
    assert instr_func.args == ["ABC", "A"]


def test_hex():
    hex_func = Hex("ABC")
    assert str(hex_func) == "HEX(%s)"
    assert hex_func.args == ["ABC"]


def test_function_expression():
    expr = IfNull(Column("column1"), 0) + 1
    assert str(expr) == "(IFNULL(`column1`, %s) + %s)"
    assert expr.args == [0, 1]


def test_multiple_expressions():
    base_price_sum = Sum("table1.base_price") + Sum("table2.base_price")
    expr = If(
        Column("discount_price") != None,
        base_price_sum - Column("discount_price"),
        If(
            Column("discount_percentage") != None,
            base_price_sum * ((Column("discount_percentage") / 100) * -1 + 1),
            base_price_sum,
        ),
    )

    assert str(expr) == (
        "IF("
        "`discount_price` IS NOT %s, "
        "((SUM(`table1`.`base_price`) + SUM(`table2`.`base_price`)) - `discount_price`), "
        "IF(`discount_percentage` IS NOT %s, "
        "((SUM(`table1`.`base_price`) + SUM(`table2`.`base_price`)) * (((`discount_percentage` / %s) * %s) + %s)), "
        "(SUM(`table1`.`base_price`) + SUM(`table2`.`base_price`))"
        ")"
        ")"
    )
    assert expr.args == [None, None, 100, -1, 1]
