from ward import test
from year2022.day11.main import SAMPLE_INPUT, part_one, part_two


@test("2022-11: Part One")  # type: ignore
def _() -> None:
    expected = 10605
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2022-11: Part Two")  # type: ignore
def _() -> None:
    expected = 2713310158
    output = part_two(SAMPLE_INPUT)

    assert expected == output
