import enum
import typing
import pathlib
import datetime
import importlib

import typer
import pytest

import aoclib


class Action(enum.StrEnum):
    RUN = "run"
    TEST = "test"


app = typer.Typer()
python = typer.Typer()
app.add_typer(python, name="python")


@python.command()
def run(
    year: int = datetime.date.today().year,
    day: int = datetime.date.today().day,
    part: typing.Annotated[int, typer.Option(show_default="Both parts")] = -1,
) -> None:
    module = importlib.import_module(f".year{year:04d}.day{day:02d}.main", package="aoc")

    if part in (-1, 1):
        print(module.part_one(aoclib.load_input(f"{year:04d}", f"{day:02d}")))

    if part in (-1, 2):
        print(module.part_two(aoclib.load_input(f"{year:04d}", f"{day:02d}")))


@python.command()
def test(
    year: int = datetime.date.today().year,
    day: int = datetime.date.today().day,
) -> None:
    path = pathlib.Path(__file__).parent.joinpath(f"year{year:04d}", f"day{day:02d}")

    exit(pytest.main(["-v", str(path)]))


@app.command()
def new(year: int = datetime.date.today().year, day: int = datetime.date.today().day) -> None:
    pass


if __name__ == "__main__":
    app()
