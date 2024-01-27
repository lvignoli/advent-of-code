import sys
from copy import deepcopy


board = [list(l.strip()) for l in sys.stdin.readlines()]

# Cut each column in chunk.
# Put all round rocks at the beginning of the chunk.


def print_board(b):
    for i in range(len(b)):
        print("".join(b[i]))


print_board(board)


def tilt_north(b):
    board = deepcopy(b)
    h, w = len(board), len(board[0])
    for j in range(w):
        col = "".join(board[i][j] for i in range(h))

        chunks = col.split("#")
        for i in range(len(chunks)):
            chunks[i] = sorted(chunks[i], reverse=True)

        # print(chunks)
        col = "#".join("".join(c) for c in chunks)
        # print(col)

        for i in range(h):
            board[i][j] = col[i]
    return board


def tilt_east(b):
    b = rotate_counterclockwise(b)
    b = tilt_north(b)
    b = rotate_clockwise(b)
    return b


def tilt_south(b):
    b = rotate_counterclockwise(rotate_counterclockwise(b))
    b = tilt_north(b)
    b = rotate_clockwise(rotate_clockwise(b))
    return b


def tilt_west(b):
    b = rotate_clockwise(b)
    b = tilt_north(b)
    b = rotate_counterclockwise(b)
    return b


def load_north(board) -> int:
    h, w = len(board), len(board[0])
    tot = 0
    for i, l in enumerate(board):
        load = sum(1 for x in l if x == "O") * (h - i)
        tot += load
    return tot


def rotate_clockwise(board):
    h, w = len(board), len(board[0])
    rows = []
    for j in range(w):
        col = [board[i][j] for i in range(h)]
        rows.append(col[::-1])
    return [r for r in rows]


def rotate_counterclockwise(board):
    return rotate_clockwise(rotate_clockwise(rotate_clockwise(board)))


print()
print(load_north(tilt_north(board)))

# 2


history = []
cycle_length = 0

for i in range(1_000_000_000):
    board = tilt_north(board)
    board = tilt_west(board)
    board = tilt_south(board)
    board = tilt_east(board)

    if board in history:
        end = i
        break
    history.append(board)

start = history.index(board)
history = history[start:end]
cycle_length = end - start

idx = (1_000_000_000 - start) % cycle_length

# The minus 1 is needed here because my initialization is shaky: after 1 cycle the history first element is at index 0… Refactor.
idx -= -1

print(load_north(history[idx]))
