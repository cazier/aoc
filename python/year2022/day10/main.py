import pathlib
import itertools

from rich import print  # pylint: disable=redefined-builtin
from year2022.day10.device import Device

import utils
from utils.display import Display

SAMPLE_INPUT: str = pathlib.Path(__file__).parent.joinpath("sample.txt").read_text(encoding="utf8")


def part_one(inputs: str) -> int:
    cpu = Device(inputs.splitlines())

    return cpu.run()


def part_one_comp(inputs: str) -> int:
    cmds = [[0] if command == "noop" else [0, int(value[0])] for command, *value in map(str.split, inputs.splitlines())]

    return sum(
        cycle * sum([1] + list(itertools.chain.from_iterable(cmds))[: cycle - 1])
        for cycle in (20, 60, 100, 140, 180, 220)
    )


def part_two(inputs: str) -> Display:
    cpu = Device(inputs.splitlines())

    cpu.draw()

    return cpu.screen


if __name__ == "__main__":  # pragma: no cover
    input_string = utils.load_input("2022", "10")

    print(part_one(input_string))
    print(part_two(input_string).characters())
