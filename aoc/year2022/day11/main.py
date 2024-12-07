import pathlib
import functools

from rich import print  # pylint: disable=redefined-builtin

import aoclib

from .monkey import Monkey

SAMPLE_INPUT: str = pathlib.Path(__file__).parent.joinpath("sample.txt").read_text(encoding="utf8")


def part_one(inputs: str) -> int:
    monkeys = {number: Monkey.parse(data) for number, data in enumerate(inputs.split("\n\n"))}
    number = len(monkeys)

    for _ in range(20):
        for monkey in range(number):
            for direction, item in monkeys[monkey].step():
                monkeys[direction].items.append(item)

    sort = sorted(monkeys.values(), key=lambda k: k.count, reverse=True)

    return sort[0].count * sort[1].count


def part_two(inputs: str) -> int:
    monkeys = {number: Monkey.parse(data) for number, data in enumerate(inputs.split("\n\n"))}
    number = len(monkeys)

    modulo = functools.reduce(lambda x, y: x * y, map(lambda k: k.divisor, monkeys.values()))

    for _ in range(10000):
        for monkey in range(number):
            for direction, item in monkeys[monkey].step(modulo):
                monkeys[direction].items.append(item)

    sort = sorted(monkeys.values(), key=lambda k: k.count, reverse=True)

    return sort[0].count * sort[1].count


if __name__ == "__main__":  # pragma: no cover
    input_string = aoclib.load_input("2022", "11")

    print(part_one(input_string))
    print(part_two(input_string))
