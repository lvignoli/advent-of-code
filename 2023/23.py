import collections
import math

import sys
import typing

T = typing.TypeVar("T")

DELTA_TO_UDLR = {
    (-1, 0): "U",
    (1, 0): "D",
    (0, -1): "L",
    (0, 1): "R",
}

AIR = "."
WALL = "#"
SLOPES = {"v", ">", "<"}
AIR_OR_SLOPES = SLOPES.union(SLOPES, {AIR})
# AIR_OR_DR_SLOPES = {".", ">", "v"}

board: list[list[str]] = [list(l) for l in sys.stdin.read().splitlines()]

h, w = len(board), len(board[0])

air_or_slopes = [
    (i, j) for i in range(h) for j in range(w) if board[i][j] in AIR_OR_SLOPES
]
neighbors = {
    (i, j): [
        (i + d[0], j + d[1])
        for d in DELTA_TO_UDLR
        if (i + d[0] in range(h) and j + d[1] in range(w))
        and board[i + d[0]][j + d[1]] in AIR_OR_SLOPES
    ]
    for i, j in air_or_slopes
}


def bfs(
    start: T,
    goals: typing.Iterable[T],
    expand: typing.Callable[[T], typing.Iterable[T]],
    cost: typing.Callable[[T, T], float],
):
    ...
    frontier = collections.deque([])
    frontier.append(start)
    came_from = {}
    came_from[start] = None
    distance_so_far = {}
    distance_so_far[start] = 0
    # seen = set()

    found = []

    while frontier:
        current = frontier.popleft()

        # if current in seen:
        #     continue

        if current in goals and current != start:
            # return current, distance_so_far[current]
            found.append((current, distance_so_far[current]))
            continue

        # seen.add(current)

        for n in expand(current):
            new_distance = distance_so_far[current] + cost(current, n)
            if n not in distance_so_far or new_distance < distance_so_far[n]:
                if new_distance == math.inf:
                    continue
                distance_so_far[n] = new_distance
                frontier.append(n)
                came_from[n] = current

    return found


def expand(p: tuple[int, int]) -> list[tuple[int, int]]:
    return neighbors[p]


def cost(p: tuple[int, int], q: tuple[int, int]) -> float:
    delta = q[0] - p[0], q[1] - p[1]
    assert delta in DELTA_TO_UDLR
    match (DELTA_TO_UDLR[delta], board[q[0]][q[1]]):
        case "U", "v":
            return math.inf
        case "L", ">":
            return math.inf
        case _, _:
            return 1


start = (0, board[0].index(AIR))
end = (len(board) - 1, board[-1].index(AIR))
intersections = [p for p, ns in neighbors.items() if len(ns) > 2]


# Collect the directed edges between intersections.
edge = {}
for p in {start, *intersections}:
    edge[p] = bfs(p, intersections + [end], expand, cost)

# Enumerate the path costs.
costs = []


def walk_from_to(start, end, x):
    if start == end:
        costs.append(x)
        return
    for n, y in edge[start]:
        walk_from_to(n, end, x + y)


walk_from_to(start, end, 0)

print(max(costs))


# 2
edge = {}
for p in {start, *intersections}:
    edge[p] = bfs(p, intersections + [end], expand, lambda p, q: 1)


def walk_from_to_with_seen(start, end, x, seen):
    # print(start, seen)
    if start in seen:
        return
    if start == end:
        costs.append(x)
        return
    for n, y in edge[start]:
        walk_from_to_with_seen(n, end, x + y, seen.union([start]))


costs = []
walk_from_to_with_seen(start, end, 0, set())
print(max(costs))
