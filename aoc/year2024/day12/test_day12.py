import typing

import pytest

from aoc.year2024.day12.day12 import SAMPLE_INPUT, part_one, part_two

T = typing.TypeVar("T")


@pytest.mark.parametrize(
    ("expected", "func"),
    [
        (1930, part_one),
        (1206, part_two),
    ],
    ids=("one", "two"),
)
class TestYear2024:
    def test_day(self, expected: T, func: typing.Callable[[str], T]) -> None:
        assert expected == func(SAMPLE_INPUT)
