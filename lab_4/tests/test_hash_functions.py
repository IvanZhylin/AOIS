"""Тесты функций хеширования."""

import unittest

from src.hash_functions import (
    BASE,
    RUSSIAN_ALPHABET,
    hash_address,
    key_to_value,
    letter_value,
)


class TestHashFunctions(unittest.TestCase):
    """Проверка V и h по примерам методички."""

    def test_alphabet_size(self) -> None:
        self.assertEqual(len(RUSSIAN_ALPHABET), 33)
        self.assertEqual(BASE, 33)

    def test_letter_value_examples(self) -> None:
        self.assertEqual(letter_value("А"), 0)
        self.assertEqual(letter_value("В"), 2)
        self.assertEqual(letter_value("я"), 32)

    def test_key_to_value_vyatkin(self) -> None:
        # V[Вя] = 2·33 + 32 = 98
        self.assertEqual(key_to_value("Вяткин"), 98)

    def test_key_to_value_tretyak(self) -> None:
        # V[Тр] = 19·33 + 17 = 644
        self.assertEqual(key_to_value("Третьяк"), 644)

    def test_hash_address(self) -> None:
        self.assertEqual(hash_address(98, 20, 0), 18)
        self.assertEqual(hash_address(644, 20, 0), 4)

    def test_hash_address_with_base(self) -> None:
        self.assertEqual(hash_address(98, 20, 5), 23)

    def test_short_key_raises(self) -> None:
        with self.assertRaises(ValueError):
            key_to_value("А")

    def test_invalid_letter_raises(self) -> None:
        with self.assertRaises(ValueError):
            letter_value("1")

    def test_invalid_table_size(self) -> None:
        with self.assertRaises(ValueError):
            hash_address(10, 0, 0)


if __name__ == "__main__":
    unittest.main()
