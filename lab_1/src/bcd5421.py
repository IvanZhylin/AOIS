"""Кодирование 5421 BCD и сложение."""

ENCODE_5421: dict[int, list[int]] = {
    0: [0, 0, 0, 0],
    1: [0, 0, 0, 1],
    2: [0, 0, 1, 0],
    3: [0, 0, 1, 1],
    4: [0, 1, 0, 0],
    5: [1, 0, 0, 0],
    6: [1, 0, 0, 1],
    7: [1, 0, 1, 0],
    8: [1, 0, 1, 1],
    9: [1, 1, 0, 0],
}
DECODE_5421 = {tuple(v): k for k, v in ENCODE_5421.items()}


def encode_5421(number: int) -> list[int]:
    """Закодировать неотрицательное целое число в биты 5421 BCD."""
    if number < 0:
        raise ValueError("5421 BCD поддерживает только неотрицательные числа")

    digits: list[int] = []
    current = number
    if current == 0:
        digits = [0]
    else:
        while current > 0:
            digits.append(current % 10)
            current //= 10
        digits.reverse()

    bits: list[int] = []
    for d in digits:
        bits.extend(ENCODE_5421[d])
    return bits


def decode_5421(bits: list[int]) -> int:
    """Декодировать список битов 5421 BCD в целое число."""
    if len(bits) % 4 != 0:
        raise ValueError("Количество битов BCD должно делиться на 4")

    value = 0
    idx = 0
    while idx < len(bits):
        chunk = tuple(bits[idx : idx + 4])
        if chunk not in DECODE_5421:
            raise ValueError("Недопустимая цифра 5421 BCD")
        value = value * 10 + DECODE_5421[chunk]
        idx += 4
    return value


def add_5421(a: int, b: int) -> tuple[list[int], int]:
    """Сложить два десятичных числа и вернуть 5421 BCD и десятичный результат."""
    if a < 0 or b < 0:
        raise ValueError("Сложение 5421 BCD поддерживает только неотрицательные числа")
    value = a + b
    return encode_5421(value), value

