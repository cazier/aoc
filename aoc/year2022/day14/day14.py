import typing
import itertools

from aoclib.grid import Grid, Coord
from aoclib.helpers import zip_longest_repeating

SAMPLE_INPUT: str = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

START = Coord(500, 0)


def _gen_path(start: int, stop: int) -> typing.Iterator[int]:
    if start > stop:
        step = -1

    else:
        step = 1

    yield from range(start, stop + step, step)


class WallGrid(Grid[str]):
    def __init__(self, inputs: str) -> None:
        super().__init__({})

        for path in inputs.splitlines():
            for start, finish in itertools.pairwise(path.split(" -> ")):
                x1, y1 = tuple(map(int, start.split(",")))
                x2, y2 = tuple(map(int, finish.split(",")))

                for x, y in zip_longest_repeating(_gen_path(x1, x2), _gen_path(y1, y2)):
                    self.set(Coord(x, y), "#", True)

    def next(self, center: Coord) -> bool | Coord:
        possibilities = [(center + c) for c in ((0, 1), (-1, 1), (1, 1))]

        for new in possibilities:
            if (new in self and self.get(new) not in ("#", "o")) or (new not in self and self.within(new)):
                return new

        if all(map(self.within, possibilities)):
            return True

        return False


def part_one(inputs: str) -> int:
    grid = WallGrid(inputs)

    grid.set(START, "+", True)

    counter = 0

    while True:
        cell = START

        while True:
            result = grid.next(cell)

            if isinstance(result, Coord):
                cell = result

            elif result is True:
                grid.set(cell, "o", anywhere=True)
                break

            else:
                return counter

        counter += 1


def part_two(inputs: str) -> int:
    start = Coord(500, 0)
    grid = WallGrid(inputs)

    floor = grid.max_bound.y + 2

    grid.set(start, "+", True)

    counter = 0

    while True:
        cell = start

        while True:
            grid.set(Coord(cell.x - 1, floor), "#", True)
            grid.set(Coord(cell.x + 1, floor), "#", True)

            result = grid.next(cell)

            if isinstance(result, Coord):
                cell = result

            elif result is True and cell != START:
                grid.set(cell, "o", anywhere=True)
                break

            else:
                return counter + 1

        counter += 1
