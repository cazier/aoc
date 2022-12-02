from main import SAMPLE_INPUT, part_one, part_two
from ward import test


@test("2022-02: Part One")
def _() -> None:
    expected = 15
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2022-02: Part Two")
def _() -> None:
    expected = 12
    output = part_two(SAMPLE_INPUT)

    assert expected == output
