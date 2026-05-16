import unittest
from src.bits import (
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


class TestBits(unittest.TestCase):
    def test_unsigned_roundtrip(self):
        bits = int_to_bits_unsigned(37, 8)
        self.assertEqual(bits, [0, 0, 1, 0, 0, 1, 0, 1])
        self.assertEqual(bits_to_unsigned(bits), 37)

    def test_direct_and_complements_for_negative(self):
        direct = int_to_direct_code(-5, 8)
        ones = direct_to_ones(direct)
        twos = direct_to_twos(direct)
        self.assertEqual(direct, [1, 0, 0, 0, 0, 1, 0, 1])
        self.assertEqual(ones, [1, 1, 1, 1, 1, 0, 1, 0])
        self.assertEqual(twos, [1, 1, 1, 1, 1, 0, 1, 1])
        self.assertEqual(direct_code_to_int(direct), -5)

    def test_twos_roundtrip_positive_and_negative(self):
        self.assertEqual(twos_to_int(int_to_twos(15, 8)), 15)
        self.assertEqual(twos_to_int(int_to_twos(-15, 8)), -15)

    def test_add_bit_arrays_carry(self):
        result, carry = add_bit_arrays([1, 1, 1, 1], [0, 0, 0, 1])
        self.assertEqual(result, [0, 0, 0, 0])
        self.assertEqual(carry, 1)

    def test_bits_error_paths(self):
        with self.assertRaises(ValueError):
            int_to_bits_unsigned(-1, 8)
        with self.assertRaises(OverflowError):
            int_to_bits_unsigned(256, 8)
        with self.assertRaises(ValueError):
            add_bit_arrays([0, 1], [1])
        with self.assertRaises(OverflowError):
            int_to_direct_code(1000, 8)
        with self.assertRaises(OverflowError):
            int_to_twos(200, 8)


if __name__ == "__main__":
    unittest.main()
