from y2022.d03.main import SAMPLE_INPUT, part_one, part_two
from ward import test


@test("2022-03: Part One")
def _() -> None:
    expected = 157
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2022-03: Part Two")
def _() -> None:
    expected = 70
    output = part_two(SAMPLE_INPUT)

    assert expected == output
