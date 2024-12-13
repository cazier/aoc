import itertools

from aoclib.grid import Grid, Region

SAMPLE_INPUT: str = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""


def part_one(inputs: str) -> int:
    grid = Grid.create(inputs)
    return sum(region.area * len(region.perimeter()) for region in itertools.starmap(Region, grid.regions().items()))


def part_two(inputs: str) -> int:
    grid = Grid.create(inputs)
    return sum(region.area * region.edges() for region in itertools.starmap(Region, grid.regions().items()))
