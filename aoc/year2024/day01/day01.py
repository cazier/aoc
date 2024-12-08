SAMPLE_INPUT: str = """
3   4
4   3
2   5
1   3
3   9
3   3
"""


def parse(inputs: str) -> list[tuple[int, ...]]:
    return [tuple(map(int, line.split())) for line in inputs.splitlines() if line]


def part_one(inputs: str) -> int:
    pairs = parse(inputs)
    left_column, right_column = list(zip(*pairs))

    return sum(abs(left - right) for left, right in zip(sorted(left_column), sorted(right_column)))


def part_two(inputs: str) -> int:
    pairs = parse(inputs)
    left_column, right_column = list(zip(*pairs))

    return sum(left * right_column.count(left) for left in left_column)
