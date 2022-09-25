# Advent of Code

This is at least my third or fourth attempt at maintaining a repo with my AoC solutions, but I'm going to try again.

## Getting Started

### Requirements

#### Languages
I'm going to be doing this in at least Python 3.10+ and Golang 1.19+. Ensure one (or both) are installed.

#### Tools
- pre-commit ([link](https://pre-commit.com/))
- bash (technically)

### Running

To get started pulling the information, you can use the [`new.sh`](./new.sh) bash script. Run it with `--help` to get some usage information. It will download the input file and the available portions of the puzzle descriptions, putting each into the respective directory.

Additionally, the script will create new folders, as needed, for the language, year, and day, and creates a pair of code files. One for the actual executed code, and a test file.

For golang, they will be named `<day>.go` and `<day>_test.go`.

```bash
$ ./new.sh --day 3 --year 2021
readme.py: Successfully retrieved data!
Succesfully created all the files. Get to work!
```

Once you've filled in all the code in their individual files, you can run them with the [`run.sh`](./run.sh) script. It also has its own help flag (`--help/-h`). As an example:

```bash
$ ./run.sh --run --day 1 --year 2021
Part One: A number
Part Two: Another number!
```
