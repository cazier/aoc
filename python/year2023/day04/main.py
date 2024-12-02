import re
import collections

from rich import print  # pylint: disable=redefined-builtin

import utils

SAMPLE_INPUT: str = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def _set_map(inputs: str) -> set[int]:
    return set(map(int, inputs.split()))


def part_one(inputs: str) -> int:
    cards = {
        num: _set_map((group := re.search(r": (.*) \| (.*)", line).groups())[0]).intersection(_set_map(group[1]))
        for num, line in enumerate(utils.splitlines(inputs))
    }

    return sum(int(2 ** (len(card) - 1)) for card in cards.values())


def part_two(inputs: str) -> int:
    cards = {
        num: len(_set_map((group := re.search(r": (.*) \| (.*)", line).groups())[0]).intersection(_set_map(group[1])))
        for num, line in enumerate(utils.splitlines(inputs), start=1)
    }

    cutoff = max(cards.keys())
    print(cards)

    counters = {key: 1 for key in cards.keys()}

    for key in cards:
        for step in range(key, min(key + cards[key] + 1, cutoff)):
            print(f"{key=}, {step=}")
            counters[step] += counters[key]

    print(counters)

    # key = 1
    # total = 0
    # duplicates = collections.defaultdict(int)

    # while key <= cutoff:
    #     count = cards[key]
    #     for increase in range(key + 1, key + count + 1):
    #         print(f'{key=} {increase=} Adding {cards[increase]} to total')
    #         total += cards[increase]

    #     total += 1
    #     print(key)
    #     key += 1

    return sum(counters.values())


# import sys
# import re
# from collections import defaultdict

if __name__ == "__main__":  # pragma: no cover
    input_string = utils.load_input("2023", "04")

    # D = open(sys.argv[1]).read().strip()
    lines = input_string.splitlines()
    p1 = 0
    N = collections.defaultdict(int)
    for i, line in enumerate(lines):
        N[i] += 1
        first, rest = line.split("|")
        id_, card = first.split(":")
        card_nums = [int(x) for x in card.split()]
        rest_nums = [int(x) for x in rest.split()]
        val = len(set(card_nums) & set(rest_nums))
        if val > 0:
            p1 += 2 ** (val - 1)
        for j in range(val):
            N[i + 1 + j] += N[i]
    print(p1)
    print(sum(N.values()))

    print(part_one(input_string))
    print(part_two(SAMPLE_INPUT))
