import typing as t
import pathlib
import tempfile

from ward import Scope, fixture
from ward.hooks import hook
from ward.config import Config
from ward.testing import Test


@hook  # type: ignore
def preprocess_tests(config: Config, collected_tests: list[Test]) -> None:  # pylint: disable=unused-argument
    collected_tests.sort(key=lambda k: k.description)


@fixture(scope=Scope.Global)  # type: ignore
def tmpdir() -> t.Iterator[pathlib.Path]:
    with tempfile.TemporaryDirectory() as name:
        yield pathlib.Path(name)
