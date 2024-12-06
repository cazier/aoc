from ward import test
from year2022.day06.main import SAMPLE_INPUT, part_one, part_two


@test("2022-06: Part One")  # type: ignore
def _() -> None:
    expected = 7
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2022-06: Part Two")  # type: ignore
def _() -> None:
    expected = 19
    output = part_two(SAMPLE_INPUT)

    assert expected == output
