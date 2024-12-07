import typing
from collections import deque

_T = typing.TypeVar("_T")


def bfs(
    start: _T,
    end_when: typing.Callable[[_T], bool],
    generate: typing.Callable[[_T], typing.Iterable[_T]],
    predicate: typing.Callable[[_T, _T], bool],
) -> list[_T]:
    """Implementation of a Breadth-First Search algorithm, to find the shortest path between two nodes.

    .. caution:: This method is extremely bare-bones, and depends a **lot** on well written callables!


    Args:
        start (T): the node to start the search
        end_when (typing.Callable[[T], bool]): when passed a node value, returns a boolean whether the search is complete
        generate (typing.Callable[[T], typing.Iterable[T]]): when passed a node value, return an iterable of the next values to
           add to the search
        predicate (typing.Callable[[T, T], bool]): when passed a current and a next node value, returns a boolean whether the
           next value is valid

    Returns:
        list[T]: a list of each of the visited nodes leading to the end result found via ``end_when``
    """
    pending: deque[list[_T]] = deque([[start]])
    visited: set[_T] = set()

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


class _Comparable(typing.Protocol):
    def __le__(self: "_B", other: "_B") -> bool: ...  # pragma: nocover

    def __lt__(self: "_B", other: "_B") -> bool: ...  # pragma: nocover


_B = typing.TypeVar("_B", bound=_Comparable)


def _cmp(lhs: _B, rhs: _B) -> int:
    if lhs < rhs:
        return -1

    if lhs == rhs:
        return 0

    return 1


def bubble(items: typing.Iterable[_B], cmp: typing.Callable[[_B, _B], int] = _cmp) -> list[_B]:
    """An implementation of a (rather slow probably) bubble sort with support for arbitray generic iterable types.

    .. note:: A better option than this is probably to use `functools.cmp_to_key` as the key value for the builtin
       `sort` function, but this is kept for... Posterity? It's very slow. Use `functools.cmp_to_key`

    Args:
        items (typing.Iterable[B]): an iterable of items to be sorted
        cmp (typing.Callable[[B, B], int], optional): A callable used to compare two items in the list. The callable that
            takes two arguments, and returns -1 if the first argument is smaller, 0 if the they are equal, and 1 if the
            second argument is smaller. Defaults to a simple comparison.

    Returns:
        list[B]: the sorted values in a list
    """
    result = list(items)[:]

    for stop in range(len(items)):  # type: ignore[arg-type]
        for index in range(0, len(items) - (1 + stop)):  # type: ignore[arg-type]
            lhs, rhs = result[index], result[index + 1]

            if cmp(lhs, rhs) > 0:
                result[index] = rhs
                result[index + 1] = lhs

    return result
