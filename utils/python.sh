TEST_NAME="test_main.py"
RUN_NAME="main.py"

TEST_CODE=$(cat <<EOF
from ward import test
from main import part_one, part_two, SAMPLE_INPUT

@test("${YEAR}-${DAY}: Part One")
def _() -> None:
    expected =
    output = part_one(SAMPLE_INPUT)

    assert expected == output

@test("${YEAR}-${DAY}: Part Two")
def _() -> None:
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
    input_string = utils.load_input("${YEAR}", "${DAY}")

    print(part_one(input_string))
    print(part_two(input_string))
EOF
)
