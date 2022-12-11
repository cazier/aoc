"""
A simple module to implement a fairly basic Grid type.
"""

import enum
import typing as t

T = t.TypeVar("T")


class Coord:
    """A Coordinate type that is used in a Grid to identify the specific location on the grid."""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"<Coord({self.x}, {self.y})>"

    @property
    def G(self) -> tuple[int, int]:
        """Returns a tuple with the (x, y) coordinates.

        Returns:
            tuple[int, int]: Coordinate location in (x, y) format
        """
        return (self.x, self.y)

    def __add__(self, other: t.Any) -> "Coord":
        if not isinstance(other, Coord):
            other = Coord(*other)

        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other: t.Any) -> "Coord":
        if not isinstance(other, Coord):
            other = Coord(*other)

        return Coord(self.x - other.x, self.y - other.y)

    def __mul__(self, other: t.Any) -> "Coord":
        return Coord(self.x * other, self.y * other)

    def __truediv__(self, other: t.Any) -> "Coord":
        raise NotImplementedError()

    def __floordiv__(self, other: t.Any) -> "Coord":
        raise NotImplementedError()

    def __iadd__(self, other: t.Any) -> "Coord":
        if not isinstance(other, Coord):
            other = Coord(*other)

        self.x += other.x
        self.y += other.y

        return self

    def __abs__(self) -> "Coord":
        return Coord(abs(self.x), abs(self.y))

    def __hash__(self) -> int:
        return hash(self.G)

    def __eq__(self, other: t.Any) -> bool:
        if isinstance(other, tuple) and len(other) == 2:
            other = Coord(*other)

        if isinstance(other, Coord):
            return self.G == other.G

        raise NotImplementedError()

    def normalize(self) -> "Coord":
        return Coord(*map(lambda k: k // abs(k) if k else 0, self.G))

    def touching(self, other: t.Any) -> bool:
        if not isinstance(other, Coord):
            other = Coord(*other)

        if (diff := abs(self - other).G) == (0, 0):
            return True

        if max(diff) == 1:
            return True

        return False


class Direction(enum.Enum):
    """An enumerator for each direction that can be moved along a grid.

    # TODO: Add support for diagonals
    """

    LEFT = (Coord(-1, 0),)
    RIGHT = (Coord(1, 0),)
    UP = (Coord(0, -1),)
    DOWN = (Coord(0, 1),)

    ROW = (LEFT[0], RIGHT[0])
    COLUMN = (UP[0], DOWN[0])

    ALL = (UP[0], LEFT[0], RIGHT[0], DOWN[0])

    @classmethod
    def types(cls) -> t.Iterator["Direction"]:
        yield from (name for name in cls if name not in (cls.ALL, cls.COLUMN, cls.ROW))


class Grid(t.Generic[T]):
    """A generic Grid type to store arbitrary values at specific coordinate locations."""

    @staticmethod
    def create(string: str, predicate: t.Optional[t.Callable[[str], T]] = None, split: str = "") -> "Grid[T]":
        """Create a grid from a string input

        Args:
            string (str): input string with grid values
            predicate (t.Optional[t.Callable[[str], T]], optional): If set, the predicate will be run for each value
                added to the grid. Defaults to None.
            split (str, optional): An optional value used to split each line of the input string. Defaults to "".

        Returns:
            Grid[T]: the created Grid type
        """
        return Grid(
            {
                Coord(x, y): predicate(col) if predicate else t.cast(T, col)
                for y, row in enumerate(string.splitlines())
                for x, col in enumerate(row.split(split) if split else row)
            }
        )

    def __init__(self, grid: dict[Coord, T]) -> None:
        self._grid = grid

    def __contains__(self, key: t.Any) -> bool:
        return key in self._grid

    def iter_coord(self) -> t.Iterator[Coord]:
        """An iterator for all of the coordinates in the grid. This will return each of the coordinates
        in the order they were initally added to the grid.

        Yields:
            t.Iterator[Coord]: grid coordinates
        """
        yield from self._grid.keys()

    def iter_values(self) -> t.Iterator[T]:
        """An iterator for all of the values stored in the grid. This will return each of the values
        in the order they were initally added to the grid.

        Yields:
            t.Iterator[T]: grid values
        """
        yield from self._grid.values()

    def items(self) -> t.Iterator[tuple[Coord, T]]:
        """An iterator for all of the (coordinate, value) pairs stored in the grid. This will return each item
        in the order they were initally added to the grid.

        Yields:
            t.Iterator[tuple[Coord, T]]: (coordinate, value) pairs
        """
        yield from self._grid.items()

    def is_on_edge(self, center: Coord | tuple[int, int]) -> bool:
        """Returns whether the specified coordinate is located on the edge of the grid, as opposed to
        being internal

        Args:
            center (Coord | tuple[int, int]): the coordinate location being checked

        Returns:
            bool: True, if the coordinate is on the edge
        """
        return any(not list(self._iter(center, False, direction)) for direction in Direction.ALL.value)

    def get(self, center: Coord | tuple[int, int]) -> T:
        """Get the value stored at a specific coordinate location on the grid

        Args:
            center (Coord | tuple[int, int]): the coordinate location

        Returns:
            T: the value at that coordinate location
        """
        if not isinstance(center, Coord):
            center = Coord(*center)

        return self._grid[center]

    def set(self, center: Coord | tuple[int, int], value: T) -> None:
        """Set a new value at the specific coordinate location on the grid

        Args:
            center (Coord | tuple[int, int]): the coordinate location
            value (T): the value to set in the grid
        """
        if not isinstance(center, Coord):
            center = Coord(*center)

        self._grid[center] = value

    def _iter(self, center: Coord | tuple[int, int], include_self: bool, shift: Coord) -> t.Iterator[Coord]:
        if not isinstance(center, Coord):
            center = Coord(*center)

        if not include_self:
            center = center + shift

        while True:
            if center in self:
                yield center
                center = center + shift
                continue

            break

    def coordinates(
        self, center: Coord | tuple[int, int], direction: Direction, include_self: bool = False
    ) -> t.Iterator[Coord]:
        """Generates an iterator of coordinates along a particular direction

        Args:
            center (Coord | tuple[int, int]): the center point to radiate from
            direction (Direction): direction to step over
            include_self (bool, optional): If true, include the center in the result. Defaults to False.

        Yields:
            t.Iterator[Coord]: the coordinate value along each direction
        """
        shown = set()

        for shift in direction.value:
            for coord in self._iter(center=center, include_self=include_self, shift=shift):
                if coord not in shown:
                    shown.add(coord)
                    yield coord

    def values(
        self, center: Coord | tuple[int, int], direction: Direction, include_self: bool = False
    ) -> t.Iterator[T]:
        """Generates an iterator of values along a particular direction

        Args:
            center (Coord | tuple[int, int]): the center point to radiate from
            direction (Direction): direction to step over
            include_self (bool, optional): If true, include the center in the result. Defaults to False.

        Yields:
            t.Iterator[T]: the value along each direction
        """
        yield from map(self.get, self.coordinates(center=center, direction=direction, include_self=include_self))
