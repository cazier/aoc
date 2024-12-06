from ward import test
from year2022.day03.main import SAMPLE_INPUT, part_one, part_two


@test("2022-03: Part One")  # type: ignore
def _() -> None:
    expected = 157
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2022-03: Part Two")  # type: ignore
def _() -> None:
    expected = 70
    output = part_two(SAMPLE_INPUT)

    assert expected == output
