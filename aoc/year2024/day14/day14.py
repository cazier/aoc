import re
import math
import typing
import itertools
import collections
import dataclasses

from aoclib.grid import Grid, Coord

import aoclib

SAMPLE_INPUT: str = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

pattern = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")


class deque(list["Robot"]):
    def __eq__(self, other: typing.Any) -> bool:
        return len(self) == len(other)

    def __ne__(self, other: typing.Any) -> bool:
        return len(self) != len(other)


@dataclasses.dataclass
class Robot:
    position: Coord
    velocity: Coord
    grid: "RoboGrid" = dataclasses.field(init=False)

    @classmethod
    def parse(cls, config: str) -> typing.Self:
        [(px, py, vx, vy)] = pattern.findall(config)
        return cls(Coord(int(px), int(py)), Coord(int(vx), int(vy)))

    def step(self) -> typing.Self:
        x, y = (self.position + self.velocity).G

        if x < self.grid.min_bound.x:
            x = self.grid.max_bound.x - (self.grid.min_bound.x - x - 1)

        elif x > self.grid.max_bound.x:
            x = self.grid.min_bound.x + (x - self.grid.max_bound.x - 1)

        if y < self.grid.min_bound.y:
            y = self.grid.max_bound.y - (self.grid.min_bound.y - y - 1)

        elif y > self.grid.max_bound.y:
            y = self.grid.min_bound.y + (y - self.grid.max_bound.y - 1)

        self.position = Coord(x, y)
        return self


class RoboGrid(Grid[deque]):
    def __init__(self, inputs: str) -> None:
        grid: dict[Coord | tuple[int, int], deque] = collections.defaultdict(deque)

        for robot in map(Robot.parse, aoclib.splitlines(inputs)):
            grid[robot.position].append(robot)
            robot.grid = self

        return super().__init__(grid)

    def _str_get(self, center: tuple[int, int]) -> str:
        try:
            value = len(self.get(center))

            if value != 0:
                return str(value)

            return " "

        except KeyError:
            return self.background

    def step(self, until: int = 100) -> typing.Self:
        for _ in range(until):
            grid: dict[Coord, deque] = collections.defaultdict(deque)

            for coords in self.iter_values():
                for robot in coords:
                    new = robot.step()
                    grid[new.position].append(new)

            self._grid = grid

        return self

    def score(self) -> dict[tuple[bool, bool], int]:
        mid_x = (self.max_bound.x - self.min_bound.x) // 2
        mid_y = (self.max_bound.y - self.min_bound.y) // 2

        result: dict[tuple[bool, bool], int] = collections.defaultdict(int)

        for coord, value in self.items():
            if coord.x == mid_x or coord.y == mid_y:
                continue

            result[(coord.x < mid_x, coord.y < mid_y)] += len(value)

        return result


def part_one(inputs: str) -> int:
    return math.prod(RoboGrid(inputs).step().score().values())


def part_two(inputs: str) -> int:
    grid = RoboGrid(inputs)

    for step in itertools.count(start=1):
        grid.step(until=1)

        for coord, robots in grid.items():
            if len(robots) != 1:
                continue

            if len(grid.region(coord)) > 50:
                return step

    return -1
