import os
import pathlib
from unittest.mock import patch

from ward import test, raises
from utils.helpers import load_input, splitlines, zip_longest_repeating
from utils.conftest import tmpdir


@test("load_input")  # type: ignore
def _(directory: pathlib.Path = tmpdir) -> None:
    input_string = b"hello\nline\ntwo\nfour"
    expected = "hello\nline\ntwo\nfour"

    file = directory.joinpath("inputs", "2020", "15.txt")
    file.parent.mkdir(parents=True, exist_ok=True)

    file.write_bytes(input_string)

    with patch.dict(os.environ, {"AOC_ROOT_DIRECTORY": str(directory)}):
        assert load_input("2020", "15") == expected

        with raises(FileNotFoundError) as no_file:
            expected = load_input("2020", "16")
        assert "No such file or directory" in str(no_file.raised)

    with raises(SystemExit) as no_env:  # type: ignore[type-var]
        expected = load_input("2020", "15")
    assert "Could not determine the proper $AOC_ROOT_DIRECTORY" in str(no_env.raised)


@test("zip_longest_repeating")  # type: ignore
def _() -> None:
    assert list(zip_longest_repeating(["a"], ["b", "c"], ["d", "r", "f"])) == [
        ["a", "b", "d"],
        ["a", "c", "r"],
        ["a", "c", "f"],
    ]
    assert list(zip_longest_repeating([], [], [])) == []  # pylint: disable=use-implicit-booleaness-not-comparison


@test("splitlines")  # type: ignore
def _() -> None:
    assert list(splitlines("")) == []  # pylint: disable=use-implicit-booleaness-not-comparison
    assert list(splitlines("\nhello\n\n")) == ["hello"]
    assert list(splitlines("\nhello\ngoodbye\n \n")) == ["hello", "goodbye", " "]
