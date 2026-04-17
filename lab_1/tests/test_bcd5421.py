import pytest

from bcd5421 import add_5421, decode_5421, encode_5421


def test_encode_decode_roundtrip():
    bits = encode_5421(259)
    assert bits == [0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0]
    assert decode_5421(bits) == 259


def test_add_5421():
    bits, value = add_5421(259, 76)
    assert value == 335
    assert decode_5421(bits) == 335


def test_bcd_validation():
    with pytest.raises(ValueError):
        decode_5421([1, 1, 1])
    with pytest.raises(ValueError):
        add_5421(-1, 5)

