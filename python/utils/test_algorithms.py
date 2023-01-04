import random

from ward import test

from .algorithms import bfs, bubble

# TODO: this probably needs more testing


@test("algorithms: bfs: dict")  # type: ignore
def _() -> None:
    graph = {0: [1, 2], 1: [2, 3], 2: [3], 3: [6], 4: [5, 6, 7]}

    assert bfs(0, lambda k: k == 6, lambda k: graph.get(k, []), lambda _, __: True) == [0, 1, 3, 6]
    assert bfs(0, lambda k: k == 7, lambda k: graph.get(k, []), lambda _, __: True) == []


@test("algorithms: bubble sort")  # type: ignore
def _() -> None:
    def cmp(lhs: int, rhs: int) -> int:
        if rhs < lhs:
            return -1

        if lhs == rhs:
            return 0

        return 1

    numbers = list(range(10))
    random.shuffle(numbers)

    assert bubble(numbers) == sorted(numbers)

    assert bubble(numbers, cmp) == sorted(numbers, reverse=True)
