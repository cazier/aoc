from ward import test
from year2022.day15.main import SAMPLE_INPUT, part_one, part_two


@test("2022-15: Part One")  # type: ignore
def _() -> None:
    expected = 26
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2022-15: Part Two")  # type: ignore
def _() -> None:
    expected = 26
    output = part_two(SAMPLE_INPUT)

    assert expected == output
