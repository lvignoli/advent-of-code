import functools
import re
import sys


def ints(s) -> list[int]:
    matches = re.findall(r"\d+", s)
    return [int(m) for m in matches]


@functools.cache  # memoization
def count_arrangements(pattern, rules) -> int:
    """I had to look for how to properly handle this."""
    if not rules:
        return "#" not in pattern
    if pattern == "":
        return not rules

    result = 0

    if pattern[0] in ".?":
        result += count_arrangements(pattern[1:], rules)
    if pattern[0] in "#?":
        head_match_first_rule = (len(pattern) == rules[0] and "." not in pattern) or (
            len(pattern) > rules[0]
            and "." not in pattern[: rules[0]]
            and pattern[rules[0]] != "#"
        )
        if head_match_first_rule:
            result += count_arrangements(pattern[rules[0] + 1 :], rules[1:])

    return result


lines = sys.stdin.read().splitlines()

counts = []
for l in lines:
    pattern = l.split()[0]
    rules = tuple(ints(l))

    counts.append(count_arrangements(pattern, rules))

print(sum(counts))

# 2

counts = []
for l in lines:
    pattern = l.split()[0]
    rules = tuple(ints(l))

    pattern = "?".join([pattern] * 5)
    rules = rules * 5

    counts.append(count_arrangements(pattern, rules))
print(sum(counts))
