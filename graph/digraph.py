from __future__ import annotations

from typing import Dict, Hashable, List, Optional, Set, Tuple
from math import inf

from .exceptions import VertexError, EdgeError
from .basegraph import BaseGraph


class Digraph(BaseGraph):
    def __init__(self, name: str = None, description: str = None):
        """Creates an empty directed graph.

        Args:
            name: The name of the graph.
            description: The description of the graph.
        """
        super().__init__(name or 'unnamed digraph', description)

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
        """Returns a list of edges without their data.

        Each edge in the list is composed of vertex u and vertex v.

        Returns:
            A list of edges.
        """
        return [(u, v) for u in self._edges for v in self._edges[u]]

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

    def remove_edge(self, vertex_u: Hashable, vertex_v: Hashable):
        if not self.has_edge(vertex_u, vertex_v):
            raise EdgeError(f"edge '{{{vertex_u}, {vertex_v}}}' isn't in the graph '{self}'")

        del self._edges[vertex_u][vertex_v]
        if not self._edges[vertex_u]:
            del self._edges[vertex_u]

    def get_edge_data(self, vertex_u: Hashable, vertex_v: Hashable):
        if not self.has_edge(vertex_u, vertex_v):
            raise EdgeError(f"edge '{{{vertex_u}, {vertex_v}}}' isn't in the graph '{self}'")

        return self._edges[vertex_u][vertex_v]

    def set_edge_data(self, vertex_u: Hashable, vertex_v: Hashable, /, **data):
        if not self.has_edge(vertex_u, vertex_v):
            raise EdgeError(f"edge '{{{vertex_u}, {vertex_v}}}' isn't in the graph '{self}'")

        self._edges[vertex_u][vertex_v].update(data)

    # PROPERTIES

    def order(self) -> int:
        return len(self._vertices)

    def size(self) -> int:
        return sum(len(self._edges[u]) for u in self._edges)

    # NEIGHBOURS

    def neighbours(self, vertex_v: Hashable) -> Set[Hashable]:
        if vertex_v not in self._vertices:
            raise VertexError(f"vertex '{vertex_v}' isn't in the graph '{self}'")

        return set(self._edges[vertex_v]) if vertex_v in self._edges else set()

    def is_neighbour(self, vertex_u: Hashable, vertex_v: Hashable) -> bool:
        return self.has_edge(vertex_u, vertex_v)

    # REPRESENTATIONS

    def edges_list(self) -> List[Tuple[Hashable, Hashable, dict]]:
        return [(u, v, self._edges[u][v]) for u in self._edges for v in self._edges[u]]

    def adjacency_list(self) -> Dict[Hashable, Set[Hashable]]:
        return {u: set(self._edges[u]) for u in self._edges}

    def adjacency_matrix(self, weight_key: Hashable = None) -> Dict[Hashable, Dict[Hashable, int]]:
        weighted = weight_key is not None
        adjacency_matrix = {}
        for u in self._vertices:
            adjacency_matrix[u] = {}
            for v in self._vertices:
                if u in self._edges and v in self._edges[u]:
                    adjacency_matrix[u][v] = int(self._edges[u][v][weight_key]) if weighted else 1
                else:
                    adjacency_matrix[u][v] = inf if weighted else 0
        return adjacency_matrix

    # DEGREES

    def degree(self, vertex_v: Hashable) -> Tuple[int, int]:
        """Returns the in and out degree of the vertex.

        Args:
            vertex_v: The vertex v.

        Returns:
            The in and out degree of the vertex.

        Raises:
            VertexError: Raises when the vertex isn't in the graph.
        """
        if vertex_v not in self._vertices:
            raise VertexError(f"vertex '{vertex_v}' isn't in the graph '{self}'")

        return self.in_degree(vertex_v), self.out_degree(vertex_v)

    def in_degree(self, vertex_v: Hashable) -> int:
        """Returns the in-degree of the vertex.

        Args:
            vertex_v: The vertex v.

        Returns:
            The in-degree of the vertex.

        Raises:
            VertexError: Raises when the vertex isn't in the graph.
        """
        if vertex_v not in self._vertices:
            raise VertexError(f"vertex '{vertex_v}' isn't in the graph '{self}'")

        return sum(1 for u in self._edges if vertex_v in self._edges[u])

    def out_degree(self, vertex_v: Hashable) -> int:
        """Returns the out-degree of the vertex.

        Args:
            vertex_v: The vertex v.

        Returns:
            The out-degree of the vertex.

        Raises:
            VertexError: Raises when the vertex isn't in the graph.
        """
        if vertex_v not in self._vertices:
            raise VertexError(f"vertex '{vertex_v}' isn't in the graph '{self}'")

        return len(self._edges[vertex_v]) if vertex_v in self._edges else 0

    def minimum_degree(self) -> Tuple[int, int]:
        """Returns the lowest in and out degree in the graph.

        Returns:
            The lowest in and out degree.

        Raises:
            VertexError: Raises when the graph is empty.
        """
        if not self._vertices:
            raise VertexError(f"the graph '{self}' is empty")

        return min((self.in_degree(v), self.out_degree(v)) for v in self._vertices)

    def minimum_in_degree(self) -> int:
        """Returns the lowest in-degree in the graph.

        Returns:
            The lowest in-degree.

        Raises:
            VertexError: Raises when the graph is empty.
        """
        if not self._vertices:
            raise VertexError(f"the graph '{self}' is empty")

        return min((self.in_degree(v) for v in self._vertices))

    def minimum_out_degree(self) -> int:
        """Returns the lowest out-degree in the graph.

        Returns:
            The lowest out-degree.

        Raises:
            VertexError: Raises when the graph is empty.
        """
        if not self._vertices:
            raise VertexError(f"the graph '{self}' is empty")

        return min(self.out_degree(v) for v in self._vertices)

    def maximum_degree(self) -> Tuple[int, int]:
        """Returns the highest in and out degree in the graph.

        Returns:
            The highest in and out degree.

        Raises:
            VertexError: Raises when the graph is empty.
        """
        if not self._vertices:
            raise VertexError(f"the graph '{self}' is empty")

        return max((self.in_degree(v), self.out_degree(v)) for v in self._vertices)

    def maximum_in_degree(self) -> int:
        """Returns the highest in-degree in the graph.

        Returns:
            The highest in-degree.

        Raises:
            VertexError: Raises when the graph is empty.
        """
        if not self._vertices:
            raise VertexError(f"the graph '{self}' is empty")

        return max((self.in_degree(v) for v in self._vertices))

    def maximum_out_degree(self) -> int:
        """Returns the highest out-degree in the graph.

        Returns:
            The highest out-degree.

        Raises:
            VertexError: Raises when the graph is empty.
        """
        if not self._vertices:
            raise VertexError(f"the graph '{self}' is empty")

        return max(self.out_degree(v) for v in self._vertices)

    def degree_sequence(self) -> List[Tuple[int, int]]:
        """Returns a list with each vertex's in-degrees and out-degrees in the graph.

        Returns:
            A list of in and out degrees.

        Raises:
            VertexError: Raises when the graph is empty.
        """
        if not self._vertices:
            raise VertexError(f"the graph '{self}' is empty")

        return [(self.in_degree(v), self.out_degree(v)) for v in self._vertices]

    # FROM

    @staticmethod
    def graph_from(vertices: Set[Hashable],
                   edges: List[Tuple[Hashable, Hashable, Optional[dict]]],
                   name: str = None,
                   desc: str = None) -> Digraph:
        """Creates a directed graph from the vertices and edges.

        Args:
            vertices: The vertices.
            edges: The edges.
            name: The name of the graph.
            desc: The description of the graph.

        Returns:
            A directed graph.

        Raises:
            VertexError: Raises when a vertex from the set of edges isn't in set of vertices.
        """
        graph = Digraph(name, desc)
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
                         desc: str = None) -> Digraph:
        """Creates a directed graph from the edges.

        Args:
            edges: The edges.
            name: The name of the graph.
            desc: The description of the graph.

        Returns:
            A directed graph.
        """
        graph = Digraph(name, desc)
        for e in edges:
            u, v = e[0], e[1]
            graph.add_vertex(u)
            graph.add_vertex(v)

            graph._edges.setdefault(u, {})[v] = e[2] if len(e) == 3 else {}
        return graph
