import sys
import re
from typing import NamedTuple


def hash(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h


input = sys.stdin.read()
input = input.replace("\n", "")
steps = input.split(",")


ret = sum(hash(s) for s in steps)
print(ret)


class Lens(NamedTuple):
    label: str
    focal: int

    def __repr__(self) -> str:
        return f"[{self.label} {self.focal}]"


class HASHMAP:
    def __init__(self) -> None:
        self.box = [[] for _ in range(256)]

    def insert_in(self, i: int, l: Lens):
        existing_labels = [k.label for k in self.box[i]]

        if l.label in existing_labels:
            idx = existing_labels.index(l.label)
            self.box[i][idx] = l
            return

        self.box[i].append(l)

    def remove_from(self, i: int, label: str):
        existing_labels = [k.label for k in self.box[i]]

        if label in existing_labels:
            idx = existing_labels.index(label)
            self.box[i] = self.box[i][:idx] + self.box[i][idx + 1 :]

    def handle(self, step: str):
        m = re.match(r"^(\w+)([=-])(\d?)$", step)
        if m is None:
            raise ValueError

        label = m.group(1)
        op = m.group(2)

        h = hash(label)
        if op == "-":
            self.remove_from(h, label)
        elif op == "=":
            focal = int(m.group(3))
            self.insert_in(h, Lens(label, focal))

    def focusing_power(self):
        total = 0
        for i, b in enumerate(self.box):
            for j, l in enumerate(b):
                t = (i + 1) * (j + 1) * l.focal
                total += t
        return total

    def __repr__(self) -> str:
        ret = ""
        for i, b in enumerate(self.box):
            if len(b) == 0:
                continue
            ret += f"Box {i}: "
            lenses = " ".join(str(l) for l in b)
            ret += lenses + "\n"
        return ret


hm = HASHMAP()

for s in steps:
    hm.handle(s)
    # print(f"After {s}")
    # print(hm)

print(hm.focusing_power())
