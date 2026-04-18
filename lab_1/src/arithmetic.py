"""Целочисленная арифметика на базе двоичных представлений."""

from src.bits import (
    WIDTH,
    add_bit_arrays,
    bits_to_unsigned,
    direct_code_to_int,
    int_to_bits_unsigned,
    int_to_direct_code,
    int_to_twos,
    twos_to_int,
)


def add_twos(a: int, b: int, width: int = WIDTH) -> tuple[list[int], int]:
    """Сложить два числа через дополнительный код; вернуть (биты_результата, число)."""
    a_bits = int_to_twos(a, width)
    b_bits = int_to_twos(b, width)
    result_bits, _ = add_bit_arrays(a_bits, b_bits)
    return result_bits, twos_to_int(result_bits)


def sub_twos(a: int, b: int, width: int = WIDTH) -> tuple[list[int], int]:
    """Вычесть через отрицание и сложение в дополнительном коде."""
    return add_twos(a, -b, width)


def _multiply_unsigned_bits(a_bits: list[int], b_bits: list[int]) -> list[int]:
    """Умножить два беззнаковых числа одинаковой разрядности в битовом виде."""
    width = len(a_bits)
    result = [0] * width
    shift = 0
    idx = width - 1
    while idx >= 0:
        if b_bits[idx] == 1:
            partial = [0] * width
            src = 0
            while src < width:
                dst = src - shift
                if dst >= 0:
                    partial[dst] = a_bits[src]
                src += 1
            result, _ = add_bit_arrays(result, partial)
        shift += 1
        idx -= 1
    return result


def mul_direct(a: int, b: int, width: int = WIDTH) -> tuple[list[int], int]:
    """Умножить два целых числа в логике прямого кода."""
    da = int_to_direct_code(a, width)
    db = int_to_direct_code(b, width)
    sign = da[0] ^ db[0]
    magnitude_bits = _multiply_unsigned_bits(da[1:], db[1:])
    result_bits = [sign] + magnitude_bits
    return result_bits, direct_code_to_int(result_bits)


def div_direct(a: int, b: int, precision: int = 5, width: int = WIDTH) -> tuple[str, float]:
    """Разделить два целых в логике прямого кода с фиксированной точностью."""
    if b == 0:
        raise ZeroDivisionError("Деление на ноль")

    sign = -1 if (a < 0) ^ (b < 0) else 1
    dividend = -a if a < 0 else a
    divisor = -b if b < 0 else b

    integer_part = dividend // divisor
    remainder = dividend % divisor

    frac_digits: list[int] = []
    for _ in range(precision):
        remainder *= 10
        frac_digits.append(remainder // divisor)
        remainder %= divisor

    text = str(integer_part) + "." + "".join(str(d) for d in frac_digits)
    value = integer_part
    factor = 0.1
    for digit in frac_digits:
        value += digit * factor
        factor /= 10

    if sign < 0:
        return "-" + text, -value
    return text, value


def format_int_binary(value: int, width: int = WIDTH) -> str:
    """Вернуть строковое двоичное представление числа в дополнительном коде."""
    bits = int_to_twos(value, width)
    return "".join(str(bit) for bit in bits)


def direct_binary(value: int, width: int = WIDTH) -> str:
    """Вернуть строковое двоичное представление числа в прямом коде."""
    bits = int_to_direct_code(value, width)
    return "".join(str(bit) for bit in bits)


def unsigned_binary(value: int, width: int = WIDTH) -> str:
    """Вернуть строковое двоичное представление беззнакового числа."""
    bits = int_to_bits_unsigned(value, width)
    return "".join(str(bit) for bit in bits)


def binary_to_unsigned(text: str) -> int:
    """Преобразовать двоичную строку без встроенных средств смены системы счисления."""
    bits = [0] * len(text)
    idx = 0
    for ch in text:
        if ch not in ("0", "1"):
            raise ValueError("Двоичная строка содержит недопустимый символ")
        bits[idx] = 1 if ch == "1" else 0
        idx += 1
    return bits_to_unsigned(bits)

