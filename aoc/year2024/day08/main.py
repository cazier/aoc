import itertools
import collections

from aoclib.grid import Grid, Coord

SAMPLE_INPUT: str = """
............
........O...
.....O......
.......O....
....O.......
......A.....
............
............
........A...
.........A..
............
............
"""


def part_one(inputs: str) -> int:
    values: dict[str, set[Coord]] = collections.defaultdict(set)

    grid = Grid.create(inputs, filter=lambda k: k != ".")

    for coord, value in grid.items():
        values[value].add(coord)

    result = set()

    for value, items in values.items():
        for first, second in itertools.combinations(items, 2):
            for opposite in first.opposites(second):
                if Coord(0, 0) <= opposite <= grid.max_bound:
                    result.add(opposite)

    return len(result)


def part_two(inputs: str) -> int:
    values: dict[str, set[Coord]] = collections.defaultdict(set)

    grid = Grid.create(inputs, filter=lambda k: k != ".")

    for coord, value in grid.items():
        values[value].add(coord)

    antinodes = Grid.new(grid.max_bound.x + 1, grid.max_bound.y + 1)

    for value, items in values.items():
        for first, second in itertools.combinations(items, 2):
            antinodes.set(first, value)
            antinodes.set(second, value)

            for opposite in first.inline(second, (Coord(0, 0), grid.max_bound)):
                if grid.get(opposite, None) not in ("O", "A"):
                    antinodes.set(opposite, "#", anywhere=True)

    return len([value for value in antinodes.iter_values() if value != "."])
