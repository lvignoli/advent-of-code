import re
import sys
import itertools


def ints(s) -> list[int]:
    matches = re.findall(r"\d+", s)
    return [int(m) for m in matches]


def construct_regex(group_sizes):
    return r"^\.*" + r"\.+".join(["#{" + str(s) + "}" for s in group_sizes]) + r"\.*$"


lines = sys.stdin.readlines()

total = 0

counts = []

for l in lines:
    left, right = l.strip().split()

    # left = "?".join([left] * 5)
    # right = ",".join([right] * 5)
    # print(left, right)

    pattern = ints(right)

    r = construct_regex(pattern)

    for s in (left, "?" + left, left + "?", "?" + left + "?"):
        idx = [i for i, c in enumerate(s) if c == "?"]
        missing = sum(pattern) - s.count("#")
        plain = s.replace("?", ".")
        count = 0
        for c in itertools.combinations(idx, missing):
            target = "".join(
                [plain[i] if i not in c else "#" for i in range(len(plain))]
            )
            if re.match(r, target) is not None:
                count += 1

        # print(count)

    counts.append(count)

print(counts)
total = sum(counts)
