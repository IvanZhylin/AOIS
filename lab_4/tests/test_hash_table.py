"""Тесты хеш-таблицы и CRUD."""

import unittest

from src.demo_data import MATH_TERMS
from src.hash_table import DuplicateKeyError, HashTable, KeyNotFoundError


class TestHashTable(unittest.TestCase):
    """Операции create, read, update, delete и статистика."""

    def setUp(self) -> None:
        self.table = HashTable(size=20, base_address=0)

    def test_create_and_read(self) -> None:
        self.table.create("интеграл", "анализ")
        self.assertEqual(self.table.read("интеграл"), "анализ")
        self.assertTrue(self.table.contains("интеграл"))

    def test_duplicate_key(self) -> None:
        self.table.create("предел", "анализ")
        with self.assertRaises(DuplicateKeyError):
            self.table.create("предел", "другое")

    def test_update(self) -> None:
        self.table.create("вектор", "алгебра")
        self.table.update("вектор", "линейная алгебра")
        self.assertEqual(self.table.read("вектор"), "линейная алгебра")

    def test_read_missing(self) -> None:
        with self.assertRaises(KeyNotFoundError):
            self.table.read("отсутствует")

    def test_delete_single_entry(self) -> None:
        self.table.create("теорема", "геометрия")
        self.table.delete("теорема")
        self.assertFalse(self.table.contains("теорема"))

    def test_collision_chain_in_bucket(self) -> None:
        """Три термина на «ин» попадают в одну корзину."""
        self.table.create("интеграл", "a")
        self.table.create("инверсия", "b")
        self.table.create("индукция", "c")
        h = self.table.compute_h("интеграл")
        self.assertEqual(self.table.compute_h("инверсия"), h)
        self.assertEqual(self.table.read("инверсия"), "b")

    def test_collision_pr_bucket(self) -> None:
        self.table.create("производная", "1")
        self.table.create("прогрессия", "2")
        self.assertEqual(self.table.compute_h("производная"), self.table.compute_h("прогрессия"))

    def test_delete_from_chain_middle(self) -> None:
        self.table.create("интеграл", "a")
        self.table.create("инверсия", "b")
        self.table.create("индукция", "c")
        self.table.delete("инверсия")
        self.assertFalse(self.table.contains("инверсия"))
        self.assertEqual(self.table.read("интеграл"), "a")
        self.assertEqual(self.table.read("индукция"), "c")

    def test_delete_last_in_chain(self) -> None:
        self.table.create("производная", "1")
        self.table.create("прогрессия", "2")
        self.table.delete("прогрессия")
        self.assertEqual(self.table.read("производная"), "1")

    def test_reuse_deleted_slot(self) -> None:
        self.table.create("лимит", "x")
        entry = self.table.search_entry("лимит")
        assert entry is not None
        entry.deleted = True
        entry.occupied = False
        self.table._active_count = 0
        self.table.create("лимит", "новое")
        self.assertEqual(self.table.read("лимит"), "новое")

    def test_load_factor(self) -> None:
        self.table.create("аа", "1")  # noqa: ключ из двух «а»
        self.assertAlmostEqual(self.table.load_factor(), 1 / 20)

    def test_keys_and_dump(self) -> None:
        for key, value in list(MATH_TERMS.items())[:5]:
            self.table.create(key, value)
        self.assertEqual(len(self.table.keys()), 5)
        dump = self.table.dump()
        self.assertIn("Коэффициент заполнения", dump)

    def test_collision_stats_demo_data(self) -> None:
        for key, value in MATH_TERMS.items():
            self.table.create(key, value)
        buckets, chained = self.table.collision_stats()
        self.assertGreaterEqual(buckets, 2)
        self.assertGreaterEqual(chained, 3)
        self.assertGreaterEqual(self.table.count, 10)

    def test_invalid_table_size(self) -> None:
        with self.assertRaises(ValueError):
            HashTable(size=0)

    def test_search_entry_none(self) -> None:
        self.assertIsNone(self.table.search_entry("нет"))

    def test_format_entry(self) -> None:
        self.table.create("вектор", "данные")
        entry = self.table.search_entry("вектор")
        assert entry is not None
        text = self.table.format_entry(entry, 0)
        self.assertIn("ID='вектор'", text)


if __name__ == "__main__":
    unittest.main()
