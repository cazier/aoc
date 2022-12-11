import typing as t
import pathlib
import itertools

from rich import print  # pylint: disable=redefined-builtin

import utils
from utils.display import Display

SAMPLE_INPUT: str = pathlib.Path(__file__).parent.joinpath("sample.txt").read_text(encoding="utf8")


class Device:  # pylint: disable=missing-class-docstring
    cycle: int = 1
    register: int = 1
    commands: list[t.Iterator[int]] = []
    screen: Display = Display(6, 40)

    def __init__(self, commands: list[str]):
        self.commands = []

        for command, *value in (cmd.split() for cmd in reversed(commands)):
            if command == "noop":
                self.commands.append(self._noop(None))

            elif command == "addx":
                self.commands.append(self._addx(value[0]))

    def run(self) -> int:
        strength = 0

        while True:
            command = self.commands.pop()

            for out in iter(command):
                self.cycle += 1
                self.register += out

                if self.cycle in [20, 60, 100, 140, 180, 220]:
                    strength += self.cycle * self.register

                if self.cycle > 220:
                    return strength

    def draw(self) -> int:
        while True:
            command = self.commands.pop()

            for out in iter(command):
                self.color_pixel()
                self.cycle += 1
                self.register += out

                if self.cycle > 240:
                    return 1

    def color_pixel(self) -> None:
        cycle = self.cycle - 1

        row = cycle // 40
        column = cycle % 40

        self.screen.draw(column, row, "#" if abs(self.register - column) <= 1 else ".")

    @staticmethod
    def _noop(_: None) -> t.Iterator[int]:
        yield 0

    @staticmethod
    def _addx(command_value: str) -> t.Iterator[int]:
        for value in [0, int(command_value)]:
            yield value


def part_one(inputs: str) -> int:
    cpu = Device(inputs.splitlines())

    return cpu.run()


def part_one_comp(inputs: str) -> int:
    cmds = [[0] if command == "noop" else [0, int(value[0])] for command, *value in map(str.split, inputs.splitlines())]

    return sum(
        cycle * sum([1] + list(itertools.chain.from_iterable(cmds))[: cycle - 1])
        for cycle in (20, 60, 100, 140, 180, 220)
    )


def part_two(inputs: str) -> Display:
    cpu = Device(inputs.splitlines())

    cpu.draw()

    return cpu.screen


if __name__ == "__main__":  # pragma: no cover
    input_string = utils.load_input("2022", "10")

    print(part_one(input_string))
    print(part_two(input_string).characters())
