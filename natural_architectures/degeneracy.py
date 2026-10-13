"""Different route algorithms satisfy a shared, deliberately modest contract."""

from collections import deque
from collections.abc import Callable
import heapq
import math

Graph = dict[str, dict[str, float]]
Solver = Callable[[Graph, str, str], list[str]]


class SolverUnavailable(Exception):
    pass


def validate_graph(graph: Graph) -> None:
    for edges in graph.values():
        if any(node not in graph or not math.isfinite(weight) or weight < 0
               for node, weight in edges.items()):
            raise ValueError("graph requires declared nodes and finite nonnegative weights")


def weighted_route(graph: Graph, start: str, goal: str) -> list[str]:
    pending = [(0.0, start, [start])]
    visited = set()
    while pending:
        cost, node, path = heapq.heappop(pending)
        if node in visited:
            continue
        visited.add(node)
        if node == goal:
            return path
        for neighbour, weight in graph[node].items():
            if neighbour not in visited:
                heapq.heappush(pending, (cost + weight, neighbour, path + [neighbour]))
    raise SolverUnavailable("no route")


def fewest_hops(graph: Graph, start: str, goal: str) -> list[str]:
    pending = deque([(start, [start])])
    visited = {start}
    while pending:
        node, path = pending.popleft()
        if node == goal:
            return path
        for neighbour in graph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                pending.append((neighbour, path + [neighbour]))
    raise SolverUnavailable("no route")


def valid_route(graph: Graph, path: list[str], start: str, goal: str) -> bool:
    return bool(path) and path[0] == start and path[-1] == goal and all(
        b in graph.get(a, {}) for a, b in zip(path, path[1:]))


def route(graph: Graph, start: str, goal: str,
          solvers: tuple[Solver, ...] = (weighted_route, fewest_hops)) -> dict:
    validate_graph(graph)
    if start not in graph or goal not in graph:
        raise ValueError("unknown endpoint")
    for solver in solvers:
        try:
            path = solver(graph, start, goal)
        except SolverUnavailable:
            continue
        if valid_route(graph, path, start, goal):
            return {"solver": solver.__name__, "path": path,
                    "cost": sum(graph[a][b] for a, b in zip(path, path[1:]))}
    raise SolverUnavailable("no solver produced a valid route")


def demo() -> dict:
    graph = {"a": {"b": 1, "d": 10}, "b": {"c": 1}, "c": {"d": 1}, "d": {}}

    def offline(graph: Graph, start: str, goal: str) -> list[str]:
        raise SolverUnavailable("weighted service offline")

    return {"normal": route(graph, "a", "d"),
            "degraded": route(graph, "a", "d", (offline, fewest_hops))}
