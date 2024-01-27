import math
import re
import sys

lines = sys.stdin.readlines()

instructions = [0 if c == "L" else 1 for c in lines[0].strip()]

nodes = {}

for l in lines[2:]:
    m = re.findall(r"\w{3}", l)
    nodes[m[0]] = (m[1], m[2])

# 1
cursor = "AAA"
i = 0
while cursor != "ZZZ":
    cursor = nodes[cursor][instructions[i % len(instructions)]]
    i += 1

print(i)

# 2

# Brute force exploration is taking "significantly more steps".
# Assumption: paths **A -> **Z -> **Z -> ... are cyclic, at least in the number of steps.
# Verified on the first iterations.
# Compute cycles from the starting nodes to a **Z, then take the LCM.

cursors = [n for n in nodes if n[2] == "A"]
cycles = []

for i in range(len(cursors)):
    c = cursors[i]
    i = 0
    while c[2] != "Z":
        c = nodes[c][instructions[i % len(instructions)]]
        i += 1
    cycles.append(i)

print(math.lcm(*cycles))
