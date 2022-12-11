from ward import test
from year2022.day08.main import SAMPLE_INPUT, part_one, part_two


@test("2022-08: Part One")  # type: ignore
def _() -> None:
    expected = 21
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2022-08: Part Two")  # type: ignore
def _() -> None:
    expected = 8
    output = part_two(SAMPLE_INPUT)

    assert expected == output
