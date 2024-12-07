import re

from rich import print  # pylint: disable=redefined-builtin

import aoclib

SAMPLE_INPUT_ONE: str = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

SAMPLE_INPUT_TWO: str = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

LEGEND = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


STRINGS = "|".join((r"\d", *LEGEND.keys()))

digit = re.compile(r"\d")
chars = re.compile(rf"(?=({STRINGS}))")


def _nums(word: str, char: bool = False) -> int:
    if char:
        pattern = chars
        legend = LEGEND

    else:
        pattern = digit
        legend = {value: value for value in LEGEND.values()}

    first, *remainder = re.findall(pattern, word)

    last = remainder[-1] if remainder else first

    return int(f"{legend.get(first, first)}{legend.get(last, last)}")


def part_one(inputs: str) -> int:
    return sum(_nums(line) for line in aoclib.splitlines(inputs))


def part_two(inputs: str) -> int:
    return sum(_nums(line, True) for line in aoclib.splitlines(inputs))


if __name__ == "__main__":
    input_string = aoclib.load_input("2023", "01")

    print(part_one(input_string))
    print(part_two(input_string))
