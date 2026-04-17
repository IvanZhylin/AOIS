"""Преобразование IEEE-754 (binary32) и обертки арифметических операций."""

from bits import bits_to_unsigned, int_to_bits_unsigned


def float_to_ieee754_bits(value: float) -> list[int]:
    """Преобразовать float Python в массив битов IEEE-754 binary32."""
    if value == 0.0:
        return [0] * 32

    sign = 1 if value < 0 else 0
    x = -value if value < 0 else value

    exponent = 0
    while x >= 2.0:
        x /= 2.0
        exponent += 1
    while x < 1.0:
        x *= 2.0
        exponent -= 1

    biased_exp = exponent + 127
    if biased_exp <= 0:
        raise OverflowError("В этой реализации не поддерживаются субнормальные числа")
    if biased_exp >= 255:
        raise OverflowError("Значение слишком велико для binary32")

    exponent_bits = int_to_bits_unsigned(biased_exp, 8)

    mantissa = x - 1.0
    mantissa_bits = [0] * 23
    idx = 0
    while idx < 23:
        mantissa *= 2.0
        if mantissa >= 1.0:
            mantissa_bits[idx] = 1
            mantissa -= 1.0
        idx += 1

    return [sign] + exponent_bits + mantissa_bits


def ieee754_bits_to_float(bits: list[int]) -> float:
    """Преобразовать биты IEEE-754 binary32 в float Python."""
    sign = -1.0 if bits[0] else 1.0
    exponent_raw = bits_to_unsigned(bits[1:9])
    fraction_bits = bits[9:]

    if exponent_raw == 0 and all(b == 0 for b in fraction_bits):
        return 0.0
    if exponent_raw == 255:
        raise OverflowError("В этой реализации не поддерживаются Infinity и NaN")

    exponent = exponent_raw - 127
    fraction = 1.0
    factor = 0.5
    for bit in fraction_bits:
        if bit == 1:
            fraction += factor
        factor /= 2.0

    return sign * fraction * (2.0 ** exponent)


def _binary32_op(a: float, b: float, op) -> tuple[list[int], float]:
    """Выполнить операцию и вернуть код binary32 и десятичный результат."""
    result = op(a, b)
    bits = float_to_ieee754_bits(result)
    return bits, ieee754_bits_to_float(bits)


def add_float32(a: float, b: float) -> tuple[list[int], float]:
    return _binary32_op(a, b, lambda x, y: x + y)


def sub_float32(a: float, b: float) -> tuple[list[int], float]:
    return _binary32_op(a, b, lambda x, y: x - y)


def mul_float32(a: float, b: float) -> tuple[list[int], float]:
    return _binary32_op(a, b, lambda x, y: x * y)


def div_float32(a: float, b: float) -> tuple[list[int], float]:
    if b == 0:
        raise ZeroDivisionError("Деление на ноль")
    return _binary32_op(a, b, lambda x, y: x / y)

