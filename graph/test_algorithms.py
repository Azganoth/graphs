from graph import (
    Graph, Digraph,
    breath_first_search,
    depth_first_search
)

graph_1 = ({1, 2, 3, 4, 5, 6},
           [(3, 2, {'w': 1}), (2, 1, {'w': 2}), (1, 4, {'w': 3}),
            (4, 5, {'w': 4}), (4, 6, {'w': 5}), (5, 6, {'w': 6})])

graph_2 = ({'u', 'x', 'v', 'y', 'w', 'z'},
           [('u', 'x'), ('u', 'v'), ('x', 'v'), ('v', 'y'),
            ('y', 'x'), ('w', 'y'), ('w', 'z'), ('z', 'z')])

bfs_result = breath_first_search(Graph.graph_from(*graph_1), 1)
dfs_result = depth_first_search(Digraph.graph_from(*graph_2), 'u')

assert bfs_result == ({1, 2, 3, 4, 5, 6}, {1: None, 2: 1, 4: 1, 3: 2, 5: 4, 6: 4})
assert dfs_result == ({'x', 'u', 'v', 'y'}, {'u': None, 'x': 'y', 'v': 'x', 'y': 'v'})
