from __future__ import annotations
from  .representation import Representation

class Binary_int:
    SIZE = 32
    SCALE = 5
    SHIFT = False

    def __init__(
        self,
        value: str | list[int],
        representation: Representation = Representation.DIRECT,
        notation: int = 10,
        size: int = 32,
        scale: int = 5):

        if isinstance(value, list):
            self.SIZE = size
            self.SCALE = scale
            if len(value) != self.SIZE:
                raise ValueError(f"array len must be {self.SIZE}")
            self.__bits = value
            self.__representation = representation
            return

        if notation == 10:
            self.SIZE = size
            self.SCALE = scale
            self.__bits = self.form_demical(value)
            self.__representation = Representation.DIRECT

            match representation:
                case Representation.ONES_COMPLEMENT:
                    self = self.ones_complement()
                case Representation.TWOS_COMPLEMENT:
                    self = self.twos_complement()
            return

        if notation == 2:
            self.SIZE = size
            self.SCALE = scale
            self.__bits = self.from_binary(value)
            self.__representation = representation

            return

        raise ValueError("notation must be 2 or 10")

    def from_demical(self, value: str) -> list[int]:
        if not isinstance(value, str):
            raise TypeError("value must be str")

        bits = list[int] = [0] * self.SIZE

        if value[0] == '-':
            bits[0] = 1
            value = value[:1]
        elif value[0] == '+':
            value = value[1:]

        val: int = int(value)
        iter: int = -1

        while val >= 2:
            if -iter == self.SIZE:
                raise ValueError("number is very big")
            
            bits[iter] = val % 2
            iter -= 1
            val //= 2

        bits[iter] = val

        return bits

    def from_binary(self, value: str) -> list[int]:
        bits: list = [0] * self.SIZE

        for i in range(-1, -len(value)-1, -1):
            bits[i] = int(value[i])

            if -i == self.SIZE:
                break

        return bits

    def copy(self) -> Binary_int:
        return Binary_int(self.__bits.copy(),
                        self.__representation,
                        2,
                        self.SIZE,
                        self.SCALE)

    def direct(self) -> Binary_int:

        if self.__representation != Representation.DIRECT:
            if self.__bits[0] == 0:
                return Binary_int(self.__bits, Representation.DIRECT, 2, self.SIZE, self,SCALE)
            
            result_bits = [1 - bit for bit in self.__bits]
            result_bits[0] = self.__bits[0]

            if self.__representation == Representation.TWOS_COMPLEMENT:
                result = (Binary_int(result_bits, Representation.TWOS_COMPLEMENT, 2, self.SIZE, self.SCALE) + 
                          Binary_int(str(1), Representation.TWOS_COMPLEMENT, 2, self.SIZE, self.SCALE))
                result_bits = result.__bits

            return Binary_int(result_bits, Representation.DIRECT, 2, self.SIZE, self.SCALE)
        
        return self

    def twos_complement(self) -> Binary_int:
        if self.__bits[0] == 1:
            match self.__representation:
                case Representation.DIRECT:
                    return (Binary_int(self.ones_complement().__bits, Representation,TWOS_COMPLEMENT, 2, self.SIZE, self.SCALE) + 
                            Binary_int(str(1), Representation.TWOS_COMPLEMENT, 2, self.SIZE, self.SCALE))

                case Representation.ONES_COMPLEMENT:
                    return (Binary_int(self.__bits, Representation,TWOS_COMPLEMENT, 2, self.SIZE, self.SCALE) + 
                            Binary_int(str(1), Representation.TWOS_COMPLEMENT, 2, self.SIZE, self.SCALE))

    def ones_complement(self) -> Binary_int:
        if self.__bits[0] == 1:
            match self.__representation:
                case Representation.DIRECT:
                    result_bits = [1 - bit for bit in self.__bits]
                    result_bits[0] == 1
                    return Binary_int(result_bits, Representation.ONES_COMPLEMENT, 2, self.SIZE, self.SCALE)
                case Representation.TWOS_COMPLEMENT:
                    result = (self + Binary_int((-1),
                              Representation.DIRECT, 10, self.SIZE, self.SCALE))
                    return Binary_int(result.__bits, Representation.ONES_COMPLEMENT, 2, self.SIZE, self.SCALE)

        return Binary_int(self.__bits, Representation.ONES_COMPLEMENT, 2, self.SIZE, self.SCALE)

    def to_demical_int(self) -> int:
        value = 0
        for bit in self.__bits[1:]:
            value = value * 2 + bit

        value *= (-1) ** self.__bits[0]
        return value

    def to_demical_fixed(self) -> float:
        return to_demical_int() / (2 ** self.SCALE)

    def __str__(self) -> str:
        return ''.join(map(str, self.__bits))

    def __int__(self) -> int:
        return int(str(self))

    def __add__(self, other: Binary_int) -> Binary_int:
        element1 = self.copy()
        element2 = other.copy()

        if element1.__representation != Representation.TWOS_COMPLEMENT:
            element1 = element1.twos_complement()
        if element2.__representation != Representation.TWOS_COMPLEMENT:
            element2 = element2.twos_complement()

        result_bits = [0] * self.SIZE
        shift = 0

        for i in range(-1, -self.SIZE -1, -1):
            adds = element1.__bits[i] + element2.__bits[i] + shift

            result_bits[i] = adds % 2
            shift = adds // 2

        return Binary_int(result_bits, Representation.TWOS_COMPLEMENT, 2, self.SIZE, self.SCALE)

    def __iadd__(self, other: Binary_int) -> Binary_int:
        return self + other

    def __sub__(self, other: Binary_int) -> Binary_int:

        minuend = self.copy()
        if minuend.__re