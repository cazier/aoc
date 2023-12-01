import itertools

from ward import test, raises

from .grid import Grid, Coord, Direction


@test("coord: arithmetic")  # type: ignore
def _() -> None:
    assert repr(Coord(1, 1)) == "<Coord(1, 1)>"

    assert Coord(1, 1) == Coord(1, 1)
    assert Coord(1, 1) != Coord(1, 2)
    assert Coord(12, 12) == (12, 12)

    with raises(NotImplementedError):
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

    with raises(NotImplementedError):
        coord = Coord(12, 12) / 2

    with raises(NotImplementedError):
        coord = Coord(12, 12) // 2

    assert abs(Coord(-1, 1)) == Coord(1, 1)
    assert abs(Coord(-1, -1)) == Coord(1, 1)


@test("coord: normalize")  # type: ignore
def _() -> None:
    assert Coord(0, 0).normalize() == Coord(0, 0)
    assert Coord(-1, 10).normalize() == Coord(-1, 1)
    assert Coord(50, -100).normalize() == Coord(1, -1)
    assert Coord(10, 100).normalize() == Coord(1, 1)


@test("coord: touching")  # type: ignore
def _() -> None:
    assert Coord(0, 0).touching((0, 0))
    assert Coord(1, 1).touching((0, 0))
    assert Coord(1, 1).touching((0, 2))
    assert Coord(1, 1).touching((2, 0))
    assert Coord(0, 0).touching((1, 1))
    assert not Coord(1, 1).touching((10, 1))
    assert not Coord(1, 1).touching((1, 5))


@test("direction: orthogonals")  # type:ignore
def _() -> None:
    assert list(Direction.orthogonals()) == [
        Direction.N,
        Direction.E,
        Direction.S,
        Direction.W,
    ]


@test("direction: all")  # type:ignore
def _() -> None:
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


@test("grid: create from string")  # type: ignore
def _() -> None:
    input_string = "12\n34"
    input_string_with_delim = "1,2\n3,4"
    expected = {(0, 0): "1", (1, 0): "2", (0, 1): "3", (1, 1): "4"}
    expected_with_pred = {(0, 0): 1, (1, 0): 2, (0, 1): 3, (1, 1): 4}

    assert dict(Grid.create(input_string).items()) == expected  # type: ignore
    assert dict(Grid.create(input_string, int).items()) == expected_with_pred  # type: ignore

    with raises(ValueError) as exception:
        assert dict(Grid.create(input_string_with_delim, int).items()) == expected_with_pred  # type: ignore
    assert "invalid literal" in str(exception.raised)

    assert dict(Grid.create(input_string_with_delim, int, ",").items()) == expected_with_pred  # type: ignore
    assert dict(Grid.create(input_string_with_delim, split=",").items()) == expected  # type: ignore


@test("grid: access")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert grid.get((1, 1)) == 5
    assert grid.get(Coord(1, 2)) == 8

    with raises(KeyError):
        assert grid.get((10, 10)) == -1

    grid.set((Coord(2, 2)), -1)
    assert grid.get(Coord(2, 2)) == -1

    with raises(KeyError) as exception:
        grid.set((3, 3), 10)
    assert "does not exist. Maybe use the `anywhere=True` argument" in str(exception.raised)

    grid.set((3, 3), 10, anywhere=True)
    assert grid.get(Coord(3, 3)) == 10

    assert grid.pop((3, 3)) == 10
    assert Coord(3, 3) not in grid

    with raises(KeyError) as exception:
        grid.pop((3, 3))


@test("grid: print")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)
    assert str(grid) == "123\n456\n789"

    grid = Grid({Coord(1, 2): 0, Coord(2, 1): 8})
    assert str(grid) == ".8\n0."

    grid.background = " "
    assert str(grid) == " 8\n0 "


@test("grid: bounds")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)
    assert grid.min_bound == Coord(0, 0)
    assert grid.max_bound == Coord(2, 2)

    grid.set(Coord(-50, 50), 10, True)
    assert grid.min_bound == Coord(-50, 0)
    assert grid.max_bound == Coord(2, 50)


@test("grid: left")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((2, 1), Direction.W)) == [5, 4]
    assert list(grid.values((2, 1), Direction.W, True)) == [6, 5, 4]
    assert not list(grid.values((0, 1), Direction.W, False))


@test("grid: right")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((0, 1), Direction.E)) == [5, 6]
    assert list(grid.values((0, 1), Direction.E, True)) == [4, 5, 6]
    assert not list(grid.values((2, 1), Direction.E, False))


@test("grid: up")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((1, 2), Direction.N)) == [5, 2]
    assert list(grid.values((1, 2), Direction.N, True)) == [8, 5, 2]
    assert not list(grid.values((1, 0), Direction.N, False))


@test("grid: down")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((1, 0), Direction.S)) == [5, 8]
    assert list(grid.values((1, 0), Direction.S, True)) == [2, 5, 8]
    assert not list(grid.values((1, 2), Direction.S, False))


@test("grid: row")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((1, 0), Direction.ROW)) == [1, 3]
    assert list(grid.values((1, 0), Direction.ROW, True)) == [2, 1, 3]
    assert list(grid.values((0, 0), Direction.ROW, False)) == [2, 3]


@test("grid: column")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((0, 1), Direction.COLUMN)) == [1, 7]
    assert list(grid.values((0, 1), Direction.COLUMN, True)) == [4, 1, 7]
    assert list(grid.values((0, 0), Direction.COLUMN, False)) == [4, 7]


@test("grid: all")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((1, 1), Direction.ORTHOGONAL)) == [2, 6, 8, 4]
    assert list(grid.values((1, 1), Direction.ORTHOGONAL, True)) == [5, 2, 6, 8, 4]
    assert list(grid.values((0, 0), Direction.ORTHOGONAL, False)) == [2, 3, 4, 7]


@test("grid: iterators")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

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


@test("grid: internal")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    for (x, y) in itertools.product(range(3), repeat=2):
        if (x, y) == (1, 1):
            assert grid.is_on_edge(Coord(x, y)) is False

        else:
            assert grid.is_on_edge(Coord(x, y)) is True


@test("grid: orthogonal")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)
    assert list(grid.orthogonal((1, 1))) == [Coord(1, 0), Coord(2, 1), Coord(1, 2), Coord(0, 1)]
    assert list(grid.orthogonal((0, 1))) == [Coord(0, 0), Coord(1, 1), Coord(0, 2)]
    assert list(grid.orthogonal((0, 0))) == [Coord(1, 0), Coord(0, 1)]

    with raises(KeyError) as exception:
        list(grid.orthogonal((12, 12)))
    assert "does not exist" in str(exception.raised)


@test("grid: neighbors")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)
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

    with raises(KeyError) as exception:
        list(grid.neighbors((12, 12)))
    assert "does not exist" in str(exception.raised)


@test("grid: find")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)
    assert grid.find(5) == [Coord(1, 1)]
    assert grid.find(10) == []  # pylint: disable=use-implicit-booleaness-not-comparison

    grid = Grid.create("111\n111\n111", int)
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


@test("grid: within")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)
    assert grid.within((1, 1))
    assert not grid.within((10, 10))
