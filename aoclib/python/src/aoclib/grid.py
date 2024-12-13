"""
A simple module to implement a fairly basic Grid type.
"""

from __future__ import annotations

import sys
import enum
import typing
import operator
import itertools
import dataclasses

notset = object()


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

    def __add__(self, other: typing.Any) -> typing.Self:
        if not isinstance(other, Coord):
            other = Coord(*other)

        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other: typing.Any) -> typing.Self:
        if not isinstance(other, Coord):
            other = Coord(*other)

        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, other: typing.Any) -> typing.Self:
        return type(self)(self.x * other, self.y * other)

    def __truediv__(self, other: typing.Any) -> typing.Self:
        raise NotImplementedError()

    def __floordiv__(self, other: typing.Any) -> typing.Self:
        raise NotImplementedError()

    def __iadd__(self, other: typing.Any) -> typing.Self:
        if not isinstance(other, Coord):
            other = Coord(*other)

        self.x += other.x
        self.y += other.y

        return self

    def __abs__(self) -> typing.Self:
        return type(self)(abs(self.x), abs(self.y))

    def __hash__(self) -> int:
        return hash(self.G)

    def __eq__(self, other: typing.Any) -> bool:
        if isinstance(other, tuple) and len(other) == 2:
            other = Coord(*other)

        if isinstance(other, Coord):
            return self.G == other.G

        raise NotImplementedError()

    def __lt__(self, other: typing.Any) -> bool:
        if isinstance(other, tuple) and len(other) == 2:
            other = Coord(*other)

        if isinstance(other, Coord):
            return self.x < other.x and self.y < other.y

        raise NotImplementedError()

    def __le__(self, other: typing.Any) -> bool:
        if isinstance(other, tuple) and len(other) == 2:
            other = Coord(*other)

        if isinstance(other, Coord):
            return self.x <= other.x and self.y <= other.y

        raise NotImplementedError()

    def normalize(self) -> typing.Self:
        return type(self)(*map(lambda k: k // abs(k) if k else 0, self.G))

    def touching(self, other: typing.Any) -> bool:
        if not isinstance(other, Coord):
            other = Coord(*other)

        if (diff := abs(self - other).G) == (0, 0):
            return True

        if max(diff) == 1:
            return True

        return False

    def opposites(self, other: typing.Any) -> set[typing.Self]:
        if not isinstance(other, Coord):
            other = Coord(*other)

        dx = other.x - self.x
        dy = other.y - self.y

        return {type(self)(self.x - dx, self.y - dy), type(self)(other.x + dx, other.y + dy)}

    def inline(self, other: typing.Any, bounds: tuple[typing.Any, typing.Any]) -> typing.Iterator[Coord]:
        if not isinstance(other, Coord):
            other = Coord(*other)

        lower, upper = bounds

        if not isinstance(upper, Coord):
            upper = Coord(*upper)

        if not isinstance(lower, Coord):
            lower = Coord(*lower)

        dx = other.x - self.x
        dy = other.y - self.y

        for start, operation in ((self, operator.add), (other, operator.sub)):
            while True:
                start = Coord(operation(start.x, dx), operation(start.y, dy))

                if not (lower <= start <= upper):
                    break

                if start != self and start != other:
                    yield start


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
    DIAGONAL = (NE[0], SE[0], SW[0], NW[0])
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
    def orthogonals(cls) -> "typing.Iterator[Direction]":
        yield from (cls.N, cls.E, cls.S, cls.W)

    @classmethod
    def diagonals(cls) -> "typing.Iterator[Direction]":
        yield from (cls.NE, cls.SE, cls.SW, cls.NW)

    @classmethod
    def all(cls) -> "typing.Iterator[Direction]":
        yield from (cls.N, cls.NE, cls.E, cls.SE, cls.S, cls.SW, cls.W, cls.NW)

    @classmethod
    def rotate(
        cls, facing: "Coord | Direction", *, clockwise: bool = True, orthogonal: bool = False, diagonal: bool = False
    ) -> typing.Iterator[Direction]:
        if orthogonal and diagonal:
            array = list(cls.all())

        elif orthogonal and not diagonal:
            array = list(cls.orthogonals())

        elif not orthogonal and diagonal:
            array = list(cls.diagonals())

        else:
            raise ValueError("At least one of the orthogonal or diagonal arguments must be True")

        if not isinstance(facing, Direction):
            facing = Direction((facing,))

        if not clockwise:
            array.reverse()

        try:
            start = array.index(facing)

        except ValueError:
            raise ValueError("The starting directiton is not in the desired array.")

        return itertools.islice(itertools.cycle(array), start, start + len(array))


class Grid[T]:
    """A generic Grid type to store arbitrary values at specific coordinate locations."""

    background = "."

    @typing.overload
    @classmethod
    def create(
        cls, string: str, *, filter: typing.Callable[[str], bool] = lambda k: True, split: str = ""
    ) -> Grid[str]: ...

    @typing.overload
    @classmethod
    def create(
        cls,
        string: str,
        *,
        predicate: typing.Callable[[str], T],
        filter: typing.Callable[[T], bool] = lambda k: True,
        split: str = "",
    ) -> Grid[T]: ...

    @classmethod
    def create(
        cls,
        string: str,
        *,
        predicate: typing.Optional[typing.Callable[[str], T]] = None,
        filter: typing.Callable[..., bool] = lambda k: True,
        split: str = "",
    ) -> Grid[str] | Grid[T]:
        """Create a grid from a string input

        Args:
            string (str): input string with grid values
            predicate (typing.Optional[typing.Callable[[str], T]], optional): If set, the predicate will be run for each value
                added to the grid. Defaults to None.
            filter (typing.Optional[typing.Callable[..., bool]], optional): If set, filter the values added to the grid. Defaults to None.
            split (str, optional): An optional value used to split each line of the input string. Defaults to "".

        Returns:
            Grid[T]: the created Grid type
        """
        grid = cls(
            {
                Coord(x, y): predicate(col) if predicate else typing.cast(T, col)
                for y, row in enumerate(line for line in string.splitlines() if line)
                for x, col in enumerate(row.split(split) if split else row)
            }
        )
        grid._grid = {key: value for key, value in grid._grid.items() if filter(value)}
        return grid

    @staticmethod
    def new(width: int, height: int) -> Grid[str]:
        """Create an empty grid with a specific height and width.

        Args:
            width (int): number of columns
            height (int): number of rows

        Returns:
            Grid[T]: the created Grid type
        """
        return Grid({Coord(x, y): Grid.background for y in range(height) for x in range(width)})

    def __init__(self, grid: dict[tuple[int, int] | Coord, T]) -> None:
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

    def __contains__(self, key: typing.Any) -> bool:
        return key in self._grid

    @property
    def min_bound(self) -> Coord:
        """A coordinate point representing the minimum "X" and "Y" value in the grid.

        .. note:: This point may not actually have any values in the grid, and just represents the "bottom-left" point,
           were the whole grid to be printed outyping.

        Returns:
            Coord: (Minimum X, Minimum Y) coordinate location
        """
        return self._min_bound

    @property
    def max_bound(self) -> Coord:
        """A coordinate point representing the maximum "X" and "Y" value in the grid.

        .. note:: This point may not actually have any values in the grid, and just represents the "top-right" point,
           were the whole grid to be printed outyping.

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

    def iter_coord(self) -> typing.Iterator[Coord]:
        """An iterator for all of the coordinates in the grid. This will return each of the coordinates
        in the order they were initally added to the grid.

        Yields:
            typing.Iterator[Coord]: grid coordinates
        """
        yield from self._grid.keys()

    def iter_values(self) -> typing.Iterator[T]:
        """An iterator for all of the values stored in the grid. This will return each of the values
        in the order they were initally added to the grid.

        Yields:
            typing.Iterator[T]: grid values
        """
        yield from self._grid.values()

    def items(self) -> typing.Iterator[tuple[Coord, T]]:
        """An iterator for all of the (coordinate, value) pairs stored in the grid. This will return each item
        in the order they were initally added to the grid.

        Yields:
            typing.Iterator[tuple[Coord, T]]: (coordinate, value) pairs
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

    def get(self, center: Coord | tuple[int, int], *, default: typing.Any = notset) -> T:
        """Get the value stored at a specific coordinate location on the grid

        Args:
            center (Coord | tuple[int, int]): the coordinate location
            default (typing.Any, optional): Default value if key does not exist in the grid. Defaults to raise exception.

        Raises:
            KeyError: Exception if the key is not in the grid

        Returns:
            T: the value at that coordinate location
        """
        if not isinstance(center, Coord):
            center = Coord(*center)

        if center not in self._grid:
            if default is notset:
                raise KeyError(f"The coordinate {center} does not exist")

            return default

        return self._grid[center]

    def set(self, center: Coord | tuple[int, int], value: T, anywhere: bool = False) -> None:
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

    def pop(self, center: Coord | tuple[int, int], default: typing.Optional[T] = None) -> T:
        """If ``center`` is in the grid, remove it and return its value. Otherwise, return ``default``. If ``default``
        is not set, raise a KeyError.

        Args:
            center (Coord | tuple[int, int]): A coordinate location to pop from the grid
            default (typing.Optional[T], optional): A default value to return if center is not in the dictyping. Defaults to None.

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

    def _iter(self, center: Coord | tuple[int, int], include_self: bool, shift: Coord) -> typing.Iterator[Coord]:
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
    ) -> typing.Iterator[Coord]:
        """Generates an iterator of coordinates along a particular direction

        Args:
            center (Coord | tuple[int, int]): the center point to radiate from
            direction (Direction): direction to step over
            include_self (bool, optional): If true, include the center in the resultyping. Defaults to False.

        Yields:
            typing.Iterator[Coord]: the coordinate value along each direction
        """
        shown = set()

        for shift in direction.value:
            for coord in self._iter(center=center, include_self=include_self, shift=shift):
                if coord not in shown:
                    shown.add(coord)
                    yield coord

    def values(
        self, center: Coord | tuple[int, int], direction: Direction, include_self: bool = False
    ) -> typing.Iterator[T]:
        """Generates an iterator of values along a particular direction

        Args:
            center (Coord | tuple[int, int]): the center point to radiate from
            direction (Direction): direction to step over
            include_self (bool, optional): If true, include the center in the resultyping. Defaults to False.

        Yields:
            typing.Iterator[T]: the value along each direction
        """
        yield from map(self.get, self.coordinates(center=center, direction=direction, include_self=include_self))

    def orthogonal(self, center: Coord | tuple[int, int], include_missing: bool = False) -> typing.Iterator[Coord]:
        """An iterator with each of the orthogonal neighbors to the supplied center coordinate. (Orthognal meaning
        only the coordinates directly North, East, South or East)

        .. note:: The iterator will always return values starting from the North direction, and proceeding clockwise.

        Args:
            center (Coord | tuple[int, int]): the center point

        Yields:
            typing.Iterator[Coord]: each adjacent orthogonal neighbor coordinate
        """
        self.get(center)
        for shift in Direction.ORTHOGONAL.value:
            try:
                yield next(self._iter(center, False, shift))

            except StopIteration:
                if include_missing:
                    yield shift + center

    def diagonal(self, center: Coord | tuple[int, int], include_missing: bool = False) -> typing.Iterator[Coord]:
        """An iterator with each of the diagonal neighbors to the supplied center coordinate. (Diagonal meaning
        only the coordinates directly Northeast, Southeast, Southwest or Northeast)

        .. note:: The iterator will always return values starting from the Northeast direction, and proceeding clockwise.

        Args:
            center (Coord | tuple[int, int]): the center point

        Yields:
            typing.Iterator[Coord]: each adjacent diagonal neighbor coordinate
        """
        self.get(center)
        for shift in Direction.DIAGONAL.value:
            try:
                yield next(self._iter(center, False, shift))

            except StopIteration:
                if include_missing:
                    yield shift + center

    def neighbors(self, center: Coord | tuple[int, int]) -> typing.Iterator[Coord]:
        """An iterator with each of the neighbors to the supplied center coordinate, including diagonally adjacent
        coordinates.

        .. note:: The iterator will always return values starting from the North direction, and proceeding clockwise.

        Args:
            center (Coord | tuple[int, int]): the center point

        Yields:
            typing.Iterator[Coord]: each adjacent neighbor coordinate
        """
        self.get(center)
        for shift in Direction.ALL.value:
            try:
                yield next(self._iter(center, False, shift))

            except StopIteration:
                continue

    def _n_shift(self, center: Coord | tuple[int, int], amount: Coord, n: int) -> typing.Iterator[list[Coord]]:
        result = []
        for _ in range(n):
            try:
                center = next(self._iter(center, False, amount))
                result.append(center)

            except StopIteration:
                break

        yield result

    def n_orthogonal(self, center: Coord | tuple[int, int], n: int) -> typing.Iterator[list[Coord]]:
        """An iterator with each of the orthogonal neighbors to the supplied center coordinate. (Orthognal meaning
        only the coordinates directly North, East, South or East)

        .. note:: The iterator will always return values starting from the North direction, and proceeding clockwise.

        Args:
            center (Coord | tuple[int, int]): the center point

        Yields:
            typing.Iterator[Coord]: each adjacent orthogonal neighbor coordinate
        """
        self.get(center)
        for shift in Direction.ORTHOGONAL.value:
            yield from self._n_shift(center, shift, n)

    def n_diagonal(self, center: Coord | tuple[int, int], n: int) -> typing.Iterator[list[Coord]]:
        """An iterator with each of the diagonal neighbors to the supplied center coordinate. (Diagonal meaning
        only the coordinates directly Northeast, Southeast, Southwest or Northeast)

        .. note:: The iterator will always return values starting from the Northeast direction, and proceeding clockwise.

        Args:
            center (Coord | tuple[int, int]): the center point

        Yields:
            typing.Iterator[Coord]: each adjacent diagonal neighbor coordinate
        """
        self.get(center)
        for shift in Direction.DIAGONAL.value:
            yield from self._n_shift(center, shift, n)

    def n_neighbors(self, center: Coord | tuple[int, int], n: int) -> typing.Iterator[list[Coord]]:
        """An iterator with each of the neighbors to the supplied center coordinate, including diagonally adjacent
        coordinates.

        .. note:: The iterator will always return values starting from the North direction, and proceeding clockwise.

        Args:
            center (Coord | tuple[int, int]): the center point

        Yields:
            typing.Iterator[Coord]: each adjacent neighbor coordinate
        """
        self.get(center)
        for shift in Direction.ALL.value:
            yield from self._n_shift(center, shift, n)

    def find(self, search: T, allow_multiple: bool = False) -> list[Coord]:
        """Return a list of :py:class:`Coord` that have a particular value. If the value does not exist in the grid,
        return an empty listyping.

        Args:
            search (T): the searched value
            allow_multiple (bool, optional): If true, allow multiple results in returned listyping. Defaults to False.

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

    def region(self, center: Coord) -> typing.Set[Coord]:
        def find(coord: Coord):
            if coord in visited or self.get(coord) != value:
                return

            visited.add(coord)

            for neighbor in self.orthogonal(coord):
                find(neighbor)

        value = self.get(center)
        visited: typing.Set[Coord] = set()

        find(center)
        return visited

    @typing.overload
    def regions(self, autonumber: typing.Literal[False]) -> dict[T, typing.Set[Coord]]: ...
    @typing.overload
    def regions(self, autonumber: typing.Literal[True] = True) -> dict[int, typing.Set[Coord]]: ...

    def regions(self, autonumber: bool = True) -> dict[int, typing.Set[Coord]] | dict[T, typing.Set[Coord]]:
        resp: dict[int, typing.Set[Coord]] | dict[T, typing.Set[Coord]] = {}
        visited: typing.Set[Coord] = set()
        chars = itertools.count()

        for center, identifier in self.items():
            if center not in visited:
                region = self.region(center)

                if autonumber:
                    resp[next(chars)] = region  # type: ignore[index]

                else:
                    resp[identifier] = region  # type: ignore[index]

                visited.update(region)

        return resp


class DuplicateRegionIDError(BaseException):
    pass


@dataclasses.dataclass
class Region[T]:
    identifier: T
    region: set[Coord]
    _grid: Grid[T] = dataclasses.field(init=False)

    def __post_init__(self):
        self._grid = Grid({coord: self.identifier for coord in self.region})

    def _internal(self) -> set[Coord]:
        return {coord for coord in self._grid.iter_coord() if len(list(self._grid.orthogonal(coord))) == 4}

    @property
    def area(self) -> int:
        return len(self.region)

    def perimeter(self) -> set[tuple[Coord, Direction]]:
        resp: set[tuple[Coord, Direction]] = set()

        for coordinate in self._grid.iter_coord():
            for direction, neighbor in zip(
                Direction.orthogonals(), self._grid.orthogonal(coordinate, include_missing=True)
            ):
                if self._grid.get(neighbor, default=-1) != self.identifier:
                    resp.add((neighbor, direction))

        return resp

    def edges(self) -> int:
        breakpoint()

        return 12
