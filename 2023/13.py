import sys


pars = sys.stdin.read().split("\n\n")
pars = [p.strip() for p in pars]


def horizontal_symmetry(board, i) -> bool:
    a, b = i, i + 1
    while a >= 0 and b < len(board):
        if board[a] != board[b]:
            return False
        a -= 1
        b += 1
    return True


def vertical_symmetry(board, j) -> bool:
    a, b = j, j + 1
    while a >= 0 and b < len(board[0]):
        cola = [board[i][a] for i in range(len(board))]
        colb = [board[i][b] for i in range(len(board))]
        if cola != colb:
            return False
        a -= 1
        b += 1
    return True


ret = 0

for p in pars:
    board = [list(l) for l in p.splitlines()]

    for i in range(len(board) - 1):
        if horizontal_symmetry(board, i):
            ret += (i + 1) * 100
            continue

    for j in range(len(board[0]) - 1):
        if vertical_symmetry(board, j):
            ret += j + 1
            continue


print(ret)

# 2


def horizontal_symmetry_distance(board, i) -> int:
    d = 0
    a, b = i, i + 1
    while a >= 0 and b < len(board):
        d += sum([1 for j in range(len(board[0])) if board[a][j] != board[b][j]])
        a -= 1
        b += 1
    return d


def vertical_symmetry_distance(board, j) -> int:
    d = 0
    a, b = j, j + 1
    while a >= 0 and b < len(board[0]):
        d += sum([1 for i in range(len(board)) if board[i][a] != board[i][b]])
        a -= 1
        b += 1
    return d


ret = 0

for p in pars:
    board = [list(l) for l in p.splitlines()]

    for i in range(len(board) - 1):
        d = horizontal_symmetry_distance(board, i)
        if d == 1:
            ret += (i + 1) * 100

    for j in range(len(board[0]) - 1):
        d = vertical_symmetry_distance(board, j)
        if d == 1:
            ret += j + 1

print(ret)


# Refactor to use the distance function only, and use distance 0 and 1.
