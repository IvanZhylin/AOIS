"""Модель строки (ячейки) хеш-таблицы по формату рис. 1 методички."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class HashEntry:
    """
    Элемент цепочки коллизий (связный список в корзине).

    Поля соответствуют флажкам и данным ячейки ТХ:
    ID — ключ; Pi — данные; C, U, T, L, D — флажки; next — Po (следующая запись).
    """

    key: str  # ID — ключевое слово
    data: Any  # Pi — полезные данные
    collision: bool = False  # C — признак коллизии
    occupied: bool = True  # U — ячейка занята
    terminal: bool = True  # T — последняя в цепочке
    link_is_pointer: bool = False  # L — Pi хранит указатель (не используется в ЛР)
    deleted: bool = False  # D — запись вычеркнута
    next: Optional[HashEntry] = field(default=None, repr=False)  # Po

    def clone_payload_from(self, other: HashEntry) -> None:
        """Скопировать содержимое другой записи (при удалении из середины цепочки)."""
        self.key = other.key
        self.data = other.data
        self.collision = other.collision
        self.link_is_pointer = other.link_is_pointer
