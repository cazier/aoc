import aoclib.grid

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
    grid = aoclib.grid.Grid.create(inputs.upper().strip())
    x_centers = {coord for coord in grid.iter_coord() if grid.get(coord) == "X"}

    count = 0

    for x in x_centers:
        for word in grid.n_neighbors(x, n=3):
            if "".join(map(grid.get, word)) == "MAS":
                count += 1

    return count


def part_two(inputs: str) -> int:
    grid = aoclib.grid.Grid.create(inputs.upper().strip())
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
