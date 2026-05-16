import unittest
from src.ieee754 import (
    add_float32,
    div_float32,
    float_to_ieee754_bits,
    ieee754_bits_to_float,
    mul_float32,
    sub_float32,
)


class TestIEEE754(unittest.TestCase):
    def test_float_roundtrip_simple(self):
        bits = float_to_ieee754_bits(5.75)
        value = ieee754_bits_to_float(bits)
        self.assertEqual(bits[0], 0)
        self.assertAlmostEqual(value, 5.75, places=6)

    def test_float_negative(self):
        bits = float_to_ieee754_bits(-2.5)
        value = ieee754_bits_to_float(bits)
        self.assertEqual(bits[0], 1)
        self.assertAlmostEqual(value, -2.5, places=6)

    def test_float_operations(self):
        _, add_val = add_float32(3.5, 1.25)
        _, sub_val = sub_float32(3.5, 1.25)
        _, mul_val = mul_float32(3.5, 1.25)
        _, div_val = div_float32(3.5, 1.25)
        self.assertAlmostEqual(add_val, 4.75, places=6)
        self.assertAlmostEqual(sub_val, 2.25, places=6)
        self.assertAlmostEqual(mul_val, 4.375, places=6)
        self.assertAlmostEqual(div_val, 2.8, places=6)

    def test_div_zero_error(self):
        with self.assertRaises(ZeroDivisionError):
            div_float32(1.0, 0.0)

    def test_ieee754_unsupported_values(self):
        with self.assertRaises(OverflowError):
            float_to_ieee754_bits(1e39)
        with self.assertRaises(OverflowError):
            ieee754_bits_to_float([0] + [1] * 8 + [0] * 23)


if __name__ == "__main__":
    unittest.main()
