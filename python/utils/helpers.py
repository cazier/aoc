import os
import pathlib


def load_input(year: str, day: str) -> str:
    root = os.getenv("AOC_ROOT_DIRECTORY", "")

    if root == "":
        raise SystemExit("Could not determine the proper $AOC_ROOT_DIRECTORY environment variable.")

    year_string = f"2{int(year) % 2000:03}"
    day_string = f"{int(day):02}.txt"

    path = pathlib.Path(root, "inputs", year_string, day_string)

    return path.read_text(encoding="utf8")


def splitlines(text: str) -> list[str]:
    return [line for line in text.splitlines() if line]
