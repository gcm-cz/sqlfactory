from sqlbuilder import Column
from sqlbuilder.func.agg import AggregateFunction, Avg, BitAnd, BitOr, BitXor, Count, Max, Min, Std, Sum
from sqlbuilder.func.control import IfNull, NullIf, If
from sqlbuilder.func.str import Ascii, Bin, BitLength, Char, CharLength, Chr, Concat, ConcatWs


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
