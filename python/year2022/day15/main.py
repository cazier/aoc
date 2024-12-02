import re
import typing as t

from rich import print  # pylint: disable=redefined-builtin

import utils
from utils.grid import Grid, Coord, Direction

SAMPLE_INPUT: str = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

PATTERN = re.compile(r".*x=(-?\d+), y=(-?\d+).*x=(-?\d+), y=(-?\d+)")


def manhattan(first: Coord, second: Coord) -> int:
    return sum(abs(first - second).G)


def edges(sensor: Coord, beacon: Coord) -> t.Iterator[Coord]:
    limit = manhattan(sensor, beacon)

    for quadrant in Direction.diagonals():
        for sy in range(limit + 1):
            for sx in range(limit + 1):
                if 0 < sx + sy <= limit:
                    yield sensor + (quadrant.value[0].pairwise((sx, sy)))


def get(grid: Grid, coord: Coord) -> str:
    try:
        return grid.get(coord)

    except KeyError:
        return None


def _parse(inputs: str) -> Grid[str]:
    for line in inputs.splitlines():
        yield list(map(int, PATTERN.search(line).groups()))


def part_one(inputs: str) -> int:
    grid = Grid({})

    for sx, sy, bx, by in _parse(inputs):
        grid.set(s := Coord(sx, sy), "S", anywhere=True)
        grid.set(b := Coord(bx, by), "B", anywhere=True)

        # min_bound, max_bound = Coord(*grid.min_bound.G), Coord(*grid.max_bound.G)

        # for sx, sy, bx, by in _parse(inputs):
        for i in edges(s, b):
            if i not in grid:
                grid.set(i, "#", anywhere=True)

    # grid._min_bound = min_bound
    # grid._max_bound = max_bound

    # for center in list(grid.iter_coord()):
    #     if not grid.within(center):
    #         grid.pop(center)

    # print(grid)
    return sum(1 for c in grid.columns if get(grid, Coord(c, 2000000)) == "#")

    result = {}

    for row in grid.rows:
        num = 0
        for column in grid.columns:
            if get(grid, Coord(column, row)) not in ("None", "B"):
                num += 1

        result[row] = num

    return result

    # for i in edges(Coord(8, 7), Coord(2, 10)):
    #     try:
    #         grid.set(i, "#", within=True)

    #     except ValueError:
    #         pass

    print(grid)

    return


def part_two(inputs: str) -> int:
    return


if __name__ == "__main__":  # pragma: no cover
    input_string = utils.load_input("2022", "15")
    # input_string = SAMPLE_INPUT

    print(part_one(input_string))
    print(part_two(input_string))
