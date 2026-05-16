import unittest
from src.bcd5421 import add_5421, decode_5421, encode_5421


class TestBCD5421(unittest.TestCase):
    def test_encode_decode_roundtrip(self):
        bits = encode_5421(259)
        self.assertEqual(bits, [0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0])
        self.assertEqual(decode_5421(bits), 259)

    def test_add_5421(self):
        bits, value = add_5421(259, 76)
        self.assertEqual(value, 335)
        self.assertEqual(decode_5421(bits), 335)

    def test_bcd_validation(self):
        with self.assertRaises(ValueError):
            decode_5421([1, 1, 1])
        with self.assertRaises(ValueError):
            add_5421(-1, 5)


if __name__ == "__main__":
    unittest.main()
