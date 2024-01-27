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


# # Find the accepted leaves.
# leaves = []
# for k, v in workflows.items():
#     if "A" in [ins[0] for ins in v]:
#         leaves.append(k)

T = typing.TypeVar("T")


def bfs(
    from_node: T,
    # is_goal: typing.Callable[[T], bool],
    expand: typing.Callable[[T], typing.Iterable[T]],
):
    frontier: collections.deque[T] = collections.deque()
    frontier.append(from_node)
    reached: dict[T, bool] = {from_node: True}

    # steps = 0
    # goals = []
    while frontier:
        current = frontier.popleft()
        # if is_goal(current):
        #     goals.append(current)
        for next in expand(current):
            if next not in reached:
                frontier.append(next)
                reached[next] = True

    return reached


type Node = tuple[str, tuple[tuple[int, int]]]

XMAS_TO_INDEX = {
    "x": 0,
    "m": 1,
    "a": 2,
    "s": 3,
}


@dataclasses.dataclass(frozen=True)
class Nodem:
    name: str
    x: tuple[int, int]
    m: tuple[int, int]
    a: tuple[int, int]
    s: tuple[int, int]

    def get(self, s: str) -> tuple[int, int]:
        match s:
            case "x":
                return self.x
            case "m":
                return self.m
            case "a":
                return self.a
            case "s":
                return self.s
            case _:
                raise ValueError


def expand(n: Node) -> list[Node]:
    nexts: list[Node] = []

    for w in workflows.get(n[0], []):
        if isinstance(w, str):
            nexts.append((w, n[1]))
            continue

        assert isinstance(w, Wokflow)

        i = XMAS_TO_INDEX[w.feature]
        bounds = n[1][i]

        if w.threshold <= bounds[1]:
            bounds = (w.threshold, bounds[1])
        elif bounds[0] <= w.threshold:
            bounds = (bounds[0], w.threshold)
        if bounds[1] < bounds[0]:
            continue

        new_bounds = list(deepcopy(n[1]))
        new_bounds[i] = bounds

        nexts.append((w.next_id, tuple(new_bounds)))

    # for w in workflows[n.name]:
    #     if isinstance(w, str):
    #         m.name = w
    #         nexts.append(m)
    #         continue

    #     assert isinstance(w, Wokflow)

    #     m = deepcopy(n)

    #     vmin, vmax = m.get(w.feature)
    #     idx = 0 if w.constraint_type == ">" else 1
    #     bounds = None
    #     if idx == 0:
    #         if w.threshold <= vmax:
    #             bounds = (w.threshold, vmax)
    #             nexts.append(m)
    #         else:
    #             continue
    #     elif idx == 1:
    #         if vmin <= w.threshold:
    #             bounds = (vmin, w.threshold)
    #         else:
    #             continue
    #     match w.feature:
    #         case "x":
    #             m = dataclasses.replace(m, x=bounds)
    #         case "m":
    #             m = dataclasses.replace(m, m=bounds)
    #         case "a":
    #             m = dataclasses.replace(m, a=bounds)
    #         case "s":
    #             m = dataclasses.replace(m, s=bounds)
    #         case _:
    #             raise ValueError
    #     nexts.append(m)

    return nexts


for k, v in workflows.items():
    print(k, v)
print(parts)

start: Node = (
    "in",
    (
        (0, 4000),
        (0, 4000),
        (0, 4000),
        (0, 4000),
    ),
)

reached = bfs(start, expand)

for k, v in reached.items():
    print(k, v)

accepted = [x for x in reached if x[0] == "A"]
print()
for a in accepted:
    print(a)


def overlap_1d(a: tuple[int, int], b: tuple[int, int]) -> int:
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))


def overlap(c1: tuple[tuple[int, int]], c2: tuple[tuple[int, int]]) -> int:
    tot = 1
    for a, b in zip(c1, c2):
        tot *= overlap_1d(a, b)
    return tot


def size(c) -> int:
    ret = 1
    for a, b in c:
        ret *= b - a
    return ret


ret = sum(size(x[1]) for x in accepted)
print(ret)

for i in range(len(accepted)):
    for j in range(i, len(accepted)):
        a, b = accepted[i][1], accepted[j][1]
        ret -= overlap(a, b)

print(ret)


5992976237667348
838762478928000
167409079868000

print(overlap_1d((0, 12), (5, 7)))
print(overlap(((0, 12), (0, 3)), ((5, 8), (0, 2))))
