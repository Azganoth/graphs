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


def bellman_ford(graph: BaseGraph, start_vertex: Hashable, dist: Callable[[dict], int]):
    distance = {}
    parents = {}
    for v in graph.vertices:
        distance[v] = inf
        parents[v] = None

    distance[start_vertex] = 0

    for _ in range(graph.order() - 1):
        for u, v, d in graph.edges_list():
            temp_distance = distance[u] + dist(d)
            if temp_distance < distance[v]:
                distance[v] = temp_distance
                parents[v] = u

    for u, v, d in graph.edges_list():
        if distance[u] + dist(d) < distance[v]:
            raise ValueError(f"graph {graph} contains negative-weight cycle")

    return distance, parents


def floyd_warshall(graph: BaseGraph, dist: Callable[[dict], int]):
    distance = {}
    children = {}

    for u in graph.vertices:
        distance[u] = {}
        children[u] = {}
        for v in graph.vertices:
            distance[u][v] = inf
            children[u][v] = None

    for u, v, d in graph.edges_list():
        distance[u][v] = dist(d)
        children[u][v] = v

    for w in graph.vertices:
        distance[w][w] = 0

    for w in graph.vertices:
        for u in graph.vertices:
            for v in graph.vertices:
                temp_distance = distance[u][w] + distance[w][v]
                if temp_distance < distance[u][v]:
                    distance[u][v] = temp_distance
                    children[u][v] = children[u][w]

    return distance, children
