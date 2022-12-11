import typing as t
import itertools

from rich import print  # pylint: disable=redefined-builtin

import utils
from utils.grid import Coord

SAMPLE_INPUT: str = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

DIRECTION_KEY = {"U": Coord(0, -1), "L": Coord(-1, 0), "D": Coord(0, 1), "R": Coord(1, 0)}


def read(inputs: str) -> t.Iterator[Coord]:
    for direction, steps in map(str.split, inputs.splitlines()):
        for _ in range(int(steps)):
            yield DIRECTION_KEY[direction]


def visualizer(rope: dict[int, Coord]) -> None:
    """A simple terminal visualizer for the rope movement. Note isn't universal, and currently has hardcoded values for
    the grid height/width.

    Args:
        rope (dict[int, Coord]): rope values to show
    """
    board = [["." for _ in range(6)] for _ in range(5)]

    for knot, coord in reversed(rope.items()):
        (x, y) = coord.x, coord.y + 4

        if knot == 0:
            show = "H"
        else:
            show = str(knot)

        board[y][x] = show

    print("\n".join("".join(map(str, l)) for l in board))
    input()


def part_one(inputs: str) -> int:
    head, tail = Coord(0, 0), Coord(0, 0)

    visits = set()

    for steps in read(inputs):
        head += steps

        if not tail.touching(head):
            tail += (head - tail).normalize()

        visits.add(tail.G)

    return len(list(visits))


def part_two(inputs: str) -> int:
    rope = {knot: Coord(0, 0) for knot in range(0, 10)}

    visits = set()

    for steps in read(inputs):
        rope[0] += steps

        for (_, front), (index, back) in itertools.pairwise(rope.items()):
            if not back.touching(front):
                rope[index] += (front - back).normalize()

        visits.add(rope[9].G)

    return len(list(visits))


if __name__ == "__main__":
    input_string = utils.load_input("2022", "09")

    print(part_one(input_string))
    print(part_two(input_string))
