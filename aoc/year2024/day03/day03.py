import re
import operator

SAMPLE_INPUT_ONE: str = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
SAMPLE_INPUT_TWO: str = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")


def part_one(inputs: str) -> int:
    return sum(operator.mul(*map(int, match.groups())) for match in pattern.finditer(inputs))


def part_two(inputs: str) -> int:
    enabled = True
    total = 0

    for _match in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)|(do)\(\)|(don\'t)\(\)", inputs):
        match _match.groups():
            case (*_, "do", _):
                enabled = True
            case (*_, "don't"):
                enabled = False
            case (x, y, *_):
                if enabled:
                    total += int(x) * int(y)
            case _:
                continue

    return total
