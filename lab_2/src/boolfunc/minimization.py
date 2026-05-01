"""Минимизация булевых функций."""

from __future__ import annotations

from collections.abc import Iterable


def _count_ones(term: tuple[int, ...]) -> int:
    return sum(1 for x in term if x == 1)


def _can_merge(a: tuple[int, ...], b: tuple[int, ...]) -> bool:
    diff = 0
    for av, bv in zip(a, b, strict=True):
        if av != bv:
            if av == -1 or bv == -1:
                return False
            diff += 1
        if diff > 1:
            return False
    return diff == 1


def _merge(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    out: list[int] = []
    for av, bv in zip(a, b, strict=True):
        out.append(av if av == bv else -1)
    return tuple(out)


def _covers(term: tuple[int, ...], point: tuple[int, ...]) -> bool:
    return all(tv == -1 or tv == pv for tv, pv in zip(term, point, strict=True))


def _format_dnf_term(term: tuple[int, ...], variables: list[str]) -> str:
    parts: list[str] = []
    for v, bit in zip(variables, term, strict=True):
        if bit == 1:
            parts.append(v)
        elif bit == 0:
            parts.append(f"!{v}")
    return "&".join(parts) if parts else "1"


def _format_cnf_term(term: tuple[int, ...], variables: list[str]) -> str:
    parts: list[str] = []
    for v, bit in zip(variables, term, strict=True):
        if bit == 1:
            parts.append(f"!{v}")
        elif bit == 0:
            parts.append(v)
    return "|".join(parts) if parts else "0"


class QuineMcCluskeyMinimizer:
    """Расчетный метод минимизации (QMC)."""

    def minimize(
        self,
        points: Iterable[tuple[int, ...]],
        variables: list[str],
        *,
        dnf: bool = True,
    ) -> dict[str, object]:
        initial = sorted(set(points), key=_count_ones)
        if not initial:
            return {"stages": [], "prime_implicants": [], "result": "0" if dnf else "1"}
        stages: list[list[tuple[int, ...]]] = [initial]
        current = initial
        prime_implicants: set[tuple[int, ...]] = set()
        while current:
            used: set[tuple[int, ...]] = set()
            nxt: set[tuple[int, ...]] = set()
            for i, left in enumerate(current):
                for right in current[i + 1 :]:
                    if _can_merge(left, right):
                        used.add(left)
                        used.add(right)
                        nxt.add(_merge(left, right))
            for term in current:
                if term not in used:
                    prime_implicants.add(term)
            if not nxt:
                break
            current = sorted(nxt, key=lambda t: (sum(1 for x in t if x == -1), _count_ones(t)))
            stages.append(current)

        needed = self._remove_redundant(prime_implicants, set(initial))
        formatter = _format_dnf_term if dnf else _format_cnf_term
        joiner = " | " if dnf else " & "
        body = joiner.join(
            (
                f"({formatter(term, variables)})"
                if len([x for x in term if x != -1]) > 1
                else formatter(term, variables)
            )
            for term in needed
        )
        return {
            "stages": stages,
            "prime_implicants": sorted(prime_implicants),
            "result_terms": needed,
            "result": body or ("0" if dnf else "1"),
        }

    def _remove_redundant(
        self,
        implicants: set[tuple[int, ...]],
        points: set[tuple[int, ...]],
    ) -> list[tuple[int, ...]]:
        ordered = sorted(implicants, key=lambda t: (sum(x == -1 for x in t), t))
        selected: list[tuple[int, ...]] = []
        uncovered = set(points)
        for point in list(points):
            covering = [imp for imp in ordered if _covers(imp, point)]
            if len(covering) == 1 and covering[0] not in selected:
                selected.append(covering[0])
        uncovered = {p for p in points if not any(_covers(s, p) for s in selected)}
        while uncovered:
            best = max(ordered, key=lambda imp: sum(_covers(imp, p) for p in uncovered))
            if best not in selected:
                selected.append(best)
            uncovered = {p for p in uncovered if not _covers(best, p)}
        return selected
