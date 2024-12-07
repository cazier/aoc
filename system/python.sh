TEST_NAME="test_main.py"
RUN_NAME="main.py"
DIR="${_CWD}/${LANGUAGE_DIRECTORY}/year${YEAR}/day${DAY}"

TEST_CODE=$(cat <<EOF
import typing

import pytest

from aoc.year${YEAR}.day${DAY}.main import SAMPLE_INPUT, part_one, part_two

T = typing.TypeVar("T")


@pytest.mark.parametrize(
    ("expected", "func"),
    [
        (None, part_one),
        (None, part_two),
    ],
    ids=("one", "two"),
)
class TestYear${YEAR}:
    def test_day(self, expected: T, func: typing.Callable[[str], T]) -> None:
        assert expected == func(SAMPLE_INPUT)
EOF
)

RUN_CODE=$(cat <<EOF
from rich import print  # pylint: disable=redefined-builtin

import aoclib

SAMPLE_INPUT: str = """

"""

def part_one(inputs: str) -> int:

    return

def part_two(inputs: str) -> int:

    return
EOF
)

ERRATA=""
