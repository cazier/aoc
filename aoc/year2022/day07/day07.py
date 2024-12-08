import pathlib
import tempfile

SAMPLE_INPUT: str = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


def assemble(inputs: str) -> tuple[str, dict[pathlib.Path, int]]:
    lines = (line.splitlines() for line in inputs.split("$ ") if line not in ("", "cd /\n"))
    track: dict[pathlib.Path, int] = {}

    with tempfile.TemporaryDirectory() as tmp:
        directory = pathlib.Path(tmp).absolute()

        for stdin, *stdout in lines:
            cmd, *arg = stdin.split()

            if cmd == "ls":
                size = 0
                for line in stdout:
                    detail, _ = line.split()
                    if detail != "dir":
                        size += int(detail)

                track[directory] = size

            elif cmd == "cd":
                directory = directory.joinpath(arg[0]).resolve()

    for key, value in track.items():
        for parent in key.relative_to(tmp).parents:
            track[pathlib.Path(tmp, parent)] += value

    return tmp, track


def part_one(inputs: str) -> int:
    _, track = assemble(inputs)
    return sum(i for i in track.values() if i < 1e5)


def part_two(inputs: str) -> int:
    total = 70000000
    minimum = 30000000

    tmp, track = assemble(inputs)
    missing = minimum - (total - track[pathlib.Path(tmp)])

    return min(i for i in track.values() if i > missing)
