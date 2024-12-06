from ward import test
from year2022.day12.main import SAMPLE_INPUT, part_one, part_two


@test("2022-12: Part One")  # type: ignore
def _() -> None:
    expected = 31
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2022-12: Part Two")  # type: ignore
def _() -> None:
    expected = 29
    output = part_two(SAMPLE_INPUT)

    assert expected == output
