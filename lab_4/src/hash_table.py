"""Хеш-таблица с разрешением коллизий методом цепочек (связный список)."""

from __future__ import annotations

from typing import Any, Iterator, List, Optional, Tuple

from src.hash_functions import hash_address, key_to_value
from src.models import HashEntry


class DuplicateKeyError(KeyError):
    """Попытка вставить ключ, уже присутствующий в таблице."""


class KeyNotFoundError(KeyError):
    """Ключ не найден в таблице."""


class HashTable:
    """
    Тематическая хеш-таблица: CRUD, цепочки, коэффициент заполнения.

    Каждая корзина — голова связного списка записей с одним хеш-адресом.
    """

    def __init__(self, size: int = 20, base_address: int = 0) -> None:
        if size < 1:
            raise ValueError("Размер таблицы должен быть не меньше 1")
        self._size = size
        self._base = base_address
        self._buckets: List[Optional[HashEntry]] = [None] * size
        self._active_count = 0

    @property
    def size(self) -> int:
        """H — число корзин (строк таблицы)."""
        return self._size

    @property
    def base_address(self) -> int:
        """B — начальный адрес таблицы."""
        return self._base

    @property
    def count(self) -> int:
        """Число активных (не вычеркнутых) записей."""
        return self._active_count

    def compute_v(self, key: str) -> int:
        """V(K) — числовое значение ключа."""
        return key_to_value(key)

    def compute_h(self, key: str) -> int:
        """h(V) — хеш-адрес для ключа."""
        return hash_address(self.compute_v(key), self._size, self._base)

    def load_factor(self) -> float:
        """Коэффициент заполнения: число активных записей / H."""
        return self._active_count / self._size

    def _bucket_index(self, h: int) -> int:
        """Индекс корзины по хеш-адресу (при B=0 совпадает с h)."""
        return h - self._base

    def _find_in_chain(
        self, head: Optional[HashEntry], key: str, include_deleted: bool = False
    ) -> Optional[HashEntry]:
        current = head
        while current is not None:
            if current.key == key:
                if include_deleted or not current.deleted:
                    return current
            current = current.next
        return None

    def _find_with_prev(
        self, bucket_idx: int, key: str
    ) -> Tuple[Optional[HashEntry], Optional[HashEntry]]:
        """Найти запись и предыдущий узел в цепочке (для удаления)."""
        prev: Optional[HashEntry] = None
        current = self._buckets[bucket_idx]
        while current is not None:
            if current.key == key:
                return prev, current
            prev = current
            current = current.next
        return None, None

    def _iter_chain(self, head: Optional[HashEntry]) -> Iterator[HashEntry]:
        current = head
        while current is not None:
            yield current
            current = current.next

    def _refresh_terminal_flags(self, head: Optional[HashEntry]) -> None:
        """Обновить флажки T и C для всех узлов цепочки."""
        nodes = list(self._iter_chain(head))
        for index, node in enumerate(nodes):
            node.terminal = index == len(nodes) - 1
            node.collision = index > 0

    def create(self, key: str, data: Any) -> HashEntry:
        """
        Create — вставка новой записи.

        При дубликате ключа — DuplicateKeyError.
        """
        h = self.compute_h(key)
        bucket_idx = self._bucket_index(h)
        head = self._buckets[bucket_idx]

        existing = self._find_in_chain(head, key, include_deleted=True)
        if existing is not None and not existing.deleted:
            raise DuplicateKeyError(f"Ключ «{key}» уже есть в таблице")
        if existing is not None and existing.deleted:
            existing.data = data
            existing.deleted = False
            existing.occupied = True
            self._active_count += 1
            self._refresh_terminal_flags(head)
            return existing

        entry = HashEntry(key=key, data=data)
        if head is None:
            self._buckets[bucket_idx] = entry
        else:
            tail = head
            while tail.next is not None:
                tail = tail.next
            tail.next = entry
        self._active_count += 1
        self._refresh_terminal_flags(self._buckets[bucket_idx])
        return entry

    def read(self, key: str) -> Any:
        """Read — поиск данных по ключу."""
        entry = self.search_entry(key)
        if entry is None:
            raise KeyNotFoundError(f"Ключ «{key}» не найден")
        return entry.data

    def search_entry(self, key: str) -> Optional[HashEntry]:
        """Найти запись по ключу (None, если нет или вычеркнута)."""
        h = self.compute_h(key)
        bucket_idx = self._bucket_index(h)
        return self._find_in_chain(self._buckets[bucket_idx], key)

    def update(self, key: str, data: Any) -> HashEntry:
        """Update — изменить данные по существующему ключу."""
        entry = self.search_entry(key)
        if entry is None:
            raise KeyNotFoundError(f"Ключ «{key}» не найден")
        entry.data = data
        return entry

    def delete(self, key: str) -> None:
        """
        Delete — удаление записи (флажок D, перестройка цепочки по методичке).

        Одиночная ячейка освобождается (U=0). В цепочке: последняя отцепляется;
        при удалении из начала/середины данные следующей записи переносятся в текущую.
        """
        h = self.compute_h(key)
        bucket_idx = self._bucket_index(h)
        prev, target = self._find_with_prev(bucket_idx, key)
        if target is None or target.deleted:
            raise KeyNotFoundError(f"Ключ «{key}» не найден")

        head = self._buckets[bucket_idx]
        active = [n for n in self._iter_chain(head) if not n.deleted]
        if len(active) == 1:
            self._buckets[bucket_idx] = None
            self._active_count -= 1
            return

        has_active_successor = any(
            not node.deleted for node in self._iter_chain(target.next)
        )

        if not has_active_successor:
            self._detach_node_ref(bucket_idx, prev, target)
            self._active_count -= 1
            self._refresh_terminal_flags(self._buckets[bucket_idx])
            return

        if head is target and not target.collision:
            successor = target.next
            while successor is not None and successor.deleted:
                successor = successor.next
            if successor is not None:
                succ_prev = target
                target.clone_payload_from(successor)
                target.collision = True
                self._detach_node_ref(bucket_idx, succ_prev, successor)
                self._active_count -= 1
                self._refresh_terminal_flags(self._buckets[bucket_idx])
                return

        successor = target.next
        while successor is not None and successor.deleted:
            successor = successor.next
        if successor is not None:
            succ_prev = target
            target.clone_payload_from(successor)
            self._detach_node_ref(bucket_idx, succ_prev, successor)
        else:
            self._detach_node_ref(bucket_idx, prev, target)
        self._active_count -= 1
        self._refresh_terminal_flags(self._buckets[bucket_idx])

    def _detach_node_ref(
        self,
        bucket_idx: int,
        prev: Optional[HashEntry],
        node: HashEntry,
    ) -> None:
        """Исключить узел из списка по ссылке (без поиска по ключу)."""
        if prev is None:
            self._buckets[bucket_idx] = node.next
        else:
            prev.next = node.next

    def contains(self, key: str) -> bool:
        """Проверка наличия активного ключа."""
        return self.search_entry(key) is not None

    def keys(self) -> List[str]:
        """Список всех активных ключей."""
        result: List[str] = []
        for head in self._buckets:
            for entry in self._iter_chain(head):
                if entry.occupied and not entry.deleted:
                    result.append(entry.key)
        return result

    def collision_stats(self) -> Tuple[int, int]:
        """
        Статистика коллизий: (число корзин с цепочкой > 1, число записей в таких цепочках).
        """
        buckets_with_collision = 0
        chained_entries = 0
        for head in self._buckets:
            active = [e for e in self._iter_chain(head) if not e.deleted]
            if len(active) > 1:
                buckets_with_collision += 1
                chained_entries += len(active)
        return buckets_with_collision, chained_entries

    def format_entry(self, entry: HashEntry, bucket: int) -> str:
        """Строковое представление полей одной записи."""
        v = self.compute_v(entry.key)
        h = self.compute_h(entry.key)
        flags = (
            f"C={int(entry.collision)} U={int(entry.occupied)} "
            f"T={int(entry.terminal)} L={int(entry.link_is_pointer)} D={int(entry.deleted)}"
        )
        nxt = "—" if entry.next is None else entry.next.key
        return (
            f"  корзина[{bucket:2d}] ID={entry.key!r} V={v} h={h} {flags} "
            f"Po→{nxt} Pi={entry.data!r}"
        )

    def dump(self) -> str:
        """Индикация всей таблицы, V, h и коэффициента заполнения."""
        lines = [
            f"Хеш-таблица: H={self._size}, B={self._base}, записей={self._active_count}",
            f"Коэффициент заполнения: {self.load_factor():.4f}",
        ]
        collisions, chained = self.collision_stats()
        lines.append(
            f"Корзин с коллизиями: {collisions}, записей в цепочках: {chained}"
        )
        lines.append("-" * 72)
        for index in range(self._size):
            head = self._buckets[index]
            if head is None:
                lines.append(f"  [{index:2d}] пусто")
                continue
            for entry in self._iter_chain(head):
                lines.append(self.format_entry(entry, index))
        return "\n".join(lines)
