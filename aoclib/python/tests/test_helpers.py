import os
import pathlib
from unittest.mock import patch

import pytest
from aoclib.helpers import load_input, splitlines, zip_longest_repeating


class TestAoclib:
    def test_load_input(self, tmp_path: pathlib.Path) -> None:
        input_string = b"hello\nline\ntwo\nfour"
        expected = "hello\nline\ntwo\nfour"

        file = tmp_path.joinpath("inputs", "2020", "15.txt")
        file.parent.mkdir(parents=True, exist_ok=True)

        file.write_bytes(input_string)

        with patch.dict(os.environ, {"AOC_ROOT_DIRECTORY": str(tmp_path)}):
            assert load_input("2020", "15") == expected

            with pytest.raises(FileNotFoundError, match="No such file or directory"):
                expected = load_input("2020", "16")

        with pytest.raises(SystemExit, match=r"Could not determine the proper \$AOC_ROOT_DIRECTORY"):
            expected = load_input("2020", "15")

    def test_zip_longest_repeating(self) -> None:
        assert list(zip_longest_repeating(["a"], ["b", "c"], ["d", "r", "f"])) == [
            ["a", "b", "d"],
            ["a", "c", "r"],
            ["a", "c", "f"],
        ]
        assert list(zip_longest_repeating([], [], [])) == []  # pylint: disable=use-implicit-booleaness-not-comparison

    def test_splitlines(self) -> None:
        assert list(splitlines("")) == []  # pylint: disable=use-implicit-booleaness-not-comparison
        assert list(splitlines("\nhello\n\n")) == ["hello"]
        assert list(splitlines("\nhello\ngoodbye\n \n")) == ["hello", "goodbye", " "]
