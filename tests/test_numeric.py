from sqlfactory.func.numeric import (
    Abs,
    ACos,
    ASin,
    ATan,
    ATan2,
    BitCount,
    Ceil,
    Ceiling,
    Conv,
    Cos,
    Cot,
    Crc32,
    Crc32C,
    Degrees,
    Div,
    Exp,
    Floor,
    Greatest,
    Least,
    Ln,
    Log,
    Log2,
    Log10,
    Mod,
    Oct,
    Pi,
    Pow,
    Power,
    Radians,
    Rand,
    Round,
    Sign,
    Sin,
    Sqrt,
    Tan,
    Truncate,
)


def test_div():
    div_func = Div(1, 2)
    assert str(div_func) == "DIV(%s, %s)"
    assert div_func.args == [1, 2]


def test_abs():
    abs_func = Abs(1)
    assert str(abs_func) == "ABS(%s)"
    assert abs_func.args == [1]


def test_acos():
    acos_func = ACos(1)
    assert str(acos_func) == "ACOS(%s)"
    assert acos_func.args == [1]


def test_asin():
    asin_func = ASin(1)
    assert str(asin_func) == "ASIN(%s)"
    assert asin_func.args == [1]


def test_atan():
    atan_func = ATan(1)
    assert str(atan_func) == "ATAN(%s)"
    assert atan_func.args == [1]


def test_atan2():
    atan2_func = ATan2(1, 2)
    assert str(atan2_func) == "ATAN2(%s, %s)"
    assert atan2_func.args == [1, 2]


def test_ceil():
    ceil_func = Ceil(1.5)
    assert str(ceil_func) == "CEIL(%s)"
    assert ceil_func.args == [1.5]


def test_ceiling():
    ceiling_func = Ceiling(1.5)
    assert str(ceiling_func) == "CEILING(%s)"
    assert ceiling_func.args == [1.5]


def test_cos():
    cos_func = Cos(1)
    assert str(cos_func) == "COS(%s)"
    assert cos_func.args == [1]


def test_cot():
    cot_func = Cot(1)
    assert str(cot_func) == "COT(%s)"
    assert cot_func.args == [1]


def test_conv():
    conv_func = Conv(42, 10, 16)
    assert str(conv_func) == "CONV(%s, %s, %s)"
    assert conv_func.args == [42, 10, 16]


def test_crc32():
    crc32_func = Crc32(42)
    assert str(crc32_func) == "CRC32(%s)"
    assert crc32_func.args == [42]


def test_crc32c():
    crc32c_func = Crc32C(42)
    assert str(crc32c_func) == "CRC32C(%s)"
    assert crc32c_func.args == [42]


def test_degrees():
    degrees_func = Degrees(1)
    assert str(degrees_func) == "DEGREES(%s)"
    assert degrees_func.args == [1]


def test_exp():
    exp_func = Exp(1)
    assert str(exp_func) == "EXP(%s)"
    assert exp_func.args == [1]


def test_floor():
    floor_func = Floor(1.5)
    assert str(floor_func) == "FLOOR(%s)"
    assert floor_func.args == [1.5]


def test_greatest():
    greatest_func = Greatest(1, 2, 3)
    assert str(greatest_func) == "GREATEST(%s, %s, %s)"
    assert greatest_func.args == [1, 2, 3]


def test_least():
    least_func = Least(1, 2, 3)
    assert str(least_func) == "LEAST(%s, %s, %s)"
    assert least_func.args == [1, 2, 3]


def test_log():
    log_func = Log(1)
    assert str(log_func) == "LOG(%s)"
    assert log_func.args == [1]

    log_func = Log(1, 2)
    assert str(log_func) == "LOG(%s, %s)"
    assert log_func.args == [1, 2]


def test_log10():
    log10_func = Log10(1)
    assert str(log10_func) == "LOG10(%s)"
    assert log10_func.args == [1]


def test_log2():
    log2_func = Log2(1)
    assert str(log2_func) == "LOG2(%s)"
    assert log2_func.args == [1]


def test_ln():
    ln_func = Ln(1)
    assert str(ln_func) == "LN(%s)"
    assert ln_func.args == [1]


def test_mod():
    mod_func = Mod(1, 2)
    assert str(mod_func) == "MOD(%s, %s)"
    assert mod_func.args == [1, 2]


def test_oct():
    oct_func = Oct(42)
    assert str(oct_func) == "OCT(%s)"
    assert oct_func.args == [42]


def test_pi():
    pi_func = Pi()
    assert str(pi_func) == "PI()"
    assert pi_func.args == []


def test_pow():
    pow_func = Pow(2, 3)
    assert str(pow_func) == "POW(%s, %s)"
    assert pow_func.args == [2, 3]


def test_power():
    pow_func = Power(2, 3)
    assert str(pow_func) == "POWER(%s, %s)"
    assert pow_func.args == [2, 3]


def test_radians():
    radians_func = Radians(1)
    assert str(radians_func) == "RADIANS(%s)"
    assert radians_func.args == [1]


def test_rand():
    rand_func = Rand()
    assert str(rand_func) == "RAND()"
    assert rand_func.args == []


def test_round():
    round_func = Round(1.5)
    assert str(round_func) == "ROUND(%s)"
    assert round_func.args == [1.5]


def test_sign():
    sign_func = Sign(-1)
    assert str(sign_func) == "SIGN(%s)"
    assert sign_func.args == [-1]


def test_sin():
    sin_func = Sin(1)
    assert str(sin_func) == "SIN(%s)"
    assert sin_func.args == [1]


def test_sqrt():
    sqrt_func = Sqrt(4)
    assert str(sqrt_func) == "SQRT(%s)"
    assert sqrt_func.args == [4]


def test_tan():
    tan_func = Tan(1)
    assert str(tan_func) == "TAN(%s)"
    assert tan_func.args == [1]


def test_truncate():
    truncate_func = Truncate(1.5, 1)
    assert str(truncate_func) == "TRUNCATE(%s, %s)"
    assert truncate_func.args == [1.5, 1]


def test_bitcount():
    bitcount_func = BitCount(42)
    assert str(bitcount_func) == "BIT_COUNT(%s)"
    assert bitcount_func.args == [42]
