import pytest

from bits import (
    add_bit_arrays,
    bits_to_unsigned,
    direct_code_to_int,
    direct_to_ones,
    direct_to_twos,
    int_to_bits_unsigned,
    int_to_direct_code,
    int_to_twos,
    twos_to_int,
)


def test_unsigned_roundtrip():
    bits = int_to_bits_unsigned(37, 8)
    assert bits == [0, 0, 1, 0, 0, 1, 0, 1]
    assert bits_to_unsigned(bits) == 37


def test_direct_and_complements_for_negative():
    direct = int_to_direct_code(-5, 8)
    ones = direct_to_ones(direct)
    twos = direct_to_twos(direct)
    assert direct == [1, 0, 0, 0, 0, 1, 0, 1]
    assert ones == [1, 1, 1, 1, 1, 0, 1, 0]
    assert twos == [1, 1, 1, 1, 1, 0, 1, 1]
    assert direct_code_to_int(direct) == -5


def test_twos_roundtrip_positive_and_negative():
    assert twos_to_int(int_to_twos(15, 8)) == 15
    assert twos_to_int(int_to_twos(-15, 8)) == -15


def test_add_bit_arrays_carry():
    result, carry = add_bit_arrays([1, 1, 1, 1], [0, 0, 0, 1])
    assert result == [0, 0, 0, 0]
    assert carry == 1


def test_bits_error_paths():
    with pytest.raises(ValueError):
        int_to_bits_unsigned(-1, 8)
    with pytest.raises(OverflowError):
        int_to_bits_unsigned(256, 8)
    with pytest.raises(ValueError):
        add_bit_arrays([0, 1], [1])
    with pytest.raises(OverflowError):
        int_to_direct_code(1000, 8)
    with pytest.raises(OverflowError):
        int_to_twos(200, 8)

