import itertools

import utils
from rich import print  # pylint: disable=redefined-builtin

SAMPLE_INPUT: str = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def parse(inputs: str) -> list[list[int]]:
    return [list(map(int, line.split())) for line in inputs.splitlines() if line]


def check(line: list[int]) -> bool:
    if line != sorted(line) and line != sorted(line, reverse=True):
        return False

    for first, second in itertools.pairwise(line):
        if abs(first - second) < 1 or abs(first - second) > 3:
            return False

    return True


def line_check(line: list[int]) -> bool:
    if check(line):
        return True

    for _line in [line[:index] + line[index + 1 :] for index in range(len(line))]:
        if check(_line):
            return True

    return False


def part_one(inputs: str) -> int:
    return sum(check(line) for line in parse(inputs))


def part_two(inputs: str) -> int:
    return sum(line_check(line) for line in parse(inputs))


if __name__ == "__main__":  # pragma: no cover
    input_string = utils.load_input("2024", "02")

    print(part_one(SAMPLE_INPUT))
    print(part_two(input_string))
