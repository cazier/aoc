from ward import test
from year2024.day04.main import SAMPLE_INPUT, part_one, part_two  # type: ignore[import-not-found]


@test("2024-04: Part One")  # type: ignore
def _() -> None:
    expected = 18
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2024-04: Part Two")  # type: ignore
def _() -> None:
    expected = 9
    output = part_two(SAMPLE_INPUT)

    assert expected == output
