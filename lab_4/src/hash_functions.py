"""Функции перевода ключа в V и вычисления хеш-адреса (методичка, ЛР №6)."""

# Русский алфавит: А=0 … Я=32 (основание 33 для первых двух букв ключа)
RUSSIAN_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
BASE = len(RUSSIAN_ALPHABET)


def _normalize_letter(char: str) -> str:
    """Привести букву к верхнему регистру для поиска в алфавите."""
    upper = char.upper()
    if upper == "Ё":
        return "Ё"
    return upper


def letter_value(char: str) -> int:
    """
    Номер буквы в алфавите (А=0, Б=1, …, Я=32).

    Пример из методички: «В» → 2, «я» → 32.
    """
    normalized = _normalize_letter(char)
    try:
        return RUSSIAN_ALPHABET.index(normalized)
    except ValueError as exc:
        raise ValueError(
            f"Символ «{char}» не входит в русский алфавит ({RUSSIAN_ALPHABET})"
        ) from exc


def key_to_value(key: str) -> int:
    """
    Числовое значение ключа V по первым двум буквам.

    V[K] = c1·33¹ + c2·33⁰, например V[«Вя»] = 2·33 + 32 = 98.
    """
    if len(key) < 2:
        raise ValueError("Ключ должен содержать не менее двух символов")
    first, second = key[0], key[1]
    return letter_value(first) * BASE + letter_value(second)


def hash_address(v: int, table_size: int, base_address: int = 0) -> int:
    """
    Хеш-адрес: h(V) = V mod H + B.

    table_size — H (число строк таблицы), base_address — B.
    """
    if table_size <= 0:
        raise ValueError("Размер таблицы H должен быть положительным")
    return v % table_size + base_address
