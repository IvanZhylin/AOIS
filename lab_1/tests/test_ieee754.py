import pytest

from ieee754 import (
    add_float32,
    div_float32,
    float_to_ieee754_bits,
    ieee754_bits_to_float,
    mul_float32,
    sub_float32,
)


def test_float_roundtrip_simple():
    bits = float_to_ieee754_bits(5.75)
    value = ieee754_bits_to_float(bits)
    assert bits[0] == 0
    assert abs(value - 5.75) < 1e-6


def test_float_negative():
    bits = float_to_ieee754_bits(-2.5)
    value = ieee754_bits_to_float(bits)
    assert bits[0] == 1
    assert abs(value + 2.5) < 1e-6


def test_float_operations():
    _, add_val = add_float32(3.5, 1.25)
    _, sub_val = sub_float32(3.5, 1.25)
    _, mul_val = mul_float32(3.5, 1.25)
    _, div_val = div_float32(3.5, 1.25)
    assert abs(add_val - 4.75) < 1e-6
    assert abs(sub_val - 2.25) < 1e-6
    assert abs(mul_val - 4.375) < 1e-6
    assert abs(div_val - 2.8) < 1e-6


def test_div_zero_error():
    with pytest.raises(ZeroDivisionError):
        div_float32(1.0, 0.0)


def test_ieee754_unsupported_values():
    with pytest.raises(OverflowError):
        float_to_ieee754_bits(1e39)
    with pytest.raises(OverflowError):
        ieee754_bits_to_float([0] + [1] * 8 + [0] * 23)

