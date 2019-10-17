from collections import deque

from typing import Hashable

from .basegraph import BaseGraph


def breath_first_search(graph: BaseGraph, start_vertex: Hashable):
    frontier = deque([start_vertex])  # enqueue the starting vertex to be explored
    discovered = {start_vertex}  # set the starting vertex as discovered
    parents = {start_vertex: None}  # path each vertex take to return to the starting vertex

    while frontier:  # loop through unexplored vertices
        u = frontier.popleft()  # dequeue the next vertex to be explored
        for v in graph.neighbours(u):  # search for reachable vertices (explore the vertex u)
            if v not in discovered:  # check whether the neighbour has been explored
                parents[v] = u  # set vertex parent
                discovered.add(v)  # mark vertex as discovered
                frontier.append(v)  # enqueue the newly discovered vertex to be explored

    return discovered, parents


def depth_first_search(graph: BaseGraph, start_vertex: Hashable):
    frontier = deque([start_vertex])  # push the starting vertex to be explored
    discovered = set()
    parents = {start_vertex: None}  # path each vertex take to return to the starting vertex

    while frontier:  # loop through unexplored vertices
        u = frontier.pop()  # pop the next vertex to be explored
        if u not in discovered:  # check whether the vertex has been explored
            discovered.add(u)  # mark vertex as discovered
            for v in graph.neighbours(u):  # search for reachable vertices (explore the vertex u)
                parents[v] = u  # set vertex parent
                frontier.append(v)  # push the newly discovered vertex to be explored

    return discovered, parents
