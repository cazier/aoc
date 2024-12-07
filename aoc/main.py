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

    if Language.PYTHON in language:
        support = yaml.safe_load(
            pathlib.Path(__file__).parent.joinpath("support", "python.yaml").read_text(encoding="utf8")
        )

    if Language.GO in language:
        support = yaml.safe_load(
            pathlib.Path(__file__).parent.joinpath("support", "go.yaml").read_text(encoding="utf8")
        )

    for lang in language:
        support = yaml.safe_load(
            pathlib.Path(__file__).parent.joinpath("support", f"{lang.value}.yaml").read_text(encoding="utf8")
        )

        for kind in ("run", "test"):
            # TODO: Fix for go

            day_path.joinpath(support[kind]["name"]).write_text(
                str(support[kind]["contents"].replace("$year", f"{year:04d}").replace("$day", f"{day:02d}"))
            )


if __name__ == "__main__":
    app()
