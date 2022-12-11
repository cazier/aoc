import itertools

from ward import test, raises

from .grid import Grid, Direction


@test("Creation")  # type: ignore
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


@test("left")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((2, 1), Direction.LEFT)) == [5, 4]
    assert list(grid.values((2, 1), Direction.LEFT, True)) == [6, 5, 4]
    assert not list(grid.values((0, 1), Direction.LEFT, False))


@test("right")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((0, 1), Direction.RIGHT)) == [5, 6]
    assert list(grid.values((0, 1), Direction.RIGHT, True)) == [4, 5, 6]
    assert not list(grid.values((2, 1), Direction.RIGHT, False))


@test("up")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((1, 2), Direction.UP)) == [5, 2]
    assert list(grid.values((1, 2), Direction.UP, True)) == [8, 5, 2]
    assert not list(grid.values((1, 0), Direction.UP, False))


@test("down")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((1, 0), Direction.DOWN)) == [5, 8]
    assert list(grid.values((1, 0), Direction.DOWN, True)) == [2, 5, 8]
    assert not list(grid.values((1, 2), Direction.DOWN, False))


@test("row")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((1, 0), Direction.ROW)) == [1, 3]
    assert list(grid.values((1, 0), Direction.ROW, True)) == [2, 1, 3]
    assert list(grid.values((0, 0), Direction.ROW, False)) == [2, 3]


@test("column")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((0, 1), Direction.COLUMN)) == [1, 7]
    assert list(grid.values((0, 1), Direction.COLUMN, True)) == [4, 1, 7]
    assert list(grid.values((0, 0), Direction.COLUMN, False)) == [4, 7]


@test("all")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    assert list(grid.values((1, 1), Direction.ALL)) == [2, 4, 6, 8]
    assert list(grid.values((1, 1), Direction.ALL, True)) == [5, 2, 4, 6, 8]
    assert list(grid.values((0, 0), Direction.ALL, False)) == [2, 3, 4, 7]


@test("internal")  # type: ignore
def _() -> None:
    grid = Grid.create("123\n456\n789", int)

    for coord in itertools.permutations(range(3), 2):
        if coord == (1, 1):
            assert grid.is_on_edge(coord) is False  # type: ignore[arg-type]

        else:
            assert grid.is_on_edge(coord) is True  # type: ignore[arg-type]
