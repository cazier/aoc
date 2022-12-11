import os
import pathlib
from unittest.mock import patch

from ward import test, raises

from .helpers import load_input
from .conftest import tmpdir


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
