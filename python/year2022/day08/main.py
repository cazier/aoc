from rich import print  # pylint: disable=redefined-builtin

import utils
from utils.grid import Grid, Coord, Direction

SAMPLE_INPUT: str = """30373
25512
65332
33549
35390
"""


def part_one(inputs: str) -> int:
    def visible(coordinate: Coord) -> bool:
        for direction in Direction.types():
            if heights.get(coordinate) > max(heights.values(coordinate, direction)):
                return True

        return False

    heights = Grid.create(inputs, int)

    return sum(heights.is_on_edge(coord) or visible(coord) for coord in heights.iter_coord())


def part_two(inputs: str) -> int:
    def visible(coordinate: Coord) -> int:
        height = heights.get(coordinate)
        score = 1

        for direction in Direction.types():
            multiply = 0

            for index, coord in enumerate(heights.coordinates(coordinate, direction), 1):
                multiply = index

                if heights.get(coord) >= height:
                    break

            score *= multiply

        return score

    heights = Grid.create(inputs, int)

    return max(visible(coord) for coord in heights.iter_coord())


if __name__ == "__main__":  # pragma: no cover
    input_string = utils.load_input("2022", "08")

    print(part_one(input_string))
    print(part_two(input_string))
