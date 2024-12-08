SAMPLE_INPUT: str = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""


def part_one(inputs: str) -> int:
    elves = [calories.splitlines() for calories in inputs.strip().split("\n\n")]

    return max(map(lambda k: sum(map(int, k)), elves))


def part_two(inputs: str) -> int:
    elves = [calories.splitlines() for calories in inputs.strip().split("\n\n")]

    return sum(sorted(list(map(lambda k: sum(map(int, k)), elves)), reverse=True)[:3])
