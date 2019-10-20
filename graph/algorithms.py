from typing import Hashable, Callable

from collections import deque
from math import inf

from .basegraph import BaseGraph


def breath_first_search(graph: BaseGraph, start_vertex: Hashable):
    frontier = deque([start_vertex])
    discovered = {start_vertex}
    parents = {start_vertex: None}

    while frontier:
        u = frontier.popleft()
        for v in graph.neighbours(u):
            if v not in discovered:
                parents[v] = u
                discovered.add(v)
                frontier.append(v)

    return discovered, parents


def depth_first_search(graph: BaseGraph, start_vertex: Hashable):
    frontier = deque([start_vertex])
    discovered = set()
    parents = {start_vertex: None}

    while frontier:
        u = frontier.pop()
        if u not in discovered:
            discovered.add(u)
            for v in graph.neighbours(u):
                parents[v] = u
                frontier.append(v)

    return discovered, parents


def dijkstra(graph: BaseGraph, start_vertex: Hashable, dist: Callable[[dict], int]):
    vertices = set(graph.vertices)
    distance = {}
    parents = {}
    for v in vertices:
        distance[v] = inf
        parents[v] = None

    distance[start_vertex] = 0

    while vertices:
        u = min(vertices, key=lambda x: distance[x])
        vertices.remove(u)
        for v in graph.neighbours(u):
            temp_distance = distance[u] + dist(graph.edges[u][v])
            if temp_distance < distance[v]:
                distance[v] = temp_distance
                parents[v] = u

    return distance, parents
