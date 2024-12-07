import typing

import pytest

from aoc.year2023.day01.main import SAMPLE_INPUT_ONE, SAMPLE_INPUT_TWO, part_one, part_two

T = typing.TypeVar("T")


@pytest.mark.parametrize(
    ("expected", "input", "func"),
    [
        (142, SAMPLE_INPUT_ONE, part_one),
        (281, SAMPLE_INPUT_TWO, part_two),
    ],
    ids=("one", "two"),
)
class TestYear2023:
    def test_day(self, expected: T, input: str, func: typing.Callable[[str], T]) -> None:
        assert expected == func(input)
