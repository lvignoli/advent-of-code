import re
import sys
from itertools import combinations
from typing import NamedTuple


def ints(s) -> list[int]:
    matches = re.findall(r"\d+", s)
    return [int(m) for m in matches]


class Point(NamedTuple):
    i: int
    j: int


def hamming(p: Point, q: Point) -> int:
    return abs(q.i - p.i) + abs(q.j - p.j)


def hamming_with_expansion(
    p: Point, q: Point, expanded_rows, expanded_cols, factor: int
) -> int:
    i_lim = sorted((p.i, q.i))
    i_dist = sum(factor if i in expanded_rows else 1 for i in range(i_lim[0], i_lim[1]))
    j_lim = sorted((p.j, q.j))
    j_dist = sum(factor if j in expanded_cols else 1 for j in range(j_lim[0], j_lim[1]))

    return i_dist + j_dist


lines = sys.stdin.readlines()
board = [list(l.strip()) for l in lines]
h, w = len(board), len(board[0])

# Compute the expanded rows and columns location.
i_marks, j_marks = [], []

for i in range(h):
    if board[i] == ["."] * w:
        i_marks.append(i)

for j in range(w):
    col = [board[i][j] for i in range(h)]
    if col == ["."] * h:
        j_marks.append(j)

galaxies = []

for i in range(len(board)):
    for j in range(len(board[0])):
        if board[i][j] == "#":
            galaxies.append(Point(i, j))

# 1
pairs = combinations(galaxies, 2)
distances = [hamming_with_expansion(p, q, i_marks, j_marks, factor=2) for p, q in pairs]
print(sum(distances))

# 2
pairs = combinations(galaxies, 2)
distances = [
    hamming_with_expansion(p, q, i_marks, j_marks, factor=1_000_000) for p, q in pairs
]
print(sum(distances))
