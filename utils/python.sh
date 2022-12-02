TEST_NAME="test_main.py"
RUN_NAME="main.py"

TEST_CODE=$(cat <<EOF
from ward import test
from main import part_one, part_two, SAMPLE_INPUT

@test("2022-01: Part One")
def _():
    expected =
    output = part_one(SAMPLE_INPUT)

    assert expected == output

@test("2022-01: Part Two")
def _():
    expected =
    output = part_two(SAMPLE_INPUT)

    assert expected == output
EOF
)

RUN_CODE=$(cat <<EOF
import utils

SAMPLE_INPUT: str = """

"""

def part_one(inputs: str) -> int:

    return

def part_two(inputs: str) -> int:

    return

if __name__ == "__main__":
    inputs = utils.load_input("${YEAR}", "${DAY}")

    print(part_one(inputs))
    print(part_two(inputs))
EOF
)
