SAMPLE_INPUT: str = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


def parse(inputs: str) -> list[tuple[int, list[int]]]:
    def split(line: str) -> tuple[int, list[int]]:
        result, *operands = line.split()
        return int(result), list(map(int, operands))

    return [split(line) for line in inputs.replace(":", "").splitlines() if line]


def _eval(expected: int, a: int, *operands: int, pipe: bool = False) -> bool:
    if not operands:
        return a == expected

    b, *bs = operands

    return (
        _eval(expected, a * b, *bs, pipe=pipe)
        or _eval(expected, a + b, *bs, pipe=pipe)
        or (pipe and _eval(expected, int(f"{a}{b}"), *bs, pipe=pipe))
    )


def part_one(inputs: str) -> int:
    return sum(expected for expected, (a, *bs) in parse(inputs) if _eval(expected, a, *bs))


def part_two(inputs: str) -> int:
    return sum(expected for expected, (a, *bs) in parse(inputs) if _eval(expected, a, *bs, pipe=True))
