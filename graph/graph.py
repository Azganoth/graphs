from __future__ import annotations

from typing import Callable, Dict, Hashable, List, Optional, Set, Tuple
from math import inf

from .exceptions import VertexError, EdgeError
from .basegraph import BaseGraph


class Graph(BaseGraph):
    def __init__(self, name: str = None, description: str = None):
        """Creates an empty undirected graph.

        Args:
            name: The name of the graph.
            description: The description of the graph.
        """
        super().__init__(name or 'unnamed graph', description)

    # VERTICES

    def has_vertex(self, vertex_v: Hashable) -> bool:
        return vertex_v in self._vertices

    def add_vertex(self, vertex_v: Hashable, /, **data):
        self._vertices[vertex_v] = data

    def remove_vertex(self, vertex_v: Hashable):
        if vertex_v not in self._vertices:
            raise VertexError(f"vertex '{vertex_v}' isn't in the graph '{self}'")

        del self._vertices[vertex_v]

    def get_vertex_data(self, vertex_v: Hashable) -> dict:
        if vertex_v not in self._vertices:
            raise VertexError(f"vertex '{vertex_v}' isn't in the graph '{self}'")

        return self._vertices[vertex_v]

    def set_vertex_data(self, vertex_v: Hashable, /, **data):
        if vertex_v not in self._vertices:
            raise VertexError(f"vertex '{vertex_v}' isn't in the graph '{self}'")

        self._vertices[vertex_v].update(data)

    # EDGES

    def dataless_edges(self) -> List[Tuple[Hashable, Hashable]]:
        unique_edges = []
        for u in self._edges:
            for v in self._edges[u]:
                if (v, u) not in unique_edges:  # ignore duplicates
                    unique_edges.append((u, v))
        return unique_edges

    def has_edge(self, vertex_u: Hashable, vertex_v: Hashable) -> bool:
        if vertex_u not in self._vertices:
            raise VertexError(f"vertex '{vertex_u}' from the given edge '{{{vertex_u, vertex_v}}}' "
                              f"isn't in the graph '{self}'")
        if vertex_v not in self._vertices:
            raise VertexError(f"vertex '{vertex_v}' from the given edge '{{{vertex_u, vertex_v}}}' "
                              f"isn't in the graph '{self}'")

        return vertex_u in self._edges and vertex_v in self._edges[vertex_u]

    def add_edge(self, vertex_u: Hashable, vertex_v: Hashable, /, **data):
        if vertex_u not in self._vertices:
            raise VertexError(f"vertex '{vertex_u}' from the given edge '{{{vertex_u, vertex_v}}}' "
                              f"isn't in the graph '{self}'")
        if vertex_v not in self._vertices:
            raise VertexError(f"vertex '{vertex_v}' from the given edge '{{{vertex_u, vertex_v}}}' "
                              f"isn't in the graph '{self}'")

        self._edges.setdefault(vertex_u, {})[vertex_v] = data
        self._edges.setdefault(vertex_v, {})[vertex_u] = data

    def remove_edge(self, vertex_u: Hashable, vertex_v: Hashable):
        if not self.has_edge(vertex_u, vertex_v):
            raise EdgeError(f"neither '{{{vertex_u}, {vertex_v}}}' nor '{{{vertex_v}, {vertex_u}}}'"
                            f"edges are in the graph '{self}'")

        del self._edges[vertex_u][vertex_v]
        if not self._edges[vertex_u]:
            del self._edges[vertex_u]

        if vertex_v != vertex_u:
            del self._edges[vertex_v][vertex_u]
            if not self._edges[vertex_v]:
                del self._edges[vertex_v]

    def get_edge_data(self, vertex_u: Hashable, vertex_v: Hashable):
        if not self.has_edge(vertex_u, vertex_v):
            raise EdgeError(f"neither '{{{vertex_u}, {vertex_v}}}' nor '{{{vertex_v}, {vertex_u}}}'"
                            f"edges are in the graph '{self}'")

        return self._edges[vertex_u][vertex_v]

    def set_edge_data(self, vertex_u: Hashable, vertex_v: Hashable, /, **data):
        if not self.has_edge(vertex_u, vertex_v):
            raise EdgeError(f"neither '{{{vertex_u}, {vertex_v}}}' nor '{{{vertex_v}, {vertex_u}}}'"
                            f"edges are in the graph '{self}'")

        self._edges[vertex_u][vertex_v].update(data)
        self._edges[vertex_v][vertex_u].update(data)

    # PROPERTIES

    def order(self) -> int:
        return len(self._vertices)

    def size(self) -> int:
        return len(self.dataless_edges())

    # NEIGHBOURS

    def neighbours(self, vertex_v: Hashable) -> Set[Hashable]:
        if vertex_v not in self._vertices:
            raise VertexError(f"vertex '{vertex_v}' isn't in the graph '{self}'")

        return set(self._edges[vertex_v]) if vertex_v in self._edges else set()

    def is_neighbour(self, vertex_u: Hashable, vertex_v: Hashable) -> bool:
        return self.has_edge(vertex_u, vertex_v)

    # REPRESENTATIONS

    def edges_list(self) -> List[Tuple[Hashable, Hashable, dict]]:
        return [(u, v, self._edges[u][v]) for u, v in self.dataless_edges()]

    def adjacency_list(self) -> Dict[Hashable, Set[Hashable]]:
        return {u: set(self._edges[u]) for u in self._edges}

    def adjacency_matrix(self,
                         weight: Callable[[dict], int]) -> Dict[Hashable, Dict[Hashable, int]]:
        adjacency_matrix = {}
        for u in self._vertices:
            adjacency_matrix[u] = {}
            for v in self._vertices:
                if u in self._edges and v in self._edges[u]:
                    adjacency_matrix[u][v] = weight(self._edges[u][v])
                else:
                    adjacency_matrix[u][v] = inf
        return adjacency_matrix

    # DEGREES

    def degree(self, vertex_v: Hashable) -> int:
        """Returns the degree of the vertex.

        Args:
            vertex_v: The vertex v.

        Returns:
            The degree of the vertex v.

        Raises:
            VertexError: Raises when the vertex isn't in the graph.
        """
        return sum(2 if v == vertex_v else 1 for v in self.neighbours(vertex_v))

    def lowest_degree(self) -> int:
        """Returns the lowest degree in the graph.

        Returns:
            The lowest degree.

        Raises:
            VertexError: Raises when the graph is empty.
        """
        if not self._vertices:
            raise VertexError(f"the graph '{self}' is empty")

        return min(self.degree(v) for v in self._vertices)

    def highest_degree(self) -> int:
        """Returns the highest degree in the graph.

        Returns:
            The highest degree.

        Raises:
            VertexError: Raises when the graph is empty.
        """
        if not self._vertices:
            raise VertexError(f"the graph '{self}' is empty")

        return max(self.degree(v) for v in self._vertices)

    def degree_sequence(self) -> List[int]:
        """Returns a list with each vertex's degree in the graph.

        Returns:
            A list of degrees.

        Raises:
            VertexError: Raises when the graph is empty.
        """
        if not self._vertices:
            raise VertexError(f"the graph '{self}' is empty")

        return [self.degree(v) for v in self._vertices]

    # FROM

    @staticmethod
    def graph_from(vertices: Set[Hashable],
                   edges: List[Tuple[Hashable, Hashable, Optional[dict]]],
                   name: str = None,
                   desc: str = None) -> Graph:
        """Creates a undirected graph from the vertices and edges.

        Args:
            vertices: The vertices.
            edges: The edges.
            name: The name of the graph.
            desc: The description of the graph.

        Returns:
            A undirected graph.

        Raises:
            VertexError: Raises when a vertex from the set of edges isn't in set of vertices.
        """
        graph = Graph(name, desc)
        for v in vertices:
            graph.add_vertex(v)
        for e in edges:
            if len(e) == 3:
                graph.add_edge(e[0], e[1], **e[2])
            else:
                graph.add_edge(e[0], e[1])
        return graph

    @staticmethod
    def graph_from_edges(edges: List[Tuple[Hashable, Hashable, Optional[dict]]],
                         name: str = None,
                         desc: str = None) -> Graph:
        """Creates a undirected graph from the edges.

        Args:
            edges: The edges.
            name: The name of the graph.
            desc: The description of the graph.

        Returns:
            A undirected graph.
        """
        graph = Graph(name, desc)
        for e in edges:
            u, v = e[0], e[1]
            graph.add_vertex(u)
            graph.add_vertex(v)

            data = e[2] if len(e) == 3 else {}
            graph._edges.setdefault(u, {})[v] = data
            graph._edges.setdefault(v, {})[u] = data
        return graph
