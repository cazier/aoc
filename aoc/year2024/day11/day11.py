import collections

SAMPLE_INPUT: str = "125 17"


def blink(stones: dict[int, int], limit: int) -> int:
    for _ in range(limit):
        next: dict[int, int] = collections.defaultdict(int)

        for stone, count in stones.items():
            if stone == 0:
                next[1] += count

            elif len((string := str(stone))) % 2 == 0:
                first, second = int(string[: len(string) // 2]), int(string[len(string) // 2 :])
                next[first] += count
                next[second] += count
                continue

            else:
                next[stone * 2024] += count

        stones = next

    return sum(stones.values())


def part_one(inputs: str) -> int:
    stones = {int(key): 1 for key in inputs.split()}
    return blink(stones, 25)


def part_two(inputs: str) -> int:
    stones = {int(key): 1 for key in inputs.split()}
    return blink(stones, 75)
