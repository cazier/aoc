from ward import test
from year2022.day10.main import SAMPLE_INPUT, part_one, part_two, part_one_comp


@test("2022-10: Part One")  # type: ignore
def _() -> None:
    expected = 13140
    output = part_one(SAMPLE_INPUT)

    assert expected == output

    assert expected == part_one_comp(SAMPLE_INPUT)


@test("2022-10: Part Two")  # type: ignore
def _() -> None:
    expected = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""
    output = part_two(SAMPLE_INPUT).show()

    assert expected == output
