from ward import test
from year2024.day01.main import SAMPLE_INPUT, part_one, part_two  # type: ignore[import-not-found]


@test("2024-01: Part One")  # type: ignore
def _() -> None:
    expected = 11
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2024-01: Part Two")  # type: ignore
def _() -> None:
    expected = 31
    output = part_two(SAMPLE_INPUT)

    assert expected == output
