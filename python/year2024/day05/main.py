import typing
import graphlib
import collections

import utils
from rich import print  # pylint: disable=redefined-builtin

SAMPLE_INPUT: str = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


def parse_rules(rules: str) -> list[typing.Callable[[list[int]], bool]]:
    def _gen_func(first: int, second: int) -> typing.Callable[[list[int]], bool]:
        def inner(values: list[int]) -> bool:
            if values.count(first) + values.count(second) != 2:
                return True
            return values.index(first) < values.index(second)

        return inner

    return [_gen_func(*map(int, line.split("|"))) for line in rules.splitlines() if line]


def generate_graph(rules: str, *keep: int) -> list[int]:
    nodes = collections.defaultdict(list)

    for line in rules.splitlines():
        if line:
            first, second = map(int, line.split("|", maxsplit=1))

            if first in keep and second in keep:
                nodes[second].append(first)

    return list(graphlib.TopologicalSorter(nodes).static_order())


def parse_updates(updates: str) -> list[list[int]]:
    return [[int(value) for value in line.split(",")] for line in updates.splitlines() if line]


def part_one(inputs: str) -> int:
    _rules, _updates = inputs.split("\n\n")
    rules, updates = parse_rules(_rules), parse_updates(_updates)

    return sum(update[len(update) // 2] for update in updates if all([rule(update) for rule in rules]))


def printer(values: list[bool]) -> None:
    print("".join("." if value else "X" for value in values))


def part_two(inputs: str) -> int:
    _rules, _updates = inputs.split("\n\n")
    rules, updates = parse_rules(_rules), parse_updates(_updates)

    answer = 0

    for update in updates:
        if all([rule(update) for rule in rules]):
            continue

        fix = [number for number in generate_graph(_rules, *update) if number in update]

        answer += fix[len(fix) // 2]

    return answer


if __name__ == "__main__":  # pragma: no cover
    input_string = utils.load_input("2024", "05")

    print(part_one(input_string))
    print(part_two(input_string))
