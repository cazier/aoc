from ward import test, raises

from .display import OCR, Display


@test("display: create")  # type: ignore
def _() -> None:
    assert Display(5, 5).show() == ".....\n.....\n.....\n.....\n....."
    assert Display(2, 3).show() == "...\n..."
    assert Display(5, 5, background=" ").show() == "     \n     \n     \n     \n     "


@test("display: draw/erase")  # type: ignore
def _() -> None:
    display = Display(5, 5)
    display.draw(2, 2)

    assert display.show() == ".....\n.....\n..#..\n.....\n....."

    display = Display(5, 5, foreground="*")
    for column in range(5):
        display.draw(0, column)

    assert display.show() == "*....\n*....\n*....\n*....\n*...."

    display.erase(0, 3)
    assert display.show() == "*....\n*....\n*....\n.....\n*...."

    display = Display(5, 5, background="*", foreground="-")
    for row in range(5):
        display.draw(row, 4, character="+")

    assert display.show() == "*****\n*****\n*****\n*****\n+++++"


@test("display: clear")  # type: ignore
def _() -> None:
    display = Display(5, 5)
    display.draw(2, 2)

    assert display.show() == ".....\n.....\n..#..\n.....\n....."

    display.clear()
    assert Display(5, 5).show() == ".....\n.....\n.....\n.....\n....."


@test("display: ocr")  # type: ignore
def _() -> None:
    display = Display(6, 4)

    for row in range(6):
        display.draw(0, row)

    for column in range(4):
        display.draw(column, 5)

    assert display.characters() == "L"


@test("ocr: single conversion")  # type: ignore
def _() -> None:
    assert OCR.single_to_display("A", "#", ".") == ".##.\n#..#\n#..#\n####\n#..#\n#..#"
    assert OCR.single_from_display(".##.\n#..#\n#..#\n#..#\n#..#\n.##.", "#", ".") == "O"

    with raises(NotImplementedError) as exception:
        _ = OCR.single_to_display("M", "#", ".")
    assert "does not exist yet" in str(exception.raised)

    with raises(NotImplementedError) as exception:
        _ = OCR.single_from_display("M", "#", ".")
    assert "does not exist yet" in str(exception.raised)


@test("ocr: string conversion")  # type: ignore
def _() -> None:
    abc = ".##..###...##.\n#..#.#..#.#..#\n#..#.###..#...\n####.#..#.#...\n#..#.#..#.#..#\n#..#.###...##."
    efg = "####..####...##.\n#.....#.....#..#\n###...###...#...\n#.....#.....#.##\n#.....#.....#..#\n####..#......###"

    assert OCR.string_to_display("ABC", "#", ".") == abc
    assert OCR.string_to_display("EFG", "#", ".", 2) == efg

    assert OCR.string_from_display(abc, "#", ".") == "ABC"
    assert OCR.string_from_display(efg, "#", ".", 2) == "EFG"
