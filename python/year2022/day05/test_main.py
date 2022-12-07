from ward import test
from year2022.day05.main import SAMPLE_INPUT, part_one, part_two


@test("2022-05: Part One")
def _() -> None:
    expected = "CMZ"
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2022-05: Part Two")
def _() -> None:
    expected = "MCD"
    output = part_two(SAMPLE_INPUT)

    assert expected == output
