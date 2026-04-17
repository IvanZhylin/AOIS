"""Простой CLI-демо для требований лабораторной работы."""

from arithmetic import add_twos, div_direct, mul_direct, sub_twos
from bcd5421 import add_5421
from bits import direct_to_ones, direct_to_twos, int_to_direct_code
from ieee754 import add_float32, div_float32, mul_float32, sub_float32


def _bits_text(bits: list[int]) -> str:
    return "".join(str(x) for x in bits)


def run_demo() -> None:
    """Вывести демонстрацию всех требуемых операций."""
    x, y = 13, -5
    direct = int_to_direct_code(y)
    print("1) Десятичное число -> прямой/обратный/дополнительный коды")
    print(f"{y} прямой код:        {_bits_text(direct)}")
    print(f"{y} обратный код:      {_bits_text(direct_to_ones(direct))}")
    print(f"{y} дополнительный код:{_bits_text(direct_to_twos(direct))}")

    print("\n2) Сложение в дополнительном коде")
    add_bits, add_value = add_twos(x, y)
    print(f"{x} + {y} = {_bits_text(add_bits)} (двоич.) = {add_value} (десят.)")

    print("\n3) Вычитание через отрицание и сложение")
    sub_bits, sub_value = sub_twos(x, y)
    print(f"{x} - {y} = {_bits_text(sub_bits)} (двоич.) = {sub_value} (десят.)")

    print("\n4) Умножение в прямом коде")
    mul_bits, mul_value = mul_direct(x, y)
    print(f"{x} * {y} = {_bits_text(mul_bits)} (двоич.) = {mul_value} (десят.)")

    print("\n5) Деление в прямом коде (5 знаков после запятой)")
    div_text, div_value = div_direct(x, 7, precision=5)
    print(f"{x} / 7 = {div_text} (десят. строка) = {div_value} (десят. число)")

    print("\n6) Операции IEEE-754 (binary32)")
    for label, func in (
        ("+", add_float32),
        ("-", sub_float32),
        ("*", mul_float32),
        ("/", div_float32),
    ):
        bits, value = func(3.5, 1.25)
        print(f"3.5 {label} 1.25 = {_bits_text(bits)} (bin32) = {value} (десят.)")

    print("\n7) Сложение в 5421 BCD (вариант c)")
    bcd_bits, bcd_value = add_5421(259, 76)
    print(f"259 + 76 = {_bits_text(bcd_bits)} (5421 BCD) = {bcd_value} (десят.)")


if __name__ == "__main__":
    run_demo()

