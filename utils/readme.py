#!/bin/env python3.10
"""A standalone script, using only standard library tools, to pull the input files and descriptions
from the AoC website to include in the repository.
"""

import re
import sys
import pprint
import logging
import argparse
from pathlib import Path
from dataclasses import field, dataclass
from html.parser import HTMLParser
from urllib.request import Request, urlopen


def get(year: int, day: int, cookie: str, _input: bool = False) -> str:
    """Helper function to download information from the Advent of Code website, using a users
    session cookie.

    Args:
        year (int): event year (2021, 2020, etc.)
        day (int): puzzle day to download
        cookie (str): session cookie string
        _input (bool, optional): If true, get the input instead of the readme. Defaults to False.

    Returns:
        str: _description_
    """
    url = f"https://adventofcode.com/{year}/day/{day}"

    if _input:
        logger.info("Getting puzzle input file.")
        url += "/input"

    else:
        logger.info("Getting puzzle readme data.")

    req = Request(url=url)
    req.add_header("Cookie", f"session={cookie.strip()}")

    return str(urlopen(req).read().decode("utf8"))


@dataclass(repr=True)
class Element:
    """A dataclass representing the data stored in an HTML element"""

    tag: str
    data: str

    exception: bool = field(init=False, default=False)

    def __str__(self) -> str:
        return self.__repr__()


@dataclass
class Arguments:
    """Arguments from the command line, added to a class largely for type-hinting purposes"""

    year: int
    day: int
    log_level: str
    cookie: Path
    aoc_path: Path


class Puzzle:
    """Data storing class to properly parse out values from the internal storage stack and create a
    correctly "rendered" Markdown file.
    """

    name: str
    index: int

    _part: int = 1

    _part_one: list[str] = []
    _part_two: list[str] = []

    _internal: list[Element] = []

    def add(self, values: Element) -> None:
        """Append a value to the internal storage

        Args:
            values (Element): value to be added to storage
        """
        self._internal.append(values)

    def add_to(self, back: int, extra: str) -> None:
        """Append a value to the internal storage

        Args:
            values (Element): value to be added to storage
        """
        self._internal[back].data += extra

    def next(self, value: int) -> None:
        """Used to increment the internal part storage index, and to clear the data between parts

        Args:
            value (int): next part to be analyzed
        """
        self._part = value
        self._internal.clear()

    @property
    def part(self) -> list[str]:
        """An accessor to the currently worked internal storage list

        Returns:
            list[str]: storage list
        """
        if self._part == 1:
            return self._part_one

        return self._part_two

    @property
    def part_one(self) -> str:
        """Convert the internally stored part into a complete string, in preparation for being
        written to a file

        Returns:
            str: part one Markdown data
        """
        return "".join(self._part_one)

    @property
    def part_two(self) -> str:
        """Convert the internally stored part into a complete string, in preparation for being
        written to a file

        Returns:
            str: part two Markdown data
        """
        return "".join(self._part_two)

    @property
    def parsed(self) -> int:
        """Get the number of *generated* sections

        Returns:
            int: sections
        """
        return sum((len(self._part_one) > 0, len(self._part_two) > 0))

    def generate(self) -> None:
        """Iterate over each item in the internal storage, and match each HTML tag to a particular
        action. When that action is matched, pass the element data (or possibly a list of element
        data) to the appropriate method to get proper string data output.
        """
        self.index = 0
        stop = len(self._internal)
        while self.index < stop:
            element = self._internal[self.index]

            match element.tag:
                case "h2":
                    self.header(element.data)

                case "code":
                    self.inline_code(element.data)

                case "em":
                    self.emphasis(element.data)

                case "span":
                    self.span(element.data)

                case "<control>":
                    self.part.append(element.data)
                    self.index += 1

                case "<pre>":
                    if element.data == "<start>":
                        pre_start = self.index + 1
                        for index, element in enumerate(self._internal[pre_start:stop], pre_start):
                            if element.tag == "<pre>" and element.data == "<stop>":
                                pre_stop = index
                                break

                        self.code_block(*self._internal[pre_start:pre_stop])

                        self.index = pre_stop + 1

                case "p" | "li" | "a":
                    self.generic(element.data)

                case "article" | "ul":
                    self.index += 1

                case _:
                    logger.error("Found an unexpected element tag: %s", element.tag)
                    self._surround_helper()
                    sys.exit(1)

    def _surround_helper(self) -> None:
        """Helper method to print out surrounding tags when there's an exception with one."""
        self._internal[self.index].exception = True

        logger.debug(
            "Attempting to show the surrounding 5 elements. This one has exeception=True.\n%s",
            pprint.pformat(
                [self._internal[i] for i in range(self.index - 5, self.index + 6) if 0 <= i < len(self._internal)]
            ),
        )

    def write(self) -> str:
        """Dump out the combined puzzle header and part(s) to a string to be written to a file

        Returns:
            str: output puzzle information
        """
        full_text = f"{self.name}\n\n{self.part_one}"

        if self.part_two:
            full_text += f"\n\n{self.part_two}"

        return full_text

    def header(self, data: str) -> None:
        """Parse out the header information. For Part 1, this will include the puzzle name.

        Args:
            data (str): element data
        """
        self.index += 1

        if (head := "--- Part Two ---") in data:
            self.part.append(f"## {head}")
            return

        self.name = f"# {data}"
        self.part.append("## --- Part One ---")

    def generic(self, data: str) -> None:
        """Parse out generic text information, without additional formatting

        Args:
            data (str): element data
        """
        self.part.append(clean(f"{data}"))

        self.index += 1

    def _multiliner(self, formatted_data: str) -> None:
        """A helper function to combine elements which are "inline". i.e., an inline-code block
        which SHOULDN'T have a newline character separating it from the next bit of data.

        Args:
            formatted_data (str): _description_
        """
        last_line = self.part[-1]

        next_line = clean(self._internal[self.index + 1].data)

        self.part[-1] = f"{last_line}{formatted_data}{next_line}"
        self.index += 2

    def emphasis(self, data: str) -> None:
        """Parse out emphasized text information: <em>data</em>

        Args:
            data (str): element data
        """
        data = f"*{clean(data)}*"
        return self._multiliner(data)

    def inline_code(self, data: str) -> None:
        """Parse out inline code: <code>data</code>

        Args:
            data (str): element data
        """
        data = f"`{clean(data)}`"
        self._multiliner(data)

    def code_block(self, *lines: Element) -> None:
        """Parse out multiline code blocks: <pre><code>data\ndata\ndata</code></pre>

        Args:
            *lines (Element): elements in the code block
        """
        data = "".join(map(lambda k: k.data, lines))
        self.part.append("    " + "\n    ".join(data.splitlines()) + "\n")

    def span(self, data: str) -> None:
        """Similar to the `Puzzle.generic`, this is used for spans, which are typically used to add
        mouseover text to the puzzle description.

        Args:
            data (str): element data
        """
        data = f"{clean(data)}"
        self._multiliner(data)


def clean(data: str) -> str:
    # pylint: disable-next=anomalous-backslash-in-string
    """Remove any instances of an \n\s+ within the tag data

    Args:
        data (str): an HTML data which may have extra whitespace

    Returns:
        str: the data with the extra whitespace removed
    """
    return re.sub(r"\n\s+", " ", data, 1)


class Parser(HTMLParser):
    """A class to parse out an HTML page. This will manage an internal LILO stack to track where the
    text parts of the page are, in reference to an element type, and will internally generate the
    storage page output (which is the Markdown format).
    """

    stack: list[str] = []
    storage: Puzzle = Puzzle()

    def feed(self, data: str) -> None:
        """Feed the page data to the HTML parser. This will also manage splitting the page into the
        two separate parts and advancing that index in storage.

        Args:
            data (str): page HTML data
        """

        def repl(match: re.Match[str]) -> str:
            """Remove all instances of <em> and </em> from the matched object

            Args:
                match (re.Match): a code block element that might have emphasized characters

            Returns:
                str: the same block with emphasis removed
            """
            return re.sub(r"</?em>", "", match.group(1))

        matches = re.findall(r"(<article.*?</article>)", data, re.DOTALL)

        logger.debug("Found %s sections in the page contents", len(matches))

        if not matches:
            logger.error("No articles (puzzles) were found in the pulled webpage.")
            return

        for part, results in enumerate(matches, start=1):
            # Removing emphasized sections inside <pre><code> blocks:
            results = re.sub(r"(<pre><code>.*?</code></pre>)", repl, results, flags=re.DOTALL)

            logger.info("Feeding data from Part %d", part)
            self.storage.next(part)

            super().feed(results)
            self.storage.generate()

        logger.info("Parsed out data to create %s sections", self.storage.parsed)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Manage opening a tag and appending it to the stack. In a few instances this will also add
        explicit structures to the storage element, to add newlines or manage larger
        code blocks or lists.

        Args:
            tag (str): element tag name (i.e., h2, li, etc.)
            attrs (list[tuple[str, str  |  None]]): element attributes (These are ignored right now)
        """
        logger.debug("Adding `%s` to stack", tag)
        self.stack.append(tag)

        # Use these tags to add a controlled newline to the final product
        if tag in ("ul", "pre"):
            self.storage.add(Element("<control>", "\n"))

        # Use these tags to add a controlled Markdown unsorted list dash to the final product
        elif tag in ("li"):
            self.storage.add(Element("<control>", " - "))

        # Use this to manage a larger code block
        if tag in ("pre",):
            self.storage.add(Element("<pre>", "<start>"))

        # Mostly as a sanity check, the only elements that should have attributes are spans
        if tag not in ("span",) and attrs:
            logger.warning("A tag with attributes was found: %s had attrs: %s", tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        """Manage closing a tag and popping the last instance of the stack. In a few instances, this
        will also add explicit structures to the storage element, to add newlines or manage larger
        code blocks.

        Args:
            tag (str): element tag name (i.e., h2, li, etc.)
        """
        logger.debug("Popping `%s` from stack", tag)
        self.stack.pop()

        # Use this to manage a larger code block, works with the above field in handle_starttag
        if tag in ("pre",):
            self.storage.add(Element("<pre>", "<stop>"))

        # Use these tags to add a controlled newline to the final product
        if tag in ("h2", "p", "li", "ul", "pre"):
            self.storage.add(Element("<control>", "\n"))

    def handle_data(self, data: str) -> None:
        """Get the data within an open/close html tag. This may be replaceable with a better use of
        the `HTMLParser.get_starttag_text()` method, but works for now.

        Args:
            data (str): all the character data between the tags
        """
        logger.debug("Adding data to `%s` in storage", self.stack[-1])

        # Some of the AoC code blocks include emphasis which I'm choosing to ignore
        if self.stack[-3:] == ["pre", "code", "em"]:
            pass
            # self.storage.add_to(-1, data)

        # Want to avoid matching the newlines + space that occur after the tag is closed
        elif re.match(r"\n\s+", data) is None:
            self.storage.add(Element(self.stack[-1], data))


if __name__ == "__main__":
    cli = argparse.ArgumentParser(__file__)
    cli.add_argument("--year", type=int, help="event year", required=True)
    cli.add_argument("--day", type=int, help="puzzle day", required=True)
    cli.add_argument("--cookie", type=Path, help="path to session cookie", required=True)
    cli.add_argument("--aoc-path", type=Path, help="path to the aoc directory", required=True)
    cli.add_argument("--log-level", type=str, default="INFO", help="logging level")

    args = Arguments(**vars(cli.parse_args()))

    readme = args.aoc_path.joinpath("puzzle_readmes", f"{args.year}", f"{args.day:02}.md")
    puzzle_inputs = args.aoc_path.joinpath("inputs", f"{args.year}", f"{args.day:02}.txt")

    readme.parent.mkdir(parents=True, exist_ok=True)
    puzzle_inputs.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=args.log_level,
        format="%(module)s: %(levelname)s: %(funcName)s: %(lineno)d: %(message)s",
    )
    logger = logging.getLogger()

    cookie_string = args.cookie.read_text("utf8")

    parser = Parser()
    parser.feed(get(args.year, args.day, cookie_string))

    readme.write_text(parser.storage.write(), "utf8")

    if not puzzle_inputs.exists():
        puzzle_inputs.write_text(get(args.year, args.day, cookie_string, _input=True), "utf8")

    print(f"{__file__.rsplit('/', maxsplit=1)[-1]}: Successfully retrieved data!")
