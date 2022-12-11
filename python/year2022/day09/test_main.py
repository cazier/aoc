from ward import test
from year2022.day09.main import SAMPLE_INPUT, part_one, part_two


@test("2022-09: Part One")  # type: ignore
def _() -> None:
    expected = 13
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2022-09: Part Two")  # type: ignore
def _() -> None:
    expected = 1
    output = part_two(SAMPLE_INPUT)

    assert expected == output
