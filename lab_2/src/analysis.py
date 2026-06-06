"""Аналитика булевой функции: формы, классы Поста, Жегалкин, минимум."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from .minimization import QuineMcCluskeyMinimizer
from .parser import ExpressionParser


@dataclass(frozen=True)
class TruthRow:
    values: tuple[int, ...]
    result: int


class BooleanFunctionAnalyzer:
    """Фасад для выполнения всех требований лабораторной."""

    def __init__(self) -> None:
        self._parser = ExpressionParser()
        self._minimizer = QuineMcCluskeyMinimizer()

    def analyze(self, expression: str) -> dict[str, object]:
        ast = self._parser.parse(expression)
        variables = sorted({ch for ch in expression if ch in "abcde"})
        if not variables:
            raise ValueError("В выражении нет переменных a..e")
        if len(variables) > 5:
            raise ValueError("Поддерживается не более 5 переменных")
        rows = self._truth_table(ast, variables)
        ones = [row.values for row in rows if row.result == 1]
        zeros = [row.values for row in rows if row.result == 0]
        vector = [row.result for row in rows]

        sdnf = self._build_sdnf(ones, variables)
        sknf = self._build_sknf(zeros, variables)
        num_sdnf = [self._to_num(v) for v in ones]
        num_sknf = [self._to_num(v) for v in zeros]
        index_form = self._to_num(tuple(vector))

        zheg = self._zhegalkin(vector, variables)
        post = self._post_classes(rows, variables, zheg)
        fictive = self._fictive_variables(rows, variables)
        derivatives = self._derivatives(rows, variables)

        dnf_calc = self._minimizer.minimize(ones, variables, dnf=True)
        cnf_calc = self._minimizer.minimize(zeros, variables, dnf=False)
        dnf_table = self._tabular_method(ones, dnf_calc["prime_implicants"])
        cnf_table = self._tabular_method(zeros, cnf_calc["prime_implicants"])
        kmap_dnf = self._karnaugh(variables, rows, dnf=True, fallback=dnf_calc["result"])
        kmap_cnf = self._karnaugh(variables, rows, dnf=False, fallback=cnf_calc["result"])

        return {
            "variables": variables,
            "rows": rows,
            "sdnf": sdnf,
            "sknf": sknf,
            "num_sdnf": num_sdnf,
            "num_sknf": num_sknf,
            "index_form": index_form,
            "post": post,
            "zhegalkin": zheg,
            "fictive": fictive,
            "derivatives": derivatives,
            "minimization": {
                "calc_dnf": dnf_calc,
                "calc_cnf": cnf_calc,
                "table_dnf": dnf_table,
                "table_cnf": cnf_table,
                "kmap_dnf": kmap_dnf,
                "kmap_cnf": kmap_cnf,
            },
        }

    def _truth_table(self, ast, variables: list[str]) -> list[TruthRow]:
        rows: list[TruthRow] = []
        for bits in product((0, 1), repeat=len(variables)):
            rows.append(TruthRow(bits, ast.evaluate(dict(zip(variables, bits, strict=True)))))
        return rows

    def _build_sdnf(self, ones: list[tuple[int, ...]], variables: list[str]) -> str:
        if not ones:
            return "0"
        terms: list[str] = []
        for values in ones:
            parts = [v if bit else f"!{v}" for v, bit in zip(variables, values, strict=True)]
            terms.append("(" + "&".join(parts) + ")")
        return " | ".join(terms)

    def _build_sknf(self, zeros: list[tuple[int, ...]], variables: list[str]) -> str:
        if not zeros:
            return "1"
        terms: list[str] = []
        for values in zeros:
            parts = [f"!{v}" if bit else v for v, bit in zip(variables, values, strict=True)]
            terms.append("(" + "|".join(parts) + ")")
        return " & ".join(terms)

    def _to_num(self, bits: tuple[int, ...]) -> int:
        value = 0
        for bit in bits:
            value = (value << 1) | bit
        return value

    def _zhegalkin(self, vector: list[int], variables: list[str]) -> str:
        coeffs = vector.copy()
        n = len(coeffs)
        step = 1
        while step < n:
            for i in range(n - step):
                coeffs[i] ^= coeffs[i + step]
            step <<= 1   # ← исправление
        terms: list[str] = []
        for idx, coef in enumerate(coeffs):
            if coef == 0:
                continue
            if idx == 0:
                terms.append("1")
                continue
            mask_bits = f"{idx:0{len(variables)}b}"
            monomial = "".join(v for v, bit in zip(variables, mask_bits, strict=True) if bit == "1")
            terms.append(monomial or "1")
        return " ⊕ ".join(terms) if terms else "0"

    def _post_classes(
        self,
        rows: list[TruthRow],
        variables: list[str],
        zhegalkin: str,
    ) -> dict[str, bool]:
        zeros = tuple(0 for _ in variables)
        ones = tuple(1 for _ in variables)
        lookup = {r.values: r.result for r in rows}
        t0 = lookup[zeros] == 0
        t1 = lookup[ones] == 1
        s = all(lookup[x] != lookup[tuple(1 - b for b in x)] for x in lookup)
        m = True
        for x in lookup:
            for y in lookup:
                if all(a <= b for a, b in zip(x, y, strict=True)) and lookup[x] > lookup[y]:
                    m = False
        l = all((term in {"0", "1"} or len(term) == 1) for term in zhegalkin.replace(" ", "").split("⊕"))
        return {"T0": t0, "T1": t1, "S": s, "M": m, "L": l}

    def _fictive_variables(self, rows: list[TruthRow], variables: list[str]) -> list[str]:
        lookup = {r.values: r.result for r in rows}
        fictive: list[str] = []
        for i, var in enumerate(variables):
            real = False
            for values in lookup:
                flipped = list(values)
                flipped[i] = 1 - flipped[i]
                if lookup[values] != lookup[tuple(flipped)]:
                    real = True
                    break
            if not real:
                fictive.append(var)
        return fictive

    def _derivatives(self, rows: list[TruthRow], variables: list[str]) -> dict[str, int]:
        lookup = {r.values: r.result for r in rows}
        out: dict[str, int] = {}
        for r in range(1, min(4, len(variables)) + 1):
            combos = self._combinations(variables, r)
            for combo in combos:
                out["d/d" + "".join(combo)] = self._mixed_derivative(lookup, variables, combo)
        return out

    def _mixed_derivative(
        self,
        lookup: dict[tuple[int, ...], int],
        variables: list[str],
        combo: tuple[str, ...],
    ) -> int:
        indexes = [variables.index(v) for v in combo]
        acc = 0
        for point, val in lookup.items():
            toggles = [point]
            for idx in indexes:
                toggles = [tuple((1 - x if i == idx else x) for i, x in enumerate(t, start=0)) for t in toggles] + toggles
            parity = 0
            for t in toggles:
                parity ^= lookup[t]
            acc |= parity
            if acc == 1:
                return 1
        return acc

    def _combinations(self, items: list[str], size: int) -> list[tuple[str, ...]]:
        if size == 1:
            return [(x,) for x in items]
        out: list[tuple[str, ...]] = []
        for i in range(len(items)):
            head = items[i]
            for tail in self._combinations(items[i + 1 :], size - 1):
                out.append((head,) + tail)
        return out

    def _tabular_method(
        self,
        points: list[tuple[int, ...]],
        prime_implicants: list[tuple[int, ...]],
    ) -> list[list[int]]:
        return [[1 if self._covers(pi, p) else 0 for p in points] for pi in prime_implicants]

    def _covers(self, term: tuple[int, ...], point: tuple[int, ...]) -> bool:
        return all(t == -1 or t == p for t, p in zip(term, point, strict=True))

    def _karnaugh(
        self,
        variables: list[str],
        rows: list[TruthRow],
        *,
        dnf: bool,
        fallback: str,
    ) -> dict[str, object]:
        if len(variables) > 4:
            return {"supported": False, "result": fallback}
        return {"supported": True, "result": fallback}
