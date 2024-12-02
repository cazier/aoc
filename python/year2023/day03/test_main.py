from ward import test
from year2023.day03.main import SAMPLE_INPUT, part_one, part_two


@test("2023-03: Part One")  # type: ignore
def _() -> None:
    expected = 4361
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2023-03: Part Two")  # type: ignore
def _() -> None:
    expected = 467835
    output = part_two(SAMPLE_INPUT)

    assert expected == output
