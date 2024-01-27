from __future__ import annotations

import collections
import sys
import typing

import numpy as np

T = typing.TypeVar("T")

lines = sys.stdin.read().splitlines()
board = [list(l) for l in lines]
h, w = len(board), len(board[0])

DELTA_TO_UDLR = {
    (-1, 0): "U",
    (1, 0): "D",
    (0, -1): "L",
    (0, 1): "R",
}


def bfs(
    from_node: T,
    expand: typing.Callable[[T], typing.Iterable[T]],
):
    frontier: collections.deque[T] = collections.deque()
    frontier.append(from_node)
    reached: dict[T, bool] = {from_node: True}

    # steps = 0

    while frontier:
        current = frontier.popleft()
        for next in expand(current):
            if next not in reached:
                frontier.append(next)
                reached[next] = True

    return reached


type Point = tuple[int, int]
type PointStep = tuple[Point, int]


def expand(ps: PointStep) -> list[PointStep]:
    p, s = ps
    pointsteps = []
    for delta in DELTA_TO_UDLR:
        q = p[0] + delta[0], p[1] + delta[1]
        if s >= MAX_STEPS:
            continue
        if q[0] not in range(0, h) or q[1] not in range(0, w):
            continue
        if board[q[0]][q[1]] != "#":
            pointsteps.append((q, s + 1))
    return pointsteps


# Start node
start: Point | None = None
for i in range(h):
    for j in range(w):
        if board[i][j] == "S":
            start = i, j
assert start is not None


# for k in range(max_steps):
#     reached_after_k = [p for p, s in reached if s == k]

#     print()
#     for i in range(h):
#         l = []
#         for j in range(w):
#             if (i, j) in reached_after_k:
#                 l.append("O")
#             else:
#                 l.append(board[i][j])
#         print("".join(l))


MAX_STEPS = 64
reached = bfs((start, 0), expand)
reached_after_max_steps = [p for p, s in reached if s == MAX_STEPS]
print(len(reached_after_max_steps))


# type PointStepWinding = tuple[Point, int, int]
# """Add a winding number"""


def expand_toroidal(ps: PointStep) -> list[PointStep]:
    p, s = ps
    pointsteps = []
    for delta in DELTA_TO_UDLR:
        q = (p[0] + delta[0]), (p[1] + delta[1])
        if s >= MAX_STEPS:
            continue
        if board[q[0] % h][q[1] % w] != "#":
            pointsteps.append((q, s + 1))
    return pointsteps


xs = [65, 65 + 131, 65 + 2 * 131]
# xs = [10, 50, 100, 500]
ys = []
for x in xs:
    MAX_STEPS = x
    reached = bfs((start, 0), expand_toroidal)
    reached_after_max_steps = [p for p, s in reached if s == MAX_STEPS]
    y = len(reached_after_max_steps)
    print(x, y)
    ys.append(y)


p = np.polynomial.polynomial.polyfit([0, 1, 2], ys, 2).astype(np.int64)
print(p)
print(int(p[2]) * 202300**2 + int(p[1]) * 202300 + int(p[0]))

# 604598293144065   too high
# 604551390668629   not right
