import typing

from aoclib.grid import Grid, Coord

SAMPLE_INPUT: str = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


class Topographic(Grid):
    def trail(self, part: typing.Literal[1, 2]) -> int:
        @typing.overload
        def step(visited: list[Coord], answer: set[Coord], part: typing.Literal[1]) -> set[Coord]: ...
        @typing.overload
        def step(visited: list[Coord], answer: set[tuple[Coord]], part: typing.Literal[2]) -> set[tuple[Coord]]: ...

        def step(
            visited: list[Coord], answer: set[Coord | tuple[Coord]], part: typing.Literal[1, 2]
        ) -> set[Coord | tuple[Coord]]:
            *_, current = visited

            value = self.get(current)

            if value == 9:
                if part == 1:
                    answer.add(current)
                else:
                    answer.add(tuple(stop for stop in visited))

            for neighbor in self.orthogonal(current):
                if neighbor not in visited and self.get(neighbor) == value + 1:
                    answer = step(visited + [neighbor], answer, part=part)

            return answer

        return sum(len(step([trailhead], set(), part=part)) for trailhead in self.find(0, allow_multiple=True))

    def trail_two(self) -> list[Coord]:
        def step(visited: list[Coord], answer: set[tuple[Coord]]) -> int:
            *_, current = visited

            value = self.get(current)

            if value == 9:
                answer.add(tuple(step for step in visited))

            for neighbor in self.orthogonal(current):
                if neighbor not in visited and self.get(neighbor) != "." and self.get(neighbor) == value + 1:
                    answer = step(visited + [neighbor], answer)

            return answer

        return sum(len(step([trailhead], set())) for trailhead in self.find(0, allow_multiple=True))


def part_one(inputs: str) -> int:
    grid = Topographic.create(inputs, predicate=int)
    return grid.trail(part=1)


def part_two(inputs: str) -> int:
    grid = Topographic.create(inputs, predicate=lambda k: int(k) if k != "." else k)
    return grid.trail(part=2)
