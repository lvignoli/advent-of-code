import sys


import numpy as np

DELTA_TO_UDLR = {
    (-1, 0): "U",
    (0, 1): "R",
    (1, 0): "D",
    (0, -1): "L",
}


def shoelace(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def picks_area(corners, perimeter) -> int:
    """Compute the area of a polygon with vertices on integer coordinates using Pick's theorem."""
    x = [v[0] for v in corners]
    y = [v[1] for v in corners]
    return int(shoelace(x, y) + perimeter / 2 + 1)


def dig(instructions: list[tuple[str, int]]) -> tuple[list[tuple[int, int]], int]:
    cursor = (0, 0)
    corners = []
    perimeter = 0
    for direction, amount in instructions:
        delta = [k for k, v in DELTA_TO_UDLR.items() if v == direction][0]

        cursor = cursor[0] + amount * delta[0], cursor[1] + amount * delta[1]
        perimeter += amount
        corners.append(cursor)
    return corners, perimeter


lines = [l.strip() for l in sys.stdin.readlines()]

# 1
instructions = []

for l in lines:
    fields = l.split()
    direction = fields[0]
    amount = int(fields[1])
    instructions.append((direction, amount))

corners, perimeter = dig(instructions)

print(picks_area(corners, perimeter))

# 2
NUMBER_TO_URDL = {
    0: "R",
    1: "D",
    2: "L",
    3: "U",
}

instructions = []

for l in lines:
    fields = l.split()
    hex_part = fields[2].removeprefix("(#").removesuffix(")")

    amount = int(hex_part[:5], 16)

    direction_number = int(hex_part[5])
    assert direction_number in NUMBER_TO_URDL
    direction = NUMBER_TO_URDL[direction_number]

    instructions.append((direction, amount))

corners, perimeter = dig(instructions)

print(picks_area(corners, perimeter))
