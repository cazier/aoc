"""A set of tools to manipulate, perform OCR on, and display a simple pixel-based display screen."""

import typing as t


class OCR:
    """Very basic OCR for the Display class"""

    # Most of the credit to: https://github.com/bsoyka/advent-of-code-ocr/blob/main/advent_of_code_ocr/characters.py, I
    # just moved things around, added some missing characters, and switched to integer values.
    _character_to_display = {
        "A": "0110\n1001\n1001\n1111\n1001\n1001",
        "B": "1110\n1001\n1110\n1001\n1001\n1110",
        "C": "0110\n1001\n1000\n1000\n1001\n0110",
        "D": "1110\n1001\n1001\n1001\n1001\n1110",
        "E": "1111\n1000\n1110\n1000\n1000\n1111",
        "F": "1111\n1000\n1110\n1000\n1000\n1000",
        "G": "0110\n1001\n1000\n1011\n1001\n0111",
        "H": "1001\n1001\n1111\n1001\n1001\n1001",
        "I": "1110\n0100\n0100\n0100\n0100\n1110",
        "J": "0011\n0001\n0001\n0001\n1001\n0110",
        "K": "1001\n1010\n1100\n1010\n1010\n1001",
        "L": "1000\n1000\n1000\n1000\n1000\n1111",
        "M": "1001\n1111\n1111\n1001\n1001\n1001",
        "N": "1001\n1101\n1101\n1011\n1011\n1001",
        "O": "0110\n1001\n1001\n1001\n1001\n0110",
        "P": "1110\n1001\n1001\n1110\n1000\n1000",
        "Q": "0110\n1001\n1001\n1001\n0110\n0001",
        "R": "1110\n1001\n1001\n1110\n1010\n1001",
        "S": "0110\n1001\n0100\n0010\n1001\n0110",
        "T": "1110\n0100\n0100\n0100\n0100\n0100",
        "U": "1001\n1001\n1001\n1001\n1001\n0110",
        "V": "1001\n1001\n1001\n1001\n0110\n0110",
        "W": "1001\n1001\n1001\n1111\n1111\n1001",
        "X": "1001\n1001\n0110\n0110\n1001\n1001",
        "Y": "1010\n1010\n1010\n0100\n0100\n0100",
        "Z": "1111\n0001\n0010\n0100\n1000\n1111",
        "0": "0110\n1011\n1011\n1101\n1101\n0110",
        "1": "0100\n1100\n0100\n0100\n0100\n1110",
        "2": "0110\n1001\n0001\n0010\n0100\n1111",
        "3": "0110\n1001\n0010\n0001\n1001\n0110",
        "4": "1001\n1001\n1111\n0001\n0001\n0001",
        "5": "1111\n1000\n1110\n0001\n0001\n1110",
        "6": "0111\n1000\n1110\n1001\n1001\n0110",
        "7": "1111\n0001\n0001\n0001\n0001\n0001",
        "8": "0110\n1001\n0110\n1001\n1001\n0110",
        "9": "0110\n1001\n0111\n0001\n0001\n0001",
    }

    _display_to_character = {value: key for key, value in _character_to_display.items()}

    _width = 4
    _height = 6

    @staticmethod
    def single_to_display(character: str, foreground: str, background: str) -> str:
        """Converts a single character into its display orientation

        .. code-block::
                       .##.
                       #..#
                       #..#
            "A" ->     ####
                       #..#
                       #..#

        Args:
            character (str): single character letter
            foreground (str): pixel style to use for the foreground mark
            background (str): pixel style to use for the background mark

        Raises:
            NotImplementedError: The character does not exist in the display "settings"

        Returns:
            str: the display output
        """
        try:
            return OCR._character_to_display[character].replace("1", foreground).replace("0", background)

        except KeyError as exc:
            raise NotImplementedError("The requested character does not exist yet. Add it!") from exc

    @staticmethod
    def single_from_display(display: str, foreground: str, background: str) -> str:
        """Performs "OCR" to convert a single-character display value into its character representation.

        .. code-block::
            .##.
            #..#
            #..#
            ####     -> "A"
            #..#
            #..#

        Args:
            display (str): full string of characters
            foreground (str): pixel style to use for the foreground mark
            background (str): pixel style to use for the background mark
            spacing (int, optional): columns of background pixels between characters. Defaults to 1.

        Returns:
            str: the display output
        """
        try:
            return OCR._display_to_character[display.replace(foreground, "1").replace(background, "0")]

        except KeyError as exc:
            raise NotImplementedError("The requested character does not exist yet. Add it!") from exc

    @staticmethod
    def string_to_display(string: str, foreground: str, background: str, spacing: int = 1) -> str:
        """Converts a full string into its display orientation

        .. code-block::
                        .##. ###.
                        #..# #..#
                        #..# ###.
            "AB" ->     #### #..#
                        #..# #..#
                        #..# ###.

        Args:
            string (str): full string of characters
            foreground (str): pixel style to use for the foreground mark
            background (str): pixel style to use for the background mark
            spacing (int, optional): columns of background pixels between characters. Defaults to 1.

        Raises:
            NotImplementedError: The character does not exist in the display "settings"

        Returns:
            str: the display output
        """

        def _load(character: str) -> list[str]:
            return OCR.single_to_display(character, foreground, background).splitlines()

        return "\n".join((background * spacing).join(line) for line in zip(*map(_load, string)))

    @staticmethod
    def string_from_display(display: str, foreground: str, background: str, spacing: int = 1) -> str:
        """Performs "OCR" to convert a full multi-character display value into individual characters

        .. code-block::
            .##. ###.
            #..# #..#
            #..# ###.
            #### #..#     -> "AB"
            #..# #..#
            #..# ###.

        Args:
            display (str): full string of characters
            foreground (str): pixel style to use for the foreground mark
            background (str): pixel style to use for the background mark
            spacing (int, optional): columns of background pixels between characters. Defaults to 1.

        Returns:
            str: the display output
        """

        def _split(line: str) -> t.Iterator[str]:
            index = 0
            while index < len(line):
                yield line[index : index + OCR._width]
                index += OCR._width + spacing

        return "".join(
            OCR.single_from_display("\n".join(line), foreground, background)
            for line in zip(*map(_split, display.splitlines()))
        )


class Display:
    """A rudimentary display pixel-based display."""

    _screen: list[list[str]] = []

    def __init__(self, height: int, width: int, background: str = ".", foreground: str = "#") -> None:
        self.height = height
        self.width = width

        self.background = background
        self.foreground = foreground

        self.clear()

    def _set(self, x: int, y: int, character: str) -> None:
        self._screen[y][x] = character

    def clear(self) -> None:
        """Delete all the pixels set on the screen by resetting them to the value of ``self.background``"""
        self._screen = [[self.background for _ in range(self.width)] for _ in range(self.height)]

    def draw(self, x: int, y: int, character: t.Optional[str] = None) -> None:
        """Fill in a pixel at the coordinates supplied.

        Args:
            x (int): x pixel coordinate (i.e., column)
            y (int): y pixel coordinate (i.e., row)
            character (t.Optional[str], optional): If supplied, a custom value to fill in the pixel. If none, use
                ``self.foreground``. Defaults to None.
        """
        if character is not None:
            use_character = character

        else:
            use_character = self.foreground

        self._set(x, y, use_character)

    def erase(self, x: int, y: int) -> None:
        """Erase a single pixel by resetting its value to that of ``self.background``

        Args:
            x (int): x pixel coordinate (i.e., column)
            y (int): y pixel coordinate (i.e., row)
        """
        self._set(x, y, self.background)

    def show(self) -> str:
        """Create a string of the current display settings

        Returns:
            str: the display output
        """
        return "\n".join("".join(row) for row in self._screen)

    def characters(self, spacing: int = 1) -> str:
        """Match each of the characters on the display to a set of known possible values from the :py:class:`OCR`

        Args:
            spacing (int, optional): Number of ``self.background`` pixels between each character. Defaults to 1.

        Returns:
            str: string characters found on the display
        """
        return OCR.string_from_display(self.show(), "#", ".", spacing)
