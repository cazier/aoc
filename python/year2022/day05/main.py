import re
from collections import defaultdict

import utils

SAMPLE_INPUT: str = """    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


def parse(commands: str) -> tuple[dict[int, list[str]], list[tuple[int, ...]]]:
    out = defaultdict(list)
    for line in (order := commands.split("\n\n"))[0].splitlines()[-2::-1]:
        for num in range(len(line) // 3):
            if char := line[(num * 4) + 1 : (num * 4) + 2].strip():
                out[num + 1].append(char)

    moves = [tuple(map(int, i)) for i in re.findall(r"move (\d+) from (\d+) to (\d+)", order[1])]

    return dict(out), moves


def part_one(inputs: str) -> str:
    maps, moves = parse(inputs)

    for (count, _from, _to) in moves:
        for _ in range(count):
            maps[_to].append(maps[_from].pop())

    return "".join(l[-1] for l in maps.values())


def part_two(inputs: str) -> str:
    maps, moves = parse(inputs)

    for (count, _from, _to) in moves:
        storage = [maps[_from].pop() for _ in range(count)]

        for crates in storage[-1::-1]:
            maps[_to].append(crates)

    return "".join(l[-1] for l in maps.values())


if __name__ == "__main__":
    input_string = utils.load_input("2022", "05")

    print(part_one(input_string))
    print(part_two(input_string))
