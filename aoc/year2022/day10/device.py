import typing

from aoclib.display import Display


class Device:
    cycle: int = 1
    register: int = 1
    commands: list[typing.Iterator[int]] = []
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
    def _noop(_: None) -> typing.Iterator[int]:
        yield 0

    @staticmethod
    def _addx(command_value: str) -> typing.Iterator[int]:
        for value in [0, int(command_value)]:
            yield value
