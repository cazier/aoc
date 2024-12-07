import typing

import pytest

from aoc.year2024.day03.day03 import SAMPLE_INPUT_ONE, SAMPLE_INPUT_TWO, part_one, part_two

T = typing.TypeVar("T")


@pytest.mark.parametrize(
    ("expected", "input", "func"),
    [
        (161, SAMPLE_INPUT_ONE, part_one),
        (48, SAMPLE_INPUT_TWO, part_two),
    ],
    ids=("one", "two"),
)
class TestYear2024:
    def test_day(self, expected: T, input: str, func: typing.Callable[[str], T]) -> None:
        assert expected == func(input)
