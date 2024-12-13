import typing
import itertools
import dataclasses
from collections import deque, defaultdict

SAMPLE_INPUT: str = "2333133121414131402"


def _iter_chars() -> typing.Generator[int, None, None]:
    start = 0
    while True:
        yield start
        start += 1


@dataclasses.dataclass
class Disk:
    _disk: str
    map: list[int | None] = dataclasses.field(init=False, default_factory=list)
    ids: dict[bool, deque[int]] = dataclasses.field(default_factory=lambda: defaultdict(deque))
    spans: dict[int | None, list[tuple[int, int]]] = dataclasses.field(default_factory=lambda: defaultdict(list))

    def __post_init__(self) -> None:
        disk = list(map(int, str(self._disk).strip()))
        chars = _iter_chars()

        start = 0

        for value, free in zip(disk, itertools.cycle([False, True])):
            if free:
                self.map.extend([None] * value)
            else:
                char = next(chars)
                self.map.extend([char] * value)

            stop = start + value
            self.spans[None if free else char].append((start, stop))
            start = stop

        self.spans[None].pop()

        for index, key in enumerate(self.map):
            self.ids[key is not None].append(index)

    def __str__(self) -> str:
        return "".join([str(value) if value is not None else "." for value in self.map])

    def compact(self) -> None:
        while self.ids[False][0] < self.ids[True][-1]:
            empty = self.ids[False].popleft()
            filled = self.ids[True].pop()

            self.map[empty] = self.map[filled]
            self.map[filled] = None

    def compact_fit(self) -> None:
        for key in reversed(sorted(key for key in self.spans if key is not None)):
            [(start, stop)] = self.spans[key]
            length = stop - start

            for span_index, (span_start, span_stop) in enumerate(self.spans[None]):
                span_length = span_stop - span_start

                if span_start <= start and span_length >= length:
                    for pop_index, insert_index in zip(range(start, stop), range(span_start, span_stop)):
                        self.map[insert_index] = self.map[pop_index]
                        self.map[pop_index] = None

                    if span_length > length:
                        self.spans[None][span_index] = (span_start + length, span_stop)

                    else:
                        self.spans[None].pop(span_index)

                    break

    def checksum(self) -> int:
        return sum(value * index for index, value in enumerate(self.map) if value)


def part_one(inputs: str) -> int:
    disk = Disk(inputs)
    disk.compact()
    return disk.checksum()


def part_two(inputs: str) -> int:
    disk = Disk(inputs)
    disk.compact_fit()
    return disk.checksum()
