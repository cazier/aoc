import typing

import pytest

from aoc.year2024.day04.main import SAMPLE_INPUT, part_one, part_two

T = typing.TypeVar("T")


@pytest.mark.parametrize(
    ("expected", "func"),
    [
        (18, part_one),
        (9, part_two),
    ],
    ids=("one", "two"),
)
class TestYear2024:
    def test_day(self, expected: T, func: typing.Callable[[str], T]) -> None:
        assert expected == func(SAMPLE_INPUT)
