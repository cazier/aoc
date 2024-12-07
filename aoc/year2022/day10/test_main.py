import typing

import pytest

from aoc.year2022.day10.day10 import SAMPLE_INPUT, part_one, part_two, part_one_comp

T = typing.TypeVar("T")


@pytest.mark.parametrize(
    ("expected", "func"),
    [
        (13140, part_one),
        (13140, part_one_comp),
        (
            """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....""",
            lambda k: part_two(k).show(),
        ),
    ],
    ids=("one", "one-alt", "two"),
)
class TestYear2022:
    def test_day(self, expected: T, func: typing.Callable[[str], T]) -> None:
        assert expected == func(SAMPLE_INPUT)
