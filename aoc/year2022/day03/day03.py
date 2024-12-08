import string

SAMPLE_INPUT: str = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

SCORE = {k: v for v, k in enumerate(string.ascii_letters, 1)}


def split(line: str) -> tuple[set[str], set[str]]:
    return set(line[: len(line) // 2]), set(line[len(line) // 2 :])


def part_one(inputs: str) -> int:
    contents = [set.intersection(*split(line)) for line in inputs.splitlines()]
    return sum(SCORE[list(i)[0]] for i in contents)


def part_two(inputs: str) -> int:
    contents = [set.intersection(*[set(line) for line in lines]) for lines in zip(*[iter(inputs.splitlines())] * 3)]
    return sum(SCORE[list(i)[0]] for i in contents)
