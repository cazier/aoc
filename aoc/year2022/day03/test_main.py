import typing

import pytest

from aoc.year2022.day03.main import SAMPLE_INPUT, part_one, part_two

T = typing.TypeVar("T")


@pytest.mark.parametrize(
    ("expected", "func"),
    [
        (157, part_one),
        (70, part_two),
    ],
    ids=("one", "two"),
)
class TestYear2022:
    def test_day(self, expected: T, func: typing.Callable[[str], T]) -> None:
        assert expected == func(SAMPLE_INPUT)
