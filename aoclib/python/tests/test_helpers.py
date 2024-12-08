import typing
import pathlib
import contextlib

import pytest
from aoclib.helpers import load_input, splitlines, zip_longest_repeating


class TestAoclib:
    @pytest.mark.parametrize(
        ("exists", "cm"),
        [
            (False, pytest.raises(FileNotFoundError, match="No such file or directory")),
            (True, contextlib.nullcontext()),
        ],
        ids=("missing", "exists"),
    )
    def test_load_input(self, exists: bool, cm: typing.ContextManager[None], tmp_path: pathlib.Path) -> None:
        pytest.MonkeyPatch().chdir(tmp_path)
        input_string = b"hello\nline\ntwo\nfour"
        expected = "hello\nline\ntwo\nfour"

        if exists:
            file = tmp_path.joinpath("input")
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_bytes(input_string)

        with cm:
            assert load_input() == expected

    def test_zip_longest_repeating(self) -> None:
        assert list(zip_longest_repeating(["a"], ["b", "c"], ["d", "r", "f"])) == [
            ["a", "b", "d"],
            ["a", "c", "r"],
            ["a", "c", "f"],
        ]
        assert list(zip_longest_repeating([], [], [])) == []

    def test_splitlines(self) -> None:
        assert list(splitlines("")) == []
        assert list(splitlines("\nhello\n\n")) == ["hello"]
        assert list(splitlines("\nhello\ngoodbye\n \n")) == ["hello", "goodbye", " "]
