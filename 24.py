import re
import sys

import math
import numpy as np


def ints(s: str) -> list[int]:
    return [int(c) for c in re.findall(r"-?\d+", s)]


input_lines = sys.stdin.read().splitlines()

points = []
vecs = []
lines = []

for l in input_lines:
    ns = ints(l)
    p, v = ns[:3], ns[3:]
    a = v[1]
    b = -v[0]
    c = -p[0] * v[1] + p[1] * v[0]

    points.append(p)
    vecs.append(v)
    lines.append((a, b, c))
    print(f"{a} x + {b} y + {c} = 0")


def intersect(line1, line2):
    a, b, c = line1
    d, e, f = line2

    den = a * e - b * d
    if math.isclose(den, 0.0):
        return None

    x = float(b * f - c * e) / float(den)
    y = float(a * f - c * d) / float(-den)
    return x, y


def is_forward(p, line_vec, orig_point):
    v = p[0] - orig_point[0], p[1] - orig_point[1]

    return v[0] * line_vec[0] > 0 and v[1] * line_vec[1] > 0


def dist(p, q):
    return math.sqrt((q[1] - p[1]) ** 2 + (q[0] - p[0]) ** 2)


# LB, UB = 7, 27
LB, UB = 200000000000000, 400000000000000


def compute_intersections(lines, vecs, points):
    count = 0
    inters = []

    for i in range(len(lines)):
        for j in range(i, len(lines)):
            p1, p2 = points[i], points[j]
            v1, v2 = vecs[i], vecs[j]
            l1, l2 = lines[i], lines[j]
            inter = intersect(l1, l2)
            if inter:
                in_test_area = (
                    LB <= inter[0]
                    and inter[0] <= UB
                    and LB <= inter[1]
                    and inter[1] <= UB
                )
                in_future = is_forward(inter, v1, p1) and is_forward(inter, v2, p2)
                if in_test_area and in_future:
                    count += 1
                    inters.append((inter, (i, j)))
                # print(inter)
                # print(in_test_area)
                # print(in_future)

    return inters


inters = compute_intersections(lines, vecs, points)


for inter, (i, j) in inters:
    print(inter)
    print(i, j)


# Let's brute force for small velocity inputs
r = range(-200, 200)

for vx in r:
    for vy in r:
        # Change reference frame to the one of the rock.
        new_vecs = [np.array(v[:1]) - np.array([vx, vy]) for v in vecs]
        inters = []
        for i in range(1, len(lines)):
            p1, p2 = points[0], points[i]
            v1, v2 = new_vecs[0], new_vecs[i]
            l1, l2 = lines[0], lines[i]
            inter = intersect(l1, l2)
            if inter:
                in_test_area = (
                    LB <= inter[0]
                    and inter[0] <= UB
                    and LB <= inter[1]
                    and inter[1] <= UB
                )
                in_future = is_forward(inter, v1, p1) and is_forward(inter, v2, p2)
                if in_test_area and in_future:
                    inters.append(inter)

        if len(inters) > 2 and inters[0] == inters[1] == inters[2]:
            print("PASS")

        # p = inters[0]
        # if all(q == p for q in inters[1:]):
        #     print(p)


def aligned(ps):
    q = ps[0]
    vecs = [(p[0] - q[0], p[1] - q[1], p[2] - q[2]) for p in ps[1:]]

    return all([np.allclose(np.cross(vecs[0], v), np.zeros(3)) for v in vecs[1:]])


def move(p, v, t):
    return (
        p[0] + t * v[0],
        p[1] + t * v[1],
        p[2] + t * v[2],
    )


print(aligned(inters))

# for t in range(100000):
#     new_points = [move(p, v, t) for p, v in zip(points, vecs)]

#     if aligned(new_points):
#         print(t)
# print(aligned([(0, 1, 1), (0, 2, 2), (0, 10, 10)]))
