import re
import sys
from typing import Callable, Sequence

type P = dict[str, int]


def score(parts: list[P]) -> int:
    return sum(P["x"] + P["m"] + P["a"] + P["s"] for P in parts)


type W = Callable[[P], str | None]
workflows: dict[str, Sequence[W]] = {}


def build_constraint(cat: str, constraint_type: str, value: int, next_id):
    def f(p: P) -> str | None:
        if constraint_type == "<":
            return next_id if p[cat] < value else None
        elif constraint_type == ">":
            return next_id if p[cat] > value else None
        else:
            raise ValueError

    return f


par1, par2 = sys.stdin.read().split("\n\n")


for l in par1.splitlines():
    if l == "":
        break
    m = re.match(r"(\w+){(.*)}", l)
    assert m is not None

    id = m.group(1)

    instructions_str = m.group(2).split(",")
    print(id, instructions_str)
    instructions = []
    for s in instructions_str:
        if ":" not in s:
            instructions.append(lambda P, s=s: s)
        else:
            cond, next_id = s.split(":")
            cat = cond[0]
            constraint_type = cond[1]
            assert constraint_type in ("<", ">")
            value = int(cond[2:])

            f = build_constraint(cat, constraint_type, value, next_id)
            instructions.append(f)

            # if constraint_type == "<":
            #     instructions.append(lambda P, j=next_id: j if P[cat] < value else None)
            # elif constraint_type == ">":
            #     instructions.append(lambda P, j=next_id: j if P[cat] > value else None)

    workflows[id] = instructions

parts = []

for l in par2.splitlines():
    fields = l.removeprefix("{").removesuffix("}").split(",")
    p: P = {}
    for f in fields:
        a, b = f.split("=")
        p[a] = int(b)
    parts.append(p)

print(parts)
print(workflows)

accepted: list[P] = []


print((workflows["in"])[0]({"x": 0, "m": 0, "a": 0, "s": 0}))
print((workflows["in"])[1]({"x": 0, "m": 0, "a": 0, "s": 0}))


def process(id: str, p: P):
    print()
    print("workflow", id)
    for w in workflows[id]:
        ret = w(p)
        print(f"{ret=}")
        if ret is None:
            continue
        elif isinstance(ret, str):
            if ret == "A":
                print("Accepted")
                accepted.append(p)
                return
            elif ret == "R":
                print("Rejected")
                return
            if ret in workflows:
                process(ret, p)
                return
        # elif isinstance(ret, bool) and ret:
        #     break


for p in parts:
    process("in", p)

for p in accepted:
    print(p)

print(score(accepted))
