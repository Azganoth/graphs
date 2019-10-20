from graph import (
    Graph, Digraph,
    breath_first_search,
    depth_first_search,
    dijkstra,
    bellman_ford
)

graph_1 = ({1, 2, 3, 4, 5, 6},
           [(3, 2, {'w': 1}), (2, 1, {'w': 2}), (1, 4, {'w': 3}),
            (4, 5, {'w': 4}), (4, 6, {'w': 5}), (5, 6, {'w': 6})])

graph_2 = ({'u', 'x', 'v', 'y', 'w', 'z'},
           [('u', 'x'), ('u', 'v'), ('x', 'v'), ('v', 'y'),
            ('y', 'x'), ('w', 'y'), ('w', 'z'), ('z', 'z')])

graph_3 = ({'s', 'x', 'u', 'v', 'y'},
           [('s', 'x', {'weight': 5}), ('s', 'u', {'weight': 10}), ('x', 'u', {'weight': 3}),
            ('x', 'y', {'weight': 2}), ('u', 'x', {'weight': 2}), ('u', 'v', {'weight': 1}),
            ('v', 'y', {'weight': 4}), ('y', 's', {'weight': 6}), ('s', 'y', {'weight': 7}),
            ('s', 's', {'weight': 1}), ('x', 'x', {'weight': 1}), ('u', 'u', {'weight': 1})])

graph_4 = ({'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'},
           [('A', 'B', {'weight': 8}), ('A', 'E', {'weight': 6}), ('B', 'C', {'weight': 6}),
            ('C', 'H', {'weight': 4}), ('H', 'G', {'weight': -2}), ('G', 'C', {'weight': -1}),
            ('G', 'D', {'weight': 1}), ('D', 'B', {'weight': 2}), ('E', 'F', {'weight': 3}),
            ('E', 'G', {'weight': 2}), ('F', 'G', {'weight': 6})])

bfs_result = breath_first_search(Graph.graph_from(*graph_1), 1)
dfs_result = depth_first_search(Digraph.graph_from(*graph_2), 'u')
dijkstra_result = dijkstra(Digraph.graph_from(*graph_3), 's', lambda data: int(data['weight']))
bellman_ford_result = bellman_ford(Digraph.graph_from(*graph_4), 'A',
                                   lambda data: int(data['weight']))

assert bfs_result == ({1, 2, 3, 4, 5, 6}, {1: None, 2: 1, 4: 1, 3: 2, 5: 4, 6: 4})
assert dfs_result == ({'x', 'u', 'v', 'y'}, {'u': None, 'x': 'y', 'v': 'x', 'y': 'v'})
assert dijkstra_result == ({'s': 0, 'u': 8, 'x': 5, 'v': 9, 'y': 7},
                           {'s': None, 'u': 'x', 'x': 's', 'v': 'u', 'y': 's'})
assert bellman_ford_result == ({'A': 0, 'E': 6, 'B': 8, 'C': 7, 'H': 11, 'G': 8, 'D': 9, 'F': 9},
                               {'A': None, 'E': 'A', 'B': 'A', 'C': 'G',
                                'H': 'C', 'G': 'E', 'D': 'G', 'F': 'E'})
