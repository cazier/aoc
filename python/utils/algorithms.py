import typing as t
from collections import deque

T = t.TypeVar("T")


def bfs(
    start: T,
    end_when: t.Callable[[T], bool],
    generate: t.Callable[[T], t.Iterable[T]],
    predicate: t.Callable[[T, T], bool],
) -> list[T]:
    """Implementation of a Breadth-First Search algorithm, to find the shortest path between two nodes.

    .. caution:: This method is extremely bare-bones, and depends a **lot** on well written callables!


    Args:
        start (T): the node to start the search
        end_when (t.Callable[[T], bool]): when passed a node value, returns a boolean whether the search is complete
        generate (t.Callable[[T], t.Iterable[T]]): when passed a node value, return an iterable of the next values to
           add to the search
        predicate (t.Callable[[T, T], bool]): when passed a current and a next node value, returns a boolean whether the
           next value is valid

    Returns:
        list[T]: a list of each of the visited nodes leading to the end result found via ``end_when``
    """
    pending: deque[list[T]] = deque([[start]])
    visited: set[T] = set()

    while pending:
        path = pending.popleft()
        current = path[-1]

        if end_when(current):
            return path

        for new in generate(current):
            if new not in visited and predicate(current, new):
                pending.append(path + [new])
                visited.add(new)

    return []
