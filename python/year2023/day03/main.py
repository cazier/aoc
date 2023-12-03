import string
import operator
import collections

from rich import print  # pylint: disable=redefined-builtin

import utils
from utils.grid import Grid, Coord

SAMPLE_INPUT: str = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


class Schematic(Grid[str]):
    """Grid subclass to support day 03's parts list/schematic"""

    NON_PARTS = list(string.digits) + [".", None]

    def parts(self, centers: list[Coord]) -> set[Coord]:
        resp = set()
        for coord in centers:
            for neighbor in self.neighbors(coord):
                if self.get(neighbor) not in self.NON_PARTS:
                    resp.add(neighbor)

        return resp


def find_numbers(grid: Schematic) -> list[tuple[int, list[Coord]]]:
    numbers = []

    for row in grid.iter_rows():
        number = ""
        coords = []
        for column in grid.iter_columns():
            coordinate = Coord(column, row)
            value = grid.get(coordinate)

            if value and value in string.digits:
                number = f"{number}{value}"
                coords.append(coordinate)
                continue

            if number:
                numbers.append((int(number), coords[:]))
                number = ""
                coords = []

        if number:
            numbers.append((int(number), coords[:]))

    return numbers


def part_one(inputs: str) -> int:
    schematic = Schematic.create(inputs)
    return sum(number for number, coords in find_numbers(schematic) if schematic.parts(coords))


def part_two(inputs: str) -> int:
    schematic = Schematic.create(inputs)

    gears = collections.defaultdict(list)

    for number, coords in find_numbers(schematic):
        for part in schematic.parts(coords):
            gears[part].append(number)

    return sum(operator.mul(*numbers) for numbers in gears.values() if len(numbers) == 2)


if __name__ == "__main__":  # pragma: no cover
    input_string = utils.load_input("2023", "03")

    print(part_one(input_string))
    print(part_two(input_string))
