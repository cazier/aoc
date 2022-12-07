from ward import test
from year2022.day04.main import SAMPLE_INPUT, part_one, part_two


@test("2022-04: Part One")  # type: ignore
def _() -> None:
    expected = 2
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2022-04: Part Two")  # type: ignore
def _() -> None:
    expected = 4
    output = part_two(SAMPLE_INPUT)

    assert expected == output
