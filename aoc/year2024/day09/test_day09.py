import typing

import pytest

from aoc.year2024.day09.day09 import SAMPLE_INPUT, part_one, part_two

T = typing.TypeVar("T")


@pytest.mark.parametrize(
    ("expected", "func"),
    [
        (1928, part_one),
        (2858, part_two),
    ],
    ids=("one", "two"),
)
class TestYear2024:
    def test_day(self, expected: T, func: typing.Callable[[str], T]) -> None:
        assert expected == func(SAMPLE_INPUT)
