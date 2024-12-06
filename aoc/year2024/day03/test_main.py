from ward import test
from year2024.day03.main import SAMPLE_INPUT, SAMPLE_INPUT_2, part_one, part_two  # type: ignore[import-not-found]


@test("2024-03: Part One")  # type: ignore
def _() -> None:
    expected = 161
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2024-03: Part Two")  # type: ignore
def _() -> None:
    expected = 48
    output = part_two(SAMPLE_INPUT_2)

    assert expected == output
