"""Битовые вспомогательные функции для 32-битных представлений."""

WIDTH = 32
MAX_UNSIGNED = (1 << WIDTH) - 1


def int_to_bits_unsigned(value: int, width: int = WIDTH) -> list[int]:
    """Преобразовать неотрицательное число в биты фиксированной длины (MSB first)."""
    if value < 0:
        raise ValueError("Беззнаковое преобразование ожидает неотрицательное число")
    limit = 1
    for _ in range(width):
        limit *= 2
    if value >= limit:
        raise OverflowError("Число не помещается в указанную разрядность")

    result = [0] * width
    current = value
    idx = width - 1
    while idx >= 0:
        result[idx] = current % 2
        current //= 2
        idx -= 1
    return result


def bits_to_unsigned(bits: list[int]) -> int:
    """Преобразовать биты (MSB first) в неотрицательное целое число."""
    value = 0
    for bit in bits:
        value = value * 2 + bit
    return value


def invert_bits(bits: list[int]) -> list[int]:
    """Вернуть инверсию битов."""
    return [1 - b for b in bits]


def add_bit_arrays(a: list[int], b: list[int]) -> tuple[list[int], int]:
    """Сложить два массива битов и вернуть (сумма, перенос)."""
    if len(a) != len(b):
        raise ValueError("Массивы битов должны иметь одинаковую разрядность")
    width = len(a)
    result = [0] * width
    carry = 0
    idx = width - 1
    while idx >= 0:
        total = a[idx] + b[idx] + carry
        result[idx] = total % 2
        carry = total // 2
        idx -= 1
    return result, carry


def int_to_direct_code(value: int, width: int = WIDTH) -> list[int]:
    """Представление в прямом коде (знак + модуль)."""
    max_magnitude = (1 << (width - 1)) - 1
    if value > max_magnitude or value < -max_magnitude:
        raise OverflowError("Число вне диапазона прямого кода")
    sign = 1 if value < 0 else 0
    magnitude = -value if value < 0 else value
    bits = int_to_bits_unsigned(magnitude, width - 1)
    return [sign] + bits


def direct_code_to_int(bits: list[int]) -> int:
    """Преобразовать прямой код (знак + модуль) в целое число."""
    sign = bits[0]
    magnitude = bits_to_unsigned(bits[1:])
    return -magnitude if sign else magnitude


def direct_to_ones(bits: list[int]) -> list[int]:
    """Преобразовать прямой код в обратный код."""
    if bits[0] == 0:
        return bits[:]
    return [1] + invert_bits(bits[1:])


def direct_to_twos(bits: list[int]) -> list[int]:
    """Преобразовать прямой код в дополнительный код."""
    ones = direct_to_ones(bits)
    if ones[0] == 0:
        return ones
    one = [0] * len(bits)
    one[-1] = 1
    twos, _ = add_bit_arrays(ones, one)
    return twos


def int_to_twos(value: int, width: int = WIDTH) -> list[int]:
    """Преобразовать целое число в дополнительный код."""
    min_value = -(1 << (width - 1))
    max_value = (1 << (width - 1)) - 1
    if value < min_value or value > max_value:
        raise OverflowError("Число вне диапазона дополнительного кода")
    if value >= 0:
        return int_to_bits_unsigned(value, width)
    direct = int_to_direct_code(value, width)
    return direct_to_twos(direct)


def twos_to_int(bits: list[int]) -> int:
    """Преобразовать дополнительный код в целое число."""
    if bits[0] == 0:
        return bits_to_unsigned(bits)
    inverted = invert_bits(bits)
    one = [0] * len(bits)
    one[-1] = 1
    abs_bits, _ = add_bit_arrays(inverted, one)
    return -bits_to_unsigned(abs_bits)

