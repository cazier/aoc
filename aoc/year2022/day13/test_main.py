from ward import test
from year2022.day13.main import SAMPLE_INPUT, part_one, part_two


@test("2022-13: Part One")  # type: ignore
def _() -> None:
    expected = 13
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2022-13: Part Two")  # type: ignore
def _() -> None:
    expected = 140
    output = part_two(SAMPLE_INPUT)

    assert expected == output
