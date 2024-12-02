from rich import print  # pylint: disable=redefined-builtin

import utils
from utils.grid import Grid
from utils.algorithms import bfs

SAMPLE_INPUT: str = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""


def part_one(inputs: str) -> int:
    grid: Grid[int] = Grid.create(inputs, predicate=lambda k: (ord(k) - 97))

    [start] = grid.find(-14)
    [stop] = grid.find(-28)

    grid.set(start, 0)
    grid.set(stop, 25)

    path = bfs(
        start,
        lambda k: k == stop,
        grid.orthogonal,
        lambda k, j: (grid.get(j) - grid.get(k)) <= 1,
    )

    return len(path) - 1


def part_two(inputs: str) -> int:
    grid: Grid[int] = Grid.create(inputs, predicate=lambda k: (ord(k) - 97))

    [start] = grid.find(-14)
    [stop] = grid.find(-28)

    grid.set(start, 0)
    grid.set(stop, 25)

    path = bfs(
        stop,
        lambda k: grid.get(k) == 0,
        grid.orthogonal,
        lambda k, j: (grid.get(j) - grid.get(k)) >= -1,
    )

    return len(path) - 1


if __name__ == "__main__":  # pragma: no cover
    input_string = utils.load_input("2022", "12")

    print(part_one(input_string))
    print(part_two(input_string))
