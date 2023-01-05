from ward import test
from year2022.day14.main import SAMPLE_INPUT, part_one, part_two


@test("2022-14: Part One")  # type: ignore
def _() -> None:
    expected = 24
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2022-14: Part Two")  # type: ignore
def _() -> None:
    expected = 93
    output = part_two(SAMPLE_INPUT)

    assert expected == output
