import sys
import re
import itertools


def ints(s) -> list[int]:
    matches = re.findall(r"-?\d+", s)
    return [int(m) for m in matches]


lines = sys.stdin.readlines()


def difference(arr: list[int]) -> list[int]:
    pairs = itertools.pairwise(arr)
    return [b - a for a, b in pairs]


values = []
values2 = []

for l in lines:
    arrs = [ints(l)]
    while not all(x == 0 for x in arrs[-1]):
        arrs.append(difference(arrs[-1]))
    values.append(sum(arr[-1] for arr in arrs))

    ret = 0
    for arr in arrs[::-1]:
        ret = arr[0] - ret
    values2.append(ret)


print(sum(values))
print(sum(values2))
