import re
import sys
from collections import defaultdict, deque
from copy import deepcopy

import numpy as np


def ints(s) -> list[int]:
    matches = re.findall(r"\d+", s)
    return [int(m) for m in matches]


type Point = tuple[int, int, int]


def parse(s: str) -> list[tuple[int, tuple[Point, Point]]]:
    blocks: list[tuple[int, tuple[Point, Point]]] = []
    for i, l in enumerate(s.splitlines()):
        ns = ints(l)
        p: Point = ns[0], ns[1], ns[2]
        q: Point = ns[3], ns[4], ns[5]
        blocks.append((i, (p, q)))
    return blocks


def compute_xy_span(start: Point, end: Point) -> tuple[list[tuple[int, int]], int, int]:
    z_min = min(start[2], end[2])
    z_max = max(start[2], end[2])
    xs = range(start[0], end[0] + 1)
    ys = range(start[1], end[1] + 1)
    return [(x, y) for x in xs for y in ys], z_min, z_max


blocks = parse(sys.stdin.read())
for b in blocks:
    print(b)

elevation: dict[tuple[int, int], int] = {}

settled_blocks: list[tuple[int, tuple[Point, Point]]] = []

for name, b in sorted(blocks, key=lambda b: b[1][0][2]):
    # Compute the difference in each (x,y) column of the block to the current elevation
    xy_span, z_min, z_max = compute_xy_span(b[0], b[1])

    # difference with ground
    z_diffs = [z_min - elevation.get((p[0], p[1]), 1) for p in xy_span]
    displace_by = min(z_diffs)

    # Bring the block down by this much
    new_start = (b[0][0], b[0][1], b[0][2] - displace_by)
    new_end = (b[1][0], b[1][1], b[1][2] - displace_by)
    settled_blocks.append((name, (new_start, new_end)))

    # Update elevation
    for x, y in xy_span:
        elevation[(x, y)] = z_max - displace_by + 1

# Compute occupation map.
occupation: dict[Point, int] = {}
for name, b in settled_blocks:
    xy_span, z_min, z_max = compute_xy_span(b[0], b[1])

    for x, y in xy_span:
        for z in range(z_min, z_max + 1):
            occupation[(x, y, z)] = name


# Compute support map: map a block to the ones it supports above him.
support_map = defaultdict(list)

for i in range(len(settled_blocks)):
    name, b = settled_blocks[i]
    xy_span, z_min, z_max = compute_xy_span(b[0], b[1])

    for x, y in xy_span:
        loc = occupation.get((x, y, z_max + 1), None)
        if loc is None:
            continue
        support_map[name].append(loc)


# Compute destroyable bricks.
# Destroyable: removing this key from the support map let the values unchanged.
destroyable: list[int] = []
all_supported = set(sum([v for v in support_map.values()], []))

for name, b in settled_blocks:
    if name not in support_map.keys():
        destroyable.append(name)
        continue

    still_supported = set(
        sum([support_map[j] for j in support_map.keys() if j != name], [])
    )

    if all_supported.issubset(still_supported):
        destroyable.append(name)

print(len(destroyable))

# Chain reaction.


fallen_score = {}
for name, _ in settled_blocks:
    smap = deepcopy(support_map)

    fallen = set()
    frontier = deque([name])

    while frontier:
        cur = frontier.popleft()

        # Mark it fallen. If it does not support anything, just continue.
        fallen.add(cur)
        if cur not in smap:
            continue

        # Otherwise, determine what falls.
        above = smap.pop(cur)
        for next in above:
            levitating = True
            for v in smap.values():
                if next in v:
                    levitating = False
            if levitating:
                # Falling, so must be added to the queue.
                frontier.append(next)

    # We want only the other brick: remove the original one.
    fallen.difference_update({name})
    fallen_score[name] = len(fallen)

# for k, v in fallen_score.items():
#     print(k, v)

print(sum(fallen_score.values()))
