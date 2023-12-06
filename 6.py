import sys
import re
import math
from functools import reduce
import operator

l = sys.stdin.readlines()


def ints(s) -> list[int]:
    matches = re.findall(r"\d+", s)
    return [int(m) for m in matches]


time, distance = ints(l[0]), ints(l[1])

counts = []
for t, d in zip(time, distance):
    delta = t**2 - 4 * d
    if delta < 0:
        continue
    x0 = math.floor((t - math.sqrt(delta)) / 2 + 1)
    x1 = math.ceil((t + math.sqrt(delta)) / 2 - 1)

    print(x0, x1)

    counts.append(x1 - x0 + 1)

print(counts)
ret = reduce(operator.mul, counts)
print(ret)

# 2
# Did it by hand. Come on.
