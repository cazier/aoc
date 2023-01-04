import typing as t
import functools
from ast import literal_eval

from rich import print  # pylint: disable=redefined-builtin

import utils
from utils.algorithms import bubble  # pylint: disable=unused-import

SAMPLE_INPUT: str = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""


def compare(lhs: t.Any, rhs: t.Any) -> int:
    def _compare(lhs: int, rhs: int) -> int:
        if lhs < rhs:
            return -1

        if lhs == rhs:
            return 0

        return 1

    if isinstance(lhs, int) and isinstance(rhs, int):
        return _compare(int(lhs), int(rhs))

    if isinstance(lhs, list) and isinstance(rhs, list):
        for _lhs, _rhs in zip(lhs, rhs):
            if (res := compare(_lhs, _rhs)) != 0:
                return res

        return _compare(len(lhs), len(rhs))

    if isinstance(lhs, list):
        return compare(lhs, [rhs])

    return compare([lhs], rhs)


def part_one(inputs: str) -> int:
    total = 0

    for index, (lhs, rhs) in enumerate(map(str.splitlines, inputs.split("\n\n")), start=1):
        if compare(literal_eval(lhs), literal_eval(rhs)) < 1:
            total += index

    return total


def part_two(inputs: str) -> int:
    first = "[[2]]"
    second = "[[6]]"

    packets = [k for k in inputs.splitlines() + [first, second] if k != ""]
    cmp = lambda k, l: compare(literal_eval(k), literal_eval(l))  # pylint: disable=unnecessary-lambda-assignment

    # result = bubble(packets, cmp)
    result = sorted(packets, key=functools.cmp_to_key(cmp))

    return (1 + result.index(first)) * (1 + result.index(second))


if __name__ == "__main__":  # pragma: no cover
    input_string = utils.load_input("2022", "13")

    print(part_one(input_string))
    print(part_two(input_string))
