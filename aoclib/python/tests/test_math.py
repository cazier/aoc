import pytest
from aoclib.math import gcd, gcd_ex


@pytest.mark.parametrize(
    ("a", "b", "answer"),
    [
        (120, 240, 120),
        (240, 46, 2),
        (180, 160, 20),
        (11, 7, 1),
    ],
)
def test_gcd(a: int, b: int, answer: int) -> None:
    assert gcd(a, b) == answer


@pytest.mark.parametrize(
    ("a", "b"),
    [
        (120, 240),
        (240, 46),
        (180, 160),
        (11, 7),
    ],
)
def test_gcd_ex(a: int, b: int) -> None:
    _, x, y = gcd_ex(a, b)
    assert (a * x) + (b * y) == gcd(a, b)
