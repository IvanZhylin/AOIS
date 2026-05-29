"""Тесты модели записи."""

import unittest

from src.models import HashEntry


class TestHashEntry(unittest.TestCase):
    def test_clone_payload(self) -> None:
        source = HashEntry(key="б", data="данные_b", collision=True)
        target = HashEntry(key="а", data="данные_a")
        target.clone_payload_from(source)
        self.assertEqual(target.key, "б")
        self.assertEqual(target.data, "данные_b")
        self.assertTrue(target.collision)


if __name__ == "__main__":
    unittest.main()
