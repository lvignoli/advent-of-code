from __future__ import annotations

import sys
from typing import NamedTuple

type Coord = tuple[int, int]


class Coord(NamedTuple):
    i: int
    j: int


def fromto(c: Coord, tile: str) -> tuple[Coord, Coord]:
    match tile:
        case "F":
            return (Coord(c.i + 1, c.j), Coord(c.i, c.j + 1))
        case "L":
            return (Coord(c.i - 1, c.j), Coord(c.i, c.j + 1))
        case "7":
            return (Coord(c.i + 1, c.j), Coord(c.i, c.j - 1))
        case "J":
            return (Coord(c.i - 1, c.j), Coord(c.i, c.j - 1))
        case "|":
            return (Coord(c.i - 1, c.j), Coord(c.i + 1, c.j))
        case "-":
            return (Coord(c.i, c.j - 1), Coord(c.i, c.j + 1))
        case _:
            raise Exception("unreachable")


lines = sys.stdin.readlines()
board = [[x for x in l.strip()] for l in lines]


# Find start.
def find_start(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == "S":
                return Coord(i, j)


s = find_start(board)

# Find beginning of pipe.
for i, j in [
    Coord(s.i, s.j + 1),
    Coord(s.i, s.j - 1),
    Coord(s.i - 1, s.j),
    Coord(s.i + 1, s.j),
]:
    n = Coord(i, j)
    if s in fromto(n, board[i][j]):
        break
loop = [s, n]

# Unwind pipe loop.
while True:
    c = loop[-1]
    tiles = fromto(c, board[c.i][c.j])
    n = [t for t in tiles if t not in loop]
    if len(n) == 0:
        break
    loop.append(n[0])

dist = [min(i, len(loop) - i) for i in range(len(loop))]

max_index = dist.index(max(dist))
print(max_index)


# 2
count = 0

filled_board = [[" "] * len(board[0]) for i in range(len(board))]

for i in range(len(board)):
    is_in = False
    for j in range(len(board[0])):
        if Coord(i, j) in loop:
            filled_board[i][j] = board[i][j]
            continue

        # An horizontal ray cross the pipe everytime char is |, 7 or F.
        # Equivalently, replacing 7, F by L, J should amount to the same
        # results, but it does not which is very weird.
        pipe_crossings = [
            board[i][k] in ["|", "7", "F"] and Coord(i, k) in loop for k in range(j)
        ]
        is_in = sum(pipe_crossings) % 2 == 1
        if is_in:
            count += 1
            filled_board[i][j] = "I"

print(count)

# print()
# for l in filled_board:
#     print("".join(l))
