import re
import sys
from typing import NamedTuple


numbers = "0123456789"
dot = "."


lines = sys.stdin.readlines()
board = []
for l in lines:
    board.append(l.strip())


class IntSpan(NamedTuple):
    number: int
    line: int
    start: int
    end: int


ints: list[IntSpan] = []

for i in range(len(board)):
    for x in re.finditer(r"\d+", board[i]):
        number = int(x.group(0))
        line = i
        start, end = x.span()
        ints.append(IntSpan(number, line, start, end))


def neighbors(line, start, end):
    return (
        [(line, start - 1), (line, end)]
        + list(zip([line - 1] * (end - start + 2), range(start - 1, end + 2)))
        + list(zip([line + 1] * (end - start + 2), range(start - 1, end + 2)))
    )


# 1


part_numbers = []

for n in ints:
    idx = neighbors(n.line, n.start, n.end)
    chars = []
    for a, b in idx:
        try:
            chars.append(board[a][b])
        except IndexError:
            pass
    if set(chars).difference(set(numbers + dot)):
        # There is a symbol in the neighborhood.
        part_numbers.append(n.number)

print(sum([int(n) for n in part_numbers]))


# 2


gear_ratio_sum = 0

for i in range(len(board)):
    for j, c in enumerate(board[i]):
        if c == "*":
            idx = neighbors(i, j, j + 1)
            parts = []
            for n in ints:
                number_span = zip([n.line] * (end - start), range(n.start, n.end))
                intersect = set(number_span) & set(idx)
                if intersect:
                    parts.append(n.number)

            if len(parts) == 2:
                gear_ratio_sum += parts[0] * parts[1]

print(gear_ratio_sum)
