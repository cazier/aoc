import typing

import utils
from rich import print  # pylint: disable=redefined-builtin
from utils.grid import Grid, Coord, Direction

SAMPLE_INPUT: str = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""


@typing.overload
def patrol(start: Coord, grid: Grid[str], part: typing.Literal[1]) -> set[Coord]: ...


@typing.overload
def patrol(start: Coord, grid: Grid[str], part: typing.Literal[2]) -> bool: ...


def patrol(start: Coord, grid: Grid[str], part: typing.Literal[1, 2] = 1) -> set[Coord] | bool:
    def step(center: Coord, facing: Direction) -> tuple[Coord, Direction]:
        for direction in Direction.rotate(facing, orthogonal=True):
            new = center + direction.value[0]

            if new not in grid:
                raise StopIteration

            if grid.get(new) not in ("#", "O"):
                return new, direction

        raise KeyError

    steps = {start}
    facing = Direction.N
    positions = {(start, facing)}

    while True:
        try:
            start, facing = step(start, facing)
            steps.add(start)

            if part == 2 and (start, facing) in positions:
                return True

            positions.add((start, facing))

        except StopIteration:
            if part == 2:
                return False
            return steps


def part_one(inputs: str) -> int:
    grid = Grid.create(inputs)
    [guard] = grid.find("^")

    return len(list(patrol(guard, grid, part=1)))


def part_two(inputs: str) -> int:
    grid = Grid.create(inputs)
    [guard] = grid.find("^")

    valid = 0

    vals = grid.find(".", allow_multiple=True)

    for obstruction in vals:
        grid.set(obstruction, "O")

        if patrol(guard, grid, part=2):
            valid += 1

        grid.set(obstruction, ".")

    return valid


if __name__ == "__main__":  # pragma: no cover
    input_string = utils.load_input("2024", "06")

    print(part_one(input_string))
    print(part_two(input_string))
