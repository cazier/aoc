import enum
import typing
import pathlib
import datetime
import importlib

import yaml
import typer
import pytest

import aoclib


class Action(enum.StrEnum):
    RUN = "run"
    TEST = "test"


class Language(enum.StrEnum):
    PYTHON = "python"
    GO = "go"
    RUST = "rust"


app = typer.Typer()
python = typer.Typer()
app.add_typer(python, name="python")


@python.command()
def run(
    year: int = datetime.date.today().year,
    day: int = datetime.date.today().day,
    part: typing.Annotated[int, typer.Option(show_default="Both parts")] = -1,
) -> None:
    module = importlib.import_module(f".year{year:04d}.day{day:02d}.day{day:02d}", package="aoc")

    with pytest.MonkeyPatch().context() as mp:
        mp.chdir(pathlib.Path(__file__).parent.joinpath(f"year{year:04d}", f"day{day:02d}"))

        if part in (-1, 1):
            print(module.part_one(aoclib.load_input()))

        if part in (-1, 2):
            print(module.part_two(aoclib.load_input()))


@python.command()
def test(
    year: int = datetime.date.today().year,
    day: int = datetime.date.today().day,
    verbose: typing.Annotated[bool, typer.Option("-v", help="Make output more verbose")] = False,
    pdb: typing.Annotated[bool, typer.Option("--pdb", help="Enable debugging")] = False,
) -> None:
    path = pathlib.Path(__file__).parent.joinpath(f"year{year:04d}", f"day{day:02d}")

    args = {"-s"}

    if verbose:
        args.add("-vv")

    if pdb:
        args.add("--pdb")

    exit(pytest.main([*args, str(path)]))


@app.command()
def new(
    language: list[Language] = [Language.PYTHON],
    year: int = datetime.date.today().year,
    day: int = datetime.date.today().day,
    cookie: pathlib.Path = pathlib.Path(".session_cookie"),
    path: pathlib.Path = pathlib.Path("aoc"),
) -> None:
    day_path = path.joinpath(f"year{year:04d}", f"day{day:02d}")

    aoclib.fetch(
        year=year,
        day=day,
        cookie=cookie,
        readme=day_path.joinpath("README.md"),
        input=day_path.joinpath("input"),
        log_level="ERROR",
    )

    for lang in language:
        raw = pathlib.Path(__file__).parent.joinpath("support", f"{lang.value}.yaml").read_text(encoding="utf8")
        raw = raw.replace("$year", f"{year:04d}").replace("$day", f"{day:02d}")

        support: dict[str, dict[str, str]] = yaml.safe_load(raw)

        for kind in ("run", "test"):
            path = day_path.joinpath(support[kind]["name"])

            if not path.exists():
                path.write_text(support[kind]["contents"])


if __name__ == "__main__":
    app()
