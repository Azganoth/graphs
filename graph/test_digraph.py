from graph import Digraph

graph = Digraph('Digraph Test')
assert graph.name == 'Digraph Test'

# Test vertices

graph.add_vertex('A')
graph.add_vertex('B', color='blue')
graph.add_vertex('C', fruit='coco')
graph.add_vertex('A', letter='a')

assert graph.has_vertex('A')
assert graph.has_vertex('A') and graph.get_vertex_data('A')['letter'] == 'a'
assert not graph.has_vertex('D')
assert graph.order() == 3

graph.remove_vertex('A')
assert not graph.has_vertex('A')
assert graph.order() == 2

graph.add_vertex('A', letter='a')
graph.add_vertex('A', another_letter='z')
assert len(graph.get_vertex_data('A')) == 1 and graph.get_vertex_data('A')['another_letter'] == 'z'

graph.set_vertex_data('A', yet_another_letter='b')
assert len(graph.get_vertex_data('A')) == 2
assert graph.get_vertex_data('A')['yet_another_letter'] == 'b'

# Test edges

graph.add_edge('A', 'A')
graph.add_edge('B', 'A')
graph.add_edge('C', 'A', letters='ca')
assert graph.has_edge('A', 'A')
assert graph.has_edge('C', 'A') and graph.get_edge_data('C', 'A')['letters'] == 'ca'
assert graph.size() == 3

graph.remove_edge('A', 'A')
assert not graph.has_edge('A', 'A')
assert not graph.has_edge('A', 'C')
assert graph.size() == 2

graph.add_edge('A', 'A', letters='aa')
graph.set_edge_data('A', 'A', other_letter='bb')
assert len(graph.get_edge_data('A', 'A')) == 2
assert graph.get_edge_data('A', 'A')['other_letter'] == 'bb'

assert graph.degree('A') == (3, 1)
assert graph.minimum_degree() == (0, 1)
assert graph.maximum_degree() == (3, 1)
assert graph.degree_sequence() == [(0, 1), (0, 1), (3, 1)]
graph.add_edge('A', 'C')
assert graph.minimum_degree() == (0, 1)
assert graph.maximum_degree() == (3, 2)
assert graph.degree_sequence() == [(0, 1), (1, 1), (3, 2)]

assert graph.neighbours('A') == {'A', 'C'}
assert graph.is_neighbour('A', 'A') and graph.is_neighbour('A', 'C')

# Test clear

graph.add_edge('A', 'A')
assert graph.size() == 4
graph.clear()
assert graph.order() == 0
assert graph.size() == 0
