import os
import typing as t
import pathlib


def load_input(year: str, day: str) -> str:
    root = os.getenv("AOC_ROOT_DIRECTORY", "")

    if root == "":
        raise SystemExit("Could not determine the proper $AOC_ROOT_DIRECTORY environment variable.")

    year_string = f"2{int(year) % 2000:03}"
    day_string = f"{int(day):02}.txt"

    path = pathlib.Path(root, "inputs", year_string, day_string)

    return path.read_text(encoding="utf8")


Z = t.TypeVar("Z")


def zip_longest_repeating(*iterables: t.Iterable[Z]) -> t.Iterator[list[Z]]:
    """Similar to functools.zip_longest, but simply repeat the final value instead of using `None` or passing in a
    static value.

    If a zero-length iterable is supplied, it will return `None` for each value.

    Args:
        *iterables (t.Iterable[Z]): Any number of input sequences to zip through

    Yields:
        t.Iterator[list[Z]]: list of each item from the same position in the iterables, until they've run out
    """
    storage: dict[int, Z] = {}
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
