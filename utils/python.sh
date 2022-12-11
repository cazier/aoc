TEST_NAME="test_main.py"
RUN_NAME="main.py"
DIR="${_CWD}/${LANGUAGE_DIRECTORY}/year${YEAR}/day${DAY}"

TEST_CODE=$(cat <<EOF
from ward import test
from year${YEAR}.day${DAY}.main import SAMPLE_INPUT, part_one, part_two

@test("${YEAR}-${DAY}: Part One")  # type: ignore
def _() -> None:
    expected =
    output = part_one(SAMPLE_INPUT)

    assert expected == output

@test("${YEAR}-${DAY}: Part Two")  # type: ignore
def _() -> None:
    expected =
    output = part_two(SAMPLE_INPUT)

    assert expected == output
EOF
)

RUN_CODE=$(cat <<EOF
from rich import print  # pylint: disable=redefined-builtin

import utils

SAMPLE_INPUT: str = """

"""

def part_one(inputs: str) -> int:

    return

def part_two(inputs: str) -> int:

    return

if __name__ == "__main__":  # pragma: no cover
    input_string = utils.load_input("${YEAR}", "${DAY}")

    print(part_one(input_string))
    print(part_two(input_string))
EOF
)

ERRATA=""
