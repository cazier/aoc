from ward import test
from year2023.day01.main import SAMPLE_INPUT_ONE, SAMPLE_INPUT_TWO, part_one, part_two


@test("2023-01: Part One")  # type: ignore
def _() -> None:
    expected = 142
    output = part_one(SAMPLE_INPUT_ONE)

    assert expected == output


@test("2023-01: Part Two")  # type: ignore
def _() -> None:
    expected = 281
    output = part_two(SAMPLE_INPUT_TWO)

    assert expected == output
