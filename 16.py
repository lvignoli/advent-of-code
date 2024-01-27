import enum
import sys
import time
from copy import deepcopy
from typing import NamedTuple

board = [list(l.strip()) for l in sys.stdin.readlines()]
h = len(board)
w = len(board[0])


def print_board(b):
    for i in range(len(b)):
        print("".join(b[i]))


class Coord(NamedTuple):
    i: int
    j: int


class Dir(enum.Enum):
    Right = enum.auto()
    Up = enum.auto()
    Left = enum.auto()
    Down = enum.auto()


def reflect(moving_towards: Dir, tile) -> Dir:
    match (moving_towards, tile):
        case Dir.Right, "\\":
            return Dir.Down
        case Dir.Up, "\\":
            return Dir.Left
        case Dir.Left, "\\":
            return Dir.Up
        case Dir.Down, "\\":
            return Dir.Right

        case Dir.Right, "/":
            return Dir.Up
        case Dir.Up, "/":
            return Dir.Right
        case Dir.Left, "/":
            return Dir.Down
        case Dir.Down, "/":
            return Dir.Left

        case _:
            raise ValueError


def propagate(moving_towards: Dir, c: Coord) -> Coord:
    match moving_towards:
        case Dir.Right:
            return Coord(i=c.i, j=c.j + 1)
        case Dir.Up:
            return Coord(i=c.i - 1, j=c.j)
        case Dir.Left:
            return Coord(i=c.i, j=c.j - 1)
        case Dir.Down:
            return Coord(i=c.i + 1, j=c.j)
        case _:
            raise ValueError


def split(moving_towards: Dir, tile: str) -> Dir | tuple[Dir, Dir]:
    match (moving_towards, tile):
        case Dir.Right | Dir.Left, "|":
            return Dir.Up, Dir.Down
        case Dir.Up | Dir.Down as d, "|":
            return d
        case Dir.Right | Dir.Left as d, "-":
            return d
        case Dir.Up | Dir.Down, "-":
            return Dir.Left, Dir.Right
        case _:
            raise ValueError


def out_of_bounds(c: Coord) -> bool:
    return c.i not in range(0, len(board)) or c.j not in range(0, len(board[0]))


# entrypoints
entrypoints = (
    [(Coord(i=i, j=0), Dir.Right) for i in range(h)]
    + [(Coord(i=0, j=j), Dir.Down) for j in range(w)]
    + [(Coord(i=i, j=w - 1), Dir.Left) for i in range(h)]
    + [(Coord(i=h - 1, j=j), Dir.Up) for j in range(w)]
)

energy = []

for c, d in entrypoints:
    energized_board = [["."] * len(board[0]) for _ in range(len(board))]

    # d = Dir.Right
    # c = Coord(i=0, j=0)

    beam_counter = 0

    history: dict[Coord, list[Dir]] = {}

    def beam(number: int, origin: Coord, direction: Dir):
        c = origin
        d = direction

        while True:
            # Check if already visited this path
            if d in history.get(c, []):
                return

            # Add to history
            if history.get(c, None) is None:
                history[c] = [d]
            else:
                history[c].append(d)

            # Print if needed
            # print()
            # print_board(energized_board)
            # time.sleep(0.1)
            # print(number, c, d)

            # Kill if out of bound
            if out_of_bounds(c):
                return

            # Energize the tile
            energized_board[c.i][c.j] = "#"

            tile = board[c.i][c.j]

            if tile == ".":
                c = propagate(d, c)
                continue
            elif tile in ("\\", "/"):
                d = reflect(d, tile)
                c = propagate(d, c)
                continue
            elif tile in ("-", "|"):
                new_d = split(d, tile)
                if isinstance(new_d, Dir):
                    d = new_d
                    c = propagate(d, c)
                    continue
                else:
                    d0 = new_d[0]
                    c0 = propagate(d0, c)

                    beam(number + 1, c0, d0)

                    d1 = new_d[1]
                    c1 = propagate(d1, c)

                    beam(number + 2, c1, d1)

    beam(0, c, d)

    # print_board(energized_board)

    e = sum(1 for i in range(h) for j in range(w) if energized_board[i][j] == "#")
    energy.append(e)

print(energy[0])

print(max(energy))
