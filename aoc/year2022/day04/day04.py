SAMPLE_INPUT: str = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""


def srange(rng: str) -> set[int]:
    return set(range(int((split := rng.split("-"))[0]), int(split[1]) + 1))


def part_one(inputs: str) -> int:
    def fits(first: set[int], second: set[int]) -> bool:
        return first <= second if len(first) < len(second) else second <= first

    return sum(fits(*map(srange, line.split(","))) for line in inputs.splitlines())


def part_two(inputs: str) -> int:
    def fits(first: set[int], second: set[int]) -> bool:
        return len(first.intersection(second)) > 0

    return sum(fits(*map(srange, line.split(","))) for line in inputs.splitlines())
