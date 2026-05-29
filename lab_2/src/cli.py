"""CLI для лабораторной работы."""

from __future__ import annotations

from .analysis import BooleanFunctionAnalyzer


def _fmt_row(variables: list[str], values: tuple[int, ...], result: int) -> str:
    left = " ".join(f"{v}={x}" for v, x in zip(variables, values, strict=True))
    return f"{left} | f={result}"


def main() -> None:
    print("Лабораторная №2: анализ булевой функции")
    expr = input("Введите функцию: ").strip()
    analyzer = BooleanFunctionAnalyzer()
    data = analyzer.analyze(expr)
    variables = data["variables"]

    print("\nТаблица истинности:")
    for row in data["rows"]:
        print(_fmt_row(variables, row.values, row.result))

    print("\nСДНФ:", data["sdnf"])
    print("СКНФ:", data["sknf"])
    print("Числовая форма СДНФ:", data["num_sdnf"])
    print("Числовая форма СКНФ:", data["num_sknf"])
    print("Индексная форма:", data["index_form"])
    print("Классы Поста:", data["post"])
    print("Полином Жегалкина:", data["zhegalkin"])
    print("Фиктивные переменные:", data["fictive"] if data["fictive"] else "нет")
    print("Булевы производные:", data["derivatives"])

    minim = data["minimization"]
    print("\nМинимизация (расчетный метод):")
    print("ДНФ:", minim["calc_dnf"]["result"])
    print("КНФ:", minim["calc_cnf"]["result"])

    print("\nМинимизация (расчетно-табличный метод):")
    print("Таблица покрытий ДНФ:", minim["table_dnf"])
    print("Таблица покрытий КНФ:", minim["table_cnf"])

    print("\nМинимизация (карта Карно):")
    print("ДНФ:", minim["kmap_dnf"]["result"])
    print("КНФ:", minim["kmap_cnf"]["result"])
    if not minim["kmap_dnf"]["supported"]:
        print("Примечание: для 5 переменных карта Карно заменена на эквивалентный результат расчетного метода.")


if __name__ == "__main__":
    main()
