import typing

import pytest

from aoc.year2024.day02.day02 import SAMPLE_INPUT, part_one, part_two

T = typing.TypeVar("T")


@pytest.mark.parametrize(
    ("expected", "func"),
    [
        (2, part_one),
        (4, part_two),
    ],
    ids=("one", "two"),
)
class TestYear2024:
    def test_day(self, expected: T, func: typing.Callable[[str], T]) -> None:
        assert expected == func(SAMPLE_INPUT)
