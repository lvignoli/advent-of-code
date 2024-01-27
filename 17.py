import heapq
import sys
import typing
from typing import Callable, Iterable

T = typing.TypeVar("T")


def djikstra(
    from_node: T,
    to_nodes: Iterable[T],
    expand: Callable[[T], Iterable[tuple[int, T]]],
) -> tuple[dict[T, int], dict[T, T]]:
    """Performs Djikstra algorithm on a graph.

    Args:
        from_node (T): Starting node.
        to_nodes (Iterable[T]): The end nodes.
        expand (Callable[[T], Iterable[tuple[int, T]]]): Returns the neighboring nodes. It is user defined. This is where the problem logic is injected.

    Returns:
        tuple[dict[T, int], dict[T, T]]: A map of g values and a map of parent nodes.
    """
    g_values = {from_node: 0}
    frontier: list[tuple[int, T]] = [(0, from_node)]
    parents: dict[T, T] = {}
    seen: set[T] = set()

    while frontier:
        g, current = heapq.heappop(frontier)
        if current in seen:  # early return rather than empty loop down there.
            continue

        if to_nodes is not None and current in to_nodes:
            break

        seen.add(current)

        for cost, next in expand(current):
            new_g = g + cost

            if next not in g_values or new_g < g_values[next]:
                g_values[next] = new_g
                heapq.heappush(frontier, (new_g, next))
                parents[next] = current

    return (g_values, parents)


class Node(typing.NamedTuple):
    """Defines a node in the problem graph.
    Multidimensional graph, with direction and stride (number of consecutive
    blocks.)
    """

    coord: tuple[int, int]
    direction: str
    stride: int


def neighbors(coord, dimensions, deltas) -> list[tuple[int, int]]:
    """ "Helper functions to get the neighbors of a given coordinate."""
    out = []
    for d in deltas:
        new_coord = tuple(a + b for a, b in zip(coord, d))
        if all(0 <= c < c_max for c, c_max in zip(new_coord, dimensions)):
            out.append(new_coord)
    return out


DELTA_TO_UDLR = {
    (-1, 0): "U",
    (0, 1): "R",
    (1, 0): "D",
    (0, -1): "L",
}


def expand_with_constraints(
    cost: Callable[[int, int], int], reject: Callable[[Node, Node], bool]
):
    """Expand a node with neighbors in its graph.

    Args:
        reject (Callable[[Node, Node], bool]): Returns true if the node is not
        admissible.
    """

    def expand(
        node: Node,
    ) -> list[tuple[int, Node]]:
        ret = []
        coord, dir, stride = node

        for new_coord in neighbors(coord, (h, w), DELTA_TO_UDLR):
            delta = (new_coord[0] - coord[0], new_coord[1] - coord[1])

            assert delta in DELTA_TO_UDLR  # silence error on map access

            new_dir = DELTA_TO_UDLR[delta]
            new_stride = stride + 1 if new_dir == dir else 0

            new_node = Node(coord=new_coord, direction=new_dir, stride=new_stride)

            # Apply constraints.
            if reject(node, new_node):
                continue

            # cost = board[n[0]][n[1]]
            new_cost = cost(new_coord[0], new_coord[1])
            ret.append((new_cost, new_node))

        return ret

    return expand


def opposite(d: str) -> str:
    if d == "U":
        return "D"
    elif d == "R":
        return "L"
    elif d == "D":
        return "U"
    elif d == "L":
        return "R"
    else:
        return ""


def find_path(
    start: T,
    end: T,
    parents: dict[T, T],
) -> list[T]:
    """Given a start and end point and a map of parents, backtrack from end to start."""
    current = end
    path = []
    while current != start:
        path.append(current)
        current = parents[current]
    path.reverse()
    return path


def path_heatloss(path: Iterable[tuple[int, int]], board) -> int:
    """Compute the problem cost."""
    ret = 0
    for i, j in path:
        ret += board[i][j]
    return ret


def min_heatloss(ends, parents):
    """Find the path of minimum cost."""
    costs = []

    for end in ends:
        if end not in parents:
            continue
        path = find_path(start, end, parents)
        path_coord = [p.coord for p in path]
        c = path_heatloss(path_coord, board)
        costs.append(c)
    return min(costs)


board = [[int(x) for x in l.strip()] for l in sys.stdin.readlines()]
h, w = len(board), len(board[0])

start = Node(coord=(0, 0), direction="", stride=0)


ends_1 = [
    Node(coord=(h - 1, w - 1), direction=d, stride=stride)
    for d in ("U", "R", "D", "L")
    for stride in range(4)
]


def reject_1(old: Node, new: Node) -> bool:
    # Cannot backtrack.
    if new.direction == opposite(old.direction):
        return True

    # Has to turn before 3 consecutive blocks.
    if new.direction == old.direction and old.stride >= 2:
        return True

    return False


g_values, parents = djikstra(
    start, ends_1, expand_with_constraints(lambda i, j: board[i][j], reject_1)
)
print(min_heatloss(ends_1, parents))


# 2

ends_2 = [
    Node(coord=(h - 1, w - 1), direction=d, stride=stride)
    for d in ("U", "R", "D", "L")
    for stride in range(3, 10)
]


def reject_2(old: Node, new: Node) -> bool:
    # Cannot backtrack.
    if new.direction == opposite(old.direction):
        return True

    # Cannot turn before 4 consecutive blocks.
    if old.stride < 3 and new.direction != old.direction and old.direction != "":
        return True

    # Has to turn before 10 consecutive blocks.
    if new.direction == old.direction and old.stride >= 9:
        return True

    return False


g_values, parents = djikstra(
    start, ends_2, expand_with_constraints(lambda i, j: board[i][j], reject_2)
)
print(min_heatloss(ends_2, parents))
