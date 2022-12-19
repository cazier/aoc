from ward import test

from .algorithms import bfs

# TODO: this probably needs more testing


@test("algorithms: bfs: dict")  # type: ignore
def _() -> None:
    graph = {0: [1, 2], 1: [2, 3], 2: [3], 3: [6], 4: [5, 6, 7]}

    assert bfs(0, lambda k: k == 6, lambda k: graph.get(k, []), lambda _, __: True) == [0, 1, 3, 6]
    assert bfs(0, lambda k: k == 7, lambda k: graph.get(k, []), lambda _, __: True) == []
