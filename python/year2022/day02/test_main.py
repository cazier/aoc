from ward import test
from year2022.day02.main import SAMPLE_INPUT, part_one, part_two


@test("2022-02: Part One")  # type: ignore
def _() -> None:
    expected = 15
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2022-02: Part Two")  # type: ignore
def _() -> None:
    expected = 12
    output = part_two(SAMPLE_INPUT)

    assert expected == output
