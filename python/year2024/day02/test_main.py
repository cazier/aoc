from ward import test
from year2024.day02.main import SAMPLE_INPUT, part_one, part_two  # type: ignore[import-not-found]


@test("2024-02: Part One")  # type: ignore
def _() -> None:
    expected = 2
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2024-02: Part Two")  # type: ignore
def _() -> None:
    expected = 2
    output = part_two(SAMPLE_INPUT)

    assert expected == output
