"""
A simple module to implement a fairly basic Grid type.
"""

import sys
import enum
import typing as t

_T = t.TypeVar("_T")


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

    .. note:: When the enumerator returns multiple values (i.e., :py:attr:`Direction.COLUMN`), the iterated values will
       always return in a clockwise order, starting from the North direction.
    """

    N = (Coord(0, -1),)
    E = (Coord(1, 0),)
    S = (Coord(0, 1),)
    W = (Coord(-1, 0),)

    NE = (Coord(1, -1),)
    SE = (Coord(1, 1),)
    SW = (Coord(-1, 1),)
    NW = (Coord(-1, -1),)

    ROW = (W[0], E[0])
    COLUMN = (N[0], S[0])

    ORTHOGONAL = (N[0], E[0], S[0], W[0])
    ALL = (
        N[0],
        NE[0],
        E[0],
        SE[0],
        S[0],
        SW[0],
        W[0],
        NW[0],
    )

    @classmethod
    def orthogonals(cls) -> t.Iterator["Direction"]:
        yield from (cls.N, cls.E, cls.S, cls.W)

    @classmethod
    def all(cls) -> t.Iterator["Direction"]:
        yield from (cls.N, cls.NE, cls.E, cls.SE, cls.S, cls.SW, cls.W, cls.NW)


class Grid(t.Generic[_T]):
    """A generic Grid type to store arbitrary values at specific coordinate locations."""

    background = "."

    @staticmethod
    def create(string: str, predicate: t.Optional[t.Callable[[str], _T]] = None, split: str = "") -> "Grid[_T]":
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
                Coord(x, y): predicate(col) if predicate else t.cast(_T, col)
                for y, row in enumerate(string.splitlines())
                for x, col in enumerate(row.split(split) if split else row)
            }
        )

    def __init__(self, grid: dict[tuple[int, int] | Coord, _T]) -> None:
        self._grid = {k if isinstance(k, Coord) else Coord(*k): v for k, v in grid.items()}
        self._calculate_boundaries()

    def __str__(self) -> str:
        def get(center: tuple[int, int]) -> str:
            try:
                return str(self.get(center))

            except KeyError:
                return self.background

        return "\n".join(
            "".join(get((x, y)) for x in range(self.min_bound.x, self.max_bound.x + 1))
            for y in range(self.min_bound.y, self.max_bound.y + 1)
        )

    def __contains__(self, key: t.Any) -> bool:
        return key in self._grid

    @property
    def min_bound(self) -> Coord:
        """A coordinate point representing the minimum "X" and "Y" value in the grid.

        .. note:: This point may not actually have any values in the grid, and just represents the "bottom-left" point,
           were the whole grid to be printed out.

        Returns:
            Coord: (Minimum X, Minimum Y) coordinate location
        """
        return self._min_bound

    @property
    def max_bound(self) -> Coord:
        """A coordinate point representing the maximum "X" and "Y" value in the grid.

        .. note:: This point may not actually have any values in the grid, and just represents the "top-right" point,
           were the whole grid to be printed out.

        Returns:
            Coord: (Maximum X, Maximum Y) coordinate location
        """
        return self._max_bound

    def _update_minimums(self, other: Coord) -> None:
        self._min_bound.x = min(self._min_bound.x, other.x)
        self._min_bound.y = min(self._min_bound.y, other.y)
        self._max_bound.x = max(self._max_bound.x, other.x)
        self._max_bound.y = max(self._max_bound.y, other.y)

    def _calculate_boundaries(self) -> None:
        self._min_bound = Coord(sys.maxsize, sys.maxsize)
        self._max_bound = Coord(-sys.maxsize, -sys.maxsize)

        for center in self.iter_coord():
            self._update_minimums(center)

    def iter_coord(self) -> t.Iterator[Coord]:
        """An iterator for all of the coordinates in the grid. This will return each of the coordinates
        in the order they were initally added to the grid.

        Yields:
            t.Iterator[Coord]: grid coordinates
        """
        yield from self._grid.keys()

    def iter_values(self) -> t.Iterator[_T]:
        """An iterator for all of the values stored in the grid. This will return each of the values
        in the order they were initally added to the grid.

        Yields:
            t.Iterator[T]: grid values
        """
        yield from self._grid.values()

    def items(self) -> t.Iterator[tuple[Coord, _T]]:
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
        return any(not list(self._iter(center, False, direction)) for direction in Direction.ORTHOGONAL.value)

    def get(self, center: Coord | tuple[int, int]) -> _T:
        """Get the value stored at a specific coordinate location on the grid

        Args:
            center (Coord | tuple[int, int]): the coordinate location

        Returns:
            T: the value at that coordinate location
        """
        if not isinstance(center, Coord):
            center = Coord(*center)

        if center not in self._grid:
            raise KeyError(f"The coordinate {center} does not exist")

        return self._grid[center]

    def set(self, center: Coord | tuple[int, int], value: _T, anywhere: bool = False) -> None:
        """Set a new value at the specific coordinate location on the grid. If the ``anywhere`` flag is not used, the
        coordinate location cannot be a new location. (i.e., replacing an existing value.)

        Args:
            center (Coord | tuple[int, int]): the coordinate location
            value (T): the value to set in the grid
            anywhere (bool, optional): If True, the value set can be applied anywhere on the grid. Defaults to False.
        """
        if not isinstance(center, Coord):
            center = Coord(*center)

        if not anywhere and center not in self._grid:
            raise KeyError(f"The coordinate {center} does not exist. Maybe use the `anywhere=True` argument")

        self._grid[center] = value

        self._update_minimums(center)

    def pop(self, center: Coord | tuple[int, int], default: t.Optional[_T] = None) -> _T:
        """If ``center`` is in the grid, remove it and return its value. Otherwise, return ``default``. If ``default``
        is not set, raise a KeyError.

        Args:
            center (Coord | tuple[int, int]): A coordinate location to pop from the grid
            default (t.Optional[T], optional): A default value to return if center is not in the dict. Defaults to None.

        Raises:
            KeyError: When the key doesn't exist and no default is provided.

        Returns:
            T: The value at the grid location that was removed.
        """
        if not isinstance(center, Coord):
            center = Coord(*center)

        if default is None:
            return self._grid.pop(center)

        return self._grid.pop(center, default)

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
    ) -> t.Iterator[_T]:
        """Generates an iterator of values along a particular direction

        Args:
            center (Coord | tuple[int, int]): the center point to radiate from
            direction (Direction): direction to step over
            include_self (bool, optional): If true, include the center in the result. Defaults to False.

        Yields:
            t.Iterator[T]: the value along each direction
        """
        yield from map(self.get, self.coordinates(center=center, direction=direction, include_self=include_self))

    def orthogonal(self, center: Coord | tuple[int, int]) -> t.Iterator[Coord]:
        """An iterator with each of the orthogonal neighbors to the supplied center coordinate. (Orthognal meaning
        only the coordinates directly North, East, South or East)

        .. note:: The iterator will always return values starting from the North direction, and proceeding clockwise.

        Args:
            center (Coord | tuple[int, int]): the center point

        Yields:
            t.Iterator[Coord]: each adjacent orthogonal neighbor coordinate
        """
        self.get(center)
        for shift in Direction.ORTHOGONAL.value:
            try:
                yield next(self._iter(center, False, shift))

            except StopIteration:
                continue

    def neighbors(self, center: Coord | tuple[int, int]) -> t.Iterator[Coord]:
        """An iterator with each of the neighbors to the supplied center coordinate, including diagonally adjacent
        coordinates.

        .. note:: The iterator will always return values starting from the North direction, and proceeding clockwise.

        Args:
            center (Coord | tuple[int, int]): the center point

        Yields:
            t.Iterator[Coord]: each adjacent neighbor coordinate
        """
        self.get(center)
        for shift in Direction.ALL.value:
            try:
                yield next(self._iter(center, False, shift))

            except StopIteration:
                continue

    def find(self, search: _T, allow_multiple: bool = False) -> list[Coord]:
        """Return a list of :py:class:`Coord` that have a particular value. If the value does not exist in the grid,
        return an empty list.

        Args:
            search (T): the searched value
            allow_multiple (bool, optional): If true, allow multiple results in returned list. Defaults to False.

        Returns:
            list[Coord]: Coordinates locations with the desired value
        """
        results: list[Coord] = []

        for coord, value in self._grid.items():
            if value == search:
                if not allow_multiple:
                    return [coord]

                results.append(coord)

        return results

    def within(self, center: Coord | tuple[int, int]) -> bool:
        """Returns true if the supplied coordinate fits within the boundaries of the grid

        Args:
            center (Coord | tuple[int, int]): Checked coordinate

        Returns:
            bool: If coordinate is inside the minimum/maximum boundaries of the grid, return True. Else, return False.
        """
        if not isinstance(center, Coord):
            center = Coord(*center)

        return (self.min_bound.x <= center.x <= self.max_bound.x) and (self.min_bound.y <= center.y <= self.max_bound.y)
