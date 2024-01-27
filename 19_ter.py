import collections
import dataclasses
import re
import sys
import typing
from copy import deepcopy
from typing import Callable, NamedTuple, Sequence


class Wokflow(NamedTuple):
    next_id: str
    feature: str
    threshold: int
    constraint_type: str


par1, par2 = sys.stdin.read().split("\n\n")

workflows = {}
for l in par1.splitlines():
    if l == "":
        break
    m = re.match(r"(\w+){(.*)}", l)
    assert m is not None

    id = m.group(1)
    instructions_str = m.group(2).split(",")
    instructions: list[Wokflow | str] = []

    for s in instructions_str:
        if ":" not in s:
            next_id = s
            instructions.append(next_id)
        else:
            cond, next_id = s.split(":")
            feature = cond[0]
            c_type = cond[1]
            assert c_type in ("<", ">")
            threshold = int(cond[2:])
            instructions.append(Wokflow(next_id, feature, threshold, c_type))

    workflows[id] = instructions

parts = []

for l in par2.splitlines():
    fields = l.removeprefix("{").removesuffix("}").split(",")
    p = {}
    for f in fields:
        a, b = f.split("=")
        p[a] = int(b)
    parts.append(p)


type Node = tuple[str, tuple[tuple[int, int]]]

XMAS_TO_INDEX = {
    "x": 0,
    "m": 1,
    "a": 2,
    "s": 3,
}


def acceptance_range_inner(w0: str) -> list[tuple[int, int]]:
    if w0 == "R":
        return []
    elif w0 == "A":
        return ((1, 4000), (1, 4000), (1, 4000), (1, 4000))

    ret = 0
    for w in workflows[w0]:
        if isinstance(w, str):
            return acceptance_range_inner(w)
        assert isinstance(w, Wokflow)

        gt = w.feature == ">"

        i = XMAS_TO_INDEX[w.feature]

        bounds = acceptance_range_inner(w.next_id)

        if w.threshold <= bounds[i][1]:
            bounds[i] = (w.threshold, bounds[i][1])
        elif bounds[i][0] <= w.threshold:
            bounds[i] = (bounds[i][0], w.threshold)
        if bounds[i][1] < bounds[i][0]:
        
        ret += boun
            
    return ret
    
