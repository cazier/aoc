import functools


@functools.cache
def gcd(a: int, b: int) -> int:
    if b == 0:
        return a

    return gcd(b, a % b)


@functools.cache
def gcd_ex(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0

    div, x_, y_ = gcd_ex(b, a % b)

    x = y_
    y = x_ - (a // b) * y_

    return div, x, y
