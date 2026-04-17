import pytest

from arithmetic import (
    add_twos,
    binary_to_unsigned,
    direct_binary,
    div_direct,
    format_int_binary,
    mul_direct,
    sub_twos,
    unsigned_binary,
)


def test_add_sub_twos():
    add_bits, add_value = add_twos(13, -5, 8)
    sub_bits, sub_value = sub_twos(13, -5, 8)
    assert add_value == 8
    assert sub_value == 18
    assert "".join(str(b) for b in add_bits) == "00001000"
    assert "".join(str(b) for b in sub_bits) == "00010010"


def test_mul_direct_sign_and_value():
    bits, value = mul_direct(-6, 3, 8)
    assert bits[0] == 1
    assert value == -18


def test_div_direct_precision_and_sign():
    text, value = div_direct(-10, 4, precision=5)
    assert text == "-2.50000"
    assert value == -2.5


def test_div_direct_by_zero():
    with pytest.raises(ZeroDivisionError):
        div_direct(7, 0)


def test_binary_helpers():
    assert format_int_binary(-1, 8) == "11111111"
    assert direct_binary(-3, 8) == "10000011"
    assert unsigned_binary(9, 8) == "00001001"
    assert binary_to_unsigned("1011") == 11


def test_binary_parse_error():
    with pytest.raises(ValueError):
        binary_to_unsigned("10a1")

