import functools
import re
import sys
import typing


def ints(s) -> list[int]:
    matches = re.findall(r"\d+", s)
    return [int(m) for m in matches]


count = 0


def output():
    print("output!")
    global count
    count += 1


@functools.cache
def process(s: str, groups: tuple, output: typing.Callable, id, head):
    # print(id, head + " " + s, groups)
    if s == "":
        if len(groups) > 0:
            return
        else:
            # global count
            # count += 1
            output()
            return
    x, tail = s[0], s[1:]

    if x == ".":
        process(tail, groups, output, id + 1, head + x)
    elif x == "?":
        process("#" + tail, groups, output, id + 1, head)
        process("." + tail, groups, output, id + 2, head)
    elif x == "#":
        if len(groups) == 0:
            return
        n = groups[0]
        xs, rest = s[:n], s[n:]
        # if xs == "#" * n:
        if all(x != "." for x in xs):
            # print("potential match:", xs, n)
            if len(rest) == 0:
                # print("match")
                return process(rest, groups[1:], output, id + 1, head + xs)
            elif rest[0] == "#":
                return
            elif rest[0] == "?":
                rest = "." + rest[1:]
                # print("match")
                return process(rest, groups[1:], output, id + 1, head + xs)
            elif rest[0] == ".":
                # print("match")
                return process(rest, groups[1:], output, id + 1, head + xs)
        else:
            # if len(groups) > 0:
            #     process(tail, [groups[0] - 1] + groups[1:], output, id + 1, head + x)
            # else:
            return
            # process(tail, groups, output, id + 1, head + x)

        #     if len(s) > n:
        #         if s[n] == "#":
        #             return
        #         if s[n] == "?":
        #             process("." + s[n + 1 :], groups[1:], output, id+1)
        #         else:


lines = sys.stdin.read().splitlines()


class Counter:
    def __init__(self) -> None:
        self.count = 0

    def add_one(self):
        self.count += 1


counts = []

for l in lines:
    pattern = l.split()[0]
    groups = ints(l)

    c = Counter()

    def callback():
        # print("output!")
        # print()
        c.add_one()

    process(pattern, tuple(groups), callback, 0, "")

    counts.append(c.count)


print(counts[:20])
print(sum(counts))
