import itertools

from ward import test, raises

from .grid import Grid, Coord, Direction


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


@test("grid: left")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((2, 1), Direction.LEFT)) == [5, 4]
    assert list(grid.values((2, 1), Direction.LEFT, True)) == [6, 5, 4]
    assert not list(grid.values((0, 1), Direction.LEFT, False))


@test("grid: right")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((0, 1), Direction.RIGHT)) == [5, 6]
    assert list(grid.values((0, 1), Direction.RIGHT, True)) == [4, 5, 6]
    assert not list(grid.values((2, 1), Direction.RIGHT, False))


@test("grid: up")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((1, 2), Direction.UP)) == [5, 2]
    assert list(grid.values((1, 2), Direction.UP, True)) == [8, 5, 2]
    assert not list(grid.values((1, 0), Direction.UP, False))


@test("grid: down")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((1, 0), Direction.DOWN)) == [5, 8]
    assert list(grid.values((1, 0), Direction.DOWN, True)) == [2, 5, 8]
    assert not list(grid.values((1, 2), Direction.DOWN, False))


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

    assert list(grid.values((1, 1), Direction.ALL)) == [2, 4, 6, 8]
    assert list(grid.values((1, 1), Direction.ALL, True)) == [5, 2, 4, 6, 8]
    assert list(grid.values((0, 0), Direction.ALL, False)) == [2, 3, 4, 7]


@test("grid: internal")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    for coord in itertools.permutations(range(3), 2):
        if coord == (1, 1):
            assert grid.is_on_edge(coord) is False  # type: ignore[arg-type]

        else:
            assert grid.is_on_edge(coord) is True  # type: ignore[arg-type]


@test("coord: arithmetic")  # type: ignore
def _() -> None:
    assert Coord(1, 1) == Coord(1, 1)
    assert Coord(1, 1) != Coord(1, 2)

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
