import typing

SAMPLE_INPUT: str = """
mjqjpqmgbljsphdztnvjfqwrcgsmlb
"""


def subset(iterable: list[str], count: int) -> typing.Iterator[set[str]]:
    for start in range(len(iterable) - count):
        yield set(iterable[start : start + count])


def part_one(inputs: str) -> int:
    characters = list(inputs.strip())
    for index, values in enumerate(subset(characters, 4)):
        if len(values) == 4:
            return index + 4

    raise SystemExit(1)


def part_two(inputs: str) -> int:
    characters = list(inputs.strip())
    for index, values in enumerate(subset(characters, 14)):
        if len(values) == 14:
            return index + 14

    raise SystemExit(1)
