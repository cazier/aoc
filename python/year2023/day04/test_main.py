from ward import test
from year2023.day04.main import SAMPLE_INPUT, part_one, part_two


@test("2023-04: Part One")  # type: ignore
def _() -> None:
    expected = 13
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2023-04: Part Two")  # type: ignore
def _() -> None:
    expected = 30
    output = part_two(SAMPLE_INPUT)

    assert expected == output
