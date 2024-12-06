import typing
import datetime
import importlib
from typing import Annotated

import typer

import aoclib

app = typer.Typer()


@app.command()
def run(
    year: int = datetime.date.today().year,
    day: int = datetime.date.today().day,
    part: Annotated[int, typer.Option(show_default="Both parts")] = -1,
) -> None:
    module = importlib.import_module(f".year{year:04d}.day{day:02d}.main", package="aoc")

    if part in (-1, 1):
        print(module.part_one(aoclib.load_input(f"{year:04d}", f"{day:02d}")))

    if part in (-1, 2):
        print(module.part_two(aoclib.load_input(f"{year:04d}", f"{day:02d}")))


@app.command()
def test(
    year: int = datetime.date.today().year, day: int = datetime.date.today().day, part: typing.Optional[int] = None
) -> None:
    module = importlib.import_module(f".year{year:04d}.day{day:02d}.main", package="aoc")
    print(module.part_one("hello-world"))


if __name__ == "__main__":
    app()
