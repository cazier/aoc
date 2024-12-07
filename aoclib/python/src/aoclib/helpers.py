import typing
import pathlib


def load_input() -> str:
    return pathlib.Path("input").read_text(encoding="utf8")


_Z = typing.TypeVar("_Z")


def zip_longest_repeating(*iterables: typing.Iterable[_Z]) -> typing.Iterator[list[_Z]]:
    """Similar to functools.zip_longest, but simply repeat the final value instead of using `None` or passing in a
    static value.

    If a zero-length iterable is supplied, it will return `None` for each value.

    Args:
        *iterables (typing.Iterable[Z]): Any number of input sequences to zip through

    Yields:
        typing.Iterator[list[Z]]: list of each item from the same position in the iterables, until they've run out
    """
    storage: dict[int, _Z] = {}
    iterators = [iter(i) for i in iterables]

    num_active = len(iterators)

    while True:
        done = 0
        out = []

        for index, iterator in enumerate(iterators):
            try:
                storage[index] = next(iterator)

            except StopIteration:
                done += 1

            try:
                out.append(storage[index])

            except KeyError:
                pass

        if done == num_active:
            return

        yield out


def splitlines(text: str) -> typing.Iterator[str]:
    yield from (line for line in text.splitlines() if line)
