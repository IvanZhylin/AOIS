"""Консольная демонстрация операций с хеш-таблицей."""

from src.demo_data import MATH_TERMS
from src.hash_table import DuplicateKeyError, HashTable, KeyNotFoundError


def run() -> None:
    """Построить таблицу, выполнить CRUD и вывести состояние."""
    table = HashTable(size=20, base_address=0)

    print("=== Лабораторная работа №6: хеш-таблица (математика) ===\n")
    print("Загрузка терминов...")
    for term, definition in MATH_TERMS.items():
        v = table.compute_v(term)
        h = table.compute_h(term)
        table.create(term, definition)
        print(f"  {term}: V={v}, h={h}")

    collisions, chained = table.collision_stats()
    print(
        f"\nКоллизий (корзин с цепочкой > 1): {collisions}, "
        f"записей в цепочках: {chained}"
    )
    print(f"Коэффициент заполнения: {table.load_factor():.4f}\n")
    print(table.dump())

    sample_key = "интеграл"
    print(f"\n--- Поиск: {sample_key} ---")
    print(f"  {table.read(sample_key)}")

    print("\n--- Обновление: производная ---")
    table.update("производная", "Скорость изменения функции; дифференциальное исчисление")
    print(f"  {table.read('производная')}")

    print("\n--- Контроль дубликата ---")
    try:
        table.create("интеграл", "дубликат")
    except DuplicateKeyError as err:
        print(f"  Ожидаемо: {err}")

    print("\n--- Удаление: тождество ---")
    table.delete("тождество")
    print(f"  Содержит «тождество»? {table.contains('тождество')}")

    print("\n--- Удаление несуществующего ключа ---")
    try:
        table.delete("несуществующий")
    except KeyNotFoundError as err:
        print(f"  Ожидаемо: {err}")

    print("\n=== Состояние таблицы после операций ===\n")
    print(table.dump())


if __name__ == "__main__":
    run()
