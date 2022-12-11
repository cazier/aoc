from rich import print  # pylint: disable=redefined-builtin

import utils

SAMPLE_INPUT: str = """A Y
B X
C Z
"""


def value(first: str, second: str) -> tuple[int, int]:
    return ord(first) - 64, ord(second) - 87


def part_one(inputs: str) -> int:
    def score(first: int, second: int) -> int:
        if (first % 3) + 1 == second:
            return second + 6

        if first == second:
            return second + 3

        return second

    guide = map(lambda k: k.split(" "), inputs.splitlines())

    return sum(score(*value(a, b)) for a, b in guide)


def part_two(inputs: str) -> int:
    def score(first: int, order: int) -> int:
        if order == 1:
            return ((first - 2) % 3) + 1

        if order == 2:
            return first + 3

        return (first % 3) + 1 + 6

    guide = map(lambda k: k.split(" "), inputs.splitlines())

    return sum(score(*value(a, b)) for a, b in guide)


if __name__ == "__main__":  # pragma: no cover
    input_string = utils.load_input("2022", "02")

    print(part_one(input_string))
    print(part_two(input_string))
