from ward import test
from year2024.day05.main import SAMPLE_INPUT, part_one, part_two  # type: ignore[import-not-found]


@test("2024-05: Part One")  # type: ignore
def _() -> None:
    expected = 143
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2024-05: Part Two")  # type: ignore
def _() -> None:
    expected = 123
    output = part_two(SAMPLE_INPUT)

    assert expected == output
