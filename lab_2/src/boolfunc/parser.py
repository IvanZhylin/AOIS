"""Парсер булевых выражений с операциями !, &, |, ->, ~."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Node:
    """Базовый узел AST."""

    def evaluate(self, values: dict[str, int]) -> int:
        raise NotImplementedError


@dataclass(frozen=True)
class Var(Node):
    name: str

    def evaluate(self, values: dict[str, int]) -> int:
        return int(values[self.name])


@dataclass(frozen=True)
class Not(Node):
    operand: Node

    def evaluate(self, values: dict[str, int]) -> int:
        return 1 - self.operand.evaluate(values)


@dataclass(frozen=True)
class Binary(Node):
    op: str
    left: Node
    right: Node

    def evaluate(self, values: dict[str, int]) -> int:
        lval = self.left.evaluate(values)
        rval = self.right.evaluate(values)
        if self.op == "&":
            return lval & rval
        if self.op == "|":
            return lval | rval
        if self.op == "->":
            return int((not lval) or rval)
        if self.op == "~":
            return int(lval == rval)
        raise ValueError(f"Неизвестная операция: {self.op}")


class ExpressionParser:
    """Рекурсивный нисходящий парсер для булевой алгебры."""

    _VARIABLES = set("abcde")

    def parse(self, text: str) -> Node:
        normalized = (
            text.replace("¬", "!")
            .replace("∧", "&")
            .replace("∨", "|")
            .replace("→", "->")
            .replace(" ", "")
        )
        self._tokens = self._tokenize(normalized)
        self._index = 0
        node = self._parse_equiv()
        if self._peek() is not None:
            raise ValueError(f"Лишний токен: {self._peek()}")
        return node

    def _tokenize(self, text: str) -> list[str]:
        tokens: list[str] = []
        i = 0
        while i < len(text):
            ch = text[i]
            if ch in "()!&|~":
                tokens.append(ch)
                i += 1
            elif ch in self._VARIABLES:
                tokens.append(ch)
                i += 1
            elif text[i : i + 2] == "->":
                tokens.append("->")
                i += 2
            else:
                raise ValueError(f"Недопустимый символ: {ch}")
        return tokens

    def _peek(self) -> str | None:
        if self._index >= len(self._tokens):
            return None
        return self._tokens[self._index]

    def _next(self) -> str:
        token = self._peek()
        if token is None:
            raise ValueError("Неожиданный конец выражения")
        self._index += 1
        return token

    def _parse_equiv(self) -> Node:
        node = self._parse_impl()
        while self._peek() == "~":
            self._next()
            node = Binary("~", node, self._parse_impl())
        return node

    def _parse_impl(self) -> Node:
        node = self._parse_or()
        if self._peek() == "->":
            self._next()
            node = Binary("->", node, self._parse_impl())
        return node

    def _parse_or(self) -> Node:
        node = self._parse_and()
        while self._peek() == "|":
            self._next()
            node = Binary("|", node, self._parse_and())
        return node

    def _parse_and(self) -> Node:
        node = self._parse_not()
        while self._peek() == "&":
            self._next()
            node = Binary("&", node, self._parse_not())
        return node

    def _parse_not(self) -> Node:
        if self._peek() == "!":
            self._next()
            return Not(self._parse_not())
        return self._parse_atom()

    def _parse_atom(self) -> Node:
        token = self._peek()
        if token == "(":
            self._next()
            expr = self._parse_equiv()
            if self._next() != ")":
                raise ValueError("Ожидалась ')'")
            return expr
        if token in self._VARIABLES:
            return Var(self._next())
        raise ValueError(f"Ожидалась переменная или '(', получено: {token}")
