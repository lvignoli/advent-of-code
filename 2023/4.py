import sys
import re

lines = sys.stdin.readlines()


def ints(s) -> list[int]:
    matches = re.findall(r"\d+", s)
    return [int(m) for m in matches]


counts = []


for l in lines:
    left, right = l.split(":")[1].split("|")
    winning, mine = ints(left), ints(right)
    intersection = set(winning) & set(mine)
    counts.append(len(intersection))

score = (2 ** (c - 1) if c > 0 else 0 for c in counts)
print(sum(score))


copies = [1] * len(counts)

for i, c in enumerate(counts):
    for j in range(i + 1, i + 1 + c):
        copies[j] += 1 * copies[i]

print(sum(copies))
