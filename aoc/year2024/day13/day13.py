import re
import typing
import dataclasses

from aoclib.grid import Coord

SAMPLE_INPUT: str = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""


@dataclasses.dataclass
class Machine:
    a_step: Coord
    b_step: Coord
    prize: Coord

    _prize = re.compile(r"Prize: X=(?P<px>\d+), Y=(?P<py>\d+)")
    _buttons = re.compile(r"Button A: X\+(?P<ax>\d+), Y\+(?P<ay>\d+)\nButton B: X\+(?P<bx>\d+), Y\+(?P<by>\d+)")

    @classmethod
    def parse(cls, config: str, offset: int = 0) -> typing.Self:
        buttons = {key: int(value) for key, value in cls._buttons.search(config).groupdict().items()}  # type: ignore[union-attr]
        prize = {key: int(value) for key, value in cls._prize.search(config).groupdict().items()}  # type: ignore[union-attr]

        return cls(
            a_step=Coord(buttons["ax"], buttons["ay"]),
            b_step=Coord(buttons["bx"], buttons["by"]),
            prize=Coord(offset + prize["px"], offset + prize["py"]),
        )

    def solve(self) -> int:
        s = self.prize.det(self.a_step) // self.a_step.T.det(self.b_step.T)
        t = self.prize.det(self.b_step) // self.b_step.T.det(self.a_step.T)

        if (self.a_step.x * t + self.b_step.x * s, self.a_step.y * t + self.b_step.y * s) == self.prize.G:
            return (3 * t) + s

        return 0


def part_one(inputs: str) -> int:
    machines = [Machine.parse(data) for data in inputs.strip().split("\n\n")]
    return sum(machine.solve() for machine in machines)


def part_two(inputs: str) -> int:
    machines = [Machine.parse(data, int(1e13)) for data in inputs.strip().split("\n\n")]
    return sum(machine.solve() for machine in machines)
