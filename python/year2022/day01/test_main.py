from ward import test
from year2022.day01.main import SAMPLE_INPUT, part_one, part_two


@test("2022-01: Part One")
def _() -> None:
    expected = 24000
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2022-01: Part Two")
def _() -> None:
    expected = 45000
    output = part_two(SAMPLE_INPUT)

    assert expected == output
