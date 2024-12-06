from ward import test
from year2022.day07.main import SAMPLE_INPUT, part_one, part_two


@test("2022-07: Part One")  # type: ignore
def _() -> None:
    expected = 95437
    output = part_one(SAMPLE_INPUT)

    assert expected == output


@test("2022-07: Part Two")  # type: ignore
def _() -> None:
    expected = 24933642
    output = part_two(SAMPLE_INPUT)

    assert expected == output
