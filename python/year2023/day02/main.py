# pylint: disable=missing-class-docstring

import re
import itertools
import dataclasses

from rich import print  # pylint: disable=redefined-builtin

import utils

SAMPLE_INPUT: str = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

"""


@dataclasses.dataclass
class Colors:
    red: int = 0
    green: int = 0
    blue: int = 0

    def __add__(self, other: "Colors") -> "Colors":
        self.red = max(self.red, other.red)
        self.green = max(self.green, other.green)
        self.blue = max(self.blue, other.blue)

        return self

    def mul(self) -> int:
        return self.red * self.green * self.blue

    def __le__(self, other: "Colors") -> bool:
        return self.red <= other.red and self.green <= other.green and self.blue <= other.blue


LIMITS = Colors(red=12, green=13, blue=14)
PATTERN = re.compile(r" (?:(\d+) (\w+),?)+")


def _parse(game: str) -> Colors:
    _, rounds = game.split(":")

    return list(
        itertools.accumulate(
            (Colors(**{color: int(num) for num, color in PATTERN.findall(round)}) for round in rounds.split(";")),
            initial=Colors(),
        )
    )[-1]


def part_one(inputs: str) -> int:
    return sum(id for id, game in enumerate(utils.splitlines(inputs), start=1) if LIMITS >= _parse(game))


def part_two(inputs: str) -> int:
    return sum(_parse(game).mul() for game in utils.splitlines(inputs))


if __name__ == "__main__":  # pragma: no cover
    input_string = utils.load_input("2023", "02")

    print(part_one(input_string))
    print(part_two(input_string))
