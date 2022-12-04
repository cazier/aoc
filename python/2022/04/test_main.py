from main import SAMPLE_INPUT, part_one, part_two
from ward import test


@test("2022-04: Part One")
def _() -> None:
    expected = 2
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2022-04: Part Two")
def _() -> None:
    expected = 4
    output = part_two(SAMPLE_INPUT)

    assert expected == output
