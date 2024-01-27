import re
import sys
from typing import NamedTuple

import numpy as np

line = sys.stdin.readline()


def ints(s) -> list[int]:
    matches = re.findall(r"\d+", s)
    return [int(m) for m in matches]


seeds = ints(line)

pars = sys.stdin.read().split("\n\n")
pars = [p.strip() for p in pars]


def make_f(xs: list[list[int, int, int]]):
    def f(n: int) -> int:
        for x in xs:
            if n in range(x[1], x[1] + x[2]):
                return x[0] + (n - x[1])
        return n

    return f


funcs = []
func_args = []


for p in pars:
    lines = p.splitlines()
    args = [ints(s) for s in lines[1:]]
    f = make_f(args)
    func_args.append(args)
    funcs.append(f)

locations = []
for s in seeds:
    for f in funcs:
        s = f(s)
    locations.append(s)

print(min(locations))


# 2
# Mathematically this is a composition of permutations of N.
# Having to deal with large ranges of numbers makes the whole thing more
# intricate, but the concept remains simple at its core.


class Interval(NamedTuple):
    """An interval of N, equivalent to [start, start+length)."""

    start: int
    length: int


class IntervalPermutation:
    """A maping from N to N that permutes ranges of integers."""

    def __init__(self, args: list[tuple[int, int, int]]):
        args = sorted(args, key=lambda x: x[1])
        self.starts = []
        self.ends = []
        self.image = []
        for a in args:
            self.image.append(a[0])
            self.starts.append(a[1])
            self.ends.append(a[1] + a[2])

    def sanitize(self, inter: Interval):
        """Sanitize the interval into a list of sane ones.

        A sane interval is either fully included in an encoding interval, or
        outside of any of them (partial overlap is not sane). Sane intervals are
        readily encodable.
        """
        nums = []
        for s, e in zip(self.starts, self.ends):
            nums.append(s)
            nums.append(e)

        a, b = inter.start, inter.start + inter.length
        nums = [n for n in nums if a <= n and n < b]
        _, idxes = np.unique(nums, return_index=True)
        nums = [nums[i] for i in sorted(idxes)]

        nums = [x for x in nums for _ in range(2)]
        nums.insert(0, a)
        nums.append(b)

        inters = []
        for x, y in zip(nums[::2], nums[1::2]):
            if x == y:
                continue
            inters.append(Interval(x, y - x))
        return inters

    def imageof_sanitized(self, inter: Interval) -> Interval:
        """Encode a sane interval.

        If outside of any encoding intervals, it's id. Otherwise, it totally
        included in one of them, so we use this encoding interval.
        """
        a, k = inter.start, inter.length

        for i in range(len(self.starts)):
            s = self.starts[i]
            e = self.ends[i]
            if s <= a and a < e:
                return Interval(self.image[i] + a - s, k)
        return inter


vals = [Interval(start=s, length=k) for s, k in zip(seeds[::2], seeds[1::2])]

for args in func_args:
    mixer = IntervalPermutation(args)
    vals = sum([mixer.sanitize(v) for v in vals], [])  # split the interval in sane ones
    vals = [mixer.imageof_sanitized(v) for v in vals]  # process them

ret = min(vals, key=lambda x: x[0]).start
print(ret)
