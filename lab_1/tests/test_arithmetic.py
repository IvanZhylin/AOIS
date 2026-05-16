import unittest
from src.arithmetic import (
    add_twos,
    binary_to_unsigned,
    direct_binary,
    div_direct,
    format_int_binary,
    mul_direct,
    sub_twos,
    unsigned_binary,
)


class TestArithmetic(unittest.TestCase):
    def test_add_sub_twos(self):
        add_bits, add_value = add_twos(13, -5, 8)
        sub_bits, sub_value = sub_twos(13, -5, 8)
        self.assertEqual(add_value, 8)
        self.assertEqual(sub_value, 18)
        self.assertEqual("".join(str(b) for b in add_bits), "00001000")
        self.assertEqual("".join(str(b) for b in sub_bits), "00010010")

    def test_mul_direct_sign_and_value(self):
        bits, value = mul_direct(-6, 3, 8)
        self.assertEqual(bits[0], 1)
        self.assertEqual(value, -18)

    def test_div_direct_precision_and_sign(self):
        text, value = div_direct(-10, 4, precision=5)
        self.assertEqual(text, "-2.50000")
        self.assertEqual(value, -2.5)

    def test_div_direct_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            div_direct(7, 0)

    def test_binary_helpers(self):
        self.assertEqual(format_int_binary(-1, 8), "11111111")
        self.assertEqual(direct_binary(-3, 8), "10000011")
        self.assertEqual(unsigned_binary(9, 8), "00001001")
        self.assertEqual(binary_to_unsigned("1011"), 11)

    def test_binary_parse_error(self):
        with self.assertRaises(ValueError):
            binary_to_unsigned("10a1")


if __name__ == "__main__":
    unittest.main()
