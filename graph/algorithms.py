from typing import Callable, Hashable

from collections import deque
from random import choice
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


def dijkstra(graph: BaseGraph, start_vertex: Hashable, weight: Callable[[dict], int]):
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
            temp_distance = distance[u] + weight(graph.edges[u][v])
            if temp_distance < distance[v]:
                distance[v] = temp_distance
                parents[v] = u

    return distance, parents


def bellman_ford(graph: BaseGraph, start_vertex: Hashable, weight: Callable[[dict], int]):
    distance = {}
    parents = {}
    for v in graph.vertices:
        distance[v] = inf
        parents[v] = None

    distance[start_vertex] = 0

    for _ in range(graph.order() - 1):
        for u, v, d in graph.edges_list():
            temp_distance = distance[u] + weight(d)
            if temp_distance < distance[v]:
                distance[v] = temp_distance
                parents[v] = u

    for u, v, d in graph.edges_list():
        if distance[u] + weight(d) < distance[v]:
            raise ValueError(f"graph {graph} contains negative-weight cycle")

    return distance, parents


def floyd_warshall(graph: BaseGraph, weight: Callable[[dict], int]):
    distance = {}
    children = {}

    for u in graph.vertices:
        distance[u] = {}
        children[u] = {}
        for v in graph.vertices:
            distance[u][v] = inf
            children[u][v] = None

    for u, v, d in graph.edges_list():
        distance[u][v] = weight(d)
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


def kruskal(graph: BaseGraph, weight: Callable[[dict], int]):
    edges = []
    cost = 0

    subsets = {frozenset([v]) for v in graph.vertices}

    for u, v, d in sorted(graph.edges_list(), key=lambda e: weight(e[2])):
        subset_u = next((s for s in subsets if u in s))
        subset_v = next((s for s in subsets if v in s))
        if subset_u != subset_v:
            edges.append((u, v))
            cost += weight(d)
            subsets.remove(subset_u)
            subsets.remove(subset_v)
            subsets.add(subset_u | subset_v)

        if len(subsets) == 1:
            break

    return cost, edges


def prim_jarnik(graph: BaseGraph, weight: Callable[[dict], int], start_vertex: Hashable = None):
    vertices = set(graph.vertices)
    costs = {v: inf for v in vertices}
    parents = {}

    costs[start_vertex or choice(tuple(vertices))] = 0

    while vertices:
        u = min(vertices, key=lambda x: costs[x])
        vertices.remove(u)
        for v in graph.neighbours(u):
            temp_cost = weight(graph.edges[u][v])
            if v in vertices and temp_cost < costs[v]:
                costs[v] = temp_cost
                parents[v] = u

    return sum(costs.values()), [(u, parents[u]) for u in parents]
