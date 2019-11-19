from typing import Callable, Dict, Hashable, List, Set, Tuple
from abc import abstractmethod


class BaseGraph:
    def __init__(self, name: str, description: str):
        """Creates an empty graph.

        Args:
            name: The name of the graph.
            description: The description of the graph.
        """
        self._name = name
        self._description = description
        self._vertices = {}
        self._edges = {}

    def __contains__(self, vertex: Hashable):
        return vertex in self._vertices

    def __len__(self):
        return len(self._vertices)

    def __str__(self):
        return self._name

    def __repr__(self):
        return (f'G({{{", ".join(map(str, self.vertices))}}}, '
                f'[{", ".join(map(lambda e: f"({e[0]}, {e[1]})", self.edges_list()))}])')

    @property
    def name(self):
        """The name of the graph."""
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def description(self):
        """The description of the graph."""
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def vertices(self) -> Dict[Hashable, dict]:
        """The vertices of the graph."""
        return self._vertices

    @property
    def edges(self) -> Dict[Hashable, Dict[Hashable, dict]]:
        """The edges of the graph."""
        return self._edges

    def clear(self):
        """Clears the graph, removing all vertices and edges from it."""
        self._vertices.clear()
        self._edges.clear()

    # VERTICES

    @abstractmethod
    def has_vertex(self, vertex_v: Hashable) -> bool:
        """Checks if the vertex is in the graph.

        Args:
            vertex_v: The vertex v.

        Returns:
            True if the vertex is in the graph, False otherwise.
        """
        pass

    @abstractmethod
    def add_vertex(self, vertex_v: Hashable, /, **data):
        """Adds a vertex to the graph.

        Args:
            vertex_v: The vertex v.
            **data: The data of the vertex. Each pair of key=value passed as parameter will be
                inserted/updated in the vertex's data.
        """
        pass

    @abstractmethod
    def remove_vertex(self, vertex_v: Hashable):
        """Removes a vertex from the graph.

        Args:
            vertex_v: The vertex v.

        Raises:
            VertexError: Raises when the vertex isn't in the graph.
        """
        pass

    @abstractmethod
    def pop_vertex(self, vertex_v: Hashable) -> dict:
        """Removes a vertex from the graph and returns it's data.

        Args:
            vertex_v: The vertex v.

        Raises:
            VertexError: Raises when the vertex isn't in the graph.
        """
        pass

    @abstractmethod
    def get_vertex_data(self, vertex_v: Hashable) -> dict:
        """Returns the vertex's data.

        Args:
            vertex_v: The vertex v.

        Returns:
            The data associated with the vertex.

        Raises:
            VertexError: Raises when the vertex isn't in the graph.
        """
        pass

    @abstractmethod
    def set_vertex_data(self, vertex_v: Hashable, /, **data):
        """Sets the vertex's data.

        Args:
            vertex_v: The vertex v.
            **data: The data of the vertex. Each pair of key=value passed as parameter will be
                inserted/updated in the vertex's data.

        Raises:
            VertexError: Raises when the vertex isn't in the graph.
        """
        pass

    # EDGES

    @abstractmethod
    def dataless_edges(self) -> List[Tuple[Hashable, Hashable]]:
        """Returns a list of unique edges without their data.

        Each edge in the list is composed of vertex u and vertex v.

        Returns:
            A list of unique edges.
        """
        pass

    @abstractmethod
    def has_edge(self, vertex_u: Hashable, vertex_v: Hashable) -> bool:
        """Checks if the edge is in the graph.

        Args:
            vertex_u: The vertex u of the edge.
            vertex_v: The vertex v of the edge.

        Returns:
            True if the edge is in the graph, False otherwise.

        Raises:
            VertexError: Raises when a vertex isn't in the graph.
        """
        pass

    @abstractmethod
    def add_edge(self, vertex_u: Hashable, vertex_v: Hashable, /, **data):
        """Adds an edge to the graph.

        Args:
            vertex_u: The vertex u of the edge.
            vertex_v: The vertex v of the edge.
            **data: The data of the edge. Each pair of key=value passed as parameter will be
                inserted/updated in the edge's data.

        Raises:
            VertexError: Raises when a vertex isn't in the graph.
        """
        pass

    @abstractmethod
    def remove_edge(self, vertex_u: Hashable, vertex_v: Hashable):
        """Removes an edge from the graph.

        Args:
            vertex_u: The vertex u of the edge.
            vertex_v: The vertex v of the edge.

        Raises:
            VertexError: Raises when a vertex isn't in the graph.
            EdgeError: Raises when the edge isn't in the graph.
        """
        pass

    @abstractmethod
    def pop_edge(self, vertex_u: Hashable, vertex_v: Hashable) -> dict:
        """Removes an edge from the graph and returns it's data.

        Args:
            vertex_u: The vertex u of the edge.
            vertex_v: The vertex v of the edge.

        Raises:
            VertexError: Raises when a vertex isn't in the graph.
            EdgeError: Raises when the edge isn't in the graph.
        """
        pass

    @abstractmethod
    def get_edge_data(self, vertex_u: Hashable, vertex_v: Hashable) -> dict:
        """Returns the edge's data.

        Args:
            vertex_u: The vertex u of the edge.
            vertex_v: The vertex v of the edge.

        Returns:
            The data associated with the edge.

        Raises:
            VertexError: Raises when a vertex isn't in the graph.
            EdgeError: Raises when the edge isn't in the graph.
        """
        pass

    @abstractmethod
    def set_edge_data(self, vertex_u: Hashable, vertex_v: Hashable, /, **data):
        """Sets the edge's data.

        Args:
            vertex_u: The vertex u of the edge.
            vertex_v: The vertex v of the edge.
            **data: The data of the edge. Each pair of key=value passed as parameter will be
                inserted/updated in the edge's data.

        Raises:
            VertexError: Raises when a vertex isn't in the graph.
            EdgeError: Raises when the edge isn't in the graph.
        """
        pass

    # PROPERTIES

    @abstractmethod
    def order(self) -> int:
        """Returns the order of the graph.

        The order of the graph is its number of vertices.

        Returns:
            The order of the graph.
        """
        pass

    @abstractmethod
    def size(self) -> int:
        """Returns the size of the graph.

        The size of the graph is its number of edges (unique edges).

        Returns:
            The size of the graph.
        """
        pass

    # NEIGHBOURS

    @abstractmethod
    def neighbours(self, vertex_v: Hashable) -> Set[Hashable]:
        """Returns a set of vertices neighbours to the vertex v.

        Args:
            vertex_v: The vertex v.

        Returns:
            A set of vertices neighbours to the vertex v.

        Raises:
            VertexError: Raises when a vertex isn't in the graph.
        """
        pass

    @abstractmethod
    def is_neighbour(self, vertex_u: Hashable, vertex_v: Hashable) -> bool:
        """Tests if the vertex u is adjacent/neighbour to the vertex v.

        Args:
            vertex_u: The vertex u of the edge.
            vertex_v: The vertex v of the edge.

        Returns:
            True if there is an edge from the vertex u to the vertex v, False otherwise.

        Raises:
            VertexError: Raises when a vertex isn't in the graph.
        """
        pass

    # REPRESENTATIONS

    @abstractmethod
    def edges_list(self) -> List[Tuple[Hashable, Hashable, dict]]:
        """Returns a list of unique edges.

        Each edge in the list is composed of vertex u, vertex v and the edge's data.

        Returns:
            A list of unique edges.
        """
        pass

    @abstractmethod
    def adjacency_list(self) -> Dict[Hashable, Set[Hashable]]:
        """Returns the adjacency list representation of the graph.

        Returns:
            A dictionary of vertices each with a set of adjacent vertices.
        """
        pass

    @abstractmethod
    def adjacency_matrix(self,
                         weight: Callable[[dict], int]) -> Dict[Hashable, Dict[Hashable, int]]:
        """Returns the adjacency matrix representation of the graph.

        Args:
            weight: The function that will extract the weight value of the edge's data.

        Returns:
            A multi-dimensional dictionary.

        Raises:
            KeyError: Raises when the weight key don't exists in one of the edges' data.
        """
        pass
