from math import inf

from graph import (
    Graph, Digraph,
    breath_first_search,
    depth_first_search,
    dijkstra,
    bellman_ford,
    floyd_warshall,
    kruskal,
    prim_jarnik
)


# method to get the edge's weight
def weight_fun(data: dict) -> int:
    return data['weight']


# breadth-first search test
graph_1 = Graph.graph_from({1, 2, 3, 4, 5, 6},
                           [(3, 2, {'w': 1}), (2, 1, {'w': 2}), (1, 4, {'w': 3}),
                            (4, 5, {'w': 4}), (4, 6, {'w': 5}), (5, 6, {'w': 6})])

bfs_result = breath_first_search(graph_1, 1)
assert bfs_result == ({1, 2, 3, 4, 5, 6}, {1: None, 2: 1, 4: 1, 3: 2, 5: 4, 6: 4})

print('\nBreath-First Search: ', bfs_result, 'Runned on the graph: ', repr(graph_1), sep='\n')

# depth-first search test
digraph_1 = Digraph.graph_from({'u', 'x', 'v', 'y', 'w', 'z'},
                               [('u', 'x', {}), ('u', 'v', {}), ('x', 'v', {}), ('v', 'y', {}),
                                ('y', 'x', {}), ('w', 'y', {}), ('w', 'z', {}), ('z', 'z', {})])

dfs_result = depth_first_search(digraph_1, 'u')
assert dfs_result == ({'x', 'u', 'v', 'y'}, {'u': None, 'x': 'y', 'v': 'x', 'y': 'v'})

print('\nDepth-First Search: ', dfs_result, 'Runned on the graph: ', repr(digraph_1), sep='\n')

# dijkstra test
digraph_2 = Digraph.graph_from({'s', 'x', 'u', 'v', 'y'},
                               [('s', 'x', {'weight': 5}), ('s', 'u', {'weight': 10}),
                                ('x', 'u', {'weight': 3}), ('x', 'y', {'weight': 2}),
                                ('u', 'x', {'weight': 2}), ('u', 'v', {'weight': 1}),
                                ('v', 'y', {'weight': 4}), ('y', 's', {'weight': 6}),
                                ('s', 'y', {'weight': 7}), ('s', 's', {'weight': 1}),
                                ('x', 'x', {'weight': 1}), ('u', 'u', {'weight': 1})])

dijkstra_result = dijkstra(digraph_2, 's', weight_fun)
assert dijkstra_result == ({'s': 0, 'u': 8, 'x': 5, 'v': 9, 'y': 7},
                           {'s': None, 'u': 'x', 'x': 's', 'v': 'u', 'y': 's'})

print('\nDijkstra: ', dijkstra_result, 'Runned on the graph: ', repr(digraph_2), sep='\n')

# bellman-ford test
digraph_3 = Digraph.graph_from({'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'},
                               [('A', 'B', {'weight': 8}), ('A', 'E', {'weight': 6}),
                                ('B', 'C', {'weight': 6}), ('C', 'H', {'weight': 4}),
                                ('H', 'G', {'weight': -2}), ('G', 'C', {'weight': -1}),
                                ('G', 'D', {'weight': 1}), ('D', 'B', {'weight': 2}),
                                ('E', 'F', {'weight': 3}), ('E', 'G', {'weight': 2}),
                                ('F', 'G', {'weight': 6})])

bellman_ford_result = bellman_ford(digraph_3, 'A', weight_fun)
assert bellman_ford_result == ({'A': 0, 'E': 6, 'B': 8, 'C': 7, 'H': 11, 'G': 8, 'D': 9, 'F': 9},
                               {'A': None, 'E': 'A', 'B': 'A', 'C': 'G',
                                'H': 'C', 'G': 'E', 'D': 'G', 'F': 'E'})

print('\nBellman-Ford: ', bellman_ford_result, 'Runned on the graph: ', repr(digraph_3), sep='\n')

# floyd-marshall test
digraph_4 = Digraph.graph_from({1, 2, 3, 4, 5},
                               [(1, 3, {'weight': 6}), (3, 4, {'weight': 2}), (4, 3, {'weight': 1}),
                                (4, 2, {'weight': 1}), (2, 1, {'weight': 3}), (5, 4, {'weight': 2}),
                                (5, 2, {'weight': 4}), (1, 4, {'weight': 3})])

floyd_warshall_result = floyd_warshall(digraph_4, weight_fun)
assert floyd_warshall_result == ({1: {1: 0, 2: 4, 3: 4, 4: 3, 5: inf},
                                  2: {1: 3, 2: 0, 3: 7, 4: 6, 5: inf},
                                  3: {1: 6, 2: 3, 3: 0, 4: 2, 5: inf},
                                  4: {1: 4, 2: 1, 3: 1, 4: 0, 5: inf},
                                  5: {1: 6, 2: 3, 3: 3, 4: 2, 5: 0}},
                                 {1: {1: None, 2: 4, 3: 4, 4: 4, 5: None},
                                  2: {1: 1, 2: None, 3: 1, 4: 1, 5: None},
                                  3: {1: 4, 2: 4, 3: None, 4: 4, 5: None},
                                  4: {1: 2, 2: 2, 3: 3, 4: None, 5: None},
                                  5: {1: 4, 2: 4, 3: 4, 4: 4, 5: None}})

print('\nFloyd-Warshall: ', floyd_warshall_result, 'Runned on the graph: ', repr(digraph_4),
      sep='\n')

# kruskal test
graph_2 = Graph.graph_from({0, 1, 2, 3, 4, 5, 6, 7, 8},
                           [(0, 1, {'weight': 4}), (1, 7, {'weight': 11}), (0, 7, {'weight': 8}),
                            (1, 2, {'weight': 8}), (2, 3, {'weight': 7}), (3, 4, {'weight': 9}),
                            (4, 5, {'weight': 10}), (5, 3, {'weight': 14}), (2, 5, {'weight': 4}),
                            (2, 8, {'weight': 2}), (8, 6, {'weight': 6}), (6, 5, {'weight': 2}),
                            (8, 7, {'weight': 7}), (6, 7, {'weight': 1})])

kruskal_result = kruskal(graph_2, weight_fun)
assert kruskal_result[0] == 37 and len(kruskal_result[1]) == graph_2.order() - 1

print('\nKruskal: ', kruskal_result, 'Runned on the graph: ', repr(graph_2), sep='\n')

# prim-jarnik test
prim_jarnik_result = prim_jarnik(graph_2, weight_fun)
assert prim_jarnik_result[0] == 37 and len(prim_jarnik_result[1]) == graph_2.order() - 1

print('\nPrim-Jarnik: ', prim_jarnik_result, 'Runned on the graph: ', repr(graph_2), sep='\n')
