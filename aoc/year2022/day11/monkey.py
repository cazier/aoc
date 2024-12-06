# pylint: disable=missing-class-docstring
import re
import typing as t

OPERATIONS = {
    "+": lambda x, y: x + y,
    "*": lambda x, y: x * y,
}


class Operator(t.Protocol):  # pylint: disable=too-few-public-methods
    def __call__(self, first: int, second: int) -> int: ...


# pylint: disable=too-many-instance-attributes,too-many-arguments
class Monkey:
    worry: int
    operation: Operator

    _a: int | str
    _b: int | str

    def __init__(self, items: list[int], operation: str, divisor: int, if_true: int, if_false: int):
        self.items = items
        self.if_true, self.if_false = if_true, if_false
        self.divisor = divisor
        self.operation = self.parse_op(operation)

        self.count = 0

    @property
    def first(self) -> int:
        if self._a == "old":
            return self.worry

        return t.cast(int, self._a)

    @property
    def second(self) -> int:
        if self._b == "old":
            return self.worry

        return t.cast(int, self._b)

    @staticmethod
    def parse(data: str) -> "Monkey":
        pattern = re.compile(
            r"Monkey \d+:\s+.+: (.*)$\s+.+: new = (.*)$\s+.+?(\d+)$\s+If true.+? (\d+)$\s+If false.+? (\d+)",
            re.MULTILINE,
        )
        if matches := pattern.search(data):
            items, operation, divisor, true, false = matches.groups()

        monkey = Monkey(list(map(int, items.split(", "))), operation, int(divisor), int(true), int(false))

        return monkey

    def parse_op(self, op_string: str) -> Operator:
        first, operation, second = op_string.split(" ")

        self._a = int(first) if first != "old" else "old"
        self._b = int(second) if second != "old" else "old"

        return OPERATIONS[operation]

    def step(self, modulo: t.Optional[int] = None) -> t.Iterator[tuple[int, int]]:
        while self.items:
            self.count += 1
            self.worry = self.items.pop(0)
            self.worry = self.operation(self.first, self.second)

            if modulo is None:  # Part One
                self.worry = self.worry // 3

            else:  # Part Two
                self.worry = self.worry % modulo

            if self.worry % self.divisor == 0:
                yield self.if_true, self.worry

            else:
                yield self.if_false, self.worry
