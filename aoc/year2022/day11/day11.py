import pathlib
import functools

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
