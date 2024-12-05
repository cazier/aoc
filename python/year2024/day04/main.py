import utils
import utils.grid
from rich import print  # pylint: disable=redefined-builtin

SAMPLE_INPUT: str = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


def part_one(inputs: str) -> int:
    grid = utils.grid.Grid.create(inputs.upper().strip())
    x_centers = {coord for coord in grid.iter_coord() if grid.get(coord) == "X"}

    count = 0

    for x in x_centers:
        for word in grid.n_neighbors(x, n=3):
            if "".join(map(grid.get, word)) == "MAS":
                count += 1

    return count


def part_two(inputs: str) -> int:
    grid = utils.grid.Grid.create(inputs.upper().strip())
    a_centers = {coord for coord in grid.iter_coord() if grid.get(coord) == "A"}

    count = 0

    for a in a_centers:
        diagonals = [grid.get(coord) for coord in grid.diagonal(a)]

        if (
            (diagonals.count("M") == 2 and diagonals.count("S") == 2)
            and diagonals[0] != diagonals[2]
            and diagonals[1] != diagonals[3]
        ):
            count += 1

    return count


if __name__ == "__main__":  # pragma: no cover
    input_string = utils.load_input("2024", "04")

    print(part_one(input_string))
    print(part_two(input_string))
