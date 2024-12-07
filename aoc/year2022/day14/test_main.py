import typing

import pytest

from aoc.year2022.day14.main import SAMPLE_INPUT, part_one, part_two

T = typing.TypeVar("T")


@pytest.mark.parametrize(
    ("expected", "func"),
    [
        (24, part_one),
        (93, part_two),
    ],
    ids=("one", "two"),
)
class TestYear2022:
    def test_day(self, expected: T, func: typing.Callable[[str], T]) -> None:
        assert expected == func(SAMPLE_INPUT)
