import typing
import itertools

import pytest
from aoclib.grid import Grid, Coord, Direction


class TestCoordinate:
    def test_arithmetic(self) -> None:
        assert repr(Coord(1, 1)) == "<Coord(1, 1)>"

        assert Coord(1, 1) == Coord(1, 1)
        assert Coord(1, 1) != Coord(1, 2)
        assert Coord(12, 12) == (12, 12)

        with pytest.raises(NotImplementedError):
            assert Coord(12, 12) == "(12, 12)"

        assert Coord(1, 1) + Coord(2, 2) == Coord(3, 3)
        assert Coord(1, 1) + Coord(2, -2) == Coord(3, -1)
        assert Coord(5, 5) - Coord(2, 2) == Coord(3, 3)
        assert Coord(5, 5) - Coord(-2, -2) == Coord(7, 7)

        coord = Coord(10, 10)
        coord += Coord(15, 15)
        assert coord == Coord(25, 25)

        assert Coord(10, 10) * 5 == Coord(50, 50)

        assert Coord(1, 1) + (1, 2) == Coord(2, 3)
        assert Coord(1, 1) - (1, 2) == Coord(0, -1)
        coord += (9, 10)
        assert coord == Coord(34, 35)

        with pytest.raises(NotImplementedError):
            coord = Coord(12, 12) / 2

        with pytest.raises(NotImplementedError):
            coord = Coord(12, 12) // 2

        assert abs(Coord(-1, 1)) == Coord(1, 1)
        assert abs(Coord(-1, -1)) == Coord(1, 1)

        assert Coord(0, 0) < Coord(1, 1)
        assert Coord(0, 0) < (1, 2)
        assert not Coord(0, 0) < Coord(1, 0)

        with pytest.raises(NotImplementedError):
            Coord(12, 12) < 2

        assert Coord(0, 0) <= Coord(1, 0)
        assert Coord(0, 0) <= (1, 0)
        assert not Coord(0, 0) <= Coord(-1, 0)

        with pytest.raises(NotImplementedError):
            Coord(12, 12) <= 2

    @pytest.mark.parametrize(
        ("input", "expected"),
        [
            ((0, 0), Coord(0, 0)),
            ((-1, 10), Coord(-1, 1)),
            ((50, -100), Coord(1, -1)),
            ((10, 100), Coord(1, 1)),
        ],
    )
    def test_normalize(self, input: tuple[int, int], expected: Coord) -> None:
        assert Coord(*input).normalize() == expected

    @pytest.mark.parametrize(
        ("original", "other", "touching"),
        [
            (Coord(0, 0), (0, 0), True),
            (Coord(0, 0), (0, 0), True),
            (Coord(1, 1), (0, 0), True),
            (Coord(1, 1), (0, 2), True),
            (Coord(1, 1), (2, 0), True),
            (Coord(0, 0), (1, 1), True),
            (Coord(1, 1), (10, 1), False),
            (Coord(1, 1), (1, 5), False),
        ],
    )
    def test_touching(self, original: Coord, other: tuple[int, int], touching: bool) -> None:
        assert original.touching(other) == touching

    @pytest.mark.parametrize(
        ("x", "y", "a", "b"),
        [
            (Coord(1, 1), Coord(2, 2), Coord(0, 0), Coord(3, 3)),
            (Coord(1, 1), (2, 2), Coord(0, 0), Coord(3, 3)),
            (Coord(1, 1), Coord(2, 1), Coord(0, 1), Coord(3, 1)),
            (Coord(1, 2), Coord(1, 3), Coord(1, 1), Coord(1, 4)),
            (Coord(1, 2), Coord(2, 5), Coord(0, -1), Coord(3, 8)),
            (Coord(1, 2), Coord(2, -1), Coord(0, 5), Coord(3, -4)),
        ],
    )
    def test_opposites(self, x: Coord, y: Coord, a: Coord, b: Coord) -> None:
        assert x.opposites(y) == {a, b}

    @pytest.mark.parametrize(
        ("x", "y", "bounds", "inlines"),
        [
            (Coord(1, 1), Coord(2, 2), (Coord(0, 0), Coord(3, 3)), {Coord(0, 0), Coord(3, 3)}),
            (Coord(1, 1), (2, 2), ((0, 0), (3, 3)), {Coord(0, 0), Coord(3, 3)}),
            (Coord(0, 0), Coord(1, 2), (Coord(0, 0), Coord(9, 9)), {Coord(2, 4), Coord(3, 6), Coord(4, 8)}),
            (
                Coord(4, 0),
                Coord(5, 0),
                (Coord(0, 0), Coord(9, 9)),
                {
                    Coord(0, 0),
                    Coord(1, 0),
                    Coord(2, 0),
                    Coord(3, 0),
                    Coord(6, 0),
                    Coord(7, 0),
                    Coord(8, 0),
                    Coord(9, 0),
                },
            ),
        ],
    )
    def test_inline(self, x: Coord, y: Coord, bounds: tuple[Coord, Coord], inlines: set[Coord]) -> None:
        assert set(x.inline(y, bounds=bounds)) == inlines


class TestDirection:
    def test_orthogonals(self) -> None:
        assert list(Direction.orthogonals()) == [
            Direction.N,
            Direction.E,
            Direction.S,
            Direction.W,
        ]

    def test_diagonals(self) -> None:
        assert list(Direction.diagonals()) == [
            Direction.NE,
            Direction.SE,
            Direction.SW,
            Direction.NW,
        ]

    def test_all(self) -> None:
        assert list(Direction.all()) == [
            Direction.N,
            Direction.NE,
            Direction.E,
            Direction.SE,
            Direction.S,
            Direction.SW,
            Direction.W,
            Direction.NW,
        ]

    @pytest.mark.parametrize(
        ("kwargs", "expected"),
        [
            ({"facing": Direction.N, "orthogonal": True}, [Direction.N, Direction.E, Direction.S, Direction.W]),
            ({"facing": Coord(0, -1), "orthogonal": True}, [Direction.N, Direction.E, Direction.S, Direction.W]),
            (
                {"facing": Direction.NE, "clockwise": False, "diagonal": True},
                [Direction.NE, Direction.NW, Direction.SW, Direction.SE],
            ),
            (
                {"facing": Direction.S, "diagonal": True, "orthogonal": True},
                [
                    Direction.S,
                    Direction.SW,
                    Direction.W,
                    Direction.NW,
                    Direction.N,
                    Direction.NE,
                    Direction.E,
                    Direction.SE,
                ],
            ),
        ],
        ids=("direction-orthogonal", "coord-orthogonal", "counterclockwise-diagonal", "all"),
    )
    def test_rotate(self, kwargs: dict[str, typing.Any], expected: list[Direction]) -> None:
        assert list(Direction.rotate(**kwargs)) == expected

    @pytest.mark.parametrize(
        ("kwargs", "kind", "message"),
        [
            (
                {"facing": Direction.NW, "orthogonal": True},
                ValueError,
                "The starting directiton is not in the desired array.",
            ),
            ({"facing": Direction.N}, ValueError, "At least one of the orthogonal or diagonal arguments must be True"),
        ],
        ids=("invalid-start", "invalid-arguments"),
    )
    def test_rotate_invalid_face(self, kwargs: dict[str, typing.Any], kind: type[Exception], message: str) -> None:
        with pytest.raises(kind, match=message):
            list(Direction.rotate(**kwargs))


class TestGrid:
    def test_create_new(self) -> None:
        assert dict(Grid.new(2, 2).items()) == {(0, 0): ".", (0, 1): ".", (1, 0): ".", (1, 1): "."}

    def test_create_from_string(self) -> None:
        input_string = "12\n34"
        input_string_with_delim = "1,2\n3,4"
        expected = {(0, 0): "1", (1, 0): "2", (0, 1): "3", (1, 1): "4"}
        expected_with_pred = {(0, 0): 1, (1, 0): 2, (0, 1): 3, (1, 1): 4}

        assert dict(Grid.create(input_string).items()) == expected
        assert dict(Grid.create(input_string, predicate=int).items()) == expected_with_pred

        with pytest.raises(ValueError, match="invalid literal"):
            assert dict(Grid.create(input_string_with_delim, predicate=int).items()) == expected_with_pred

        assert dict(Grid.create(input_string_with_delim, predicate=int, split=",").items()) == expected_with_pred
        assert dict(Grid.create(input_string_with_delim, split=",").items()) == expected

    def test_access(self) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)

        assert grid.get((1, 1)) == 5
        assert grid.get(Coord(1, 2)) == 8

        with pytest.raises(KeyError):
            assert grid.get((10, 10)) == -1

        assert grid.get((10, 10), default=-1) == -1

        grid.set((Coord(2, 2)), -1)
        assert grid.get(Coord(2, 2)) == -1

        with pytest.raises(KeyError, match="does not exist. Maybe use the `anywhere=True` argument"):
            grid.set((3, 3), 10)

        grid.set((3, 3), 10, anywhere=True)
        assert grid.get(Coord(3, 3)) == 10

        assert grid.pop((3, 3)) == 10
        assert Coord(3, 3) not in grid

        with pytest.raises(KeyError):
            grid.pop((3, 3))

        assert grid.pop((100, 100), 100) == 100

    def test_print(self) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)
        assert str(grid) == "123\n456\n789"

        grid = Grid({Coord(1, 2): 0, Coord(2, 1): 8})
        assert str(grid) == ".8\n0."

        grid.background = " "
        assert str(grid) == " 8\n0 "

    def test_bounds(self) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)
        assert grid.min_bound == Coord(0, 0)
        assert grid.max_bound == Coord(2, 2)

        grid.set(Coord(-50, 50), 10, True)
        assert grid.min_bound == Coord(-50, 0)
        assert grid.max_bound == Coord(2, 50)

    def test_left(self) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)

        assert list(grid.values((2, 1), Direction.W)) == [5, 4]
        assert list(grid.values((2, 1), Direction.W, True)) == [6, 5, 4]
        assert not list(grid.values((0, 1), Direction.W, False))

    def test_right(self) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)

        assert list(grid.values((0, 1), Direction.E)) == [5, 6]
        assert list(grid.values((0, 1), Direction.E, True)) == [4, 5, 6]
        assert not list(grid.values((2, 1), Direction.E, False))

    def test_up(self) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)

        assert list(grid.values((1, 2), Direction.N)) == [5, 2]
        assert list(grid.values((1, 2), Direction.N, True)) == [8, 5, 2]
        assert not list(grid.values((1, 0), Direction.N, False))

    def test_down(self) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)

        assert list(grid.values((1, 0), Direction.S)) == [5, 8]
        assert list(grid.values((1, 0), Direction.S, True)) == [2, 5, 8]
        assert not list(grid.values((1, 2), Direction.S, False))

    def test_row(self) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)

        assert list(grid.values((1, 0), Direction.ROW)) == [1, 3]
        assert list(grid.values((1, 0), Direction.ROW, True)) == [2, 1, 3]
        assert list(grid.values((0, 0), Direction.ROW, False)) == [2, 3]

    def test_column(self) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)

        assert list(grid.values((0, 1), Direction.COLUMN)) == [1, 7]
        assert list(grid.values((0, 1), Direction.COLUMN, True)) == [4, 1, 7]
        assert list(grid.values((0, 0), Direction.COLUMN, False)) == [4, 7]

    def test_all(self) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)

        assert list(grid.values((1, 1), Direction.ORTHOGONAL)) == [2, 6, 8, 4]
        assert list(grid.values((1, 1), Direction.ORTHOGONAL, True)) == [5, 2, 6, 8, 4]
        assert list(grid.values((0, 0), Direction.ORTHOGONAL, False)) == [2, 3, 4, 7]

    def test_iterators(self) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)

        assert list(grid.iter_coord()) == list(
            itertools.starmap(Coord, [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)])
        )

        assert list(grid.iter_values()) == [1, 2, 3, 4, 5, 6, 7, 8, 9]

        assert list(grid.items()) == [
            (Coord(0, 0), 1),
            (Coord(1, 0), 2),
            (Coord(2, 0), 3),
            (Coord(0, 1), 4),
            (Coord(1, 1), 5),
            (Coord(2, 1), 6),
            (Coord(0, 2), 7),
            (Coord(1, 2), 8),
            (Coord(2, 2), 9),
        ]

    def test_internal(self) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)

        for x, y in itertools.product(range(3), repeat=2):
            if (x, y) == (1, 1):
                assert grid.is_on_edge(Coord(x, y)) is False

            else:
                assert grid.is_on_edge(Coord(x, y)) is True

    def test_orthogonal(self) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)
        assert list(grid.orthogonal((1, 1))) == [Coord(1, 0), Coord(2, 1), Coord(1, 2), Coord(0, 1)]
        assert list(grid.orthogonal((0, 1))) == [Coord(0, 0), Coord(1, 1), Coord(0, 2)]
        assert list(grid.orthogonal((0, 0))) == [Coord(1, 0), Coord(0, 1)]

        with pytest.raises(KeyError, match="does not exist"):
            list(grid.orthogonal((12, 12)))

    def test_diagonal(self) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)
        assert list(grid.diagonal((1, 1))) == [Coord(2, 0), Coord(2, 2), Coord(0, 2), Coord(0, 0)]
        assert list(grid.diagonal((0, 1))) == [Coord(1, 0), Coord(1, 2)]
        assert list(grid.diagonal((0, 0))) == [Coord(1, 1)]

        with pytest.raises(KeyError, match="does not exist"):
            list(grid.diagonal((12, 12)))

    def test_neighbors(self) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)
        assert list(grid.neighbors((1, 1))) == [
            Coord(1, 0),
            Coord(2, 0),
            Coord(2, 1),
            Coord(2, 2),
            Coord(1, 2),
            Coord(0, 2),
            Coord(0, 1),
            Coord(0, 0),
        ]
        assert list(grid.neighbors((0, 1))) == [Coord(0, 0), Coord(1, 0), Coord(1, 1), Coord(1, 2), Coord(0, 2)]
        assert list(grid.neighbors((0, 0))) == [Coord(1, 0), Coord(1, 1), Coord(0, 1)]

        with pytest.raises(KeyError, match="does not exist"):
            list(grid.neighbors((12, 12)))

    @pytest.mark.parametrize(
        ("kwargs", "expected"),
        [
            ({"center": (0, 0), "n": 2}, [[], [Coord(1, 0), Coord(2, 0)], [Coord(0, 1), Coord(0, 2)], []]),
            ({"center": (0, 0), "n": 1}, [[], [Coord(1, 0)], [Coord(0, 1)], []]),
            ({"center": (1, 1), "n": 1}, [[Coord(1, 0)], [Coord(2, 1)], [Coord(1, 2)], [Coord(0, 1)]]),
            ({"center": (0, 0), "n": 3}, [[], [Coord(1, 0), Coord(2, 0)], [Coord(0, 1), Coord(0, 2)], []]),
        ],
        ids=("to-edge", "limit", "surrounding", "insufficient"),
    )
    def test_n_orthogonal(self, kwargs: dict[str, typing.Any], expected: list[list[Coord]]) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)
        assert list(grid.n_orthogonal(**kwargs)) == expected

    @pytest.mark.parametrize(
        ("kwargs", "expected"),
        [
            ({"center": (0, 2), "n": 2}, [[Coord(1, 1), Coord(2, 0)], [Coord(1, 3), Coord(2, 4)], [], []]),
            ({"center": (0, 2), "n": 1}, [[Coord(1, 1)], [Coord(1, 3)], [], []]),
            ({"center": (0, 3), "n": 3}, [[Coord(1, 2), Coord(2, 1), Coord(3, 0)], [Coord(1, 4)], [], []]),
        ],
        ids=("to-edge", "limit", "insufficient"),
    )
    def test_n_diagonal(self, kwargs: dict[str, typing.Any], expected: list[list[Coord]]) -> None:
        grid = Grid.create("12345\n67890\nabcde\nfghij\nklmno")
        assert list(grid.n_diagonal(**kwargs)) == expected

    @pytest.mark.parametrize(
        ("kwargs", "expected"),
        [
            (
                {"center": (0, 0), "n": 2},
                [
                    *([], []),
                    [Coord(1, 0), Coord(2, 0)],
                    [Coord(1, 1), Coord(2, 2)],
                    [Coord(0, 1), Coord(0, 2)],
                    *([], [], []),
                ],
            ),
            ({"center": (0, 0), "n": 1}, [[], [], [Coord(1, 0)], [Coord(1, 1)], [Coord(0, 1)], [], [], []]),
            (
                {"center": (0, 0), "n": 3},
                [
                    *([], []),
                    [Coord(1, 0), Coord(2, 0)],
                    [Coord(1, 1), Coord(2, 2)],
                    [Coord(0, 1), Coord(0, 2)],
                    *([], [], []),
                ],
            ),
        ],
        ids=("to-edge", "limit", "insufficient"),
    )
    def test_n_neighbors(self, kwargs: dict[str, typing.Any], expected: list[list[Coord]]) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)
        assert list(grid.n_neighbors(**kwargs)) == expected

    @pytest.mark.parametrize(
        "method", (Grid.n_orthogonal, Grid.n_diagonal, Grid.n_neighbors), ids=("orthogonal", "diagonal", "neighbors")
    )
    def test_n__invalid(self, method: typing.Callable[..., typing.Iterator[list[Coord]]]) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)

        with pytest.raises(KeyError, match="does not exist"):
            list(method(grid, (12, 12), n=3))

    def test_find(self) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)
        assert grid.find(5) == [Coord(1, 1)]
        assert grid.find(10) == []

        grid = Grid.create("111\n111\n111", predicate=int)
        assert grid.find(1, allow_multiple=True) == [
            Coord(0, 0),
            Coord(1, 0),
            Coord(2, 0),
            Coord(0, 1),
            Coord(1, 1),
            Coord(2, 1),
            Coord(0, 2),
            Coord(1, 2),
            Coord(2, 2),
        ]

    def test_within(self) -> None:
        grid = Grid.create("123\n456\n789", predicate=int)
        assert grid.within((1, 1))
        assert not grid.within((10, 10))
